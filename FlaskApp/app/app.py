from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from flask_cors import CORS
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'user'
app.config['MYSQL_DATABASE_PASSWORD'] = 'pass'
app.config['MYSQL_DATABASE_DB'] = 'mydb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


# Set a secret key for encrypting session data
app.secret_key = 'my_secret_key'

# dictionary to store user and password
users = {
    'andy': '1234',
    'user': 'pass'
}

""" API CALLS
"""

@app.route('/api/permissions/global/<int:id_user>', methods=['get'])
def api(id_user):
    if 'id_user' in session:
        return jsonify({"error": "Missing 'name' field", "value": id_user}), 400
    else:
        return jsonify({"error": "Not logged in", "value": id_user}), 400



@app.route('/delete_session')
def delete_session():
    session.pop('id_user', default=None)
    session.pop('username', default=None)
    session.pop('first_name', default=None)

    return render_template('login.html')

# To render a login form
@app.route('/')
def view_form():
    if 'id_user' in session:
        first_name = session['first_name']
        url = url_for("delete_session")
        return f'<h1>{first_name}</h1><a href="{url}">Link Text</a>'
    else:
        return render_template('login.html')




@app.route('/handle_post', methods=['post'])
def handle_post():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)

        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM users WHERE users.username = '{username}' AND users.password = '{password}';")
        data = cursor.fetchone()
        if data:
            session['id_user'] = data[0]
            session['username'] = username
            session['first_name'] = data[3]
            url = url_for("delete_session")
            return f'<h1>Welcome {username} !!!</h1><a href="{url}">Link Text</a>'
        else:
            return '<h1>invalid credentials!</h1>'
    else:
        return render_template('login.html')

if __name__ == '__main__':
    #app.run()
    app.run(debug=True)


"""
200 OK: For successful operations.
400 Bad Request:
401 Unauthorized: When authentication is needed and has failed (e.g., invalid credentials).
403 Forbidden: When the server understands the request but refuses to fulfill it (e.g., user is not logged in).
404 Not Found: When the resource doesn’t exist (e.g., invalid endpoint).
500 Internal Server Error: For unexpected errors on the server.
"""

"""
@app.route('/test')
def test():
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    #print(data)
    return str(data)
"""

"""
@app.route('/handle_get', methods=['GET'])
def handle_get():
    if request.method == 'GET':
        username = request.args['username']
        password = request.args['password']
        print(username, password)
        if username in users and users[username] == password:
            return '<h1>Welcome!!!</h1>'
        else:
            return '<h1>invalid credentials!</h1>'
    else:
        return render_template('login.html')
"""

"""
# For handling post request form we can get the form
# inputs value by using POST attribute.
# this values after submitting you will never see in the urls.
@app.route('/handle_post', methods=['post'])
def handle_post():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        if username in users and users[username] == password:
            session['username'] = username
            url = url_for("delete_session")
            return f'<h1>Welcome!!!</h1><a href="{url}">Link Text</a>'
        else:
            return '<h1>invalid credentials!</h1>'
    else:
        return render_template('login.html')
"""
