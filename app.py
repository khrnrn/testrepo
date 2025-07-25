from flask import Flask, render_template, request, redirect, url_for
import re

app = Flask(__name__)

def is_xss(input_str):
    xss_patterns = [r"<.*?>", r"script", r"alert", r"on\w+="]
    return any(re.search(pattern, input_str, re.IGNORECASE) for pattern in xss_patterns)

def is_sqli(input_str):
    sqli_patterns = [r"(\bor\b|\band\b)\s+\d+=\d+", r"('|--|#|;)", r"union.*select", r"drop\s+table"]
    return any(re.search(pattern, input_str, re.IGNORECASE) for pattern in sqli_patterns)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        term = request.form.get("search_term", "")
        if is_xss(term) or is_sqli(term):
            return render_template("home.html", term="", error="Invalid input detected.")
        return redirect(url_for("result", term=term))
    return render_template("home.html", term="", error="")

@app.route("/result")
def result():
    term = request.args.get("term", "")
    return render_template("result.html", term=term)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000) 