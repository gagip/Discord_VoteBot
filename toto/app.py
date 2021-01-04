from flask import *
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/betting", methods=["POST"])
def betting():
    if request.method == "POST":
        result = request.form
        title = result["title"]
        choice = (result["choice1"], result["choice1"])
        return render_template("result.html", title=title,
                                choice=choice)
    


if __name__ == '__main__':
    app.run()