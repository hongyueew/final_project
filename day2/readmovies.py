from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

df = pd.read_csv('day2/movies.csv')

@app.route('/')
def home():
    movie_list = df.to_dict('records')
    return render_template('movies.html', movies = movie_list, title = 'All Movies')

@app.route('/runtime/<runtime_threshold>')
def runtime(runtime_threshold):
    runtime_threshold = int(runtime_threshold)
    filtered = df[df['runtime']>runtime_threshold]
    filtered = filtered.sort_values('runtime')
    movies_list = filtered.to_dict('records')

    return render_template('movies.html',
                           movies = movies_list,
                           title = f'Movies With Minimum Runtime {runtime_threshold}')

@app.route('/stats')
def stats():
    total_movies = len(df)
    average_runtime = df['runtime'].mean()
    longest_movie = df.loc[df['runtime'].idxmax()]

    return render_template('moviestats.html',
                           total_movies = total_movies,
                           average_runtime = average_runtime,
                           longest_movie = (longest_movie['title'], longest_movie['runtime']))

if __name__ == '__main__':
    app.run(debug=True)