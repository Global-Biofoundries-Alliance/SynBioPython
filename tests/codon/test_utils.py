"""
Synbiopython (c) Global BioFoundry Alliance 2020

Synbiopython is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author: neilswainston
"""
# pylint: disable=fixme,C0330
from collections import Counter
import unittest

from synbiopython.codon import table, utils


class TestUtils(unittest.TestCase):
    """Class to test the utils module."""

    def test_sample(self):
        """Test sample method."""
        codon_table = table.get_table("Escherichia coli")
        amino_acid = "L"

        # Get codon usage for amino acid:
        aa_codons = codon_table[amino_acid]

        # Apply sample a number of times:
        sampled = [utils.sample(codon_table, amino_acid) for _ in range(10000)]

        # Test:
        self._test(sampled, aa_codons)

    def test_codon_optimise(self):
        """Test codon optimise method."""
        # TODO: update in future to codon optimise random amino acid sequence,
        # then translate back to original amino acid sequence.
        # (Will need Biopython, but don't want to add extra dependency.
        codon_table = table.get_table(9606)
        amino_acid = "S"

        # Get codon usage for amino acid:
        aa_codons = codon_table[amino_acid]

        # Generate amino acid sequence and codon optimise:
        aa_seq = "".join([amino_acid] * 100000)
        dna_seq = utils.optimise(codon_table, aa_seq)

        # Extract codons from DNA sequence:
        codons = [dna_seq[i : i + 3] for i in range(0, len(dna_seq), 3)]

        # Test:
        self._test(codons, aa_codons)

    def _test(self, target, aa_codons):
        """Test method."""
        codons = Counter(target)

        # Ensure codon usage and sample frequencies are similar:
        for codon, count in codons.items():
            self.assertAlmostEqual(count / len(target), aa_codons[codon], delta=1e-2)


if __name__ == "__main__":
    unittest.main()
