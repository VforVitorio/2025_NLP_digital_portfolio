# Lab Exercise 03 Víctor Vega Sobral

---

## F1 Strategy Assistant

The F1 Strategy Assistant is a specialized chat application built to provide Formula 1 enthusiasts with expert insights on race strategies, technical regulations, and F1 history, alongisde simple explanations of complex concepts of this sport, in order to help new fans familiarize with the sport.

The app also provides the user the option to select from their local LLMs.

---

### Tools and Technologies Selection

#### Core technologies

1. **Streamlit** is selected as the primary framework for several reasons. It has rapid prototypiing capabilites for data-focused applications, with built-in widgets that simplify UI development. Moreover, and most important, it´s Python-based, allowing easy integration with other libraries.
2. **LM Studio** is the chosen LLM backend, becuase it provides an easy API integration that allows us to connect easily the model through endpoints. It also allows experimenting with different model sizes and capabilities, apart from reducing latency and removing dependency of cloud-base services.
3. **Python Libraries** needed:
   1. `requests`: handles the API communication with LM Studio.
   2. `uuid`: generates unique identifiers for the chat sessions,
   3. `datetime`: used for timestamping the conversations.
   4. `json`: used for processing API responses.

---

### Development Process

#### First Step: Initial Setup and Requirements Analysis

First step involded is defining the scope and requirements for the F1 Strategy Assistant. The application needed to:

- Provide expert-level F1 Knowledge through an LLM (in our case, LLama 3.2).
- Support multi-session chat management.
- Present information in a F1-themed interface.
- Allow customization of model parameters.

This step is crucial for defining what we want to do with the LLM and also the parts that our application will have. The purpose is to mimic ChatGPT-liked chat applications with some of the parts that are common in them (chat history, model selection, etc).

#### Second step: backend integration with LM Studip

LM studio was set up to serve LMs locally, and API integration was implemented to discover the available models through endpoint `v1/models`, send queries to the selected model through a POST petition with our `payload` dictionary and finally parsing to JSON format the model response.

[T](model_select.png)exto alternativo
