.PHONY: clean distclean

CFLAGS_DEFAULT=-O2 -fomit-frame-pointer -DNDEBUG -fPIC
CFLAGS_WARNING=-Wall

CC=gcc
CFLAGS= -pipe ${CFLAGS_DEFAULT} ${CFLAGS_WARNING}  -I/usr/include/tcl8.6
LDFLAGS= -Wl,--export-dynamic 
LD=${CC} -shared ${CFLAGS} ${LDFLAGS} ${CFLAGS}

# apply specific flags to libtclenvmodules build if code coverage asked
ifeq ($(COVERAGE),y)
CFLAGS_COVERAGE=-coverage -O0
endif

libtclenvmodules.so: envmodules.c
	$(LD) ${CFLAGS_COVERAGE} $< -o $@ -L/usr/lib/x86_64-linux-gnu -ltclstub8.6

libtestutil-closedir.so: testutil-closedir.c
	$(LD) $< -o $@

clean:
	rm -f libtclenvmodules.so
	rm -f libtestutil-closedir.so
	rm -f envmodules.c.gcov envmodules.gcda envmodules.gcno

distclean: clean
	rm -f config.log config.status
	rm -f config.h config.h.in~
	rm -f Makefile
ifeq ($(wildcard ../.git),../.git)
	rm configure
	rm config.h.in
ifeq ($(wildcard autom4te.cache),autom4te.cache)
	rm -f autom4te.cache/*
	rmdir autom4te.cache
endif
endif
