
from flask import Flask, render_template, request
import sqlite3
import plotly.graph_objects as go

app = Flask(__name__)

def get_songs_results(sort_by,sort_range):
    conn = sqlite3.connect('songs.sqlite')
    cur = conn.cursor()

    if sort_by == 'ranking':
        sort_column = 'Rank'
    elif sort_by == 'track name':
        sort_column = 'Track_Name'
    else:
         sort_column = 'Artist_Name'
    
    if sort_range == 'All':
        sort_range_nm = 100
    elif sort_range == '50':
        sort_range_nm = 50
    elif sort_range == '30':
        sort_range_nm = 30
    elif sort_range == '10':
        sort_range_nm = 10
 

    q = f'''
        SELECT Track_Name, Artist_Name, Rank
        FROM Hits
        ORDER BY {sort_column}
        LIMIT {sort_range_nm}
    '''
    results = cur.execute(q).fetchall()
    conn.close()
    return results

def get_more_results(rank_number):
    conn = sqlite3.connect('songs.sqlite')
    cur = conn.cursor()
    
    q = f'''
        SELECT Track_Name, Artist_Name, Rank
        FROM Hits
        WHERE Artist_Name == (SELECT Artist_Name FROM Hits
                             WHERE RANK == {rank_number})
    '''
    moreresults = cur.execute(q).fetchall()
    conn.close()
    return moreresults

def get_spotify_results(rank_number):
    conn = sqlite3.connect('songs.sqlite')
    cur = conn.cursor()
    
    q = f'''
        SELECT Tracks.artist_name, Tracks.track_name, Tracks.popularity
        FROM Tracks 
        WHERE Tracks.artist_name == (SELECT Artist_Name FROM Hits
                             WHERE RANK == {rank_number})
    '''
    spotifyresults = cur.execute(q).fetchall()
    conn.close()
    return spotifyresults


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/results', methods=['POST'])
def results():
    sort_by = request.form['sort']
    sort_range = request.form['region']
    results = get_songs_results(sort_by, sort_range)
    return render_template('results.html', 
        sort=sort_by, results=results,region= sort_range)

@app.route('/moreresults', methods=['POST'])

def moreresults():
    rank_number = request.form["number"]
    moreresults = get_more_results(rank_number)
    spotifyresults = get_spotify_results(rank_number)
    plot_results = request.form.get('plot', False)
    if (plot_results):
        x_vals = [r[1] for r in spotifyresults]
        y_vals = [r[2] for r in spotifyresults]
        bars_data = go.Bar(
            x=x_vals,
            y=y_vals
        )
        fig = go.Figure(data=bars_data)
        div = fig.to_html(full_html=False)
        return render_template('moreresults.html',number=rank_number, moreresults=moreresults,spotifyresults=spotifyresults,  plot_div=div)
    else:
        return render_template('moreresults.html', 
            number=rank_number, moreresults=moreresults,spotifyresults=spotifyresults)




if __name__ == '__main__':
    app.run(debug=True)