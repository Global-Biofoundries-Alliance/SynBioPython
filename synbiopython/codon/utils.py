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
    codon usage frequency.

    :param table: a codon usage table.
    :type table: dict
    :param amino_acid: a single-character string representing an amino acid.
    :type amino_acid: str
    :return: a codon encoding the supplied amino acid, sampled
        probabilistically.
    :rtype: str
    """
    cum_freq = 0
    rand_val = random.random()

    for codon, freq in table[amino_acid].items():
        cum_freq += freq

        if cum_freq > rand_val:
            return codon

    return None


def optimise(table, aa_seq):
    """Codon optimise an amino acid sequence.

    :param table: a codon usage table.
    :type table: dict
    :param aa_seq: an amino acid sequence.
    :type table: str
    :return: a codon-optimised nucleic acid sequence, encoding the supplied
        amino acid sequence
    :rtype: str
    """
    return ''.join([sample(table, amino_acid) for amino_acid in aa_seq])
