import requests
from bs4 import BeautifulSoup

class MALScraper:
    def __init__(self, url):
        self.url = url

    def scrape_top_anime(self):
        response = requests.get(f"{self.url}/topanime.php")

        if response.status_code != 200:
            print("Failed to retrieve anime data.")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        anime_entries = soup.find_all("tr", class_="ranking-list")

        anime_data = []
        for anime_entry in anime_entries:
            rank = anime_entry.select_one("td span.lightLink").text.strip()
            name = anime_entry.select_one("td div.detail h3 a").text.strip()
            score = anime_entry.select_one("td span.text.on.score-label").text.strip()
            infos = [info.text.strip() for info in anime_entry.select("td div.detail div.information")]
            split_info = infos[0].split('\n')
            cleaned_parts = [part.strip() for part in split_info]

            anime_info = (
                rank,
                name,
                score,
                cleaned_parts[0],
                cleaned_parts[1],
                cleaned_parts[2]
            )
            anime_data.append(anime_info)

        return anime_data

    def scrape_top_manga(self):
        response = requests.get(f"{self.url}/topmanga.php")

        if response.status_code != 200:
            print("Failed to retrieve manga data.")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        manga_entries = soup.find_all("tr", class_="ranking-list")

        manga_data = []
        for manga_entry in manga_entries:
            rank = manga_entry.select_one("td span.lightLink").text.strip()
            name = manga_entry.select_one("td div.detail h3 a").text.strip()
            score = manga_entry.select_one("td span.text.on.score-label").text.strip()
            infos = [info.text.strip() for info in manga_entry.select("td div.detail div.information")]
            split_info = infos[0].split('\n')
            cleaned_parts = [part.strip() for part in split_info]

            manga_info = (
                rank,
                name,
                score,
                cleaned_parts[0],
                cleaned_parts[1],
                cleaned_parts[2]
            )
            manga_data.append(manga_info)

        return manga_data

    def scrape_seasonal_anime(self, year, season):
        url = f"{self.url}/anime/season/{year}/{season.lower()}"
        response = requests.get(url)

        if response.status_code != 200:
            print("Failed to retrieve seasonal anime data.")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        anime_entries = soup.find_all("div", class_="seasonal-anime")

        seasonal_anime_data = []
        for anime_entry in anime_entries:
            title = anime_entry.find("span", class_="js-title").text.strip()
            episodes = anime_entry.select_one("div div.prodsrc div.info span.item span").text.strip()
            airing = anime_entry.select_one("div div.prodsrc div.info span.item").text.strip()
            span_elements = anime_entry.find_all('span', class_="genre")
            genre_list = [span.get_text() for span in span_elements]
            cleaned_genres = ', '.join(genre.strip() for genre in genre_list)  

            anime_info = (
                title,
                episodes,
                airing,
                cleaned_genres
            )
            seasonal_anime_data.append(anime_info)

        return seasonal_anime_data

    def scrape_specific_anime(self, anime_name):
        anime_url = f"{self.url}/anime.php?q={anime_name}"
        response = requests.get(anime_url)

        if response.status_code != 200:
            print("Failed to retrieve specific anime data.")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        anime_info = soup.find("div", class_="js-categories-seasonal js-block-list list")
        rows = anime_info.find_all('tr')

        specific_anime_data = []
        for row in rows[1:2]:
            title = row.select_one("td div.title a strong").text.strip()
            episodes = anime_info.find("td", class_="borderClass ac bgColor0", width="40").text.strip()
            score = anime_info.find("td", class_="borderClass ac bgColor0", width="50").text.strip()
            synopsis = anime_info.find("div", class_="pt4").text.strip()

            anime_info = (
                title,
                episodes,
                score,
                synopsis
            )
            specific_anime_data.append(anime_info)

        return specific_anime_data
