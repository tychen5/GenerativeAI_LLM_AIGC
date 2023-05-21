# Pre-Sale Agent

This Python code snippet is designed to create a pre-sale Q&A agent for products. The agent is capable of answering customer questions about products and their specifications, providing technical advice, and promoting the products in a friendly and helpful manner.

### Features

- Utilizes OpenAI's GPT-3 model for natural language understanding and generation.
- Integrates with AWS Kendra for searching and retrieving relevant information.
- Handles conversation flow and calls appropriate functions based on user input and conversation state.
- Supports multiple languages with a language table for easy customization.
- Automatically manages conversation history and session data.

### Key Functions

- `dbquery_chain()`: Optimizes GPT indexing query and returns high-confidence and low-confidence search results.
- `kendra_search()`: Searches AWS Kendra for relevant information based on the user's query.
- `productname_api()`: Calls an external API to replace product names in the user's query.
- `kendra_to_gpt3_search()`: Handles the conversation flow and calls appropriate functions based on user input and conversation state.
- `kendra_to_gbt3_search()`: Handles conversation flow when transitioning from Kendra to GPT-3 search.

### Usage

1. Replace the placeholders for sensitive information (API keys, URLs, etc.) with your actual information.
2. Ensure that the required libraries are installed, such as `openai`, `boto3`, and `requests`.
3. Import the `UniFiOSConsolePreSaleAgent` module and create an instance of the agent.
4. Use the agent's methods to handle user queries and generate appropriate responses.

### Dependencies

- Python 3.6 or higher
- openai
- boto3
- requests
