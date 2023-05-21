# Chatbot Assistant

`chatbot_assistant.py` is a Python script that implements a chatbot assistant using the RevChatGPT API, AWS Kendra, and Amazon Connect. The chatbot is designed to handle customer inquiries and provide relevant information based on the user's input.

### Features

- Utilizes the RevChatGPT API to generate human-like responses to user queries.
- Integrates with AWS Kendra to search for relevant information in a knowledge base.
- Manages session and conversation history for a seamless user experience.
- Handles multiple languages with a configurable language table.
- Implements a custom class `SessConvID` to manage session and conversation IDs.
- Provides utility functions for handling session attributes and closing intent requests.

### Usage

1. Set up the required environment variables:
   - `MSG_LIST_LIMIT`: The maximum number of messages to store in the message list (default: 10).
   - `HIST_STORE_LIMIT`: The maximum number of conversation histories to store (default: 100).
   - `INIT_LANGUAGE`: The initial language for the chatbot (default: "en").
   - `your_email@example.com`: Your email address for the RevChatGPT API.
   - `your_password`: Your password for the RevChatGPT API.
   - `your_aws_kendra_index_id`: Your AWS Kendra index ID.

2. Import the `ChatGPT` class and create an instance of the chatbot:

   ```python
   from chatbot_assistant import ChatGPT

   chatbot = ChatGPT()
   ```

3. Use the chatbot's methods to manage sessions, conversations, and generate responses:

   ```python
   # Add a new message to the chatbot's prompt
   chatbot.prompt.add_msg("Customer: What is the weather like today?")

   # Generate a response using the RevChatGPT API
   response = chatbot.generate_response()

   # Manage session and conversation IDs
   managesess = SessConvID()
   ```

4. Use the utility functions `get_session_attributes` and `close` to handle session attributes and close intent requests in Amazon Connect.

### Dependencies

- `openai`: Required for interacting with the RevChatGPT API.
- `boto3`: Required for interacting with AWS Kendra.

### Notes

Please ensure that you have the necessary API keys and credentials for the RevChatGPT API and AWS Kendra before using this script.