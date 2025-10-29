import os
from flask import Flask, Response
import psycopg2

app = Flask(__name__)

@app.route('/')
def index():
    host=os.getenv('DB_HOST')
    dbname=os.getenv('DB_NAME')
    user=os.getenv('DB_USER')
    password=os.getenv('DB_PASS')

    conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password,options="-c search_path=public")
    cur = conn.cursor()
    cur.execute("SELECT * FROM cs2_skins WHERE id=1;")

    rows = cur.fetchall()

    # Get column names
    colnames = [desc[0] for desc in cur.description]

    # Filter out 'id' column
    filtered_cols = [i for i, col in enumerate(colnames) if col != 'id']

    # Format each row as a string without the id
    lines = [" | ".join(f"{colnames[i]}: {row[i]}" for i in filtered_cols) for row in rows]

    cur.close()
    conn.close()

    return Response("\n".join(lines), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
