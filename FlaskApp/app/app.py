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

""" API CALLS
"""

@app.route('/api/permissions/global/<int:id_user>', methods=['get'])
def global_premissions(id_user):
    if 'id_user' in session:
        conn = mysql.connect()
        cursor = conn.cursor()

        gPremission = session['global_premission'];
        cursor.execute(f"SELECT modify_users FROM global_premissions WHERE id_premission_level={gPremission}")
        if cursor.fetchone()[0] == True:
            cursor.execute(f"SELECT * FROM global_premissions WHERE id_premission_level={id_user}")
            res = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            return res, 200
        return jsonify({"error": "User has no premission to see global premissions for other users", "value": -1}), 401
    else:
        return jsonify({"error": "Not logged in", "value": id_user}), 403

"""
@app.route('/api/permissions/group/<int:id_user>/<int:id_group>', methods=['get'])
def api(id_user, id_group):
    if 'id_user' in session:
"""

@app.route('/api/create_group/<string:group_name>', methods=['get'])
def create_group(group_name):
    if 'id_user' in session:
        conn = mysql.connect()
        cursor = conn.cursor()

        id_user = session['id_user']

        gPremission = session['global_premission'];
        cursor.execute(f"SELECT add_group FROM global_premissions WHERE id_premission_level={gPremission}")
        res = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        if res[0]['add_group']:
            cursor.execute(f'INSERT INTO group_data(group_name, creation_date) VALUES("{group_name}", now() );')
            cursor.execute(f'INSERT INTO group_premissions VALUES( DEFAULT, {id_user}, LAST_INSERT_ID(), "CREATOR", 1, 1, 1, 1, 1, 1, 1, 1);')
            conn.commit()
            return jsonify({"Info": "Group is created", "value": group_name}), 200
        return jsonify({"error": "You dont have premission to create groups", "value": -1}), 401

    return jsonify({"error": "Not logged in", "value": -1}), 403


@app.route('/api/group_list', methods=['get'])
def group_list():
    if 'id_user' in session:
        conn = mysql.connect()
        cursor = conn.cursor()

        id_user = session['id_user']
        cursor.execute(f'''SELECT group_data.id_group, group_premissions.id_user, group_premissions.role_name, group_data.group_name, group_data.creation_date
                       FROM group_data CROSS JOIN group_premissions ON group_data.id_group=group_premissions.id_group
                       WHERE id_user={id_user}
                       ''')
        res = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        return jsonify(res), 200;
    return jsonify({"error": "Not logged in", "value": -1}), 403

@app.route('/api/group_remove/<int:id_group>', methods=['get'])
def group_remove(id_group):
    if 'id_user' in session:
        conn = mysql.connect()
        cursor = conn.cursor()
        id_user = session['id_user']

        globalPremissionDelete = None;
        groupPremissionDelete = None;

        gPremission = session['global_premission'];
        cursor.execute(f"SELECT remove_group FROM global_premissions WHERE id_premission_level={gPremission}")
        res = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        globalPremissionDelete = res[0]['remove_group']

        if cursor.execute(f"SELECT remove_group from group_premissions where id_user={id_user} AND id_group={id_group}"):
            res = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            groupPremissionDelete = res[0]['remove_group']

        if globalPremissionDelete or groupPremissionDelete:
            cursor.execute(f"SELECT group_name FROM group_data WHERE id_group={id_group}")
            groupName = cursor.fetchone()[0]
            cursor.execute(f"DELETE FROM group_premissions WHERE id_group={id_group}")
            cursor.execute(f"DELETE FROM group_data WHERE id_group={id_group}")
            conn.commit()
            return jsonify({"Info": "Group deleted", "value": groupName}), 200


        return jsonify({"error": "Group doesn't exist or you dont have premission", "value": -1}), 200
    return jsonify({"error": "Not logged in", "value": -1}), 403


@app.route('/delete_session')
def delete_session():
    session.pop('id_user', default=None)
    session.pop('username', default=None)
    session.pop('first_name', default=None)
    session.pop('last_name', default=None)
    session.pop('global_premission', default=None)
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


@app.route('/login_post', methods=['post'])
def login_post():
    data = request.json
    print(data)
    username = data['username']
    password = data['password']

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM users WHERE users.username = '{username}' AND users.password = '{password}';")
    data = cursor.fetchone()
    if data:
        session['id_user'] = data[0]
        session['username'] = username
        session['first_name'] = data[3]
        session['last_name'] = data[4]
        session['global_premission'] = data[9]
        return jsonify({"Info": "You logged in", "value": username}), 200
    else:
        return jsonify({"error": "Wrong username or password", "value": -1}), 401

@app.route('/handle_post', methods=['post'])
def handle_post():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #print(username, password)

        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM users WHERE users.username = '{username}' AND users.password = '{password}';")
        data = cursor.fetchone()
        if data:
            session['id_user'] = data[0]
            session['username'] = username
            session['first_name'] = data[3]
            session['last_name'] = data[4]
            session['global_premission'] = data[9]
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
