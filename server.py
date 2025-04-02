import os
from flask import Flask, send_from_directory

app = Flask(__name__, static_folder="webapp", static_url_path="")

@app.route("/")
def index():
    return send_from_directory("webapp", "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Берём порт из окружения или 10000 по умолчанию
    app.run(host="0.0.0.0", port=port)