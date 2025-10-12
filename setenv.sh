# source /opt/python-virtual-env/py313/bin/activate
py313

ADMIN_TOOL_SOURCE_PATH=${PWD}

# PYTHONDONTWRITEBYTECODE
#   If this is set to a non-empty string, Python won’t try to write .pyc files on the import of source modules.
#   This is equivalent to specifying the -B option.
# export PYTHONDONTWRITEBYTECODE=True

# PYTHONPYCACHEPREFIX
#   If this is set, Python will write .pyc files in a mirror directory tree at this path,
#   instead of in __pycache__ directories within the source tree.
#   This is equivalent to specifying the -X pycache_prefix=PATH option.
export PYTHONPYCACHEPREFIX=${ADMIN_TOOL_SOURCE_PATH}/.pycache-${USER}

append_to_python_path_if_not $PWD
# append_to_path_if_not $PWD/bin
