from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shift.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Shift(db.Model):
    __tablename__ = 'shift'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shift/monthly', methods=['GET', 'POST'])
def submit_monthly_shift():
    if request.method == 'POST':
        name = request.form['name']
        selected_days = request.form.getlist('shift_days')
        for d in selected_days:
            shift_date = date.fromisoformat(d)
            new_entry = Shift(name=name, date=shift_date.isoformat())
            db.session.add(new_entry)
        db.session.commit()
        return redirect('/')
    today = date.today()
    start_date = today.replace(day=1)
    if start_date.month == 12:
        next_month = start_date.replace(year=start_date.year+1, month=1, day=1)
    else:
        next_month = start_date.replace(month=start_date.month+1, day=1)
    days = []
    while start_date < next_month:
        days.append(start_date.isoformat())
        start_date += timedelta(days=1)
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
