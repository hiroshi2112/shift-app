from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shift.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(10), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shift/monthly_submit', methods=['GET', 'POST'])
def monthly_submit():
    today = date.today()
    start_date = date(today.year, today.month, 1)
    next_month = start_date.replace(month=(start_date.month % 12) + 1, day=1)
    days = []
    while start_date < next_month:
        days.append(start_date.isoformat())
        start_date += timedelta(days=1)

    if request.method == 'POST':
        name = request.form['name']
        selected_days = request.form.getlist('days')
        for day in selected_days:
            if not Shift.query.filter_by(name=name, date=day).first():
                shift = Shift(name=name, date=day)
                db.session.add(shift)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('monthly_shift.html', days=days)

@app.route('/shift/view_edit', methods=['GET', 'POST'])
def view_edit_shift():
    shifts = []
    name = ""
    if request.method == 'POST':
        name = request.form['name']
        if request.form['action'] == 'search':
            shifts = Shift.query.filter_by(name=name).order_by(Shift.date).all()
        elif request.form['action'] == 'delete':
            delete_days = request.form.getlist('delete_days')
            for d in delete_days:
                shift = Shift.query.filter_by(name=name, date=d).first()
                if shift:
                    db.session.delete(shift)
            db.session.commit()
            shifts = Shift.query.filter_by(name=name).order_by(Shift.date).all()
    return render_template('view_edit_shift.html', name=name, shifts=shifts)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


