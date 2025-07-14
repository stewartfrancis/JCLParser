# -*- coding: utf-8 -*-
#
# TARGET arch is: ['-isysroot', '/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk']
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 8
#
import ctypes


class AsDictMixin:
    @classmethod
    def as_dict(cls, self):
        result = {}
        if not isinstance(self, AsDictMixin):
            # not a structure, assume it's already a python object
            return self
        if not hasattr(cls, "_fields_"):
            return result
        # sys.version_info >= (3, 5)
        # for (field, *_) in cls._fields_:  # noqa
        for field_tuple in cls._fields_:  # noqa
            field = field_tuple[0]
            if field.startswith('PADDING_'):
                continue
            value = getattr(self, field)
            type_ = type(value)
            if hasattr(value, "_length_") and hasattr(value, "_type_"):
                # array
                type_ = type_._type_
                if hasattr(type_, 'as_dict'):
                    value = [type_.as_dict(v) for v in value]
                else:
                    value = [i for i in value]
            elif hasattr(value, "contents") and hasattr(value, "_type_"):
                # pointer
                try:
                    if not hasattr(type_, "as_dict"):
                        value = value.contents
                    else:
                        type_ = type_._type_
                        value = type_.as_dict(value.contents)
                except ValueError:
                    # nullptr
                    value = None
            elif isinstance(value, AsDictMixin):
                # other structure
                value = type_.as_dict(value)
            result[field] = value
        return result


class Structure(ctypes.Structure, AsDictMixin):

    def __init__(self, *args, **kwds):
        # We don't want to use positional arguments fill PADDING_* fields

        args = dict(zip(self.__class__._field_names_(), args))
        args.update(kwds)
        super(Structure, self).__init__(**args)

    @classmethod
    def _field_names_(cls):
        if hasattr(cls, '_fields_'):
            return (f[0] for f in cls._fields_ if not f[0].startswith('PADDING'))
        else:
            return ()

    @classmethod
    def get_type(cls, field):
        for f in cls._fields_:
            if f[0] == field:
                return f[1]
        return None

    @classmethod
    def bind(cls, bound_fields):
        fields = {}
        for name, type_ in cls._fields_:
            if hasattr(type_, "restype"):
                if name in bound_fields:
                    if bound_fields[name] is None:
                        fields[name] = type_()
                    else:
                        # use a closure to capture the callback from the loop scope
                        fields[name] = (
                            type_((lambda callback: lambda *args: callback(*args))(
                                bound_fields[name]))
                        )
                    del bound_fields[name]
                else:
                    # default callback implementation (does nothing)
                    try:
                        default_ = type_(0).restype().value
                    except TypeError:
                        default_ = None
                    fields[name] = type_((
                        lambda default_: lambda *args: default_)(default_))
            else:
                # not a callback function, use default initialization
                if name in bound_fields:
                    fields[name] = bound_fields[name]
                    del bound_fields[name]
                else:
                    fields[name] = type_()
        if len(bound_fields) != 0:
            raise ValueError(
                "Cannot bind the following unknown callback(s) {}.{}".format(
                    cls.__name__, bound_fields.keys()
            ))
        return cls(**fields)


class Union(ctypes.Union, AsDictMixin):
    pass



def string_cast(char_pointer, encoding='utf-8', errors='strict'):
    value = ctypes.cast(char_pointer, ctypes.c_char_p).value
    if value is not None and encoding is not None:
        value = value.decode(encoding, errors=errors)
    return value


def char_pointer_cast(string, encoding='utf-8'):
    if encoding is not None:
        try:
            string = string.encode(encoding)
        except AttributeError:
            # In Python3, bytes has no encode attribute
            pass
    string = ctypes.c_char_p(string)
    return ctypes.cast(string, ctypes.POINTER(ctypes.c_char))



class FunctionFactoryStub:
    def __getattr__(self, _):
      return ctypes.CFUNCTYPE(lambda y:y)

