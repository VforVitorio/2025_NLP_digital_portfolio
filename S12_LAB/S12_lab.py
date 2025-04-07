######################### BASIC CONFIG #################################
# Import necessary libraries
import streamlit as st  # For the web interface
import requests  # For making API calls to the LLM server
import json  # For handling JSON data
import uuid  # For generating unique IDs for chat sessions
import datetime  # For timestamping chat sessions

# Configure the Streamlit page properties - MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="F1 Strategy Assistant",  # Sets the browser tab title
    page_icon="🏎️",  # Sets the browser tab icon
    layout="wide"  # Uses the wide layout for more space
)

# Base URL for LM Studio's API endpoint
BASE_URL = "http://localhost:1234"  # Default port for LM Studio

# Custom CSS to apply a dark purple/blue theme similar to Reflex UI
st.markdown("""
<style>
    /* Main background and text colors */
    .main {
        background-color: #0e0e1a;
        color: #ffffff;
    }
    
    /* Sidebar styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background-color: #1a1a2e;
    }
    
    /* Buttons styling with more curved borders and no hover shadow */
    .stButton>button {
        background-color: #6c5ce7;
        color: white;
        border: none;
        border-radius: 12px;  /* More curved borders */
        transition: background-color 0.3s;
        box-shadow: none !important;  /* Remove default shadow */
    }
    .stButton>button:hover {
        background-color: #7f6ff0;
        box-shadow: none !important;  /* Remove hover shadow */
    }
    
    /* Input fields with more curved borders */
    .stTextInput>div>div>input, [data-testid="stChatInput"] {
        background-color: #252540;
        color: white;
        border: 1px solid #6c5ce7;
        border-radius: 12px;  /* More curved borders */
    }
    
    /* Headers */
    h1, h2, h3 {
        color: white;
    }
    
    /* Chat messages with more curved borders */
    .chat-message {
        padding: 1rem;
        border-radius: 16px;  /* More curved borders */
        margin-bottom: 1rem;
        box-shadow: none !important;  /* Remove shadow */
    }
    .user-message {
        background-color: #252540;
    }
    .assistant-message {
        background-color: #3a3a5c;
    }
    
    /* History items with more curved borders */
    .history-item {
        padding: 0.5rem;
        border-radius: 12px;  /* More curved borders */
        margin-bottom: 0.5rem;
        background-color: #252540;
        cursor: pointer;
        box-shadow: none !important;  /* Remove shadow */
    }
    .history-item:hover {
        background-color: #333355;
        box-shadow: none !important;  /* Remove hover shadow */
    }
    
    /* Remove hover effects and shadows from other elements */
    .element-container:hover, .stAlert:hover, .stTextArea:hover {
        box-shadow: none !important;
    }
    
    /* Ensure chat container has curved borders too */
    [data-testid="stChatMessageContent"] {
        border-radius: 14px !important;
        overflow: hidden;
    }
    
    /* Add curved borders to select boxes and other controls */
    .stSelectbox > div > div {
        border-radius: 12px !important;
    }
    
    /* Adjust chat message avatar containers */
    [data-testid="stChatMessageAvatar"] {
        background-color: transparent !important;
    }
</style>
""", unsafe_allow_html=True)
########################################################################

################## RETRIEVING AVAILABLE MODELS #########################


def get_models():
    """
    Fetches the list of available models from the LLM server.

    Returns:
        list: A list of model IDs available on the server
    """
    url = f"{BASE_URL}/v1/models"

    try:
        # Send GET request to the models endpoint opened from LM Studio
        response = requests.get(url)
        # Raise an HTTP error if it occurs
        response.raise_for_status()
        # Parse the JSON Response
        data = response.json()

        # We extract and return the model IDs
        return [model["id"] for model in data.get("data", [])]
    except Exception as e:
        # If request fails, show error in Streamlit
        st.error(f"Error fetching models: {e}")
        return []
###########################################################################

########################### LLM QUERY ##########################


