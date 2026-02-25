import os
from flask import Flask, request, render_template, render_template_string
from safehtml import parse_and_serialize, ParseError

app = Flask(__name__)

FLAG = os.environ.get("FLAG", "flag{test_flag}")
app.config["FLAG"] = FLAG


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", prefill="", error=None, output=None)


@app.route("/render", methods=["POST"])
def render():
    doc = request.form.get("doc", "")
    try:
        serialized = parse_and_serialize(doc)
    except ParseError as e:
        return str(e), 400
    except Exception:
        return "Parse error.", 400

    try:
        output = render_template_string(serialized)
    except Exception:
        return "Render error.", 400

    return output, 200, {"Content-Type": "text/plain; charset=utf-8"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)