# libraries['FIXME_STUB'] explanation
# As you did not list (-l libraryname.so) a library that exports this function
# This is a non-working stub instead. 
# You can either re-run clan2py with -l /path/to/library.so
# Or manually fix this by comment the ctypes.CDLL loading
_libraries = {}
_libraries['FIXME_STUB'] = FunctionFactoryStub() #  ctypes.CDLL('FIXME_STUB')
c_int128 = ctypes.c_ubyte*16
c_uint128 = c_int128
void = None
if ctypes.sizeof(ctypes.c_longdouble) == 8:
    c_long_double_t = ctypes.c_longdouble
else:
    c_long_double_t = ctypes.c_ubyte*8



# src/jclargs.h:26
class struct_OptInfo_T(Structure):
    pass

struct_OptInfo_T._pack_ = 1 # source:False
struct_OptInfo_T._fields_ = [
    # src/jclargs.h 26
    ('arguments', ctypes.POINTER(ctypes.c_char)),
    ('inputFile', ctypes.POINTER(ctypes.c_char)),
    ('outputFile', ctypes.POINTER(ctypes.c_char)),
    ('useJES3', ctypes.c_uint32, 1),
    ('debug', ctypes.c_uint32, 1),
    ('verbose', ctypes.c_uint32, 1),
    ('verboseStatements', ctypes.c_uint32, 1),
    ('help', ctypes.c_uint32, 1),
    ('PADDING_0', ctypes.c_uint64, 59),
]

# src/jclargs.h:35
OptInfo_T = struct_OptInfo_T
# src/jclmsgs.h:13

# values for enumeration 'JCLScanMsg_T'
JCLScanMsg_T__enumvalues = {
    -2: 'UnreachableCodeError',
    -1: 'InputEOF',
    0: 'NoError',
    1: 'TooFewArgsSingular',
    2: 'TooFewArgsPlural',
    3: 'TooManyArgs',
    4: 'UnrecognizedOption',
    5: 'InternalOutOfMemory_Generic',
    6: 'UnableToEstablishEnvironment',
    7: 'ErrorEstablishingEnvironment',
    8: 'IssueHelp',
    9: 'NoArgSpecified',
    10: 'UnableToOpenInput',
    11: 'UnableToOpenOutput',
    12: 'UnableToReopenInput',
    13: 'UnableToReopenOutput',
    14: 'InvalidRecordEncountered',
    15: 'ErrorScanningJCL',
    40: 'InvalidRecordUnknownType',
    41: 'InvalidRecordSlashSlashUnk',
    42: 'InvalidRecordSlashUnk',
    43: 'InvalidRecordUnk',
    44: 'InvalidRecordContinuedComment',
    45: 'InvalidRecordContinuedStringNoSlash',
    46: 'InvalidRecordContinuedCommentTooFewBlanks',
    47: 'InvalidRecordContinuedConditional',
    48: 'InvalidRecordContinuedParameter',
    100: 'InternalOutOfMemory_A',
    101: 'InternalOutOfMemory_B',
    102: 'InternalOutOfMemory_C',
    103: 'InternalOutOfMemory_D',
    104: 'InternalOutOfMemory_E',
    105: 'InternalOutOfMemory_F',
    106: 'InternalOutOfMemory_G',
    107: 'InternalOutOfMemory_H',
    108: 'InternalOutOfMemory_I',
    109: 'InternalOutOfMemory_J',
    110: 'InternalOutOfMemory_K',
    111: 'InternalOutOfMemory_L',
    112: 'InternalOutOfMemory_M',
    113: 'InternalOutOfMemory_N',
    114: 'InternalOutOfMemory_O',
    115: 'InternalOutOfMemory_P',
    116: 'InternalOutOfMemory_Q',
    117: 'InternalOutOfMemory_R',
    118: 'InternalOutOfMemory_S',
    119: 'InternalOutOfMemory_T',
    120: 'InternalOutOfMemory_U',
    121: 'InternalOutOfMemory_V',
    122: 'InternalOutOfMemory_W',
    123: 'InternalOutOfMemory_X',
}
UnreachableCodeError = -2
InputEOF = -1
NoError = 0
TooFewArgsSingular = 1
TooFewArgsPlural = 2
TooManyArgs = 3
UnrecognizedOption = 4
InternalOutOfMemory_Generic = 5
UnableToEstablishEnvironment = 6
ErrorEstablishingEnvironment = 7
IssueHelp = 8
NoArgSpecified = 9
UnableToOpenInput = 10
UnableToOpenOutput = 11
UnableToReopenInput = 12
UnableToReopenOutput = 13
InvalidRecordEncountered = 14
ErrorScanningJCL = 15
InvalidRecordUnknownType = 40
InvalidRecordSlashSlashUnk = 41
InvalidRecordSlashUnk = 42
InvalidRecordUnk = 43
InvalidRecordContinuedComment = 44
InvalidRecordContinuedStringNoSlash = 45
InvalidRecordContinuedCommentTooFewBlanks = 46
InvalidRecordContinuedConditional = 47
InvalidRecordContinuedParameter = 48
InternalOutOfMemory_A = 100
InternalOutOfMemory_B = 101
InternalOutOfMemory_C = 102
InternalOutOfMemory_D = 103
InternalOutOfMemory_E = 104
InternalOutOfMemory_F = 105
InternalOutOfMemory_G = 106
InternalOutOfMemory_H = 107
InternalOutOfMemory_I = 108
InternalOutOfMemory_J = 109
InternalOutOfMemory_K = 110
InternalOutOfMemory_L = 111
InternalOutOfMemory_M = 112
InternalOutOfMemory_N = 113
InternalOutOfMemory_O = 114
InternalOutOfMemory_P = 115
InternalOutOfMemory_Q = 116
InternalOutOfMemory_R = 117
InternalOutOfMemory_S = 118
InternalOutOfMemory_T = 119
InternalOutOfMemory_U = 120
InternalOutOfMemory_V = 121
InternalOutOfMemory_W = 122
InternalOutOfMemory_X = 123
JCLScanMsg_T = ctypes.c_int32 # enum
# src/jclargs.h:44
class struct_Option(Structure):
    pass

