import __main__
import os

if hasattr(__main__, '__file__'):
    main_directory = os.path.dirname(os.path.abspath(__main__.__file__))
else:
    main_directory = os.getcwd()
main_sibling_filenames = set(os.listdir(main_directory))

# This list was generated by running this code at the end of cmu_graphics.py:
# import sys
# print('\n'.join(sorted(x for x in list(sys.modules.keys()) if '.' not in x)))

disallowed_filenames = {
    f'{x}.py'
    for x in [
        'PIL', '__future__', '__main__', '_abc', '_ast', '_bisect', '_blake2',
        '_bz2', '_codecs', '_collections', '_collections_abc', '_compression',
        '_datetime', '_decimal', '_distutils_hack', '_frozen_importlib',
        '_frozen_importlib_external', '_functools', '_hashlib', '_imp', '_io',
        '_json', '_locale', '_lzma', '_opcode', '_operator',
        '_posixsubprocess', '_random', '_scproxy', '_sha512', '_signal',
        '_sitebuiltins', '_socket', '_sre', '_ssl', '_stat', '_string',
        '_struct', '_thread', '_uuid', '_virtualenv', '_warnings', '_weakref',
        '_weakrefset', 'abc', 'array', 'ast', 'atexit', 'base64', 'binascii',
        'bisect', 'builtins', 'bz2', 'cairo', 'calendar', 'certifi',
        'cmu_graphics', 'code', 'codecs', 'codeop', 'collections',
        'contextlib', 'copy', 'copyreg', 'datetime', 'decimal', 'dis', 'email',
        'encodings', 'enum', 'errno', 'fcntl', 'fnmatch', 'functools',
        'genericpath', 'hashlib', 'http', 'importlib', 'inspect', 'io',
        'itertools', 'json', 'keyword', 'linecache', 'locale', 'logging',
        'lzma', 'marshal', 'math', 'ntpath', 'numbers', 'opcode', 'operator',
        'os', 'pathlib', 'platform', 'posix', 'posixpath', 'quopri', 'random',
        're', 'reprlib', 'select', 'selectors', 'shutil', 'signal', 'site',
        'socket', 'sre_compile', 'sre_constants', 'sre_parse', 'ssl', 'stat',
        'string', 'struct', 'subprocess', 'sys', 'tempfile', 'threading',
        'time', 'token', 'tokenize', 'traceback', 'types', 'typing',
        'unicodedata', 'urllib', 'uu', 'uuid', 'warnings', 'weakref',
        'zipimport', 'zlib'
    ]
}

overlap_filenames = sorted(list(main_sibling_filenames & disallowed_filenames))

if overlap_filenames:
    raise Exception(f'''

******************************************************************************
* The following files in {main_directory}
* may prevent your program from running correctly. Please rename or remove
* these files.
*
* {", ".join(overlap_filenames)}
******************************************************************************
''')

from .libs import loader_util

loader_util.verify_support()

from cmu_graphics.cmu_graphics import (
    app,
    Arc,
    Circle,
    Group,
    Image,
    Label,
    Line,
    Oval,
    Polygon,
    Rect,
    RegularPolygon,
    Star,
    drawArc,
    drawCircle,
    drawImage,
    drawLabel,
    drawLine,
    drawOval,
    drawPolygon,
    drawRect,
    drawRegularPolygon,
    drawStar,
    ArcShape,
    CircleShape,
    ImageShape,
    LabelShape,
    LineShape,
    OvalShape,
    PolygonShape,
    RectShape,
    RegularPolygonShape,
    StarShape,
    Sound,
    gradient,
    rgb,
    almostEqual,
    rounded,
    round,
    dcos,
    dsin,
    onSteps,
    onKeyHolds,
    onKeyPresses,
    setLanguage,
    print,
    assertEqual,
    Robot,
    runApp,
    runAppWithScreens,
    setActiveScreen,
    getImageSize,
    pygameEvent,
    onStepEvent,
    onMainLoopEvent,
)

from cmu_graphics.utils import (
    angleTo,
    distance,
    fromPythonAngle,
    getPointInDir,
    makeList,
    rounded,
    pythonRound,
    toPythonAngle
)

from random import (
    choice,
    random,
    randrange,
    seed,
)

from cmu_graphics.shape_logic import (
    TRANSLATED_GLOBALS,
    TRANSLATED_BOOLEANS,
    TRANSLATED_KEY_NAMES,
    accentCombinations,
    PILWrapper as CMUImage
)

__all__ = TRANSLATED_GLOBALS['keys']
__all__.extend(['setLanguage', 'cmu_graphics', 'runApp', 'runAppWithScreens', 'setActiveScreen', 'getImageSize', 'dcos', 'dsin'])
__all__.extend(['drawArc', 'ArcShape', 'drawCircle', 'CircleShape', 'drawImage', 'ImageShape', 'drawLabel', 'LabelShape', 'drawLine', 'LineShape', 'drawOval', 'OvalShape', 'drawPolygon', 'PolygonShape', 'drawRect', 'RectShape', 'drawRegularPolygon', 'RegularPolygonShape', 'drawStar', 'StarShape'])

g = globals()
for language in TRANSLATED_GLOBALS:
    if language != 'keys':
        for (en_name, trans_name) in TRANSLATED_GLOBALS[language].items():
            if trans_name and trans_name != en_name and en_name in g:
                for accent_combination in accentCombinations(trans_name):
                    g[accent_combination] = g[en_name]
                    __all__.append(accent_combination)

for language in TRANSLATED_BOOLEANS:
    if language != 'keys':
        for (en_name, trans_name) in TRANSLATED_BOOLEANS[language].items():
            globals()[trans_name] = en_name == 'True'
            __all__.append(trans_name)

__all__ = list(set(__all__))