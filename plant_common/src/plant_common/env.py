from dotenv import dotenv_values

from plant_common.singleton import singleton


@singleton
class _ParseConfig:

    def __init__(self) -> None:
        self._config = dotenv_values("/usr/src/app/config/.env")
        self.config = {}
        self.parse_config()
        self.complete_config()

    def parse_config(self) -> None:
        for k, v in self._config.items():
            if v.lower() == "true":
                self.config[k] = True
                continue
            if v.lower() == "false":
                self.config[k] = False
                continue
            if "," in v.lower() and "@" in v.lower():
                # emails
                self.config[k] = v.replace(" ", "").split(",")
                continue
            try:
                number = int(v)
                self.config[k] = number
                continue
            except ValueError:
                pass
            self.config[k] = v

    def complete_config(self) -> None:
        if not self.config.get("BATTERY_READ_INTERVAL_M"):
            self.config["BATTERY_READ_INTERVAL_M"] = 30
        if not self.config.get("FONT_SIZE_RATIO"):
            self.config["FONT_SIZE_RATIO"] = 5


config = _ParseConfig().config
