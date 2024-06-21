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
# @File    : validate.py
# @Software: PyCharm


import json
from rdflib import Graph, URIRef
from rdflib.plugins.parsers.notation3 import BadSyntax
from rdflib.plugin import register, Parser
from rdflib.namespace import RDF, OWL, RDFS
import owlrl
from rdflib import Graph, Namespace, URIRef
from owlready2 import get_ontology, default_world
from rdflib.namespace import RDF, RDFS, XSD
from rdflib.compare import graph_diff, to_isomorphic
from core.helper import load_yaml_config, apply_logging_configuration
import logging

config = load_yaml_config("local_config.yml")
apply_logging_configuration(config)


def load_ontology(file_path):
    """Load ontology
    :param file_path: str
    :return owlready2.Ontology
    """
    return get_ontology(file_path).load()


def perform_reasoning(ontology):
    """
    Perform reasoning on the given ontology to check its consistency using the default world.

    This function uses the default world in `owlready2` to perform reasoning on the specified ontology.
    For more information, see: https://owlready2.readthedocs.io/en/latest/world.html

    :param ontology: owlready2.Ontology
        The ontology to perform reasoning on.
    :return: None
    """
    logger = logging.getLogger("perform_reasoning")
    try:
        with ontology:
            logger.info("Starting reasoning on the ontology...")
            default_world.reason()
            logger.info("End reasoning on the ontology...")
    except Exception as e:
        logger.error(f"An error occurred during reasoning: {e}")

def load_graph(file_path, format='json-ld'):
    """
    Load an RDF graph from a file in various formats such as JSON-LD or Turtle.

    :param file_path: str
        The path to the file containing the RDF graph.
    :param format: str, optional
        The format of the RDF graph, such as 'json-ld', 'turtle', 'xml', etc.
        Default is 'json-ld'.
    :return: rdflib.graph.Graph
        The RDF graph loaded from the file.
    :raises ValueError: If the specified format is not supported.
    :raises IOError: If there is an issue reading the file.
    :raises Exception: For other parsing errors.
    """
    logger = logging.getLogger("load_graph")
    supported_formats = ['json-ld', 'turtle', 'xml', 'n3', 'nt', 'rdfxml', 'trig']

    if format not in supported_formats:
        logger.error(f"Unsupported format: {format}. Supported formats are: {', '.join(supported_formats)}")
        raise ValueError(f"Unsupported format: {format}. Supported formats are: {', '.join(supported_formats)}")

    graph = Graph()

    try:
        graph.parse(file_path, format=format)
        return graph
    except IOError as e:
        logger.error(f"Error reading file {file_path}: {e}")
        raise IOError(f"Error reading file {file_path}: {e}")
    except Exception as e:
        logger.error(f"Error parsing graph from file {file_path} in format {format}: {e}")
        raise Exception(f"Error parsing graph from file {file_path} in format {format}: {e}")
