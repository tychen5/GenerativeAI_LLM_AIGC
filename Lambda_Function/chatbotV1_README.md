# Unifi OS Console Chatbot

This Python script, `unifi_os_console_chatbot.py`, is a chatbot implementation for the agent. The chatbot is designed to answer user questions by searching through a knowledge base using AWS Kendra and generating responses using OpenAI's GPT-3.

### Features

- Supports multiple languages with a default language set to English.
- Utilizes AWS Kendra for searching through a knowledge base.
- Generates responses using OpenAI's GPT-3.
- Handles session management for multiple users.
- Implements a product name API for identifying product names in user queries.

### Dependencies

- `openai`
- `boto3`
- `requests`

### Environment Variables

- `MSG_LIST_LIMIT`: The maximum number of messages to store in the chat history (default: 10).
- `HIST_STORE_LIMIT`: The maximum number of chat histories to store (default: 100).
- `INIT_LANGUAGE`: The initial language for the chatbot (default: "en").
- `OPENAI_MODEL`: The OpenAI model to use for generating responses (default: "text-davinci-003").
- `OPENAI_TEMPERATURE`: The temperature for the OpenAI model (default: 0).
- `OPENAI_FREQUENCY_PENALTY`: The frequency penalty for the OpenAI model (default: 0).
- `OPENAI_PRESENCE_PENALTY`: The presence penalty for the OpenAI model (default: 0).
- `OPENAI_MAX_TOKENS`: The maximum number of tokens for the OpenAI model (default: 1024).

### Classes

- `SessConvID`: Handles session management for multiple users.
- `Prompt`: Manages the message list for generating prompts.
- `ChatGPT`: Implements the chatbot using OpenAI's GPT-3.

### Functions

- `dbquery_chain`: Queries the knowledge base using AWS Kendra.
- `productname_api`: Identifies product names in user queries.
- `get_longest_doc_info`: Retrieves the longest document information from Kendra search results.
- `kendra_search`: Searches the knowledge base using AWS Kendra.

### Usage

1. Set up the required environment variables.
2. Replace placeholders for sensitive information (e.g., API keys, email, password) with your own credentials.
3. Import the `unifi_os_console_chatbot.py` script into your project.
4. Instantiate the `ChatGPT` class and use its methods to interact with the chatbot.

### Example

```python
from unifi_os_console_chatbot import ChatGPT

chatbot = ChatGPT()
response = chatbot.generate_response("What is the range of the UniFi AP?")
print(response)
```

### Note

Please ensure that you have the necessary API keys and credentials for AWS Kendra and OpenAI before using this script.