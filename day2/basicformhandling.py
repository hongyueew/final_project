from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Access form data
    name = request.form['name']
    fav_colour = request.form['fav_colour']
    age = request.form['age']

    return f"<h1>Hello, {name}!</h1><p>Your favourite colour is {fav_colour} and you are {age} years old</p>"

if __name__ == '__main__':
    app.run(debug=True)