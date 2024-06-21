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
# @File    : helper.py
# @Software: PyCharm
import logging
import yaml


def load_yaml_config(file_path):
    """
    Load YAML configuration from a file and return as a dictionary.

    :param file_path: str
        The path to the YAML configuration file.
    :return: dict
        The configuration as a dictionary.
    """
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)
    return config


def apply_logging_configuration(config):
    """
    Apply logging configuration from a dictionary.

    :param config: dict
        The logging configuration dictionary.
    :return: None
    """
    logging.config.dictConfig(config)
