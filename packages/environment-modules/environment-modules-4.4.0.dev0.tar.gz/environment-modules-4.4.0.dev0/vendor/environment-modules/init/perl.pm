# define modules runtine quarantine configuration
#$ENV{'MODULES_RUN_QUARANTINE'} = 'ENVVARNAME';

# setup quarantine if defined
my $_mlre = '';
if (defined $ENV{'MODULES_RUN_QUARANTINE'}) {
  foreach my $_mlv (split(' ', $ENV{'MODULES_RUN_QUARANTINE'})) {
     if ($_mlv =~ /^[A-Za-z_][A-Za-z0-9_]*$/) {
        if (defined $ENV{$_mlv}) {
           $_mlre .= "${_mlv}_modquar='$ENV{$_mlv}' ";
        }
        my $_mlrv = "MODULES_RUNENV_$_mlv";
        $_mlre .= "$_mlv='$ENV{$_mlrv}' ";
    }
  }
  if ($_mlre ne "") {
     $_mlre = "env $_mlre";
  }
}

eval `${_mlre}/usr/bin/tclsh /home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/libexec/modulecmd.tcl perl autoinit`;

# clean temp variable used to setup quarantine
undef $_mlre;

# redefine module command if compat version has been activated
if ($ENV{'MODULES_USE_COMPAT_VERSION'} eq '1') {
   $ENV{'MODULES_CMD'} = '/home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/libexec/modulecmd-compat';
   { no warnings 'redefine';
      *module = sub {
         eval `/home/bukzor/repo/environment-modules-setuptools/build/temp.linux-x86_64-3.5/libexec/modulecmd-compat perl @_`;
         # return value as done on new main version
         return 1;
      };
   }
}

1;
