import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from utils import read_uploaded_file, process_text_with_llm

# Load environment variables
load_dotenv()

# Load task prompts from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

app = Flask(__name__)


@app.route("/process", methods=["POST"])
def process_request():
    """
    Process text or file through the API based on the specified task.

    Supports processing:
    - Plain text via form data
    - File uploads
    - Multiple task types (summarize, tag, sentiment, complexity)

    Returns:
        JSON response with processing results or error information.
    """
    try:
        task_type = request.form.get("task")

        if not task_type:
            return jsonify({"error": "Task type is required"}), 400

        if "text" in request.form:
            text = request.form["text"]
            result = process_text_with_llm(text=text, task_type=task_type, task_prompts=config)
            return jsonify({"status": "success", "task": task_type, "result": result})

        if "file" in request.files:
            file = request.files["file"]

            if not file.filename:
                return jsonify({"error": "No selected file"}), 400

            text = read_uploaded_file(file)
            result = process_text_with_llm(text=text, task_type=task_type, task_prompts=config)

            return jsonify(
                {
                    "status": "success",
                    "filename": file.filename,
                    "task": task_type,
                    "result": result,
                }
            )

        return jsonify({"error": "No text or file provided"}), 400

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health_check():
    """
    Provide a simple health check endpoint.

    Returns:
        JSON response indicating API status.
    """
    return jsonify({"status": "healthy", "message": "Text Processing API is running"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
