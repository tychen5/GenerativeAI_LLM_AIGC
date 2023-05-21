# Pre-Sale Chatbot

This Python script implements a pre-sale chatbot products. The chatbot is designed to provide helpful, truthful, and friendly technical advice regarding networking hardware provided . It aims to promote and recommend suitable products for customers.

### Features

- Utilizes OpenAI's GPT-3.5-turbo model for generating responses.
- Handles multiple sessions and maintains conversation history.
- Supports different languages with a language table.
- Integrates with an external product name API for better product recognition.
- Searches for relevant information using the Kendra search engine.

### Dependencies

- Python 3.6+
- `openai` library
- `boto3` library
- `requests` library

### Environment Variables

The following environment variables need to be set:

- `OPENAI_MODEL`: The OpenAI model to be used (default: "gpt-3.5-turbo").
- `OPENAI_TEMPERATURE`: The temperature for the OpenAI model (default: 0).
- `OPENAI_FREQUENCY_PENALTY`: The frequency penalty for the OpenAI model (default: 0).
- `OPENAI_PRESENCE_PENALTY`: The presence penalty for the OpenAI model (default: 0).
- `OPENAI_MAX_TOKENS`: The maximum number of tokens for the OpenAI model (default: 1024).
- `MSG_LIST_LIMIT`: The maximum number of messages to store in the conversation history (default: 20).
- `HIST_STORE_LIMIT`: The maximum number of conversation histories to store (default: 100).
- `INIT_LANGUAGE`: The initial language for the chatbot (default: "en").

### Usage

1. Install the required dependencies:

   ```
   pip install openai boto3 requests
   ```

2. Set the necessary environment variables in your system or use a `.env` file to store them securely.

3. Replace the placeholder "enter_your_openai_api_key_here" with your actual OpenAI API key.

4. Run the script:

   ```
   python PreSale_Chatbot.py
   ```

### Classes and Functions

- `SessConvID`: A class to manage session IDs, conversation history, and other session-related information.
- `productname_api(text)`: A function to call an external product name API for better product recognition.
- `get_longest_doc_info(kendra_dict)`: A function to extract the most relevant information from the Kendra search results.
- `kendraSearch(query)`: A function to search for relevant information using the Kendra search engine.
- `Prompt`: A class to manage the chatbot's prompts and conversation history.
- `ChatGPT`: A class to interact with OpenAI's GPT-3.5-turbo model and generate responses.
- `kendra_to_gbt3_search()`: A function to handle the chatbot's conversation flow and integrate with the Kendra search engine.

### Note

This script is a modified version of the original code, with sensitive information removed and reformatted according to Google style guidelines for Python.