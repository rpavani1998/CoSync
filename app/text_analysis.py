from flask import Flask, request, jsonify, Blueprint, make_response, render_template_string
from transformers import pipeline
import torch
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from markupsafe import Markup
import base64 
import threading
import io

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
        pipe = pipeline("text-classification", model="cheese7858/stance_detection")
        stance = pipe(text)[0]

        # Define labels for stance categories
        labels = ["unrelated", "comment", "support", "against"]

        # Create a Pie chart
        labels_values = [0]*len(labels)
        labels_values[labels.index(stance["label"])] = stance["score"]
        total_score = sum(labels_values)

        # Distribute remaining score equally among labels to make the total score 1
        remaining_score = 1.0 - total_score
        num_remaining_labels = 3
        if num_remaining_labels > 0:
            remaining_score_per_label = remaining_score / num_remaining_labels
            labels_values = [value if value != 0 else remaining_score_per_label for value in labels_values]
        print(labels, labels_values)
        fig = px.pie(
            names=labels,
            values=labels_values,
            title="Stance Detection"
        )
        # Save the Plotly figure as an HTML file
        plotly_html_filename = "stance_pie_chart.html"
        fig.write_html(plotly_html_filename)

        # Return JSON and the HTML file as an attachment
        response_data = {
            "stance": stance,
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
    
# @analysis_blueprint.route("/extract_keywords", methods=["POST", "GET"])
# def extract_keywords():
#     try:
#         # Check if the 'text' field is present in the form data
#         text = request.form.get("text")

#         if not text:
#             return jsonify({"error": "No text provided."}), 400

#         pipe = pipeline("ner", model="yanekyuk/bert-keyword-extractor")

#         keywords = pipe(text)
#         cleaned_keywords = []
#         # processing output to return just the keywords
#         for keyword in keywords:
#             if keyword["entity"].startswith("B-"):
#                 cleaned_keywords.append(keyword["word"])
#             elif keyword["entity"].startswith("I-"):
#                 cleaned_keywords[-1] += " " + keyword["word"]
#         keywords = {"keywords": [keyword.replace(" ##", "") for keyword in cleaned_keywords]}
        
#         # pipe = pipeline("ner", model="transformer3/H2-keywordextractor")
#         # keywords = pipe(text)[0]["summary_text"]
#         # keywords = {"keywords": keywords}

#          # Create a word cloud from the keywords
#                 # Return the  keywords as JSON response
#         return jsonify(keywords), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

@analysis_blueprint.route("/extract_keywords", methods=["POST", "GET"])
def extract_keywords():
    try:
        # Check if the 'text' field is present in the form data
        text = request.form.get("text")

        if not text:
            return jsonify({"error": "No text provided."}), 400

        # Create a function to generate the WordCloud and render the image
        def generate_wordcloud(text):
            wordcloud = WordCloud(width=800, height=400, background_color="white")
            wordcloud.generate(text)
            wordcloud_image = wordcloud.to_image()

            # Save the WordCloud image as bytes
            img_byte_array = io.BytesIO()
            wordcloud_image.save(img_byte_array, format='PNG')
            img_bytes = img_byte_array.getvalue()

            # Encode the image as base64
            wordcloud_base64 = base64.b64encode(img_bytes).decode("utf-8")

            # Return the WordCloud image as base64
            return wordcloud_base64

        # Use threading to generate the WordCloud without blocking the main thread
        pipe = pipeline("ner", model="yanekyuk/bert-keyword-extractor")

        keywords = pipe(text)
        cleaned_keywords = []
        # processing output to return just the keywords
        for keyword in keywords:
            if keyword["entity"].startswith("B-"):
                cleaned_keywords.append(keyword["word"])
            elif keyword["entity"].startswith("I-"):
                cleaned_keywords[-1] += " " + keyword["word"]
        wordcloud_base64 = generate_wordcloud(text)
        text = ' '.join([keyword.replace(" ##", "") for keyword in cleaned_keywords])
        keywordcloud_base64 = generate_wordcloud(text)
        wordcloud_template = """
                            <!DOCTYPE html>
                            <html>
                            <head>
                                <title>Word Cloud</title>
                            </head>
                            <body>
                                <img src="data:image/png;base64,{{ word_cloud_image }}" alt="Word Cloud">
                                <img src="data:image/png;base64,{{ keyword_cloud_image }}" alt="Word Cloud">
                            </body>
                            </html>
                            """
        # Return an HTML page with the WordCloud image
        return render_template_string(wordcloud_template, word_cloud_image=wordcloud_base64, keyword_cloud_image=keywordcloud_base64)

    except Exception as e:
        return jsonify({"error": str(e)}), 500