from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html',
                           page_title = 'My Dashboard',
                           username = 'Alice',
                           message_count = 0,
                           foods = ['pizza', 'pasta', 'ice cream'])

@app.route('/about')
def about():
    return "<h1>About Me</h1><p>I'm learning Flask!</p>"

@app.route('/greet/<name>')
def greet(name):
    return f"<h1>Hello, {name}!</h1>"

@app.route('/square/<int:number>')
def square(number):
    result = number ** 2
    return f"<h1>The square of {number} is {result}</h1>"

@app.route('/welcome')
def welcome():
    return "<h1>Welcome to this website!</h1><p>Feel free to explore</p>"

@app.route('/projects')
def projects():
    return "<h1>My Favourite Projects!</h1><ul><li>Movie</li><li>Book</li><li>Music</li></ul>"

@app.route('/projects/<project_name>')
def project_details(project_name):
    return f"<h1>Information about {project_name} project</h1>"

@app.route('/add/<int:a>/<int:b>')
def add_numbers(a, b):
    return f"<h1>The sum of {a} and {b} is {a+b}</h1>"

favourites_db = {
    'alice': ['Inception', 'The Matrix', 'Interstellar'],
    'bob': ['Star Wars', 'LOTR', 'The Avengers', 'Dune', 'Blade Runner', 'Arrival']
}

@app.route('/favourites/<name>')
def favourites(name):
    return render_template('favourites.html',
                           name = name,
                           favourites_db = favourites_db)

@app.route('/random')
def random_page():
    number = random.randint(1, 10)
    if number > 5:
        return "<h1>You got a high number!</h1>"
    else:
        return "<h1>You got a low number</h1>"

if __name__ == '__main__':
    app.run(port = 3000, debug=True)