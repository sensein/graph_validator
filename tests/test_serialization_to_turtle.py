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
# @File    : test_serialization_to_turtle.py
# @Software: PyCharm

import unittest
from core.validate import serialize_graph_to_turtle
from rdflib import Graph
from rdflib.compare import to_isomorphic


class TestSerializationToTurtle(unittest.TestCase):
    """
    Test case for validating the serialization of a graph to Turtle format.
    """

    def test_serialize_graph_to_turtle_valid(self):
        """
        Test that a graph in N-Triples format is correctly serialized to Turtle format
        and matches the expected graph structure.
        """
        test_graph_ntriples = """
        <http://example.org/document1> <http://example.org/creationDate> "2024-06-23"^^<http://www.w3.org/2001/XMLSchema#date> .
        <http://example.org/document1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/prov#Entity> .
        <http://example.org/document1> <http://www.w3.org/ns/prov#wasGeneratedBy> <http://example.org/activity1> .
        <http://example.org/document1> <http://www.w3.org/ns/prov#wasAttributedTo> <http://example.org/person1> .
        """

        expected_graph = """
        @prefix ex: <http://example.org/> .
        @prefix prov: <http://www.w3.org/ns/prov#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        ex:document1 a prov:Entity ;
            prov:wasGeneratedBy ex:activity1 ;
            prov:wasAttributedTo ex:person1 ;
            ex:creationDate "2024-06-23"^^xsd:date .
        """

        response_turtle = serialize_graph_to_turtle(
            input_graph=test_graph_ntriples, input_format="ntriples"
        )

        try:
            expected_g = Graph()
            expected_g.parse(data=expected_graph, format="turtle")
            iso_expected_g = to_isomorphic(expected_g)

            response_g = Graph()
            response_g.parse(data=response_turtle, format="turtle")
            iso_response_g = to_isomorphic(response_g)

            self.assertEqual(
                iso_expected_g,
                iso_response_g,
                "The serialized graph does not match the expected graph.",
            )

            self.assertIsInstance(
                expected_g, Graph, "Expected graph is not of type Graph."
            )
            self.assertIsInstance(
                response_g, Graph, "Response graph is not of type Graph."
            )
        except Exception as e:
            self.fail(f"Test failed due to an unexpected error: {e}")


if __name__ == "__main__":
    unittest.main()
