#
# siteconfig.tcl - Site specific configuration script disabling
#   implicit_default configuration option and locking its value to ensure
#   it is not altered by users
#
# Author: Xavier Delaruelle <xavier.delaruelle@cea.fr>
# Compatibility: Modules v4.4
#
# Installation: put this file in the 'etc' directory of your Modules
#   installation. Refer to the "Modulecmd startup" section in the
#   module(1) man page to get this location.

# disable implicit_default option
setConf implicit_default 0

# forbid `implicit_default` config option superseding
lappendConf locked_configs implicit_default
