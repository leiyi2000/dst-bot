from typing import Callable, Any, List, Dict

import re
import asyncio
from functools import partial

import structlog

from bot import hook
from bot.schemas import Event


log = structlog.get_logger()


class CommandRoute:
    """命令路由"""

    def __init__(
        self,
        name: str,
        pattern: re.Pattern,
        func: Callable[..., Any],
        event_arg: bool,
        limit_room: bool,
        func_kwargs: Dict[str, Any],
    ) -> None:
        self.name = name
        self.pattern = pattern
        self.func = func
        self.event_arg = event_arg
        self.limit_room = limit_room
        self.func_kwargs = func_kwargs

    def match(self, event: Event) -> bool:
        if self.limit_room and not event.is_room:
            return False
        return self.pattern.fullmatch(event.content) is not None


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
        limit_room: bool = False,
        event_arg: bool = True,
        func_kwargs: Dict[str, Any] = {},
    ):
        """command装饰器

        Args:
            pattern (str): 指令正则匹配.
            func (Callable[..., Any]): 命令处理函数.
            name (str, optional): 名称.
            limit_room (bool, optional): True 限制只能处理群消息.
            event_arg (bool, optional): True 传递event参数到func.
            func_kwargs (Dict[str, Any], optional): func额外参数.
        """

        def decorator(func: Callable[..., Any]):
            # 初始化一个命令路由
            route = CommandRoute(
                name or getattr(func, "__name__", "unknown"),
                re.compile(pattern),
                func,
                event_arg,
                limit_room,
                func_kwargs,
            )
            self.add_route(route)
            return func

        return decorator

    def matches(self, event: Event) -> List[CommandRoute]:
        return [route for route in self.routes if route.match(event)]

    def match(self, event: Event) -> CommandRoute | None:
        for route in self.routes:
            if route.match(event):
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
    route = router.match(event)
    if route is not None:
        func = route.func
        if route.event_arg:
            func = partial(func, event)
        try:
            if asyncio.iscoroutinefunction(func):
                reply_message = await func(**route.func_kwargs)
            else:
                reply_message = func(**route.func_kwargs)
            await hook.reply(event.to, event.is_room, reply_message)
        except Exception:
            import traceback

            log.error(traceback.format_exc())
            reply_message = "哼哼~~~出错了"
            await hook.reply(event.to, event.is_room, reply_message)
