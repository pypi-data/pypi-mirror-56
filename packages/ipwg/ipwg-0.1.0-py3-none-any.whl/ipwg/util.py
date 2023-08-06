import os
from typing import Union, List


def _pick(n: int, s: Union[List[str], str]) -> List[str]:
    return [s[ord(os.urandom(1)) % len(s)] for _ in range(n)]