# src/jclargs.h:26
struct_Option._pack_ = 1 # source:False
struct_Option._fields_ = [
    ('fn', ctypes.CFUNCTYPE(JCLScanMsg_T, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(struct_Option), ctypes.POINTER(struct_OptInfo_T))),
    ('shortName', ctypes.POINTER(ctypes.c_char)),
    ('longName', ctypes.POINTER(ctypes.c_char)),
    ('defaultValue', ctypes.POINTER(ctypes.c_char)),
    ('specifiedValue', ctypes.POINTER(ctypes.c_char)),
]

Option_T = struct_Option
# src/jclargs.h:46
# src/jclargs.h:26
# src/jclargs.h 46
try:
    processArgs = _libraries['FIXME_STUB'].processArgs
    processArgs.restype = JCLScanMsg_T
# processArgs(argc, argv, optInfo)
    processArgs.argtypes = [ctypes.c_int32, ctypes.POINTER(ctypes.c_char) * 0, ctypes.POINTER(struct_OptInfo_T)]
except AttributeError:
    pass
processArgs.__doc__ = """JCLScanMsg_T processArgs(c_int32 argc, array_LP_c_char argv, LP_struct_OptInfo_T optInfo)
    src/jclargs.h:46"""
# src/gen.h:15
class struct_JCL(Structure):
    pass

# /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/_stdio.h:128
class struct___sFILE(Structure):
    pass

# src/scanjcl.h:192
class struct_JCLLines_T(Structure):
    pass

# src/scanjcl.h:244
class struct_JCLStmts_T(Structure):
    pass

struct_JCL._pack_ = 1 # source:False
struct_JCL._fields_ = [
    ('infp', ctypes.POINTER(struct___sFILE)),
    ('lines', ctypes.POINTER(struct_JCLLines_T)),
    ('stmts', ctypes.POINTER(struct_JCLStmts_T)),
]

JCL_T = struct_JCL
# src/gen.h:17
class struct_Gen(Structure):
    pass

