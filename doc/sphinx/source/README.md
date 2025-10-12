The repository contains a **Linux Administration Toolkit** written in **Python**.

The motivations of this toolkit can be resumed by this :

- UNIX implements the paradigm of everything is a file
- Microsoft PowerShell implements an object paradigm
- XTerm features 256 RGB colors
- Shell is great for quick and dirty scripts but Python is easier to maintain for more complicated tasks
- On Linux some information area available from:

  - `/dev`, `/proc`, `/sys`, `/run` virtual filesystems
  - `\etc` configuration files
  - system calls or user space API
  - commands (based on the previous ones)

- usually the content of the files of the virtual filesystems in not script friendly (some ASCII dumped by printk...)
- `\etc` is not standardized
- In the same way, many commands

 - doesn't have a colourized mode
 - doesn't have a JSON output
 - have an output which is misleading or have missing information
 - some commands can easily kill your system by mistake, for example let try this `rm -r foo/bar<space typo>/` or `dd of=/dev/<wrong device>`

Conclusion, it is somehow a pains to interact with the system.

This toolkit provides a Python API to gather system information or to do some administration tasks.
It acts as a wrapper to help scripting.

A command line utility (CLI) is provided to run "commands" or tasks, which features :

  - dynamic completions
  - XTerm colours
  - gather the commands from Python modules
  - gather an help for a command from its docstring and annotations
  - a protection for dangerous actions (nearly impossible to continue by stressed fingers)
  
A command can also be executed from the Shell if we don't want to start the CLI.

The toolkit implements an API to read files and to call commands that can instrumented by
mockups.  This is useful when you want to test and debug a particular configuration.  You just have
to copy-paste the content of a file or the output of a command and register it in a Python file.

Currently, the toolkit features :

  - os information (distribution, kernel)
  - network configuration (basic)
  - show disk information (partition, MDRaid, LVM, mountpoints, disk usage, ...)
  - rsync backup

## Note for contributors

Such A toolkit is intrinsically opinionated, thus we must separate a common
API and keep a full flexibility for commands.  That means scripts what you want.

This toolkit is designed for a command line use case and not GUI.  It means that it must run over
a SSH terminal for example.

Up to now, this toolkit is not designed to provide a full API for everything.
