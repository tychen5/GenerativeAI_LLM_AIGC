# Chatbot Session Manager

This Python script, `chatbot_session_manager.py`, is designed to manage chatbot sessions and handle user interactions with the chatbot. The script utilizes the `revChatGPT.V1` library to create a chatbot instance and manage its conversations. It also integrates with AWS Kendra for searching relevant information based on user queries.

### Features

1. Session management: The script maintains a session for each user, keeping track of their conversation history and chatbot responses.
2. AWS Kendra integration: The script uses AWS Kendra to search for relevant information based on user queries and returns high-confidence and low-confidence results.
3. Customizable message limits: The script allows setting limits on the number of messages stored in a conversation and the maximum number of tokens for the chatbot model.

### Classes and Functions

#### `SessConvID`

This class manages the chatbot sessions and their associated conversation IDs. It provides methods to:

- Get and set conversation IDs for a session
- Get and set customer and chatbot message history for a session
- Get and set the need for a human agent in a session
- Get and set the confirmation stage for a session

#### `Prompt`

This class manages the message prompts for the chatbot. It provides methods to:

- Add and remove messages from the prompt
- Generate a prompt string for the chatbot

#### `get_longest_doc_info(kendra_dict)`

This function extracts the longest document information from the AWS Kendra search results.

#### `kendraSearch(query)`

This function performs a search using AWS Kendra and returns high-confidence and low-confidence results.

#### `get_session_attributes(intent_request)`

This function retrieves session attributes from the intent request.

#### `close(intent_request, session_attributes, fulfillment_state, message)`

This function closes the intent request with the provided session attributes, fulfillment state, and message.

### Usage

To use this script, you need to have the `revChatGPT.V1` library installed and set up your AWS Kendra credentials. You can then create an instance of the `SessConvID` class to manage chatbot sessions and use the provided functions to interact with the chatbot and AWS Kendra.

### Dependencies

- `revChatGPT.V1`
- `openai`
- `boto3`
- `datetime`
- `os`
- `sys`
- `io`
- `random`
- `re`
- `time`