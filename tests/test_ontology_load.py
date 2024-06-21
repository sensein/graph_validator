# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# DISCLAIMER: This software is provided "as is" without any warranty,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose, and non-infringement.
#
# In no event shall the authors or copyright holders be liable for any
# claim, damages, or other liability, whether in an action of contract,
# tort, or otherwise, arising from, out of, or in connection with the
# software or the use or other dealings in the software.
# -----------------------------------------------------------------------------

# @Author  : Tek Raj Chhetri
# @Email   : tekraj@mit.edu
# @Web     : https://tekrajchhetri.com/
# @File    : test_ontology_load.py
# @Software: PyCharm

import unittest
from core.validate import load_ontology
import owlready2
from owlready2 import Ontology


class TestOntologyLoad(unittest.TestCase):
    def test_load_ontology_valid(self):
        ontology = "tests/sample_ontology.owl"
        ontology_loaded = load_ontology(ontology)
        self.assertIsInstance(
            ontology_loaded, Ontology, "Object should be an instance of Ontology"
        )
        self.assertEqual(
            type(ontology_loaded),
            owlready2.namespace.Ontology,
            "Object should be of type owlready2.namespace",
        )

    def test_load_ontology_invalid_file(self):
        # Arrange
        invalid_file_path = "sample_ontology_fail.owl"

        with self.assertRaises(
            Exception, msg="An invalid file path should raise an exception."
        ):
            load_ontology(invalid_file_path)
