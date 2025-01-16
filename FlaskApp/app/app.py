from flask import Flask, render_template, request, redirect, session, url_for
from flask_cors import CORS

app = Flask(__name__)


# Set a secret key for encrypting session data
app.secret_key = 'my_secret_key'

# dictionary to store user and password
users = {
    'andy': '1234',
    'user': 'pass'
}

@app.route('/delete_session')
def delete_session():
    session.pop('username', default=None)
    return render_template('login.html')

# To render a login form
@app.route('/')
def view_form():
    if 'username' in session:
        user = session['username']
        url = url_for("delete_session")
        return f'<h1>{user}</h1><a href="{url}">Link Text</a>'
    else:
        return render_template('login.html')


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

if __name__ == '__main__':
    #app.run()
    app.run(debug=True)


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


