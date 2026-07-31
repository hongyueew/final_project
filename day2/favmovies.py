from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/movie_form', methods=['GET', 'POST'])
def movie_form():
    if request.method == 'POST':
        # Process the form
        movies = [
            request.form.get('movie1'),
            request.form.get('movie2'),
            request.form.get('movie3')
        ]
        return render_template('results.html', movies=movies)
    else:
        # Display the form
        return render_template('movie_form.html')

if __name__ == '__main__':
    app.run(debug=True)
