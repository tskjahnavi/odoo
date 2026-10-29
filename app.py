from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="hospital"
)

cursor = db.cursor()

# HOME
@app.route('/')
def home():
    cursor.execute("SELECT COUNT(*) FROM patients")
    count = cursor.fetchone()[0]
    return render_template('index.html', count=count)

# ADD PAGE
@app.route('/add')
def add():
    return render_template('add.html')

# SAVE
@app.route('/save', methods=['POST'])
def save():
    name = request.form['name']
    age = request.form['age']
    disease = request.form['disease']
    medicine = request.form['medicine']
    doctor = request.form['doctor']

    cursor.execute(
        "INSERT INTO patients(name, age, disease, medicine, doctor) VALUES(%s,%s,%s,%s,%s)",
        (name, age, disease, medicine, doctor)
    )
    db.commit()

    return redirect(url_for('home'))

# VIEW
@app.route('/view')
def view():
    sort = request.args.get('sort')

    if sort == 'name':
        cursor.execute("SELECT * FROM patients ORDER BY name")
    elif sort == 'age':
        cursor.execute("SELECT * FROM patients ORDER BY age")
    else:
        cursor.execute("SELECT * FROM patients")

    data = cursor.fetchall()
    return render_template('view.html', patients=data)

# DELETE
@app.route('/delete/<int:id>')
def delete(id):
    cursor.execute("DELETE FROM patients WHERE id=%s", (id,))
    db.commit()
    return redirect(url_for('view'))

# EDIT
@app.route('/edit/<int:id>')
def edit(id):
    cursor.execute("SELECT * FROM patients WHERE id=%s", (id,))
    data = cursor.fetchone()
    return render_template('edit.html', patient=data)

# UPDATE
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    name = request.form['name']
    age = request.form['age']
    disease = request.form['disease']
    medicine = request.form['medicine']
    doctor = request.form['doctor']

    cursor.execute(
        "UPDATE patients SET name=%s, age=%s, disease=%s, medicine=%s, doctor=%s WHERE id=%s",
        (name, age, disease, medicine, doctor, id)
    )
    db.commit()

    return redirect(url_for('view'))

# SEARCH
@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']

    cursor.execute(
        "SELECT * FROM patients WHERE name LIKE %s OR disease LIKE %s",
        ('%' + keyword + '%', '%' + keyword + '%')
    )
    data = cursor.fetchall()

    return render_template('view.html', patients=data)

app.run(debug=True)