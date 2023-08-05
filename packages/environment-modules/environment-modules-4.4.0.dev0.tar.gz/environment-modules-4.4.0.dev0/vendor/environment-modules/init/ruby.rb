# define modules runtine quarantine configuration
#ENV['MODULES_RUN_QUARANTINE'] = 'ENVVARNAME'

# setup quarantine if defined
_mlre = ''
if ENV.has_key?('MODULES_RUN_QUARANTINE') then
   ENV['MODULES_RUN_QUARANTINE'].split(' ').each do |_mlv|
      if _mlv =~ /^[A-Za-z_][A-Za-z0-9_]*$/ then
         if ENV.has_key?(_mlv) then
            _mlre << _mlv + "_modquar='" + ENV[_mlv].to_s + "' "
         end
         _mlrv = 'MODULES_RUNENV_' + _mlv
         _mlre << _mlv + "='" + ENV[_mlrv].to_s + "' "
      end
   end
   unless _mlre.empty?
      _mlre = 'env ' + _mlre
   end
end

# define module command and surrounding initial environment (default value
# for MODULESHOME, MODULEPATH, LOADEDMODULES and parse of init config files)
eval `#{_mlre}/usr/bin/tclsh /home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/libexec/modulecmd.tcl ruby autoinit`

# redefine module command if compat version has been activated
if ENV['MODULES_USE_COMPAT_VERSION'] == '1' then
   ENV['MODULES_CMD'] = '/home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/libexec/modulecmd-compat'
   class ENVModule
      def ENVModule.module(*args)
         if args[0].kind_of?(Array) then
            args = args[0].join(' ')
         else
            args = args.join(' ')
         end
         eval `/home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/libexec/modulecmd-compat ruby #{args}`
         # return value as done on new main version
         return true
      end
   end
end
