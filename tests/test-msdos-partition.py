####################################################################################################

from pprint import pprint

from AdminToolkit.config import config
config.DEBUG = True
config.MOCKUP = True

from AdminToolkit.config import common_path as cp
from AdminToolkit.tools.mockup import MOCKUP_CACHE
from AdminToolkit.interface.disk.partition import *

####################################################################################################

MOCKUP_CACHE.add_cmd_mockup(
    (cp.PARTED, '--json', '/dev/sda', 'unit s', 'print'),
'''
{
   "disk": {
      "path": "/dev/sda",
      "size": "3907029168s",
      "model": "ATA ST32000644NS",
      "transport": "scsi",
      "logical-sector-size": 512,
      "physical-sector-size": 512,
      "label": "msdos",
      "max-partitions": 4,
      "partitions": [
         {
            "number": 1,
            "start": "2048s",
            "end": "999423s",
            "size": "997376s",
            "type": "primary",
            "filesystem": "ext4",
            "flags": [
                "boot"
            ]
         },{
            "number": 2,
            "start": "999424s",
            "end": "2000895s",
            "size": "1001472s",
            "type": "primary",
            "filesystem": "ext4"
         },{
            "number": 3,
            "start": "2000896s",
            "end": "33202175s",
            "size": "31201280s",
            "type": "primary",
            "filesystem": "linux-swap(v1)"
         },{
            "number": 4,
            "start": "33202176s",
            "end": "3907028991s",
            "size": "3873826816s",
            "type": "extended"
         },{
            "number": 5,
            "start": "33204224s",
            "end": "3907028991s",
            "size": "3873824768s",
            "type": "logical",
            "flags": [
                "raid"
            ]
         }
      ]
   }
}
'''
)

# _ = parted('sda')
# pprint(_)

query = 'parts /dev/sda'

from AdminToolkit.cli import Cli
cli = Cli(config.CLI_COMMANDS_PATH)
cli.start(query)
