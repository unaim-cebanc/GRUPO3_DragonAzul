from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "ABCD"

@app.route("/")
def home():
    session.clear()
    return render_template("index.html")

def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()