'''
Synbiopython (c) Global BioFoundry Alliance 2020

Synbiopython is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author: neilswainston
'''
import os.path

import pandas


DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'data')


def _get_spec_df():
    '''Get tax id, name from species.table as Pandas DataFrame.'''
    spec_tab_df = pandas.read_csv(os.path.join(DATA_DIR, 'species.table'),
                                  names=['name', 'tax_id'],
                                  sep='\t', comment='#')

    return spec_tab_df.set_index('tax_id')


_SPEC_DF = _get_spec_df()


def get_tax_id(table_id):
    '''Get tax id.'''
    table_id = str(table_id)

    if table_id in _SPEC_DF.index:
        return table_id

    tax_ids = _SPEC_DF.index[_SPEC_DF['name'] == table_id]

    return None if tax_ids.empty else tax_ids[0]


def get_name(table_id):
    '''Get name.'''
    tax_id = get_tax_id(table_id)
    return _SPEC_DF.loc[tax_id, 'name'] if tax_id else None
