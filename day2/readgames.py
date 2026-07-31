from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Read the CSV once when the app starts
df = pd.read_csv('day2/games.csv')

@app.route('/')
def home():
    games_list = df.to_dict('records')
    return render_template('games.html', games=games_list, title='All Games')

@app.route('/genre/<genre_name>')
def by_genre(genre_name):
    # Filter the DataFrame for this genre
    filtered = df[df['genre'] == genre_name]
    games_list = filtered.to_dict('records')

    return render_template('games.html',
                         games=games_list,
                         title=f'{genre_name} Games')

@app.route('/top-rated')
def top_rated():
    # Filter for games with rating >= 9.3
    filtered = df[df['rating'] >= 9.3]
    # Sort by rating, descending
    filtered = filtered.sort_values('rating', ascending=False)
    games_list = filtered.to_dict('records')

    return render_template('games.html',
                         games=games_list,
                         title='Top Rated Games (9.3+)')

@app.route('/stats')
def stats():
    # Calculate various statistics
    total_games = len(df)
    average_rating = df['rating'].mean()
    highest_rated = df.loc[df['rating'].idxmax()]
    games_by_genre = df['genre'].value_counts().to_dict()

    # Convert to a format the template can use
    genre_counts = [{'genre': k, 'count': v} for k, v in games_by_genre.items()]

    return render_template('stats.html',
                         total_games=total_games,
                         average_rating=average_rating,
                         highest_rated=highest_rated.to_dict(),
                         genre_counts=genre_counts)

@app.route('/merge')
def merge():
    

if __name__ == '__main__':
    app.run(debug=True)