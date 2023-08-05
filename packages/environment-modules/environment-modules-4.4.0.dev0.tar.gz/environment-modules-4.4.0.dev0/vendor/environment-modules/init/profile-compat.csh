# initialize compatibility version rather main version
setenv MODULES_USE_COMPAT_VERSION 1

if ($?tcsh) then
   source /home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/init/tcsh
else
   source /home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/init/csh
endif
