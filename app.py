
from flask import Flask
from routes.routes import register_risk_routes

app = Flask(__name__)

from flask import render_template

@app.route("/")
def home():
    return render_template("index.html")


register_risk_routes(app)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
