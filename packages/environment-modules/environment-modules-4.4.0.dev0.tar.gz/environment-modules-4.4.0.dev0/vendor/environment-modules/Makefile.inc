# Definitions shared across the Makefiles of this project
# run ./configure to generate Makefile.inc

# set default installation paths
baseprefix := /home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5
prefix := /home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5
bindir := /home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/bin
libdir := /home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/lib
libexecdir := /home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/libexec
etcdir := /home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/etc
initdir := /home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/init
modulefilesdir := /home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/modulefiles
datarootdir := /home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/share
mandir := /home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/share/man
docdir := /home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/share/doc
vimdatadir := /home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/share/vim/vimfiles
moduleshome := /home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5

# versioning mode installation
versioning := n

# Modules version
VERSION := 4.4.0

# modulepaths and modulefiles to enable in default config
modulepath := /home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/modulefiles
loadedmodules := 

# silent shell debug support
silentshdbgsupport := y
# define or not shell startup file to initialize module
setshellstartup := y
# runtime quarantine mechanism
quarantinesupport := y
quarantinevars := 

# also install compatibility C version
compatversion := y
EXEEXT := 

# install Modules Tcl extension library
libtclenvmodules := y
SHLIB_SUFFIX := .so

# enable or not some specific definition
setmanpath := y
appendmanpath := n
setbinpath := y
appendbinpath := n
setdotmodulespath := n
docinstall := y
vimaddons  := y
examplemodulefiles := y

# where to install init config files
initconfin := initdir

# able to build documentation?
builddoc := y
# able to handle compat as git worktree?
gitworktree := y
# able to use manpath cmd to get currently set manpath
usemanpath := y

# pager setup
pager := /usr/bin/less
pageropts := -eFKRX

# defaut verbosity
verbosity := normal

# color setup
color := n
darkbgcolors := hi=1:db=2:se=2:er=91:wa=93:me=95:in=94:mp=1;94:di=94:al=96:sy=95:de=4:cm=92
lightbgcolors := hi=1:db=2:se=2:er=31:wa=33:me=35:in=34:mp=1;34:di=34:al=36:sy=35:de=4:cm=32
termbg := dark

# automated modules handling
autohandling := n

# in depth avail search
availindepth := y

# ignore superseding value for locked configuration options
lockedconfigs := 

# unload lastly or firstly loaded module matching
unloadmatchorder := returnlast

# implicitly set a default version for modules with none defined
implicitdefault := y

# allow partial module version specification
extendeddefault := n

# advanced version specification
advversspec := n

# module name search matching style
searchmatch := starts_with

# workaround for Tcsh history issue (#277)
wa277 := n

# case sensitiveness match
icase := never

# command location
TCLSH := /usr/bin/tclsh
SPHINXBUILD := sphinx-build
PS := /bin/ps
BASENAME := /usr/bin/basename
RMDIR_IGN_NON_EMPTY := rmdir --ignore-fail-on-non-empty

