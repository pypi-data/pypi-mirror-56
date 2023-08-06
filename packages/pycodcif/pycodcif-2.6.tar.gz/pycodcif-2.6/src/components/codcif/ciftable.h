/*-------------------------------------------------------------------------*\
* $Author: antanas $
* $Date: 2019-11-15 20:06:25 +0200 (Fri, 15 Nov 2019) $ 
* $Revision: 7424 $
* $URL: svn://www.crystallography.net/cod-tools/tags/v2.6/src/components/codcif/ciftable.h $
\*-------------------------------------------------------------------------*/

#ifndef __CIFTABLE_H
#define __CIFTABLE_H

#include <stdio.h>
#include <cexceptions.h>

typedef struct CIFTABLE CIFTABLE;

#include <cifvalue.h>

CIFTABLE *new_table( cexception_t *ex );
void delete_table( CIFTABLE *table );
void table_dump( CIFTABLE *table );

size_t table_length( CIFTABLE *table );
char **table_keys( CIFTABLE *table );

void table_add( CIFTABLE *table, char *key, CIFVALUE *value,
                cexception_t *ex );
CIFVALUE *table_get( CIFTABLE *table, char *key );

#endif
