"""
Synbiopython (c) Global BioFoundry Alliance 2020

Synbiopython is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author: neilswainston
"""
from collections import defaultdict
import os.path
import re
from urllib.request import urlretrieve

from synbiopython.codon.taxonomy_utils import get_tax_id

_CODON_REGEX = r"([ATGCU]{3}) ([A-Z]|\*) (\d.\d+)"


def get_table(table_id, dna=True):
    """Gets a codon table from from supplied parameter, which may be either an
    organism name or a NCBI Taxonomy id.

    :param table_id: an organism name or a NCBI Taxonomy id (as either a str or
        int).
    :type table_id: str
    :param dna: boolean parameter specifying whether the codon table returned
        should contain DNA or RNA codons (default is DNA).
    :type dna: bool
    :return: a codon usage table.
    :rtype: dict
    """
    tax_id = get_tax_id(table_id)
    results = defaultdict(dict)
    content = _get_content(tax_id)

    for vals in sorted(re.findall(_CODON_REGEX, content),
                       key=lambda x: (x[1], x[2])):
        results[vals[1]][vals[0].replace("U", "T") if dna else vals[0]] = \
            float(vals[2])

    return dict(results)


def _get_content(tax_id):
    """Gets Codon Usage Database content, either from cached file or remotely.

    :param tax_id: a NCBI Taxonomy id.
    :type tax_id: str
    :return: the Codon Usage Database content
    :rtype: str
    """
    target_dir = os.path.join(os.path.expanduser('~'), '.synbiopython/codon')

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    target_file = os.path.join(target_dir, "%s.txt" % tax_id)

    if not os.path.exists(target_file):
        url = "http://www.kazusa.or.jp/codon/cgi-bin/showcodon.cgi?" + \
            "aa=1&style=N&species=%s" % tax_id

        urlretrieve(url, target_file)

    with open(target_file) as fle:
        return fle.read()
