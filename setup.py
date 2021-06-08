from cx_Freeze import setup, Executable


executables = [Executable("main.py", icon='icon.ico')]

includes = ["pandas", "pymssql", "yaml", "itertools", "loguru", "sys"]
excludes = ['_distutils_hack', 'email', 'lib2to3', 'email', 'html', 'http', 'msilib',
            'pkg_resources', 'pydoc_data', 'setuptools', 'sqlite3', 'test', 'unittest',
            'xmlrpc', '_decimal', '_elementtree', '_hashlib', '_lzma', '_msi', '_queue',
            '_ssl', '_testcapi', '_testinternalcapi', '_uuid']

options = {
    'build_exe': {
        'include_files': ['icon.ico', './conn_data.yaml'],
        'includes': includes,
        'excludes': excludes,
        'include_msvcr': True
    },
}

setup(
    name="Searcher",
    options=options,
    version="0.0.1",
    description='Скрипт для анализа логов UniGate на несоответствия кодов исследований',
    executables=executables
)
