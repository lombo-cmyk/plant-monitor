from dotenv import dotenv_values

from plant_common.singleton import singleton


@singleton
class _ParseConfig:

    def __init__(self):
        self._config = dotenv_values("/usr/src/app/config/.env")
        self.config = {}
        self.parse_config()
        self.complete_config()

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

    def complete_config(self):
        if not self.config.get("BATTERY_READ_INTERVAL_M"):
            self.config["BATTERY_READ_INTERVAL_M"] = 30


config = _ParseConfig().config
