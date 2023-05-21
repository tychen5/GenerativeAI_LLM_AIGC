# Chatbot

`chatbot.py` is a Python script that implements a chatbot for the pre-sale agent. The chatbot utilizes OpenAI's GPT-3 model to generate responses and AWS Kendra for searching relevant information. It also includes a product name API for extracting product names from text.

### Features

- GPT-3 based chatbot
- AWS Kendra integration for information retrieval
- Product name extraction API
- Session management for multiple users
- Language support (English and Chinese)

### Classes

- `SessConvID`: Manages sessions, conversation IDs, and chat histories for multiple users.
- `Prompt`: Handles the generation and management of prompts for the GPT-3 model.
- `ChatGPT`: Implements the chatbot using OpenAI's GPT-3 model and handles the conversation flow.

### Functions

- `dbquery_chain`: Queries AWS Kendra for relevant information based on the user's question.
- `productname_api`: Extracts product names from text using a custom API.
- `get_longest_doc_info`: Retrieves the longest document excerpt from AWS Kendra search results.
- `kendra_search`: Searches AWS Kendra for relevant information based on the user's question.
- `kendra_to_gbt3Search`: Handles the conversation flow, including querying AWS Kendra, generating GPT-3 responses, and managing sessions.

### Environment Variables

- `MSG_LIST_LIMIT`: Maximum number of messages to store in the chat history (default: 10).
- `HIST_STORE_LIMIT`: Maximum number of chat histories to store (default: 100).
- `INIT_LANGUAGE`: Initial language for the chatbot (default: "en").
- `OPENAI_MODEL`: OpenAI GPT-3 model to use (default: "text-davinci-003").
- `OPENAI_TEMPERATURE`: Temperature for GPT-3 response generation (default: 0).
- `OPENAI_FREQUENCY_PENALTY`: Frequency penalty for GPT-3 response generation (default: 0).
- `OPENAI_PRESENCE_PENALTY`: Presence penalty for GPT-3 response generation (default: 0).
- `OPENAI_MAX_TOKENS`: Maximum number of tokens for GPT-3 response generation (default: 1024).

### Usage

To use the `chatbot.py` script, you need to set up the required environment variables and API keys for OpenAI and AWS Kendra. Replace the placeholders in the script with your actual API keys and other sensitive information.

Once the setup is complete, you can import the script and use the function to handle user queries and generate chatbot responses. The function takes care of querying AWS Kendra, generating GPT-3 responses, and managing sessions for multiple users.