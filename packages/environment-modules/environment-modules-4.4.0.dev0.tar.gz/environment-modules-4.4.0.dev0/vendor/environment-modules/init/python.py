import os, re, subprocess

# define modules runtine quarantine configuration
#os.environ['MODULES_RUN_QUARANTINE'] = 'ENVVARNAME'

# setup quarantine if defined
_mlre = os.environ.copy()
if 'MODULES_RUN_QUARANTINE' in os.environ:
   for _mlv in os.environ['MODULES_RUN_QUARANTINE'].split():
      if re.match('^[A-Za-z_][A-Za-z0-9_]*$', _mlv):
         if _mlv in os.environ:
            _mlre[_mlv + '_modquar'] = os.environ[_mlv]
         _mlrv = 'MODULES_RUNENV_' + _mlv
         if _mlrv in os.environ:
            _mlre[_mlv] = os.environ[_mlrv]
         else:
            _mlre[_mlv] = ''

# define module command and surrounding initial environment (default value
# for MODULESHOME, MODULEPATH, LOADEDMODULES and parse of init config files)
exec(subprocess.Popen(['/usr/bin/tclsh', '/home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/libexec/modulecmd.tcl', 'python', 'autoinit'], stdout=subprocess.PIPE, env=_mlre).communicate()[0])

# clean temp variable used to setup quarantine
del _mlre

# redefine module command if compat version has been activated
if 'MODULES_USE_COMPAT_VERSION' in os.environ and os.environ['MODULES_USE_COMPAT_VERSION'] == '1':
   os.environ['MODULES_CMD'] = '/home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/libexec/modulecmd-compat'
   # set module command in accordance with active version
   def module(command, *arguments):
      exec(subprocess.Popen(['/home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/libexec/modulecmd-compat', 'python', command] + list(arguments), stdout=subprocess.PIPE).communicate()[0])
      # return value as done on new main version
      return True
