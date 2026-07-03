from flask import Flask, render_template
import os

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "LOCAL")


@app.route("/")
def home():
    return render_template(
        "login.html",
        version=APP_VERSION,
        environment=ENVIRONMENT
    )


if __name__ == "__main__":
   
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )