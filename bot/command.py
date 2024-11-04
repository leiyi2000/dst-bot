from typing import Callable, Any, List, Dict

import re
import asyncio
from functools import partial

import structlog

from bot.schemas import Event
from bot import napcat, models


log = structlog.get_logger()


class CommandRoute:
    """命令路由"""

    def __init__(
        self,
        name: str,
        pattern: re.Pattern,
        func: Callable[..., Any],
        inject_event: bool,
        limit_admin: bool,
        limit_group: bool,
        func_kwargs: Dict[str, Any],
    ) -> None:
        self.name = name
        self.pattern = pattern
        self.func = func
        self.inject_event = inject_event
        self.limit_admin = limit_admin
        self.limit_group = limit_group
        self.func_kwargs = func_kwargs

    async def validate_admin(self, uid: int) -> bool:
        if self.limit_admin:
            user = await models.Admin.get_or_none(uid=uid)
            return user is not None
        else:
            return True

    async def match(self, event: Event) -> bool:
        if self.limit_group and event.message_type == "private":
            return False
        for message in event.message:
            if message.type == "text":
                event.match_text = message.data.text
                if self.pattern.fullmatch(message.data.text) is not None:
                    return await self.validate_admin(event.user_id)
        return False


class CommandRouter:
    """指令路由器"""

    def __init__(self):
        self.routes: List[CommandRoute] = []

    def add_route(self, route: CommandRoute):
        self.routes.append(route)

    def command(
        self,
        pattern: str,
        *,
        name: str = None,
        limit_admin: bool = False,
        limit_group: bool = False,
        inject_event: bool = True,
        func_kwargs: Dict[str, Any] = {},
    ):
        """command装饰器.

        Args:
            pattern (str): 指令正则匹配.
            func (Callable[..., Any]): 命令处理函数.
            name (str, optional): 名称.
            limit_group (bool, optional): True 限制只能处理群消息.
            inject_event (bool, optional): True 传递event参数到func.
            func_kwargs (Dict[str, Any], optional): func额外参数.
        """

        def decorator(func: Callable[..., Any]):
            # 初始化一个命令路由
            route = CommandRoute(
                name or getattr(func, "__name__", "unknown"),
                re.compile(pattern),
                func,
                inject_event,
                limit_admin,
                limit_group,
                func_kwargs,
            )
            self.add_route(route)
            return func

        return decorator

    async def match(self, event: Event) -> CommandRoute | None:
        for route in self.routes:
            if await route.match(event):
                return route

    def include_router(self, router: "CommandRouter"):
        for route in router.routes:
            self.add_route(route)


async def run_command(router: CommandRouter, event: Event):
    """路由命令执行.

    Args:
        router (CommandRouter): 命令路由器.
        event (Event): 消息事件.
    """
    route = await router.match(event)
    if route is not None:
        func = route.func
        if route.inject_event:
            func = partial(func, event)
        try:
            if asyncio.iscoroutinefunction(func):
                reply_message = await func(**route.func_kwargs)
            else:
                reply_message = func(**route.func_kwargs)
            await napcat.reply(
                reply_message,
                event.user_id,
                event.group_id,
                event.message_type,
            )
        except Exception:
            import traceback

            log.error(traceback.format_exc())
            reply_message = "哼哼~~~出错了"
            await napcat.reply(
                reply_message,
                event.user_id,
                event.group_id,
                event.message_type,
            )
