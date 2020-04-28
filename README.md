# si507_final_project

It is a project about a simple hot song browser application is realized. 

First, the user can view the billboard information of the top 100 billboards, and can choose three different sorting methods: ranking, track name, and artist name. In addition, the number of records displayed is used as a filter for users to choose from. 

Secondly, the second part is to let the user input a ranking number, so as to get other ranked songs of the artists of the ranked songs and popular songs in Spotify. In addition, users can choose to view the plot to more intuitively view the specific popularity index on Spotify about the artist's popular tracks.

The final_proj.py file has three parts: scraping form BillBoard, accessing data from Spotify API through spotipy, creating database and load data into tables.

The cache.json file and the artists.csv file are the files for storaging the data needed for this project.

The templates folder include three html files for interacting.

The app.py file utilizes flask to display the data.
