from flask import Flask, request, jsonify, Blueprint, make_response
from transformers import pipeline
import torch
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from markupsafe import Markup

# Define a Blueprint for the analysis endpoints
analysis_blueprint = Blueprint("analysis", __name__)

# Endpoint for emotion analysis
@analysis_blueprint.route("/emotion_metrics", methods=["POST", "GET"])
def analyze_emotion_metrics():
    try:
        # Check if the 'text' field is present in the form data
        text = request.form.get("text")

        if not text:
            return jsonify({"error": "No text provided."}), 400

        # Use the emotion analysis pipeline
        classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)
        model_outputs = classifier([text])

        # Create a Plotly bar chart for emotion analysis
        emotion_labels = [e["label"] for e in model_outputs[0]]
        emotion_scores = [e["score"] for e in model_outputs[0]]

        fig = px.bar(
            x=emotion_scores,  
            y=emotion_labels,  
            orientation='h',   
            labels={"x": "Score", "y": "Emotion"},
            title="Emotion Analysis"
        )

        # Save the Plotly figure as an HTML file
        plotly_html_filename = "emotion_plot.html"
        fig.write_html(plotly_html_filename)

        # Return JSON and the HTML file as an attachment
        response_data = {
            "emotion_metrics": model_outputs[0],
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = make_response(jsonify(response_data))
        response.headers = headers
        response.headers["Content-Disposition"] = f'attachment; filename={plotly_html_filename}'
        response.data = open(plotly_html_filename, "rb").read()

        return response
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint for stance detection
@analysis_blueprint.route("/stance_detection", methods=["POST", "GET"])
def detect_stance():
    try:
        # Check if the 'text' field is present in the form data
        text = request.form.get("text")

        if not text:
            return jsonify({"error": "No text provided."}), 400

        # Use the stance detection pipeline
        pipe = pipeline("text-classification", model="cheese7858/stance_detection") #labels : unrelated, comment, support, against
        # pipe = pipeline("text-classification", model="krishnagarg09/stance-detection-semeval2016")
        stance = pipe(text)[0]
        return jsonify(stance), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@analysis_blueprint.route("/extract_keywords", methods=["POST", "GET"])
def extract_keywords():
    try:
        # Check if the 'text' field is present in the form data
        text = request.form.get("text")

        if not text:
            return jsonify({"error": "No text provided."}), 400

        pipe = pipeline("ner", model="yanekyuk/bert-keyword-extractor")

        keywords = pipe(text)
        cleaned_keywords = []
        # processing output to return just the keywords
        for keyword in keywords:
            if keyword["entity"].startswith("B-"):
                cleaned_keywords.append(keyword["word"])
            elif keyword["entity"].startswith("I-"):
                cleaned_keywords[-1] += " " + keyword["word"]
        keywords = {"keywords": [keyword.replace(" ##", "") for keyword in cleaned_keywords]}
        # Return the  keywords as JSON response
        return jsonify(keywords), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500