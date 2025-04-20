from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/play", methods=["POST"])
def play():
    mode = request.form.get("mode")
    if mode == "human_vs_human":
        subprocess.Popen(["python", "game.py", "human_vs_human"])
    elif mode == "human_vs_ai":
        subprocess.Popen(["python", "game.py", "human_vs_ai"])
    return "Game started. Check the Pygame window."

if __name__ == "__main__":
    app.run(debug=True)
