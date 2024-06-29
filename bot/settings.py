import os

from datetime import tzinfo, timedelta


APP_NAME = "bot"
# 科雷令牌
KLEI_TOKEN = os.environ.get("KLEI_TOKEN")
NAPCAT_API = os.environ.get("NAPCAT_API", default="http://127.0.0.1:3000")
DATABASE_URL = os.environ.get("DATABASE_URL", default="sqlite://bot.sqlite3")


# 数据量配置
TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        APP_NAME: {
            "models": ["bot.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "timezone": "Asia/Shanghai",
}


class ShanghaiTZ(tzinfo):
    def __init__(self):
        self._offset = timedelta(hours=8)
        self._name = "Asia/Shanghai"

    def utcoffset(self, dt):
        return self._offset

    def tzname(self, dt):
        return self._name

    def dst(self, dt):
        return timedelta(0)


# 上海时区
SHANGHAI_TIMEZONE = ShanghaiTZ()
