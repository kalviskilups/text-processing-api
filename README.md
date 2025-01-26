# Text Processing API

## Overview
This is a Flask-based text processing API that uses Azure OpenAI to perform various text analysis tasks. The application supports processing both text and files through different task types.

## Features
- Process plain text and files
- Multiple task types:
  - Summarization
  - Keyword Tagging
  - Sentiment Analysis
  - Complexity Assessment
- Supports .txt, .csv, and .json file formats
- Health check endpoint

## Setup

### 1. Environment Setup
1. Clone the repository
2. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables
   Create a `.env` file with:
   ```
   AZURE_OPENAI_ENDPOINT=your_azure_endpoint
   AZURE_OPENAI_API_KEY=your_azure_api_key
   ```

### 2. Configuration
- Modify `config.json` to customize task prompts.
- Ensure your model deployment matches the model in `utils.py`.

## Running the Application

### Start the Server

```bash
python server.py
```

The API will run on `http://127.0.0.1:5000`

## API Interaction Methods

### Using Python Client

You can just run client.py, which will provide an example of all the task options:

```bash
python client.py
```

Alternatively, you can just import the calls and test them out:

```bash
from client import process_text, process_file

# Process text
result = process_text("Your text", task_type="summarize")

# Process file
result = process_file("file.txt", task_type="tag")
```

### Using cURL

```bash
# Process Text
curl -X POST http://127.0.0.1:5000/process \
     -F "text=Your input text here" \
     -F "task=summarize"

# Process File
curl -X POST http://127.0.0.1:5000/process \
     -F "file=@/path/to/file.txt" \
     -F "task=tag"
```

## API Endpoints
- `/process` (POST): Process text or file
- `/health` (GET): Check API status

## Supported Tasks
- `summarize`: Generate a concise summary
- `tag`: Extract keywords
- `sentiment`: Analyze text sentiment
- `complexity`: Assess reading complexity

## Error Handling
The API provides informative error responses for:
- Missing task type
- Unsupported file types
- Processing errors