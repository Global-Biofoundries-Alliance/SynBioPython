"""
Synbiopython (c) Global BioFoundry Alliance 2020

Synbiopython is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author: neilswainston
"""
import os.path

import pandas as pd
from synbiopython.codon import DATA_DIR


def _get_spec_df():
    """Get NCBI Taxonomy ids and organism from species.table as a Pandas
    DataFrame.

    :return: a Pandas DataFrame, containing NCBI Taxonomy ids and organism
        names.
    :rtype: pd.DataFrame
    """
    spec_tab_df = pd.read_csv(
        os.path.join(DATA_DIR, "species.table"),
        names=["name", "tax_id"],
        sep="\t",
        comment="#",
    )

    return spec_tab_df.set_index("tax_id")


_SPEC_DF = _get_spec_df()


def get_tax_id(table_id):
    """Gets a NCBI Taxonomy id from supplied parameter, which may be either an
    organism name or a NCBI Taxonomy id.

    :param table_id: an organism name or a NCBI Taxonomy id (as either a str or
        int).
    :type table_id: str
    :return: a NCBI Taxonomy id
    :rtype: str
    """
    table_id = str(table_id)

    if table_id in _SPEC_DF.index:
        return table_id

    tax_ids = _SPEC_DF.index[_SPEC_DF["name"] == table_id]

    if tax_ids.any():
        return tax_ids[0]

    raise ValueError("Unrecognised table id: %s" % table_id)


def get_organism_name(table_id):
    """Gets an organism name from supplied parameter, which may be either an
    organism name or a NCBI Taxonomy id.

    :param table_id: an organism name or a NCBI Taxonomy id (as either a str or
        int).
    :type table_id: str
    :return: an organism name
    :rtype: str
    """
    tax_id = get_tax_id(table_id)
    return _SPEC_DF.loc[tax_id, "name"] if tax_id else None
