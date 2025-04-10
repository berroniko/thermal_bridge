from pathlib import Path
import tomllib

SRC_ROOT = Path(__file__).parent

DATA_DIR = SRC_ROOT.parent / "data"
TEST_DATA_DIR = SRC_ROOT.parent / "test/test_data"

with open(SRC_ROOT.parent / "pyproject.toml", "rb") as f:
    data = tomllib.load(f)
__version__ = data['project']['version']
