from pydantic import BaseModel


class LedState(BaseModel):
    state: bool

    @staticmethod
    def build(state: bool) -> "LedState":
        return LedState(state=state)