# /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/_stdio.h:128
struct_Gen._pack_ = 1 # source:False
struct_Gen._fields_ = [
    # src/gen.h 17
    ('outfp', ctypes.POINTER(struct___sFILE)),
]

# /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/_stdio.h:128
# /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/_stdio.h:100
class struct___sFILEX(Structure):
    pass

# /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/_stdio.h:94
class struct___sbuf(Structure):
    pass

struct___sbuf._pack_ = 1 # source:False
struct___sbuf._fields_ = [
    # /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/_stdio.h 94
    ('_base', ctypes.POINTER(ctypes.c_ubyte)),
    ('_size', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

struct___sFILE._pack_ = 1 # source:False
struct___sFILE._fields_ = [
    # /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/_stdio.h 128
    ('_p', ctypes.POINTER(ctypes.c_ubyte)),
    ('_r', ctypes.c_int32),
    ('_w', ctypes.c_int32),
    ('_flags', ctypes.c_int16),
    ('_file', ctypes.c_int16),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('_bf', struct___sbuf),
    ('_lbfsize', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('_cookie', ctypes.POINTER(None)),
    ('_close', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(None))),
    ('_read', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(None), ctypes.POINTER(ctypes.c_char), ctypes.c_int32)),
    ('_seek', ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.POINTER(None), ctypes.c_int64, ctypes.c_int32)),
    ('_write', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(None), ctypes.POINTER(ctypes.c_char), ctypes.c_int32)),
    ('_ub', struct___sbuf),
    ('_extra', ctypes.POINTER(struct___sFILEX)),
    ('_ur', ctypes.c_int32),
    ('_ubuf', ctypes.c_ubyte * 3),
    ('_nbuf', ctypes.c_ubyte * 1),
    ('_lb', struct___sbuf),
    ('_blksize', ctypes.c_int32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('_offset', ctypes.c_int64),
]

# /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/_stdio.h:100
# src/gen.h:19
Gen_T = struct_Gen
# src/gen.h:21
class struct_ProgInfo(Structure):
    pass

# src/gen.h:17
struct_ProgInfo._pack_ = 1 # source:False
struct_ProgInfo._fields_ = [
    # src/gen.h 21
    ('jcl', ctypes.POINTER(struct_JCL)),
    ('gen', ctypes.POINTER(struct_Gen)),
]

# src/gen.h:24
ProgInfo_T = struct_ProgInfo
# src/gen.h:26
# src/jclargs.h:26
# src/gen.h:21
# src/gen.h 26
try:
    establishOutput = _libraries['FIXME_STUB'].establishOutput
    establishOutput.restype = JCLScanMsg_T
# establishOutput(optInfo, progInfo)
    establishOutput.argtypes = [ctypes.POINTER(struct_OptInfo_T), ctypes.POINTER(struct_ProgInfo)]
except AttributeError:
    pass
establishOutput.__doc__ = """JCLScanMsg_T establishOutput(LP_struct_OptInfo_T optInfo, LP_struct_ProgInfo progInfo)
    src/gen.h:26"""
# src/gen.h:27
# src/jclargs.h:26
# src/gen.h:21
# src/gen.h 27
try:
    genJCL = _libraries['FIXME_STUB'].genJCL
    genJCL.restype = JCLScanMsg_T
# genJCL(optInfo, progInfo)
    genJCL.argtypes = [ctypes.POINTER(struct_OptInfo_T), ctypes.POINTER(struct_ProgInfo)]
except AttributeError:
    pass
genJCL.__doc__ = """JCLScanMsg_T genJCL(LP_struct_OptInfo_T optInfo, LP_struct_ProgInfo progInfo)
    src/gen.h:27"""
# src/scanjcl.h:123
class struct_VarStr_T(Structure):
    pass

struct_VarStr_T._pack_ = 1 # source:False
struct_VarStr_T._fields_ = [
    # src/scanjcl.h 123
    ('len', ctypes.c_uint64),
    # SOMF: updated this to c_char_p so we get a string back
    ('txt', ctypes.c_char_p),
]

# src/scanjcl.h:126
VarStr_T = struct_VarStr_T
# src/scanjcl.h:162

