from flask import Flask, request, jsonify, Blueprint
from transformers import pipeline
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

analysis_blueprint = Blueprint("analysis", __name__)

# Initialize pipelines once
emotion_classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)
stance_pipe = pipeline("text-classification", model="cheese7858/stance_detection")
keywords_pipe = pipeline("ner", model="yanekyuk/bert-keyword-extractor")

@analysis_blueprint.route("/emotion_metrics", methods=["POST"])
def analyze_emotion_metrics():
    try:
        text = request.form.get("text")
        if not text:
            return jsonify({"error": "No text provided."}), 400

        model_outputs = emotion_classifier([text])
        return jsonify(model_outputs[0]), 200
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@analysis_blueprint.route("/stance_detection", methods=["POST"])
def detect_stance():
    try:
        text = request.form.get("text")
        if not text:
            return jsonify({"error": "No text provided."}), 400

        stance = stance_pipe(text)[0]
        return jsonify(stance), 200
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@analysis_blueprint.route("/extract_keywords", methods=["POST"])
def extract_keywords():
    try:
        text = request.form.get("text")
        if not text:
            return jsonify({"error": "No text provided."}), 400

        keywords = keywords_pipe(text)
        cleaned_keywords = []
        for keyword in keywords:
            if keyword["entity"].startswith("B-"):
                cleaned_keywords.append(keyword["word"])
            elif keyword["entity"].startswith("I-"):
                cleaned_keywords[-1] += " " + keyword["word"]

        keywords = {"keywords": [keyword.replace(" ##", "") for keyword in cleaned_keywords]}
        return jsonify(keywords), 200
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(analysis_blueprint)
    app.run(debug=True)
