"""
Synbiopython (c) Global BioFoundry Alliance 2020

Synbiopython is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author: neilswainston
"""
import unittest

from synbiopython.codon import taxonomy_utils


class TestTaxonomyUtils(unittest.TestCase):
    """Class to test the taxonomy_utils module."""

    def test_get_tax_id(self):
        """Test get_tax_id method."""

        # Negative tests:
        for table_id in [-1, "hello"]:
            self.assertIsNone(taxonomy_utils.get_tax_id(table_id))

        # Positive tests:
        for table_id in [45372, "45372", "Abies alba"]:
            self.assertEqual(taxonomy_utils.get_tax_id(table_id), "45372")

    def test_get_organism_name(self):
        """Test get_organism_name method."""

        # Negative tests:
        self.assertIsNone(taxonomy_utils.get_organism_name(-1))
        self.assertIsNone(taxonomy_utils.get_organism_name("hello"))

        # Positive tests:
        self.assertEqual(taxonomy_utils.get_organism_name(255),
                         "'Flavobacterium' lutescens")
        self.assertEqual(taxonomy_utils.get_organism_name("255"),
                         "'Flavobacterium' lutescens")
        self.assertEqual(taxonomy_utils.get_organism_name("Abies alba"),
                         "Abies alba")


if __name__ == "__main__":
    unittest.main()
