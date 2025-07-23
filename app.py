from flask import Flask, render_template, request, flash, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for flash messages

# 🔹 Home route → redirects to form page
@app.route('/')
def home():
    return redirect(url_for('add_reservation'))

# 🔹 Route to view all reservations
@app.route('/view')
def view_reservations():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM reservations")
    rows = c.fetchall()
    conn.close()
    return render_template("view.html", reservations=rows)

# 🔹 Route to delete a reservation
@app.route('/delete/<reservation_no>', methods=['POST'])
def delete_reservation(reservation_no):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("DELETE FROM reservations WHERE reservation_no = ?", (reservation_no,))
        conn.commit()
        conn.close()
        flash("Reservation deleted successfully!")
    except Exception as e:
        flash(f"Error while deleting reservation: {e}")
    return redirect(url_for('view_reservations'))

# 🔹 Route to add a new reservation
@app.route('/add', methods=['GET', 'POST'])
def add_reservation():
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
            conn.close()

            flash("Reservation added successfully!")
            return redirect(url_for('view_reservations'))
        except Exception as e:
            flash(f"Error while adding reservation: {e}")
            return redirect(url_for('add_reservation'))

    return render_template("add.html")

# 🔹 Start Flask server
if __name__ == '__main__':
    app.run(debug=True)
