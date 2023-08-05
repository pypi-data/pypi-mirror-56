# get current shell name by querying shell variables or looking at parent
# process name
if [ -n "${BASH:-}" ]; then
   shell=${BASH##*/}
elif [ -n "${ZSH_NAME:-}" ]; then
   shell=$ZSH_NAME
else
   shell=$(/usr/bin/basename $(/bin/ps -p $$ -ocomm=))
fi

if [ -f /home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/init/$shell ]; then
   . /home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/init/$shell
else
   . /home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/init/sh
fi
