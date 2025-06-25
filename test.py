from os import path

from dll_types import OptInfo_T, ProgInfo_T

from ctypes import *
import ctypes

lib_path = path.join(path.dirname(__file__), "build", "libjcl.dylib")
libjcl = cdll.LoadLibrary(lib_path)

opt_info = OptInfo_T()
prog_info = ProgInfo_T()
args = (c_char_p * 2)(b'./jcl2jcl', b'--input=' + path.join(path.dirname(__file__), "testsrc", "comments.jcl").encode())

print("Process args...")
rc = libjcl.processArgs(len(args), args, byref(opt_info))

print(rc)

# for field in my_opts._fields_:
#     print(field)
#     field

if bool(opt_info.outputFile):
    print("Output file", ctypes.string_at(opt_info.outputFile).decode('UTF-8'))

if bool(opt_info.inputFile):
    print("Input file", ctypes.string_at(opt_info.inputFile).decode('UTF-8'))


print("Establish input...")
rc = libjcl.establishInput(byref(opt_info), byref(prog_info))
print(rc)

print("Establish output...")
rc = libjcl.establishOutput(byref(opt_info), byref(prog_info))
print(rc)

print("Scan JCL...")
rc = libjcl.scanJCL(byref(opt_info), byref(prog_info))
print(rc)

line = prog_info.jcl.contents.lines.contents.head.contents
while (True):
    print(line.text)
    if not bool(line.next):
        break
    line = line.next.contents



# stmt = prog_info.jcl.contents.stmts.contents.head.contents
# while (True):
#     print(stmt.text)
#     if not bool(line.next):
#         break
#     line = line.next.contents

# print("Generate JCL...")
# rc = libjcl.genJCL(byref(opt_info), byref(prog_info))
# print(rc)