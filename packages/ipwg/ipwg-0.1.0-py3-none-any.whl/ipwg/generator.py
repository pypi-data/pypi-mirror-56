import string
from random import shuffle

from ipwg.util import _pick


class Generator:
    """Generate random passwords

    generates random strings containing specific types of characters.
    You can customize the specific characters by setting the class
    variables:
     - lowers
     - uppers
     - digits
     - specials

     for example, if you only wanted to allow !@#$ as special characters, you could
     set the class variable `specials` to '!@#$'

     ```
        Generator.specials = '!@#$'
     ```

     You also must enable each character set you would like to use by way of the
     [SET]_enabled property:
      - lowers_enabled
      - uppers_enabled
      - digits_enabled
      - specials_enabled

    You can also specify a minimum required amount of any type of characters from
    a specific set by way of the [SET]_count property;
     - lowers_count
     - uppers_count
     - digits_count
     - specials_count
    """
    _specials_enabled: bool
    _digits_enabled: bool
    _uppers_enabled: bool
    _lowers_enabled: bool

    _specials_count: int
    _digits_count: int
    _uppers_count: int
    _lowers_count: int

    lowers = string.ascii_lowercase
    uppers = string.ascii_uppercase
    digits = string.digits
    specials = string.punctuation

    def __init__(self, enable_all: bool = False):
        self._lowers_count = 0
        self._lowers_enabled = enable_all

        self._uppers_count = 0
        self._uppers_enabled = enable_all

        self._digits_count = 0
        self._digits_enabled = enable_all

        self._specials_count = 0
        self._specials_enabled = enable_all

    @property
    def specials_count(self) -> int:
        return self._specials_count

    @specials_count.setter
    def specials_count(self, value: int):
        self._specials_count = value

    @property
    def uppers_count(self) -> int:
        return self._uppers_count

    @uppers_count.setter
    def uppers_count(self, value: int):
        self._uppers_count = value

    @property
    def lowers_count(self) -> int:
        return self._lowers_count

    @lowers_count.setter
    def lowers_count(self, value: int):
        self._lowers_count = value

    @property
    def digits_count(self) -> int:
        return self._digits_count

    @digits_count.setter
    def digits_count(self, value: int):
        self._digits_count = value

    @property
    def lowers_enabled(self) -> bool:
        return self._lowers_enabled

    @lowers_enabled.setter
    def lowers_enabled(self, value: bool):
        self._lowers_enabled = value

    @property
    def uppers_enabled(self) -> bool:
        return self._uppers_enabled

    @uppers_enabled.setter
    def uppers_enabled(self, value: bool):
        self._uppers_enabled = value

    @property
    def digits_enabled(self) -> bool:
        return self._digits_enabled

    @digits_enabled.setter
    def digits_enabled(self, value: bool):
        self._digits_enabled = value

    @property
    def specials_enabled(self) -> bool:
        return self._specials_enabled

    @specials_enabled.setter
    def specials_enabled(self, value: bool):
        self._specials_enabled = value

    def create_password(self, length: int):
        filler_length = self._compute_filler_length(length)
        if filler_length < 0:
            raise Exception("Requirements cannot be met.")

        base = self._get_filler_characters()
        if base == '':
            raise Exception("No character sets are enabled")

        picks = self._get_picks(base, filler_length)

        shuffle(picks)
        return "".join(picks)

    def _get_picks(self, base: str, filler_length: int):
        return _pick(filler_length, base) + \
               _pick(self._lowers_count, Generator.lowers) + \
               _pick(self._uppers_count, Generator.uppers) + \
               _pick(self._digits_count, Generator.digits) + \
               _pick(self._specials_count, Generator.specials)

    def _compute_filler_length(self, length: int):
        return length - self._lowers_count - self._digits_count - self._specials_count - self._uppers_count

    def _get_filler_characters(self):
        base = ''

        if self._lowers_enabled:
            base = base + Generator.lowers

        if self._uppers_enabled:
            base = base + Generator.uppers

        if self._digits_enabled:
            base = base + Generator.digits

        if self._specials_enabled:
            base = base + Generator.specials

        return base
