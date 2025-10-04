####################################################################################################

from pathlib import Path
import math

from AdminToolkit.filesystem.tree import Walker, Directory
from AdminToolkit.tools.format import byte_humanize

####################################################################################################

# root = Path(__file__).parents[1].joinpath('AdminToolkit')
root = Path('/home/fabrice/home/developpement')

print('walk on disk...')
root_node = Directory(root, root=True)
walker = Walker(root)
walker.run(
    top_down=True,
    sort=False,
    follow_symlinks=False,
    max_depth=-1,
)
print('done')

# print()
# pprint(root_node)

# print()
# root_node.walk(
#     callback=lambda node, depth: print(' '*4*depth + f"{node.path.name} {node.size:_}"),
#     top_down=True,
#     sort_func='name',
# )

KB = 1000
MB = 1000**2
GB = 1000**3

print('accumulate...')
root_node.update_size_accumulator()
print('done')

def show(node, depth):
    if depth <= 3 and node.size_accumulator >= GB:
        # print(' '*4*depth + f"{node.path.name} {size}")
        left = ' '*4*depth + node.path.name
        size = byte_humanize(node.size_accumulator)
        right = '='*math.ceil(50 * node.size_accumulator / root_node.size_accumulator)
        print(f"{left:50}   {size:>10}   {right}")

root_node.walk(
    callback=show,
    top_down=True,
    sort_func='name',
    cls_filter=Directory,
)
