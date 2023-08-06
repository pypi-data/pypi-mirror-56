
from pathlib import Path
from importlib import import_module

import pytest


modules_names = [p.stem
                 for p in Path(__file__).parent.glob('*example*.py')
                 if not p.stem.startswith('test_')]


@pytest.mark.parametrize("module_name", modules_names)
def test_examples(module_name):
    """just to make sure all examples are runnable and correct"""
    print(module_name)
    module = import_module(module_name)
    if hasattr(module, 'main'):
        module.main()
