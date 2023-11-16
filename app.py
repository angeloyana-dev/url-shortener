import os, validators
from dotenv import load_dotenv
from flask import Flask, render_template, request, url_for, redirect, session, flash, abort
from URLDatabaseManager import URLDatabaseManager

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Webpage
@app.route('/')
def index():
    shortened_url = session.pop("shortened_url", None)
    return render_template(
        "index.html",
        shortened_url=shortened_url,
        server_url=request.url_root
    )
    
# URL redirection route
@app.route("/<string:url_name>")
def url_redirection(url_name):
    try:
        db = URLDatabaseManager()
        url_info = db.findone(url_name)
        if url_info is None: abort(404)
        return redirect(url_info[2])
    finally: db.close()
    
# URL shortener route
@app.post("/shortener")
def url_shortener():
    try:
        db = URLDatabaseManager()
        url_name = request.form["url-name"]
        long_url = request.form["long-url"]
        if db.findone(url_name) is None:
            if not validators.url(long_url):
                flash("Invalid long url!")
                return redirect(url_for("index"))
            
            db.insertone(url_name, long_url)
            session["shortened_url"] = f"{request.url_root}{url_name}"
            return redirect(url_for("index"))
        else:
            flash("URL name is already in use")
            return redirect(url_for("index"))
    except Exception as e:
        print(f"Error: {str(e)}")
        flash("Internal Server Error")
        return redirect(url_for("index"))
    finally: db.close()
    
if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST") or "0.0.0.0",
        port=os.getenv("PORT") or 5000,
        debug=True if os.getenv("PRODUCTION") in [None, "False"] else False
    )