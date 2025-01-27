import requests
import json
import os

API_URL = "http://127.0.0.1:5000"


def process_text(text: str, task_type: str = "summarize") -> dict:
    """
    Send plain text to the API for processing.

    Args:
        text (str): The input text to be processed.
        task_type (str, optional): The type of processing task. Defaults to "summarize".

    Returns:
        dict: The API response containing processed text or error information.
    """
    try:
        response = requests.post(
            f"{API_URL}/process",
            data={"text": text, "task": task_type},
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Exception occurred: {e}")


def process_file(file_path: str, task_type: str = "summarize") -> dict:
    """
    Send a file to the API for processing.

    Args:
        file_path (str): Path to the file to be processed.
        task_type (str, optional): The type of processing task. Defaults to "summarize".

    Returns:
        dict: The API response containing processed file content or error information.
    """
    try:
        with open(file_path, "rb") as f:
            response = requests.post(
                f"{API_URL}/process",
                files={"file": f},
                data={"task": task_type},
            )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Exception occurred: {e}")


def health_check() -> dict:
    """
    Perform a health check on the API.

    Returns:
        dict: API health status information or error details.
    """
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Exception occurred: {e}")


if __name__ == "__main__":
    # Load example text from config.json
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    # Health Check
    print("Health Check:")
    print(health_check())

    # Multiple task type examples

    # Summarization
    print("\nSummarization:")
    print(process_text(config["example_text"]["content"], task_type="summarize"))

    # Keyword Tagging
    print("\nKeyword Tagging:")
    print(process_text(config["example_text"]["content"], task_type="tag"))

    # Sentiment Analysis
    print("\nSentiment Analysis:")
    print(process_text(config["example_text"]["content"], task_type="sentiment"))

    # Complexity Analysis
    print("\nComplexity Analysis:")
    print(process_text(config["example_text"]["content"], task_type="complexity"))

    # File Processing Example
    if os.path.exists("test.txt"):
        file_path = "test.txt"
        print("\nProcessing File:")
        print(process_file(file_path, task_type="summarize"))
    else:
        print("Could not process a file test.txt, as it does not exist!")
