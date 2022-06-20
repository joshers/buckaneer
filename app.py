from flask import Flask, render_template, request
import sqlite3
import datetime

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('/data/database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/', methods=['GET', 'POST'])
def display_transactions():
    if request.method == 'POST':
        if request.form.get('amount'):
            amount = request.form.get('amount')
            desc = request.form.get('description')
            amount = float(amount) * 100
            updatesql = get_db_connection()
            balance = updatesql.execute('SELECT currentbal FROM data WHERE id = 1').fetchone()[0]
            balance = balance - int(amount)
            updatesql.execute('UPDATE data SET currentbal = ? WHERE id = ?', (balance, 1))
            updatesql.execute('INSERT INTO transactions (detail, amount) VALUES (?, ?)', (desc, amount))
            updatesql.commit()
            updatesql.close()
        elif request.form.get('budget'):
            newbudget = request.form.get('budget')
            newrate = request.form.get('rate')
            newbudget = float(newbudget) * 100
            newrate = float(newrate) * 100
            updatesql = get_db_connection()
            updatesql.execute('UPDATE data SET currentbal = ? WHERE id = ?', (newbudget, 1))
            updatesql.execute('UPDATE data SET rate = ? WHERE id = ?', (newrate, 1))
            updatesql.commit()
            updatesql.close()

    conn = get_db_connection()
    transactions = conn.execute('SELECT * FROM transactions ORDER BY id DESC LIMIT 5').fetchall()
    currentbal = conn.execute('SELECT currentbal FROM data WHERE id = 1').fetchone()[0]
    currentrate = conn.execute('SELECT rate FROM data WHERE id = 1').fetchone()[0]
    lastupdate = conn.execute('SELECT lastupdate FROM data WHERE id = 1').fetchone()[0]
    f = '%Y-%m-%d %H:%M:%S'
    lastup = datetime.datetime.strptime(lastupdate, f)
    now = datetime.datetime.now()
    delta = now.date() - lastup.date()
    days = delta.days
    if days > 0:
        newbal = currentbal + (currentrate * days)
        newupdate = now.strftime(f)
        conn.execute('UPDATE data SET currentbal = ? WHERE id = ?', (newbal, 1))
        conn.execute('UPDATE data SET lastupdate = ? WHERE id = ?', (newupdate, 1))
        conn.commit()
        currentbal = conn.execute('SELECT currentbal FROM data WHERE id = 1').fetchone()[0]
    conn.close()
    return render_template('index.html', transactions=transactions, currentbal=currentbal, currentrate=currentrate)


if __name__ == '__main__':
    app.run()
