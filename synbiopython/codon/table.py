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

from synbiopython.codon import get_tax_id, DATA_DIR


_CODON_REGEX = r"([ATGCU]{3}) ([A-Z]|\*) (\d.\d+)"


def get_table(table_id, dna=True):
    """Get table."""
    tax_id = get_tax_id(table_id)

    if tax_id:
        results = defaultdict(dict)
        content = _get_content(tax_id)

        for vals in sorted(
            re.findall(_CODON_REGEX, content), key=lambda x: (x[1], x[2])
        ):
            results[vals[1]][_get_codon(vals[0], dna)] = float(vals[2])

        return dict(results)

    return None


def _get_content(tax_id):
    """Get Kazusa content, either from cached file or remotely."""
    target_file = os.path.join(DATA_DIR, "%s.txt" % tax_id)

    if not os.path.exists(target_file):
        url = (
            "http://www.kazusa.or.jp/codon/cgi-bin/showcodon.cgi?"
            + "aa=1&style=N&species=%s" % tax_id
        )

        urlretrieve(url, target_file)

    with open(target_file) as fle:
        return fle.read()


def _get_codon(codon, dna):
    """Get codon."""
    return codon.replace("U", "T") if dna else codon
