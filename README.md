## Apryse PDF generator

Minimum working example for testing Apryse PDF generation with annotations on client and server.

## The issue

Downloading the PDF (with annotations) from the webviewer and generating a PDF with the Python SDK produce different outputs.

- This may only be an issue on MacOS...


## Setup

0. Initialise a virtual environment

`python3 -m venv venv && source venv/bin/activate`

1. Install python requirements

`pip install -r requirements.txt`

2. Create env variable with apryse license

`touch .env && echo "LICENSE=<key>" >> .env`

3. Run flask application

`python server.py`

OR in docker container

`docker build -t pdf-test . && docker run -p 8000:8000 pdf-test`


## Usage

1. Open browser to `http://127.0.0.1:8000/` to interact with Apryse webviwer.
This loads and displays`./test_img.jpeg`

2. Add some annotations and click `Export Annotations`.
This will save the xfdf sting of the annotations to `./annotations.xml`

3. Click `Generate PDF` .
This will convert `./test_img.jpeg` and add `./annotations.xml` using the Apryse Python SDKs. Result is saved in `output.pdf`

4. Click Download PDF to view the generated pdf



## Directory structure

```
├── templates
│   └── index.html    # HTML and javascript for WebViewer UI
├── .gitignore
├── annotations.xml   # Exported annotations
├── convert.py        # Logic to convert image to PDF with annotations
├── Dockerfile
├── output.pdf        # Generated PDF
├── README.md
├── requirements.txt
├── server.py         # Flask server
└── test_img.jpeg     # Test image
```