from flask import request, jsonify, Blueprint
from app.text_analyzer import TextAnalyzer

analysis_blueprint = Blueprint("analysis", __name__)

# Initialize the TextAnalyzer
text_analyzer = TextAnalyzer()

@analysis_blueprint.route("/analyze", methods=["POST"])
def analyze_text():
    try:
        # Check if the 'text' field is present in the form data
        text = request.form.get("text")

        if not text:
            return jsonify({"error": "No text provided."}), 400

        analysis_result = text_analyzer.analyze_text(text)
        return jsonify(analysis_result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Create a Flask app and register the analysis_blueprint
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(analysis_blueprint)
    
    app.run(debug=True)