def query_llm(model, messages, temperature=0.7, max_tokens=2000):
    """
    Sends a query to the LLM and gets the response

    Args:
        model(str): ID of the model to use
        messages(list): List of message objects in the conversation
        temperature(float): controls randomness in response (0.0-1.0)
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

########################### CHAT HISTORY MANAGEMENT #########################


def initialize_chat_history():
    """
    Initialize the chat history data structures in session state
    This function sets up the necessary state variables for tracking chat sessions
    """
    # Initialize chat histories dictionary to store multiple conversations
    if "chat_histories" not in st.session_state:
        st.session_state.chat_histories = {}

    # Initialize current chat ID pointer
    if "current_chat_id" not in st.session_state:
        # Generate a new chat ID when starting a new session
        new_chat_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        # Store the new chat with the system prompt as the first message
        st.session_state.chat_histories[new_chat_id] = {
            "title": f"Chat {timestamp}",
            "messages": [{"role": "system", "content": f1_system_prompt}],
            "timestamp": timestamp
        }
        st.session_state.current_chat_id = new_chat_id


def create_new_chat():
    """
    Creates a new chat session with a unique ID and timestamp
    """
    # Generate a new chat ID
    new_chat_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # Store the new chat in chat histories
    st.session_state.chat_histories[new_chat_id] = {
        "title": f"Chat {timestamp}",
        "messages": [{"role": "system", "content": f1_system_prompt}],
        "timestamp": timestamp
    }

    # Switch to the new chat
    st.session_state.current_chat_id = new_chat_id
    st.session_state.messages = st.session_state.chat_histories[new_chat_id]["messages"]

    # Rerun to update the UI
    st.rerun()


def delete_current_chat():
    """
    Deletes the current chat or resets it if it's the only one
    """
    # Delete the current chat from the histories
    if len(st.session_state.chat_histories) > 1:
        # If there are other chats, delete this one and switch to another
        del st.session_state.chat_histories[st.session_state.current_chat_id]
        st.session_state.current_chat_id = next(
            iter(st.session_state.chat_histories))
        st.session_state.messages = st.session_state.chat_histories[
            st.session_state.current_chat_id]["messages"]
    else:
        # If this is the only chat, just reset it
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        st.session_state.chat_histories[st.session_state.current_chat_id] = {
            "title": f"Chat {timestamp}",
            "messages": [{"role": "system", "content": f1_system_prompt}],
            "timestamp": timestamp
        }
        st.session_state.messages = st.session_state.chat_histories[
            st.session_state.current_chat_id]["messages"]

    # Rerun to update the UI
    st.rerun()


def load_chat(chat_id):
    """
    Loads a specified chat by ID

    Args:
        chat_id (str): The ID of the chat to load
    """
    st.session_state.current_chat_id = chat_id
    st.session_state.messages = st.session_state.chat_histories[chat_id]["messages"]
    st.rerun()
#####################################################################


#################################### STREAMLIT CONFIG #############################
# Define the system prompt that specializes the model in Formula 1
# This acts as initial instructions for the AI
f1_system_prompt = """
You are a Formula 1 expert with extensive knowledge about:
- Race strategies (undercut, overcut, pit stops, etc)
- Technical and sporting regulations
- F1 history and drivers
- Circuits and their characteristics 
- Aerodynamics and technical aspects of the cars

Provide detailed and technical answers that are still easy to understand.
When analyzing hypothetical race situations, consider factors such as:
- Tire degradation
- Gaps between cars
- Rival team strategies
- Track and weather conditions

Respond in an educational and detailed manner, explaining technical concepts.
"""

# Initialize chat history management system
initialize_chat_history()

# Add the main title and description
st.title("🏎️ Formula 1 Assistant")
st.markdown("Ask any F1-related questions or pose hypothetical race scenarios.")

# Get current chat messages
current_chat = st.session_state.chat_histories[st.session_state.current_chat_id]
st.session_state.messages = current_chat["messages"]
###################################################################################

######################### SIDEBAR COMPONENTS ###########################
# Get the available models and create a dropdown selector in the sidebar
available_models = get_models()
selected_model = st.sidebar.selectbox(
    "Select a model",
    options=available_models if available_models else ["No models available"]
)

# Chat History Management in Sidebar
st.sidebar.markdown("### Chat History")

# Create a new chat button
if st.sidebar.button("+ New Chat"):
    create_new_chat()

# Display chat history
st.sidebar.markdown("#### Previous Chats")
for chat_id, chat_data in sorted(
    st.session_state.chat_histories.items(),
    key=lambda x: x[1]["timestamp"],
    reverse=True
):
    # Get the first user message as title (if available)
    title = chat_data["title"]
    for msg in chat_data["messages"]:
        if msg["role"] == "user":
            title = msg["content"][:30] + \
                "..." if len(msg["content"]) > 30 else msg["content"]
            break

    # Create a clickable container for each chat history
    chat_container = st.sidebar.container()
    chat_container.markdown(f"""
    <div class="history-item" id="{chat_id}">
        <small>{chat_data['timestamp']}</small><br>
        {title}
    </div>
    """, unsafe_allow_html=True)

    # Add a button to load this chat
    if chat_container.button("Load", key=f"load_{chat_id}"):
        load_chat(chat_id)

# Predefined example questions in the sidebar
st.sidebar.markdown("### Example Questions")
example_questions = [
    "What is an undercut and when is it effective?",
    "If Hamilton was 2 seconds behind Gasly and couldn't pass him at Suzuka, why didn't they try an undercut there?",
    "How does tire degradation affect race strategy?",
    "What are the best strategies in Monaco given the difficulty in overtaking?",
    "Why do teams sometimes sacrifice qualifying position to have different tires in the race?"
]

# Add configuration options to sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### Configuration")

# Add a temperature slider to adjust the LLM's creativity
temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.1,
    help="Higher values = more creative responses. Lower values = more predictable responses."
)

# Add a button to clear the conversation history
if st.sidebar.button("Delete Current Chat"):
    delete_current_chat()

# Add information about the project
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "This F1 assistant uses a language model to answer questions "
    "about strategies, regulations, and hypothetical Formula 1 situations. "
    "Developed for the F1 Strategy Manager project."
)
#####################################################################

####################### MAIN USER INTERFACE #####################
# Create a key in session state to track if we need to process a selected example
if "selected_example" not in st.session_state:
    st.session_state.selected_example = None

# Track displayed messages to prevent duplicates
if "displayed_messages" not in st.session_state:
    st.session_state.displayed_messages = set()

# Display previous messages in the chat
for message in st.session_state.messages:
    # Skip system messages as they shouldn't be displayed to the user
    if message["role"] != "system":
        # Create a simple message identifier based on content
        message_id = f"{message['role']}_{message['content'][:50]}"

        # Only display the message if we haven't displayed it already in this session
        if message_id not in st.session_state.displayed_messages:
            st.session_state.displayed_messages.add(message_id)

            # Add custom CSS classes for styling
            css_class = "user-message" if message["role"] == "user" else "assistant-message"

            # Use custom F1-themed icons
            icon = "🏎️" if message["role"] == "user" else "🏁"

            with st.chat_message(message["role"], avatar=icon):
                st.markdown(f"""
                <div class="chat-message {css_class}">
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)

