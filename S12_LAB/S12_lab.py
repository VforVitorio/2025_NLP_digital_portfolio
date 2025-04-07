######################### BASIC CONFIG #################################
# Import necessary libraries
import streamlit as st  # For the web interface
import requests  # For making API calls to the LLM server
import json  # For handling JSON data

BASE_URL = "http://localhost:1234"  # Default port for LM Studio
########################################################################

################## RETRIEVING AVAILABLE MODELS #########################


def get_models():
    """
    Fetches the list of available models from the LLM server.

    Returns:
        list: A list of model IDs available on the server
    """

    url = f"{BASE_URL}/v1/models"

    # Send GET request to the models endpoint opened from LM Studio
    response = requests.get(url)
    # Raise an HTTP error if it occurs
    response.raise_for_status()
    # Parse the JSON Response
    data = response.json()

    # We extract and return the model IDs
    return [model[id] for model in data.get("data", [])]
