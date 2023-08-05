# initialize compatibility version rather main version
MODULES_USE_COMPAT_VERSION=1
export MODULES_USE_COMPAT_VERSION

shell=$(/usr/bin/basename $(/bin/ps -p $$ -ocomm=))

if [ -f /home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/init/$shell ]; then
   source /home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/init/$shell
else
   source /home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/init/sh
fi
