from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/viagens')
def register_travel():
    return render_template('register_travel.html')
@app.route('/usuarios')
def user():
    return render_template('register_user.html')
if __name__ == '__main__':
    app.run(debug=True)
