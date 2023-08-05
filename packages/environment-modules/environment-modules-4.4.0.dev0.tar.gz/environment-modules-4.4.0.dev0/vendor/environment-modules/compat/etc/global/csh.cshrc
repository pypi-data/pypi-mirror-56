#----------------------------------------------------------------------#
# system-wide csh.cshrc                                                #
# aliases and settings for all csh-derivative shells                   #
#----------------------------------------------------------------------#
# module initialization
#
if ($?tcsh) then
	set modules_shell="tcsh"
else
	set modules_shell="csh"
endif

#alias module 'eval `/home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/Modules/$MODULE_VERSION/bin/modulecmd '$modules_shell '\!*`'
alias module 'eval `/home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/bin/modulecmd '$modules_shell '\!*`'

unset modules_shell

#----------------------------------------------------------------------#
# set this if bash exists on your system and to use it
# instead of sh - so per-process dot files will be sourced.
#----------------------------------------------------------------------#

alias sh bash

#----------------------------------------------------------------------#
# further system customizations can be added here
#
