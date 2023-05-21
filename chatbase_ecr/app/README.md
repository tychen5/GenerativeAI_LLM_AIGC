# Pre-Sales Agent

This Python script is designed to act as a pre-sales agent. The agent engages with customers interested in learning about UniFi OS Console products and their specifications, providing technical advice on Ubiquiti's networking hardware.

### Features

- Utilizes OpenAI GPT-3.5-turbo model for generating responses
- Retrieves information from various sources, including OpenAI, Kendra, and Chatbase
- Processes and formats the retrieved information to provide concise and relevant answers
- Supports markdown formatting for better readability
- Handles various types of questions, including product recommendations, comparisons, and specifications
- Provides additional resources and links when necessary

### Dependencies

- Python 3.6+
- `openai` library
- `boto3` library
- `tiktoken` library
- `wordfreq` library
- `langchain` library
- `asyncio` library
- `pickle` library
- `functools` library
- `datetime` library
- `concurrent.futures` library

### Configuration

Before running the script, make sure to replace the placeholders with your actual values, such as:

- `your_openai_api_key`: Your OpenAI API key
- `your_chatbase_botid`: Your Chatbase bot ID
- `OPENAI_MODEL`: The OpenAI model to use (default: "gpt-3.5-turbo")
- File paths for `revisor_chain_pkl`, `query_chain_di_pkl`, and `url_di_pkl`

Additionally, you can customize various settings through environment variables, such as:

- `min_count_doc`: Minimum document count (default: 1400)
- `max_count_doc`: Maximum document count (default: 2400)
- `max_model_tok`: Maximum model tokens (default: 2048)
- `max_model_tok_nlg`: Maximum model tokens for natural language generation (default: 4000)
- `answer_max_tok`: Maximum answer tokens (default: 1000)
- `temperature`: Temperature for OpenAI model (default: 0.95)
- `frequency_penalty`: Frequency penalty for OpenAI model (default: 0.1)
- `presence_penalty`: Presence penalty for OpenAI model (default: 0.3)
- `top_p`: Top-p for OpenAI model (default: 1)
- `max_tokens`: Maximum tokens for OpenAI model (default: 250)
- `stop_seq`: Stop sequence for OpenAI model (default: ["\n\n\n", " \n\n "])

### Usage

1. Install the required dependencies.
2. Replace the placeholders with your actual values.
3. Run the script using Python 3.6 or higher.

The script will act as a pre-sales agent, answering customer questions about UniFi OS Console products and their specifications. It will retrieve information from various sources, process and format the information, and provide concise and relevant answers to the customers.