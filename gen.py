import ctypeslib
from ctypeslib.codegen import config

cfg = config.CodegenConfig()
cfg.generate_comments = True
cfg.generate_docstrings = True
cfg.generate_locations = True

py_module3 = ctypeslib.translate_files([
    'src/scanjcl.h',
    'src/gen.h',
    'src/jclargs.h',
],
outfile=open('dll_types.py', 'w'),
cfg=cfg)
# print(open('dll_types.py').read())
