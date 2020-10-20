"""
Synbiopython (c) Global BioFoundry Alliance 2020

Synbiopython is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author: neilswainston
"""
import random

_CODON_REGEX = r"([ATGCU]{3}) ([A-Z]|\*) (\d.\d+)"


def sample(table, amino_acid):
    """Sample a codon for a given amino acid probabilistically, based on its
    codon usage frequency."""
    cum_freq = 0
    rand_val = random.random()

    for codon, freq in table[amino_acid].items():
        cum_freq += freq

        if cum_freq > rand_val:
            return codon

    return None


def optimise(table, aa_seq):
    """Codon optimise an amino acid sequence."""
    return ''.join([sample(table, amino_acid) for amino_acid in aa_seq])