# Create buttons for each example question
for i, question in enumerate(example_questions):
    # Give each button a unique key
    if st.sidebar.button(question, key=f"example_{i}"):
        # Store the selected question in session state
        st.session_state.selected_example = question
        # Add the selected question to the chat history
        st.session_state.messages.append({"role": "user", "content": question})
        # Update the current chat in the chat histories
        current_chat = st.session_state.chat_histories[st.session_state.current_chat_id]
        current_chat["messages"] = st.session_state.messages
        # Reset displayed messages to avoid issues with the new message
        st.session_state.displayed_messages = set()
        # Trigger a rerun to process the question
        st.rerun()

# Create an input field for user questions
prompt = st.chat_input("Ask about F1 or pose a hypothetical situation...")
if prompt:
    # Add the user's message to the chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Update the current chat in the chat histories
    current_chat = st.session_state.chat_histories[st.session_state.current_chat_id]
    current_chat["messages"] = st.session_state.messages
    # Set as the current prompt to process
    st.session_state.selected_example = prompt
    # Reset displayed messages to avoid issues with the new message
    st.session_state.displayed_messages = set()
    # Trigger a rerun to process the question
    st.rerun()

# Process the selected example or user input
if st.session_state.selected_example:
    # Display the user's message with F1 car icon
    with st.chat_message("user", avatar="🏎️"):
        st.markdown(f"""
        <div class="chat-message user-message">
            {st.session_state.selected_example}
        </div>
        """, unsafe_allow_html=True)

    # Create a placeholder for the assistant's response with checkered flag icon
    with st.chat_message("assistant", avatar="🏁"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Analyzing situation...")

        # Prepare the chat messages to send to the LLM
        # Filter out system messages and then add the system prompt at the beginning
        chat_messages = [
            m for m in st.session_state.messages if m["role"] != "system"]
        chat_messages = [
            {"role": "system", "content": f1_system_prompt}] + chat_messages

        # Query the LLM with the prepared messages
        response = query_llm(
            model=selected_model,
            messages=chat_messages,
            temperature=temperature,  # Use the temperature from the slider
            max_tokens=2000
        )

        # Process the LLM's response
        if response:
            # Extract the text content from the response
            llm_response = response["choices"][0]["message"]["content"]
            # Update the placeholder with the response
            message_placeholder.markdown(f"""
            <div class="chat-message assistant-message">
                {llm_response}
            </div>
            """, unsafe_allow_html=True)
            # Add the response to the chat history
            st.session_state.messages.append(
                {"role": "assistant", "content": llm_response})
            # Update the current chat in the chat histories
            current_chat = st.session_state.chat_histories[st.session_state.current_chat_id]
            current_chat["messages"] = st.session_state.messages
        else:
            # Display an error message if the query failed
            message_placeholder.markdown("""
            <div class="chat-message assistant-message">
                ❌ Error generating response. Please try again.
            </div>
            """, unsafe_allow_html=True)

    # Clear the selected example after processing
    st.session_state.selected_example = None
    # Reset displayed messages for next refresh to include these new messages
    st.session_state.displayed_messages = set()
##########################################################
