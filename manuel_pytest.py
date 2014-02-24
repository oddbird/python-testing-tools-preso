"""A variant of manuel.codeblock that executes pytest-style tests."""

import types

import manuel
import manuel.codeblock



def execute_code_block(region, document, globs):
    if not isinstance(region.parsed, manuel.codeblock.CodeBlock):
        return

    initial_keys = set(globs.keys())

    exec(region.parsed.code, globs)

    added_keys = set(globs.keys()).difference(initial_keys)

    for name in added_keys:
        obj = globs[name]
        if isinstance(obj, types.FunctionType) and obj.__name__.startswith('test_'):
            obj()

    del globs['__builtins__'] # exec adds __builtins__, we don't want it


class Manuel(manuel.Manuel):
    def __init__(self):
        manuel.Manuel.__init__(
            self,
            [manuel.codeblock.find_code_blocks],
            [execute_code_block],
            )
