from dotenv import dotenv_values

from .singleton import singleton


@singleton
class _ParseConfig:

    def __init__(self):
        self._config = dotenv_values("/config/.env")
        self.config = {}
        self.parse_config()

    def parse_config(self):
        for k, v in self._config.items():
            if v.lower() == "true":
                self.config[k] = True
                continue
            if v.lower() == "false":
                self.config[k] = False
                continue
            try:
                number = int(v)
                self.config[k] = number
                continue
            except ValueError:
                pass
            self.config[k] = v


config = _ParseConfig().config