# values for enumeration 'JCLScanState_T'
JCLScanState_T__enumvalues = {
    0: 'JCLNotContinued',
    1: 'JCLContinueParameter',
    2: 'JCLContinueString',
    3: 'JCLContinueComment',
    4: 'JCLContinueJES2ControlStatement',
    5: 'JCLContinueJES3DatasetControlStatement',
    6: 'JCLInlineText',
    7: 'JCLContinueConditional',
}
JCLNotContinued = 0
JCLContinueParameter = 1
JCLContinueString = 2
JCLContinueComment = 3
JCLContinueJES2ControlStatement = 4
JCLContinueJES3DatasetControlStatement = 5
JCLInlineText = 6
JCLContinueConditional = 7
JCLScanState_T = ctypes.c_uint32 # enum
# src/scanjcl.h:173

# values for enumeration 'DatasetType_T'
DatasetType_T__enumvalues = {
    0: 'NoDataset',
    1: 'OutstreamDataset',
    2: 'InstreamDatasetStar',
    3: 'InstreamDatasetData',
}
NoDataset = 0
OutstreamDataset = 1
InstreamDatasetStar = 2
InstreamDatasetData = 3
DatasetType_T = ctypes.c_uint32 # enum
# src/scanjcl.h:180

# values for enumeration 'JCLParmContext_T'
JCLParmContext_T__enumvalues = {
    1: 'JCLParmInKeyword',
    2: 'JCLParmInValue',
    3: 'JCLParmInQuote',
    4: 'JCLParmInParen',
}
JCLParmInKeyword = 1
JCLParmInValue = 2
JCLParmInQuote = 3
JCLParmInParen = 4
JCLParmContext_T = ctypes.c_uint32 # enum
# src/scanjcl.h:191
class struct_JCLLine(Structure):
    pass

struct_JCLLine._pack_ = 1 # source:False
struct_JCLLine._fields_ = [
    ('next', ctypes.POINTER(struct_JCLLine)),
    ('text', ctypes.c_char * 81),
    ('PADDING_0', ctypes.c_ubyte * 7),
]

JCLLine_T = struct_JCLLine
# src/scanjcl.h:192
struct_JCLLines_T._pack_ = 1 # source:False
struct_JCLLines_T._fields_ = [
    # src/scanjcl.h 192
    ('head', ctypes.POINTER(struct_JCLLine)),
    ('tail', ctypes.POINTER(struct_JCLLine)),
    ('curLine', ctypes.c_uint64),
]

# src/scanjcl.h:196
JCLLines_T = struct_JCLLines_T
# src/scanjcl.h:205
class struct_KeyValuePair(Structure):
    pass

struct_KeyValuePair._pack_ = 1 # source:False
struct_KeyValuePair._fields_ = [
    ('next', ctypes.POINTER(struct_KeyValuePair)),
    ('key', VarStr_T),
    ('val', VarStr_T),
    ('comment', ctypes.POINTER(ctypes.c_char)),
    ('hasNewline', ctypes.c_int32, 1),
    ('PADDING_0', ctypes.c_uint64, 63),
]

KeyValuePair_T = struct_KeyValuePair
# src/scanjcl.h:212
class struct_ScannedLine(Structure):
    pass

struct_ScannedLine._pack_ = 1 # source:False
struct_ScannedLine._fields_ = [
    ('next', ctypes.POINTER(struct_ScannedLine)),
    ('parmText', ctypes.POINTER(ctypes.c_char)),
    ('commentText', ctypes.POINTER(ctypes.c_char)),
]

ScannedLine_T = struct_ScannedLine
# src/scanjcl.h:214
class struct_ConditionalExpression_T(Structure):
    pass

struct_ConditionalExpression_T._pack_ = 1 # source:False
struct_ConditionalExpression_T._fields_ = [
    # src/scanjcl.h 214
    ('text', ctypes.POINTER(ctypes.c_char)),
    ('comment', ctypes.POINTER(ctypes.c_char)),
]

# src/scanjcl.h:217
ConditionalExpression_T = struct_ConditionalExpression_T
# src/scanjcl.h:219
class struct_InlineData_T(Structure):
    pass

