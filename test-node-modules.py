####################################################################################################

# from AdminToolkit.locate import *
# from AdminToolkit.du import *
from AdminToolkit.filter import *

####################################################################################################

# locate_node_modules()
# du('/usr/share/code/resources/app/extensions/node_modules')

NODE_MODULES = 'node_modules'
pipe = Locate(NODE_MODULES) * Directory()
for _ in pipe.run():
    print(_)

####################################################################################################

# def locate_node_modules() -> Iterator[str]:
#     NODE_MODULES = 'node_modules'
#     for _ in locate(NODE_MODULES):
#         _ = Path(_)
#         if _.name == NODE_MODULES:
#             c = _.parts.count(NODE_MODULES)
#             parent = str(_.parent)
#             if c == 1 and NODE_MODULES not in parent and '.pnpm' not in parent:
#                 print(_)
