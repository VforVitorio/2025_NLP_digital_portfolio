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

###########################################################################


########################### LLM QUERY ##########################
def query_llm(model, messages, temperature=0.7, max_tokens=2000):
    """
    Sends a query to the LLM and gets the response

    Args:
        model(str): ID of the model to use
        messages(list): List of message objects in the conversation
        temperature(float): controls randomnsess in response (0.0-1.0)
        max_tokens(int): maximum number of tokens in the response

    Returns:
        dict: JSON response from the LLM and None if error occurs
    """

    url = f"{BASE_URL}/v1/chat/completions"

    # Prepare payload with all the parameters required
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    # Simple error handling in case the model does not process our query correctly

    try:
        # POST request with our JSON payload
        response = requests.post(url, json=payload)
        # Again raise HTTP exception if occurs
        response.raise_for_status()
        # Parsing to JSON the response
        return response.json()
    except Exception as e:
        # If request fails we put the error
        st.error(f"Error querying model: {e}")
        return None
#####################################################################
