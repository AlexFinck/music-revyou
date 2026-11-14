# Music RevYou

*Music reviews, from you.*

Music RevYou is a web application where users can share album reviews, rate music and discover albums reviewed by other users.

## Planned Features

- Users can create an account and log in to the application.

- Users can create album reviews containing the album title, artist, release year, a numerical rating (1–10) and a written review. Users can also edit and delete their own reviews.

- Users can view album reviews created by themselves and other users.

- Users can search for album reviews using criteria such as album title, artist, genre, language and release year. The search includes reviews from all users.

- The application has user profile pages displaying each user's album reviews and statistics, such as the total number of reviews and average rating.

- Users can classify the albums they review by genre and language. The available classification options are defined in the database, and users can select multiple options for each classification.

- Users can comment on album reviews created by themselves or other users. Comments are displayed alongside the corresponding reviews.

## Implemented Features

- Users can create an account and log in to the application.

- Logged-in users can create album reviews containing an album title, artist, release year, numerical rating (1–10) and written review.

- Users can view album reviews created by themselves and other users.

- Users can edit and delete reviews they have created.

- Users can search for album reviews by album title or artist.


## Installation Instructions

**Prerequisites:** Python 3, pip, Python venv, Git and SQLite3 must be installed before following these instructions. These instructions are intended for Ubuntu/Linux.

1. **Clone the repository**

   Begin by cloning the remote GitHub repository:

   `git clone https://github.com/AlexFinck/music-revyou.git`

2. **Navigate to the project directory**

   `cd music-revyou`

3. **Create a Python virtual environment**

   Create a virtual environment to keep the project's Python packages separate from other projects:

   `python3 -m venv venv`

4. **Activate the virtual environment**

   `source venv/bin/activate`

5. **Install Flask**

   Install the Flask library inside the virtual environment:

   `pip install flask`

6. **Initialize the SQLite database**

   Create the database and initialize its tables by executing the SQL statements in `schema.sql`:

   `sqlite3 database.db < schema.sql`

   This step should be performed when setting up a new database.

7. **Start the application**

   Start the Flask development server:

   `flask run`
   
8. **Open and test the application**

   Open your web browser and navigate to the address displayed in the terminal after running flask run.

   You can now test the application's functionality by creating an account, logging in, adding album reviews, viewing reviews, editing or deleting your own reviews, and searching for reviews by album title or artist.

   To stop the server, press `Ctrl+C` in the terminal.

   





