####################################################################################################

# raise_if_not_root, 
from AdminToolkit.danger import raise_if_root_device, CONFIRM_DANGER
from AdminToolkit.interface.user import raise_if_not_root
from AdminToolkit.interface.disk.partition import partion_to_device, clear_device
from AdminToolkit.tools.subprocess import RUN_DANGEROUS

####################################################################################################

print(partion_to_device('sda'))
print(partion_to_device('sda12'))
print(partion_to_device('/dev/sda'))
print(partion_to_device('/dev/sda12'))
print(partion_to_device('/dev////sda12'))

RUN_DANGEROUS('Test...', ('foo', '--bar'))

raise_if_not_root()
raise_if_root_device('sda')
CONFIRM_DANGER('Test...')

# clear_device('sdz')
