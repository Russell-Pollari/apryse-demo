import os

from flask import Flask, render_template, request
from dotenv import load_dotenv

from convert import create_pdf_with_annotations

load_dotenv()

app = Flask(__name__, static_url_path="", static_folder="")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", license_key=os.getenv("LICENSE"))


@app.route("/export", methods=["POST"])
def export_annotations():
    annot = request.json.get("xfdfString")
    if annot is not None:
        with open("annotations.xml", "w") as f:
            f.write(annot)

    return "OK"


@app.route("/generate", methods=["POST"])
def generate_pdf():
    create_pdf_with_annotations(
        image_path="test_img.jpeg",
        save_as="test_pdf.pdf",
        annotations_path="annotations.xml",
        use_streaming=True,
    )
    return "OK"


if __name__ == "__main__":
    app.run(debug=True)
