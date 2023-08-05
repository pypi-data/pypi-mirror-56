# define modules runtine quarantine configuration
#Sys.setenv('MODULES_RUN_QUARANTINE'='ENVVARNAME')

# setup quarantine if defined
mlre <- ''
if (!is.na(Sys.getenv('MODULES_RUN_QUARANTINE', unset=NA))) {
   for (mlv in strsplit(Sys.getenv('MODULES_RUN_QUARANTINE'), ' ')[[1]]) {
      if (grepl('^[A-Za-z_][A-Za-z0-9_]*$', mlv)) {
         if (!is.na(Sys.getenv(mlv, unset=NA))) {
            mlre <- paste0(mlre, mlv, "_modquar='", Sys.getenv(mlv), "' ")
         }
         mlrv <- paste0('MODULES_RUNENV_', mlv)
         mlre <- paste0(mlre, mlv, "='", Sys.getenv(mlrv), "' ")
      }
   }
   if (mlre != '') {
      mlre <- paste0('env ', mlre)
   }
}

# define module command and surrounding initial environment (default value
# for MODULESHOME, MODULEPATH, LOADEDMODULES and parse of init config files)
cmdpipe <- pipe(paste0(mlre, '/usr/bin/tclsh /home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/libexec/modulecmd.tcl r autoinit'))
eval(parse(cmdpipe))
close(cmdpipe)
