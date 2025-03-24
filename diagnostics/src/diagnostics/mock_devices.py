from random import randint


class MockMCP3008:
    def __init__(self, channel=0) -> None:
        self.channel = channel

    @property
    def raw_value(self) -> int:
        return randint(150, 1000)
