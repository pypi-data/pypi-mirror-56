/*---------------------------------------------------------------------------*\
**$Author: antanas $
**$Date: 2019-11-15 20:06:25 +0200 (Fri, 15 Nov 2019) $ 
**$Revision: 7424 $
**$URL: svn://www.crystallography.net/cod-tools/tags/v2.6/src/components/codcif/common.h $
\*---------------------------------------------------------------------------*/

#ifndef __COMMON_H
#define __COMMON_H

#include <unistd.h>
#include <math.h>

char *strclone( const char *s );
char *strnclone( const char *s, size_t length );
char *strappend( char *s, const char *suffix );
char *process_escapes( char *str );
char translate_escape( char **s );
ssize_t countchars( char c, char *s );

int starts_with_keyword( char *keyword, char *string );
int is_integer( char *s );
int is_real( char *s );

char *cif_unprefix_textfield( char *tf );
char *cif_unfold_textfield( char *tf );
int is_tag_value_unknown( char *tv );

void fprintf_escaped( const char *message,
                      int escape_parenthesis, int escape_space );

double unpack_precision( char * value, double precision );

#endif
