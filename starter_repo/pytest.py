"""Minimal pytest shim so `python -m pytest` works when pytest isn't installed."""
import importlib.util
import sys
import traceback
from pathlib import Path


def _load_module(path):
    name = path.stem
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _iter_test_files(args):
    paths = [a for a in args if not a.startswith("-")] or ["."]
    for p in paths:
        path = Path(p)
        if path.is_dir():
            yield from sorted(path.rglob("test_*.py"))
            yield from sorted(path.rglob("*_test.py"))
        elif path.is_file():
            yield path


def main():
    passed = failed = 0
    failures = []
    for file in dict.fromkeys(_iter_test_files(sys.argv[1:])):
        try:
            module = _load_module(file)
        except Exception:
            failed += 1
            failures.append((str(file), traceback.format_exc()))
            continue
        for name, obj in vars(module).items():
            if name.startswith("test_") and callable(obj):
                try:
                    obj()
                    passed += 1
                except Exception:
                    failed += 1
                    failures.append((f"{file}::{name}", traceback.format_exc()))
    for nodeid, tb in failures:
        print(f"FAILED {nodeid}")
        print(tb)
    if failed:
        print(f"{failed} failed, {passed} passed")
        return 1
    print(f"{passed} passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
