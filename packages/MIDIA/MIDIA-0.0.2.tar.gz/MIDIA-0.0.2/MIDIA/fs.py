from pprint import pprint
from pathlib import Path

ls = lambda p: pprint(list(Path(p).glob("*")))