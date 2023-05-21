# Pre-Sale Agent

This Python code snippet is designed to create a pre-sale agent products. The agent is capable of answering customer questions, providing technical advice, and marketing to potential customers. The code utilizes OpenAI's GPT-3 model to generate responses and integrates with the Kendra search service to provide high-confidence and low-confidence answers based on customer queries.

### Features

- Utilizes OpenAI's GPT-3 model for generating responses
- Integrates with Kendra search service for high-confidence and low-confidence answers
- Handles session management for multiple customers
- Supports multiple languages
- Automatically brings the conversation back when unrelated topics are discussed

### Key Functions

- `dbquery_chain()`: Queries the Kendra search service and returns high-confidence and low-confidence answers based on the customer's question.
- `SessConvID`: A class that manages session information, including customer history, bot history, agent requirements, and confirmation stages.
- `productname_api()`: An API that returns the product name based on the input text.
- `get_longest_doc_info()`: Retrieves the longest document information from the Kendra search results.
- `kendra_search()`: Searches the Kendra index and returns high-confidence and low-confidence answers.
- `Prompt`: A class that generates prompts for the GPT-3 model based on the conversation history.
- `ChatGPT`: A class that utilizes OpenAI's GPT-3 model to generate responses based on the generated prompts.

### Usage

1. Replace the placeholders for sensitive information, such as API keys and index IDs, with your actual values.
2. Set the appropriate environment variables for language, message list limit, and other configurations.
3. Instantiate the `ChatGPT` class and use the `get_response()` method to generate responses based on customer queries.

### Dependencies

- Python 3.6+
- `openai` library
- `boto3` library
- `requests` library
- `json` library
- `datetime` library
- `os` library
- `re` library
- `sys` library
- `io` library
- `time` library
- `random` library

Please ensure that you have the necessary dependencies installed before running the code.