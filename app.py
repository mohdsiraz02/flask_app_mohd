from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# 🔹 Homepage: Display all current reservations
@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM reservations")
    rows = c.fetchall()
    conn.close()
    return render_template("index.html", reservations=rows)

# 🔹 Move Reservations based on input
@app.route('/move', methods=['GET', 'POST'])
def move_records():
    message = ""
    verified_rows = []

    if request.method == 'POST':
        reservation_no = request.form.get('reservation_no')
        date = request.form.get('date')

        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        if reservation_no:
            c.execute("SELECT * FROM reservations WHERE reservation_no = ?", (reservation_no,))
        elif date:
            c.execute("SELECT * FROM reservations WHERE date = ?", (date,))
        else:
            message = "Please provide input."
            return render_template("move.html", message=message)

        records = c.fetchall()

        if not records:
            message = "No matching records found."
        else:
            try:
                for record in records:
                    c.execute("INSERT INTO moved_reservations VALUES (?, ?, ?, ?)", record)
                    c.execute("DELETE FROM reservations WHERE reservation_no = ?", (record[0],))
                conn.commit()
                message = "Relevant data has been moved successfully."
                c.execute("SELECT status FROM moved_reservations")
                verified_rows = [row[0] for row in c.fetchall()]
            except Exception as e:
                message = f"Error while moving: {e}"

        conn.close()

    return render_template("move.html", message=message, verified_rows=verified_rows)

# 🔹 View moved reservations
@app.route('/moved')
def show_moved():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM moved_reservations")
    moved = c.fetchall()
    conn.close()
    return render_template("moved.html", moved=moved)

# 🔹 Add new reservation manually
@app.route('/add', methods=['GET', 'POST'])
def add_reservation():
    message = ""

    if request.method == 'POST':
        reservation_no = request.form.get('reservation_no')
        date = request.form.get('date')
        name = request.form.get('name')
        status = request.form.get('status')

        try:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("INSERT INTO reservations VALUES (?, ?, ?, ?)", 
                      (reservation_no, date, name, status))
            conn.commit()
            message = "Reservation added successfully!"
            conn.close()
        except Exception as e:
            message = f"Error while adding reservation: {e}"

    return render_template("add.html", message=message)

# 🔹 Start Flask app
if __name__ == '__main__':
    app.run(debug=True)