"""
Synbiopython (c) Global BioFoundry Alliance 2020

Synbiopython is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author: neilswainston
"""
# pylint: disable=C0330
import itertools
import unittest

from synbiopython.codon import table


class TestTable(unittest.TestCase):
    """Class to test the table module."""

    def test_get_table(self):
        """Test get_table method."""

        # Negative tests:
        for table_id in [-1, "hello"]:
            self.assertIsNone(table.get_table(table_id))

        # Positive tests:
        for table_id, dna in itertools.product(
            [45372, "45372", "Abies alba"], [True, False]
        ):
            self.__test_table(table.get_table(table_id, dna=dna), dna=dna)

    def __test_table(self, codon_table, dna):
        """Test table."""
        self.assertEqual(len(codon_table), 21)
        self.assertEqual(len(codon_table["*"]), 3)

        cdn = "TAA" if dna else "UAA"
        self.assertEqual(codon_table["*"][cdn], 1.0)


if __name__ == "__main__":
    unittest.main()
