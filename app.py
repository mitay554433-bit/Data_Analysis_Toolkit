import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>Data Analysis Toolkit</title>
        <style>
            body {
                background:#0b1220;
                color:#fff;
                font-family:Arial;
                text-align:center;
                padding-top:80px;
            }
            h1 {font-size:42px;}
            p {opacity:.7;}
        </style>
    </head>
    <body>
        <h1>🚀 Data Analysis Toolkit</h1>
        <p>Live AI System Active</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
