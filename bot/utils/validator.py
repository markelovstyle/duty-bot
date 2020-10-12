from typing import Optional

from vbml import PatchedValidators, Patcher
from .tools import parse_interval


class Validator(PatchedValidators):
    def unix(self, value: str) -> Optional[int]:
        interval = parse_interval(value)
        if interval:
            return int(interval)


patcher = Patcher(validators=Validator)
Patcher.set_current(patcher)