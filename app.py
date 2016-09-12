import sqlite3 as lite

from flask import Flask

app = Flask(__name__)
con = lite.connect("sex.db", check_same_thread=False)


@app.route("/sex/<string:act>/increment/<int:amount>")
def increment(act, amount):
    with con:
        cur = con.cursor()
        cur.execute("""
            UPDATE sex SET amount = amount + ? WHERE act = ?;
        """, [amount, act])
    print("INCREMENTING BY", amount)
    return "Count incremented by {0} {1}".format(amount, act)

@app.route("/sex/<string:act>/decrement/<int:amount>")
def decrement(act, amount):
    with con:
        cur = con.cursor()
        cur.execute("""
            UPDATE sex SET amount = amount + ? WHERE act = ?;
        """, [amount, act])
    return "Count decremented by {0} {1}".format(amount, act)

if __name__ == "__main__":
    with con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sex (act text, amount integer);
        """)
        cur.execute("""
            INSERT INTO sex(act, amount)
                SELECT 'complete', '1'
                    WHERE NOT EXISTS(
                        SELECT 'complete' FROM sex
                            WHERE act = 'complete');
        """)
    app.run(debug=True, threaded=True, host="0.0.0.0", port=1024)
