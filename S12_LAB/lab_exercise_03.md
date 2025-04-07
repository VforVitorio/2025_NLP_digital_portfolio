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

[Model selection](images/model_select.png)

### Step 3: Defining the F1 Expert System Prompt

A critical aspect was crafting a specialized system prompt to transform a general-purpose language model into an F1 expert. This prompt provides context and boundaries for the model's responses.

[Model response](images/query.png)

### Step 4: Implementing Chat History Management

To support multiple conversations, a robust chat history management system was implemented using Streamlit's session state capabilities and unique identifiers for each chat.

[Model chat history](images/chat_history.png)

### Step 5: Designing a Formula 1 Themed UI

To create an immersive F1 experience, custom CSS styling was applied to Streamlit's default components, creating a dark theme with purple/blue accents similar to modern F1 team colors and digital dashboards.

[custom css](images/custom_css.png)

### Step 6: Implementing the Chat Interface

The chat interface was built to display messages with F1-themed icons (race car for user, checkered flag for assistant) and provide an input field for user questions. This can be seen again

[Chat Interface](images/chat_history.png)

### Step 7: Adding Example Questions for User Engagement

To help users understand the assistant's capabilities, a set of example questions was added to the sidebar, with each example functioning as a clickable button.

[Example Questions](images/questions.png)

---

## Development Challenges & Solutions

### Challenge 1: Local Model Management

**Problem** : Integrating with locally hosted language models required handling connectivity issues and model loading states.

**Solution** : Implemented robust error handling in the API communication functions and added fallback options for when models are unavailable.

### Challenge 2: Maintaining Chat State

**Problem** : Streamlit refreshes the entire application on each interaction, which can make maintaining chat state difficult.

**Solution** : Leveraged Streamlit's session state to persist chat histories and manage multiple conversations effectively.

### Challenge 3: F1-Specific Knowledge

**Problem** : General language models may not have specialized F1 strategy knowledge, or might provide overly generic responses.

**Solution** : Created a detailed system prompt that frames the model as an F1 expert and includes specific instructions for analyzing race scenarios.

## Future Enhancements

Based on the development process, several potential enhancements were identified:

1. **Race Data Integration** : Connect to live F1 timing data during race weekends
2. **Circuit Visualization** : Add interactive circuit maps when discussing track-specific strategies
3. **Team-Specific Analysis** : Allow users to select their favorite team for tailored strategic insights
4. **Historical Race Analysis** : Add specific data about historical races for more accurate comparisons
5. **Mobile Optimization** : Further refine the UI for mobile devices during trackside use

## Conclusion

The development of the F1 Strategy Assistant demonstrates how specialized LLM applications can provide value in specific domains. By combining Streamlit's rapid development capabilities with LM Studio's flexible model hosting, a powerful tool for F1 enthusiasts was created with relatively simple code.

The application shows that even without custom model training, properly prompted language models can provide domain-specific expertise when framed with the right context and user interface.
