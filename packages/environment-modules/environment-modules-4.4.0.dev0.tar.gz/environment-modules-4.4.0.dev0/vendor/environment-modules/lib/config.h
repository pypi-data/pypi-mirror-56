/* config.h.  Generated from config.h.in by configure.  */
/* config.h.in.  Generated from configure.ac by autoheader.  */

/* Define if building universal (internal helper macro) */
/* #undef AC_APPLE_UNIVERSAL_BUILD */

/* Defined when cygwin/mingw does not support EXCEPTION DISPOSITION */
/* #undef EXCEPTION_DISPOSITION */

/* Defined when compiler supports casting to union type. */
#define HAVE_CAST_TO_UNION 1

/* Define to 1 if you have the <dirent.h> header file. */
#define HAVE_DIRENT_H 1

/* Define to 1 if you have the <errno.h> header file. */
#define HAVE_ERRNO_H 1

/* Define to 1 if you have the <fcntl.h> header file. */
#define HAVE_FCNTL_H 1

/* Compiler support for module scope symbols */
#define HAVE_HIDDEN 1

/* Define to 1 if you have the <inttypes.h> header file. */
#define HAVE_INTTYPES_H 1

/* Define to 1 if you have the <limits.h> header file. */
#define HAVE_LIMITS_H 1

/* Define to 1 if you have the `lseek64' function. */
/* #undef HAVE_LSEEK64 */

/* Define to 1 if you have the <memory.h> header file. */
#define HAVE_MEMORY_H 1

/* Defined when mingw does not support SEH */
/* #undef HAVE_NO_SEH */

/* Define to 1 if you have the `open64' function. */
/* #undef HAVE_OPEN64 */

/* Define to 1 if you have the <stdint.h> header file. */
#define HAVE_STDINT_H 1

/* Define to 1 if you have the <stdlib.h> header file. */
#define HAVE_STDLIB_H 1

/* Define to 1 if you have the <strings.h> header file. */
#define HAVE_STRINGS_H 1

/* Define to 1 if you have the <string.h> header file. */
#define HAVE_STRING_H 1

/* Is 'struct dirent64' in <sys/types.h>? */
/* #undef HAVE_STRUCT_DIRENT64 */

/* Is 'struct stat64' in <sys/stat.h>? */
/* #undef HAVE_STRUCT_STAT64 */

/* Define to 1 if you have the <sys/stat.h> header file. */
#define HAVE_SYS_STAT_H 1

/* Define to 1 if you have the <sys/types.h> header file. */
#define HAVE_SYS_TYPES_H 1

/* Is off64_t in <sys/types.h>? */
/* #undef HAVE_TYPE_OFF64_T */

/* Define to 1 if you have the <unistd.h> header file. */
#define HAVE_UNISTD_H 1

/* Defined when cygwin/mingw ignores VOID define in winnt.h */
/* #undef HAVE_WINNT_IGNORE_VOID */

/* No Compiler support for module scope symbols */
#define MODULE_SCOPE extern __attribute__((__visibility__("hidden")))

/* Define to the address where bug reports for this package should be sent. */
#define PACKAGE_BUGREPORT "modules-interest@lists.sourceforge.net"

/* Define to the full name of this package. */
#define PACKAGE_NAME "Envmodules"

/* Define to the full name and version of this package. */
#define PACKAGE_STRING "Envmodules 1.0.1"

/* Define to the one symbol short name of this package. */
#define PACKAGE_TARNAME "envmodules"

/* Define to the home page for this package. */
#define PACKAGE_URL "http://modules.sf.net"

/* Define to the version of this package. */
#define PACKAGE_VERSION "1.0.1"

/* This a static build */
/* #undef STATIC_BUILD */

/* Define to 1 if you have the ANSI C header files. */
#define STDC_HEADERS 1

/* Is memory debugging enabled? */
/* #undef TCL_MEM_DEBUG */

/* Are wide integers to be implemented with C 'long's? */
#define TCL_WIDE_INT_IS_LONG 1

/* What type should be used to define wide integers? */
/* #undef TCL_WIDE_INT_TYPE */

/* UNDER_CE version */
/* #undef UNDER_CE */

/* Use TclOO stubs */
#define USE_TCLOO_STUBS 1

/* Use Tcl stubs */
#define USE_TCL_STUBS 1

/* Use Tk stubs */
/* #undef USE_TK_STUBS */

/* Define WORDS_BIGENDIAN to 1 if your processor stores words with the most
   significant byte first (like Motorola and SPARC, unlike Intel). */
#if defined AC_APPLE_UNIVERSAL_BUILD
# if defined __BIG_ENDIAN__
#  define WORDS_BIGENDIAN 1
# endif
#else
# ifndef WORDS_BIGENDIAN
/* #  undef WORDS_BIGENDIAN */
# endif
#endif

/* Add the _ISOC99_SOURCE flag when building */
/* #undef _ISOC99_SOURCE */

/* Add the _LARGEFILE64_SOURCE flag when building */
#define _LARGEFILE64_SOURCE 1

/* Add the _LARGEFILE_SOURCE64 flag when building */
/* #undef _LARGEFILE_SOURCE64 */

/* # needed in sys/socket.h Should OS/390 do the right thing with sockets? */
/* #undef _OE_SOCKETS */

/* Do we really want to follow the standard? Yes we do! */
/* #undef _POSIX_PTHREAD_SEMANTICS */

/* Do we want the reentrant OS API? */
/* #undef _REENTRANT */

/* _WIN32_WCE version */
/* #undef _WIN32_WCE */

/* Do we want to use the XOPEN network library? */
/* #undef _XOPEN_SOURCE_EXTENDED */

/* Define to `int' if <sys/types.h> does not define. */
/* #undef ssize_t */
