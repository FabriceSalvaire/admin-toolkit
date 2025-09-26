export ADMIN_TOOL_SOURCE_PATH=${PWD}

# source /opt/python-virtual-env/py313/bin/activate
py313

export PYTHONPYCACHEPREFIX=${ADMIN_TOOL_SOURCE_PATH}/.pycache
export PYTHONDONTWRITEBYTECODE=${ADMIN_TOOL_SOURCE_PATH}/.pycache

append_to_python_path_if_not $PWD
# append_to_path_if_not $PWD/bin
