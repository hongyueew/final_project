from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html',
                           page_title = 'Penguins',
                           about_link = '/about',
                           species_link = '/species')

@app.route('/about')
def about():
    return render_template('about.html',
                           page_title = 'About')

species_list = [['Emperor Penguins', 120], ['King Penguins', 90], ['Adelie Penguins', 65], ['Chinstrap Penguins', 72], ['Gentoo Penguins', 82], ['Macaroni Penguins', 70], ['African Penguins', 65]]

@app.route('/species')
def species():
    return render_template('species.html',
                           page_title = 'Species',
                           species_list = species_list)

@app.route('/species/<species_name>/<species_height>')
def specific_species(species_name, species_height):
    return render_template('specific_species.html',
                           species_name = species_name,
                           species_height = species_height)

if __name__ == '__main__':
    app.run(port = 3000, debug=True)