struct_InlineData_T._pack_ = 1 # source:False
struct_InlineData_T._fields_ = [
    # src/scanjcl.h 219
    ('len', ctypes.c_uint64),
    ('retainDelim', ctypes.c_char * 3),
    ('PADDING_0', ctypes.c_ubyte * 5),
    ('bytes', ctypes.POINTER(ctypes.c_char)),
]

# src/scanjcl.h:223
InlineData_T = struct_InlineData_T
# src/scanjcl.h:242
class struct_JCLStmt(Structure):
    pass

# src/scanjcl.h:214
# src/scanjcl.h:219
struct_JCLStmt._pack_ = 1 # source:False
struct_JCLStmt._fields_ = [
    ('next', ctypes.POINTER(struct_JCLStmt)),
    ('name', ctypes.POINTER(ctypes.c_char)),
    ('type', ctypes.POINTER(ctypes.c_char)),
    ('lines', ctypes.c_uint64),
    ('scanhead', ctypes.POINTER(struct_ScannedLine)),
    ('scantail', ctypes.POINTER(struct_ScannedLine)),
    ('kvphead', ctypes.POINTER(struct_KeyValuePair)),
    ('kvptail', ctypes.POINTER(struct_KeyValuePair)),
    ('conditional', ctypes.POINTER(struct_ConditionalExpression_T)),
    ('data', ctypes.POINTER(struct_InlineData_T)),
    ('firstJCLLine', ctypes.POINTER(struct_JCLLine)),
]

JCLStmt_T = struct_JCLStmt
# src/scanjcl.h:244
struct_JCLStmts_T._pack_ = 1 # source:False
struct_JCLStmts_T._fields_ = [
    # src/scanjcl.h 244
    ('head', ctypes.POINTER(struct_JCLStmt)),
    ('tail', ctypes.POINTER(struct_JCLStmt)),
    ('curStmt', ctypes.c_uint64),
    ('state', JCLScanState_T),
    ('datasetType', DatasetType_T),
    ('delimiter', ctypes.c_char * 3),
    ('PADDING_0', ctypes.c_ubyte * 5),
]

# src/scanjcl.h:251
JCLStmts_T = struct_JCLStmts_T
# src/scanjcl.h:259
# src/jclargs.h:26
# src/gen.h:21
ScanFn_T = ctypes.CFUNCTYPE(JCLScanMsg_T, ctypes.POINTER(struct_OptInfo_T), ctypes.POINTER(struct_ProgInfo), ctypes.c_uint64, ctypes.c_uint64)
# src/scanjcl.h:260
class struct_Scanner_T(Structure):
    pass

# src/jclargs.h:26
# src/gen.h:21
struct_Scanner_T._pack_ = 1 # source:False
struct_Scanner_T._fields_ = [
    # src/scanjcl.h 260
    ('scan', ctypes.CFUNCTYPE(JCLScanMsg_T, ctypes.POINTER(struct_OptInfo_T), ctypes.POINTER(struct_ProgInfo), ctypes.c_uint64, ctypes.c_uint64)),
]

# src/scanjcl.h:262
Scanner_T = struct_Scanner_T
# src/scanjcl.h:265
# src/jclargs.h:26
# src/gen.h:21
# src/scanjcl.h 265
try:
    scanJCL = _libraries['FIXME_STUB'].scanJCL
    scanJCL.restype = JCLScanMsg_T
# scanJCL(optInfo, progInfo)
    scanJCL.argtypes = [ctypes.POINTER(struct_OptInfo_T), ctypes.POINTER(struct_ProgInfo)]
except AttributeError:
    pass
scanJCL.__doc__ = """JCLScanMsg_T scanJCL(LP_struct_OptInfo_T optInfo, LP_struct_ProgInfo progInfo)
    src/scanjcl.h:265"""
# src/scanjcl.h:266
# src/jclargs.h:26
# src/gen.h:21
# src/scanjcl.h 266
try:
    establishInput = _libraries['FIXME_STUB'].establishInput
    establishInput.restype = JCLScanMsg_T
