from flask import Flask, render_template, send_from_directory


app = Flask(__name__, template_folder="")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/experience")
def experience():
    return render_template("experience.html")


@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/education")
def education():
    return render_template("education.html")


@app.route("/assets/<path:path>")
def send_assets(path):
    return send_from_directory("assets", path)


if __name__ == "__main__":
    app.run(host="localhost", port=8080)
