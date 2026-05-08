import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEST_HOME = PROJECT_ROOT / ".test-home"

# Ensure local package imports work during test collection.
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# EchoPrompt writes under HOME; keep tests isolated and writable.
TEST_HOME.mkdir(exist_ok=True)
os.environ["HOME"] = str(TEST_HOME)
