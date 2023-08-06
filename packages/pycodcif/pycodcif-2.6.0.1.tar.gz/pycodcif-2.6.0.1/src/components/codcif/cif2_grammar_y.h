/*---------------------------------------------------------------------------*\
**$Author: antanas $
**$Date: 2019-11-15 20:06:25 +0200 (Fri, 15 Nov 2019) $ 
**$Revision: 7424 $
**$URL: svn://www.crystallography.net/cod-tools/tags/v2.6/src/components/codcif/cif2_grammar_y.h $
\*---------------------------------------------------------------------------*/

#ifndef __CIF2_GRAMMAR_Y_H
#define __CIF2_GRAMMAR_Y_H

#include <cif.h>
#include <cif_options.h>
#include <cexceptions.h>

CIF *new_cif_from_cif2_file( FILE *in, char *filename, cif_option_t co,
                             cexception_t *ex );

void cif2_yy_debug_on( void );
void cif2_yy_debug_off( void );

#endif