# establishInput(optInfo, progInfo)
    establishInput.argtypes = [ctypes.POINTER(struct_OptInfo_T), ctypes.POINTER(struct_ProgInfo)]
except AttributeError:
    pass
establishInput.__doc__ = """JCLScanMsg_T establishInput(LP_struct_OptInfo_T optInfo, LP_struct_ProgInfo progInfo)
    src/scanjcl.h:266"""
__all__ = \
    ['ConditionalExpression_T', 'DatasetType_T',
    'ErrorEstablishingEnvironment', 'ErrorScanningJCL', 'Gen_T',
    'InlineData_T', 'InputEOF', 'InstreamDatasetData',
    'InstreamDatasetStar', 'InternalOutOfMemory_A',
    'InternalOutOfMemory_B', 'InternalOutOfMemory_C',
    'InternalOutOfMemory_D', 'InternalOutOfMemory_E',
    'InternalOutOfMemory_F', 'InternalOutOfMemory_G',
    'InternalOutOfMemory_Generic', 'InternalOutOfMemory_H',
    'InternalOutOfMemory_I', 'InternalOutOfMemory_J',
    'InternalOutOfMemory_K', 'InternalOutOfMemory_L',
    'InternalOutOfMemory_M', 'InternalOutOfMemory_N',
    'InternalOutOfMemory_O', 'InternalOutOfMemory_P',
    'InternalOutOfMemory_Q', 'InternalOutOfMemory_R',
    'InternalOutOfMemory_S', 'InternalOutOfMemory_T',
    'InternalOutOfMemory_U', 'InternalOutOfMemory_V',
    'InternalOutOfMemory_W', 'InternalOutOfMemory_X',
    'InvalidRecordContinuedComment',
    'InvalidRecordContinuedCommentTooFewBlanks',
    'InvalidRecordContinuedConditional',
    'InvalidRecordContinuedParameter',
    'InvalidRecordContinuedStringNoSlash', 'InvalidRecordEncountered',
    'InvalidRecordSlashSlashUnk', 'InvalidRecordSlashUnk',
    'InvalidRecordUnk', 'InvalidRecordUnknownType', 'IssueHelp',
    'JCLContinueComment', 'JCLContinueConditional',
    'JCLContinueJES2ControlStatement',
    'JCLContinueJES3DatasetControlStatement', 'JCLContinueParameter',
    'JCLContinueString', 'JCLInlineText', 'JCLLine_T', 'JCLLines_T',
    'JCLNotContinued', 'JCLParmContext_T', 'JCLParmInKeyword',
    'JCLParmInParen', 'JCLParmInQuote', 'JCLParmInValue',
    'JCLScanMsg_T', 'JCLScanState_T', 'JCLStmt_T', 'JCLStmts_T',
    'JCL_T', 'KeyValuePair_T', 'NoArgSpecified', 'NoDataset',
    'NoError', 'OptInfo_T', 'Option_T', 'OutstreamDataset',
    'ProgInfo_T', 'ScanFn_T', 'ScannedLine_T', 'Scanner_T',
    'TooFewArgsPlural', 'TooFewArgsSingular', 'TooManyArgs',
    'UnableToEstablishEnvironment', 'UnableToOpenInput',
    'UnableToOpenOutput', 'UnableToReopenInput',
    'UnableToReopenOutput', 'UnreachableCodeError',
    'UnrecognizedOption', 'VarStr_T', 'establishInput',
    'establishOutput', 'genJCL', 'processArgs', 'scanJCL',
    'struct_ConditionalExpression_T', 'struct_Gen',
    'struct_InlineData_T', 'struct_JCL', 'struct_JCLLine',
    'struct_JCLLines_T', 'struct_JCLStmt', 'struct_JCLStmts_T',
    'struct_KeyValuePair', 'struct_OptInfo_T', 'struct_Option',
    'struct_ProgInfo', 'struct_ScannedLine', 'struct_Scanner_T',
    'struct_VarStr_T', 'struct___sFILE', 'struct___sFILEX',
    'struct___sbuf']
