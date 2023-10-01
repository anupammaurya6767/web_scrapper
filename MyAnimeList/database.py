import sqlite3
from scraper import MALScraper

# Connect to the SQLite database
conn = sqlite3.connect('anime_database.db')#Add your own database name
cursor = conn.cursor()

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS TopAnime (
        Rank INTEGER PRIMARY KEY,
        AnimeName TEXT,
        Score TEXT,
        Episodes TEXT,
        Duration TEXT,
        Members TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS TopManga (
        Rank INTEGER PRIMARY KEY,
        MangaName TEXT,
        Score TEXT,
        Episodes TEXT,
        Duration TEXT,
        Members TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS SeasonalAnime (
        Title TEXT PRIMARY KEY,
        Episodes TEXT,
        AiringDate TEXT,
        Genres TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS SpecificAnime (
        Title TEXT PRIMARY KEY,
        Episodes TEXT,
        Score TEXT,
        Synopsis TEXT
    )
''')

conn.commit()



# Create an instance of the MALScraper class
base_url = "https://myanimelist.net"
scraper = MALScraper(base_url)

# Function to insert data into respective tables based on user choice
def insert_data(choice):
    if choice == "seasonal":
        year = int(input("Enter year:"))
        season = str(input("Enter season:"))
        seasonal_anime_data = scraper.scrape_seasonal_anime(year, season)
        cursor.executemany("INSERT INTO SeasonalAnime VALUES (?, ?, ?, ?)", seasonal_anime_data)
    elif choice == "top anime":
        top_anime_data = scraper.scrape_top_anime()
        cursor.executemany("INSERT INTO TopAnime VALUES (?, ?, ?, ?, ?, ?)", top_anime_data)
        print(top_anime_data)
    elif choice == "top manga":
        top_manga_data = scraper.scrape_top_manga()
        cursor.executemany("INSERT INTO TopManga VALUES (?, ?, ?, ?, ?, ?)", top_manga_data)
    elif choice == "specific":
        name = str(input("Enter anime name:"))
        specific_anime_data = scraper.scrape_specific_anime(name)
        cursor.executemany("INSERT INTO SpecificAnime VALUES (?, ?, ?, ?)", specific_anime_data)
    else:
        print("Invalid choice.")

    conn.commit()

# Function to display the tables

def display_tables():
    for table in ['TopAnime', 'TopManga', 'SeasonalAnime', 'SpecificAnime']:
        print(f"\nDisplaying {table}:\n")
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        for row in rows:
            print(row)


if __name__ == "__main__":
    print("Available choices: 'seasonal', 'top anime', 'top manga', 'specific'")
    choice = input("Enter your choice: ").lower()

    # Call the function to insert data into tables based on user choice
    insert_data(choice)

    # Call the function to display the tables
    #display_tables()

    # Close the database connection
    conn.close()
