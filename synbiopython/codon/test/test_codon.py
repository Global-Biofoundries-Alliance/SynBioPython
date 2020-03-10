"""
Synbiopython (c) Global BioFoundry Alliance 2020

Synbiopython is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author: neilswainston
"""
import unittest

from synbiopython import codon


class TestCodon(unittest.TestCase):
    """Class to test the codon module."""

    def test_get_tax_id(self):
        """Test get_tax_id method."""

        # Negative tests:
        for table_id in [-1, "hello"]:
            self.assertIsNone(codon.get_tax_id(table_id))

        # Positive tests:
        for table_id in [45372, "45372", "Abies alba"]:
            self.assertEqual(codon.get_tax_id(table_id), "45372")

    def test_get_name(self):
        """Test get_name method."""

        # Negative tests:
        self.assertIsNone(codon.get_name(-1))
        self.assertIsNone(codon.get_name("hello"))

        # Positive tests:
        self.assertEqual(codon.get_name(255), "'Flavobacterium' lutescens")
        self.assertEqual(codon.get_name("255"), "'Flavobacterium' lutescens")
        self.assertEqual(codon.get_name("Abies alba"), "Abies alba")


if __name__ == "__main__":
    unittest.main()
