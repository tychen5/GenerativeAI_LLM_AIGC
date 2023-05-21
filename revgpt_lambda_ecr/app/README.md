# Pre-Sale Agent

This Python code snippet is a comprehensive solution for a pre-sale agent. The agent is designed to provide helpful, truthful, and friendly technical advice regarding networking hardware. The main goal is to promote and convince customers to buy them.

### Features

- Utilizes OpenAI GPT-3 for generating responses
- Integrates with AWS Kendra for searching relevant information
- Handles session management for multiple users
- Supports multiple languages
- Automatically transfers to a human agent if needed

### Dependencies

- Python 3.6+
- `openai` library
- `boto3` library
- `requests` library

### Usage

1. Replace the placeholders for API keys and other sensitive information with your actual credentials.
2. Import the necessary functions and classes from the script.
3. Create an instance of the `SessConvID` class to manage sessions.
4. Use the `kendra_to_gpt3_search` function to handle user input and generate appropriate responses.

### Functions and Classes

- `dbquery_chain`: Searches for high and low confidence answers using AWS Kendra.
- `SessConvID`: A class for managing session-related information.
- `productname_api`: An API for extracting product names from text.
- `get_longest_doc_info`: Extracts the longest document information from Kendra search results.
- `kendra_search`: Searches for relevant information using AWS Kendra.
- `Prompt`: A class for managing conversation prompts.
- `ChatGPT`: A class for generating responses using OpenAI GPT-3.
- `kendra_to_gpt3_search`: Handles user input and generates appropriate responses.

### Example

```python
from UniFiOSConsolePreSaleAgent import SessConvID, kendra_to_gpt3_search

managesess = SessConvID()

# Process user input and generate a response
response = kendra_to_gpt3_search(intent_request, sess_id)
```

### Note

Please ensure that you have the necessary API keys and credentials set up before using this code snippet. Replace the placeholders with your actual credentials and data paths when using this code.