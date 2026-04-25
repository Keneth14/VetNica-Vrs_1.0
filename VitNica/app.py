from flask import Flask, render_template, request, redirect, flash
from db import get_connection

app = Flask(__name__)
app.secret_key = "vetnica123"


# ======================
# INICIO
# ======================
@app.route('/')
def inicio():
    return render_template("index.html")


# ======================
# ANIMALES
# ======================
@app.route('/animals')
def animals():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM animals")
    data = cursor.fetchall()

    conn.close()
    return render_template("animals.html", animals=data)


@app.route('/add_animal', methods=['POST'])
def add_animal():
    name = request.form['name']
    type_ = request.form['type']
    age = request.form['age']
    age_type = request.form['age_type']
    owner = request.form['owner']

    if age_type not in ['Años', 'Meses']:
        flash("Tipo de edad inválido", "error")
        return redirect('/animals')

    try:
        age = int(age)
        if age < 0:
            flash("Edad inválida", "error")
            return redirect('/animals')
    except:
        flash("Edad inválida", "error")
        return redirect('/animals')

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO animals (name, type, age, age_type, owner)
        VALUES (?, ?, ?, ?, ?)
    """, (name, type_, age, age_type, owner))

    conn.commit()
    conn.close()

    flash("Animal registrado correctamente", "success")
    return redirect('/animals')


# ======================
# RECORDS
# ======================
@app.route('/records')
def records():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT r.id, a.name AS animal_name, r.record_type, r.description, r.date
        FROM records r
        INNER JOIN animals a ON r.animal_id = a.id
        ORDER BY r.id DESC
    """)

    data = cursor.fetchall()
    conn.close()

    return render_template("records.html", records=data)


@app.route('/add_record', methods=['POST'])
def add_record():
    animal_id = request.form['animal_id']
    record_type = request.form['record_type']
    description = request.form['description']

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO records (animal_id, record_type, description)
        VALUES (?, ?, ?)
    """, (animal_id, record_type, description))

    conn.commit()
    conn.close()

    return redirect('/records')


# ======================
# ALERTAS
# ======================
@app.route('/alerts')
def alerts():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT a.id, an.name, a.message, a.alert_date, a.status
        FROM alerts a
        INNER JOIN animals an ON a.animal_id = an.id
        ORDER BY a.id DESC
    """)

    data = cursor.fetchall()
    conn.close()

    return render_template("alerts.html", alerts=data)


# ======================
# FACTURAS
# ======================
@app.route('/invoices')
def invoices():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, client_name, animal_id, description, price, date
        FROM invoices
        ORDER BY id DESC
    """)

    data = cursor.fetchall()
    conn.close()

    return render_template("invoices.html", invoices=data)


@app.route('/add_invoice', methods=['POST'])
def add_invoice():
    client_name = request.form['client_name']
    animal_id = request.form['animal_id']
    description = request.form['description']
    price = request.form['price']

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO invoices (client_name, animal_id, description, price)
        VALUES (?, ?, ?, ?)
    """, (client_name, animal_id, description, price))

    conn.commit()
    conn.close()

    return redirect('/invoices')


# ======================
# TICKET FACTURA (IMPRIMIR)
# ======================
@app.route('/invoice_ticket/<int:id>')
def invoice_ticket(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT i.id, i.client_name, i.description, i.price, i.date,
               a.name AS animal_name
        FROM invoices i
        LEFT JOIN animals a ON i.animal_id = a.id
        WHERE i.id = ?
    """, (id,))

    data = cursor.fetchone()
    conn.close()

    return render_template("invoice_ticket.html", invoice=data)

@app.route('/db_status')
def db_status():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()

        status = "Conectado"
        color = "green"

    except:
        status = "Desconectado"
        color = "red"

    return render_template("db_status.html", status=status, color=color)

# ======================
# RUN (SIEMPRE AL FINAL)
# ======================
if __name__ == '__main__':
    app.run(debug=True)