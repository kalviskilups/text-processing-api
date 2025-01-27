import os
import json
import pandas as pd
from io import BufferedReader
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

# Configure Azure OpenAI Client
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-08-01-preview",
)


def read_uploaded_file(file: BufferedReader) -> str:
    """
    Read and convert an uploaded file to text based on its file extension.

    Args:
        file: File object from Flask request.

    Returns:
        str: Extracted text content from the file.

    Raises:
        ValueError: If an unsupported file type is uploaded.
    """
    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension == ".txt":
        return file.read().decode("utf-8")
    elif file_extension == ".csv":
        df = pd.read_csv(file)
        return " ".join(df.apply(lambda row: " ".join(row.astype(str)), axis=1))
    elif file_extension == ".json":
        data = json.load(file)
        return json.dumps(data)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")


def process_text_with_llm(text: str, task_type: str, task_prompts: dict) -> str:
    """
    Process text using Azure OpenAI based on the specified task type.

    Args:
        text (str): Input text to be processed.
        task_type (str): The type of processing task.
        task_prompts (dict): Dictionary of task-specific system prompts.

    Returns:
        str: Processed text result from the language model.

    Raises:
        ValueError: If an unsupported task type is provided.
        RuntimeError: If an error occurs during text processing.
    """
    if task_type not in task_prompts["prompts"]:
        raise ValueError(f"Unsupported task type: {task_type}")

    system_prompt = task_prompts["prompts"][task_type]

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text},
            ],
            max_tokens=300,
        )

        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Error processing text with LLM: {str(e)}")
