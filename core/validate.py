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


from rdflib import Graph
from owlready2 import get_ontology, default_world
from core.helper import load_yaml_config, apply_logging_configuration
import logging

config = load_yaml_config("logging_config.yaml")
apply_logging_configuration(config)


def load_ontology(file_path):
    """Load ontology
    :param file_path: str
    :return owlready2.namespace.Ontology
    """
    return get_ontology(file_path).load()


def perform_reasoning(ontology):
    """
    Perform reasoning on the given ontology to check its consistency using the default world.

    This function uses the default world in `owlready2` to perform reasoning on the specified ontology.
    For more information, see: https://owlready2.readthedocs.io/en/latest/world.html

    :param ontology: owlready2.namespace.Ontology
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


def load_graph(file_path, format="json-ld"):
    """
    Load an RDF graph from a file in various formats such as JSON-LD or Turtle.

    :param file_path: str
        The path to the file containing the RDF graph.
    :param format: str, optional
        The format of the RDF graph, "json-ld", "turtle", "n3", "nt", "rdfxml", "trig"
        json-ld: https://json-ld.org/
        turtle: https://www.w3.org/TR/turtle/
        n3: https://www.w3.org/TeamSubmission/n3/
        nt: https://www.w3.org/TR/n-triples/
        rdfxml:https://www.w3.org/TR/rdf-syntax-grammar/
        trig: https://www.w3.org/TR/trig/
        Default is 'json-ld'.
    :return: rdflib.graph.Graph
        The RDF graph loaded from the file.
    :raises ValueError: If the specified format is not supported.
    :raises IOError: If there is an issue reading the file.
    :raises Exception: For other parsing errors.
    """
    logger = logging.getLogger("load_graph")
    supported_formats = ["json-ld", "turtle", "n3", "nt", "rdfxml", "trig"]

    if format not in supported_formats:
        logger.error(
            f"Unsupported format: {format}. Supported formats are: {', '.join(supported_formats)}"
        )
        raise ValueError(
            f"Unsupported format: {format}. Supported formats are: {', '.join(supported_formats)}"
        )

    graph = Graph()

    try:
        graph.parse(file_path, format=format)
        return graph
    except IOError as e:
        logger.error(f"Error reading file {file_path}: {e}")
        raise IOError(f"Error reading file {file_path}: {e}")
    except Exception as e:
        logger.error(
            f"Error parsing graph from file {file_path} in format {format}: {e}"
        )
        raise Exception(
            f"Error parsing graph from file {file_path} in format {format}: {e}"
        )
