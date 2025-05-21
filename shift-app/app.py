from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    date = db.Column(db.String(20))

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    status = db.Column(db.String(20))
    reason = db.Column(db.String(200))
    date = db.Column(db.String(20), default=datetime.today().strftime('%Y-%m-%d'))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/shift", methods=["GET", "POST"])
def shift():
    if request.method == "POST":
        name = request.form["name"]
        date = request.form["date"]
        db.session.add(Shift(name=name, date=date))
        db.session.commit()
        return redirect("/")
    return render_template("shift_form.html")

@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        name = request.form["name"]
        status = request.form["status"]
        reason = request.form.get("reason", "")
        db.session.add(Report(name=name, status=status, reason=reason))
        db.session.commit()
        return redirect("/")
    return render_template("report_form.html")

@app.route("/admin")
def admin():
    shifts = Shift.query.all()
    reports = Report.query.filter_by(date=datetime.today().strftime('%Y-%m-%d')).all()
    return render_template("admin_view.html", shifts=shifts, reports=reports)

if __name__ == "__main__":
    app.run(debug=True)
