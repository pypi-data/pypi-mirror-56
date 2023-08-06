/*---------------------------------------------------------------------------*\
**$Author: antanas $
**$Date: 2019-11-15 20:06:25 +0200 (Fri, 15 Nov 2019) $ 
**$Revision: 7424 $
**$URL: svn://www.crystallography.net/cod-tools/tags/v2.6/src/components/codcif/cif_grammar_y.h $
\*---------------------------------------------------------------------------*/

#ifndef __CIF_GRAMMAR_Y_H
#define __CIF_GRAMMAR_Y_H

#include <cif.h>
#include <cif_options.h>
#include <cexceptions.h>

CIF *new_cif_from_cif1_file( FILE *in, char *filename, cif_option_t co,
                             cexception_t *ex );

void cif_yy_debug_on( void );
void cif_yy_debug_off( void );

#endif
