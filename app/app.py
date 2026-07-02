from flask import Flask, render_template

app = Flask(__name__)

APP_VERSION = "1.0.0"
ENVIRONMENT = "LOCAL"


@app.route("/")
def home():
    return render_template(
        "login.html",
        version=APP_VERSION,
        environment=ENVIRONMENT
    )


if __name__ == "__main__":
    app.run(debug=True)