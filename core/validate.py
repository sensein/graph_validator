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


from rdflib import Graph, Namespace
from owlready2 import get_ontology, sync_reasoner_pellet
from core.helper import load_yaml_config, apply_logging_configuration
import logging
from rdflib.plugin import PluginException

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
    Perform reasoning on the given ontology to check its consistency using the default world and pallet reasoner.

    https://owlready2.readthedocs.io/en/latest/reasoning.html

    Sirin, E., Parsia, B., Grau, B.C., Kalyanpur, A. and Katz, Y., 2007. Pellet: A practical owl-dl reasoner. Journal of Web Semantics, 5(2), pp.51-53.

    This function uses the default world in `owlready2` to perform reasoning on the specified ontology.
    For more information, see: https://owlready2.readthedocs.io/en/latest/world.html

    :param ontology: owlready2.namespace.Ontology
        The ontology to perform reasoning on.
    :return: dict
        The status of the reasoning along with the reasoning message
    """
    logger = logging.getLogger("perform_reasoning")
    reasoning_message = {}
    try:
        with ontology:
            logger.info("Starting reasoning on the ontology...")
            sync_reasoner_pellet(
                infer_property_values=True, infer_data_property_values=True
            )
            logger.info("End reasoning on the ontology...")
            reasoning_message["message"] = "Success"
            reasoning_message["status"] = True
    except Exception as e:
        logger.error(f"An error occurred during reasoning: {e}")
        reasoning_message["status"] = True
        reasoning_message["message"] = f"{e}"
    return reasoning_message


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
        graph.parse(data=file_path, format=format)
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


def serialize_graph_to_turtle(input_graph: str, input_format: str) -> str:
    """
    Serialize the input graph from various formats like RDF/XML, N3, JSON-LD to Turtle format.

    :param input_graph: Input graph as a string in various formats (RDF/XML, N3, JSON-LD).
    :param input_format: The format of the input graph (e.g., 'xml', 'n3', 'json-ld').
    :return: The serialized graph in Turtle format as a string.
    :raises ValueError: If there is an error in parsing or serialization.
    """
    logger = logging.getLogger("perform_reasoning")
    graph = Graph()
    try:
        graph.parse(data=input_graph, format=input_format)
        turtle_data = graph.serialize(format="turtle")
        logger.info("Successfully serialized to Turtle format.")
        return turtle_data
    except PluginException as e:
        logger.error(f"Failed to parse or serialize graph: {e}")
        raise ValueError(f"Failed to parse or serialize graph: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise ValueError(f"An unexpected error occurred: {e}")


def check_provenance_basics(turtle_file_path: str) -> bool:
    """
    Checks if there exists any provenance information in the supplied Turtle file using the PROV ontology.

    :param turtle_file_path: Path to the input file in Turtle format.
    :return: Boolean indicating whether provenance information exists. True means provenance information is found.
    """
    logger = logging.getLogger("check_provenance_basics")
    try:
        graph = Graph()
        graph.parse(turtle_file_path, format="turtle")
    except Exception as e:
        logger.error(f"Error parsing Turtle file: {e}")
        return False

    PROV_NAMESPACE = Namespace("http://www.w3.org/ns/prov#")

    prov_ontology_elements = [
        PROV_NAMESPACE.Agent,
        PROV_NAMESPACE.Entity,
        PROV_NAMESPACE.Activity,
        PROV_NAMESPACE.Used,
        PROV_NAMESPACE.WasGeneratedBy,
        PROV_NAMESPACE.WasDerivedFrom,
        PROV_NAMESPACE.WasAttributedTo,
        PROV_NAMESPACE.WasAssociatedWith,
    ]

    for element in prov_ontology_elements:
        if (
            (element, None, None) in graph
            or (None, element, None) in graph
            or (None, None, element) in graph
        ):
            return True

    return False
