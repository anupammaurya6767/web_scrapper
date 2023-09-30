import requests
from bs4 import BeautifulSoup
import json
import logging

class Book:
    def __init__(self, name, author,format, link):
        self.name = name
        self.author = author
        self.format = format
        self.link = link

class LibGen:
    def get_books(self, book_name):
        results = 10
        mainres = 25

        if not book_name or len(book_name) < 3:
            raise ValueError("Title Too Short")

        book_name = book_name.replace(" ", "+")
        url = f"http://libgen.is/search.php?req={book_name}&lg_topic=libgen&open=0&view=simple&res={25}&phrase=1&column=def"

        try:
            res = requests.get(url)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')

            if "Search string must contain minimum 3 characters.." in soup.get_text():
                raise ValueError("Title Too Short")

            Books = []
            books_name = []
            table = soup.find_all("table")[2]
            table_rows = table.find_all("tr")[1:]

            for i, row in enumerate(table_rows):
                if len(Books) >= results:
                    break

                table_datas = row.find_all("td")
                book_name = table_datas[2].get_text()

                author = table_datas[1].get_text()
                link1 = table_datas[9].find("a",href = True)
                language = table_datas[6].get_text()
                type_of_it = table_datas[8].get_text()

                if (type_of_it != "pdf" and type_of_it != "epub") or language != "English":
                    continue

                book = Book(
                    name=book_name,
                    author=author,
                    format=type_of_it,
                    # link=link_info[0]
                    link = link1.get("href")
                )

                Books.append(book)

            if len(Books) >= 1:
                return Books
            else:
                raise ValueError("No results found")

        except Exception as e:
            raise ValueError(f"Error: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    libgen_scraper = LibGen()
    book_name = input("enter book name: ")
    BOOKS_DETAILS = []



    book_data = libgen_scraper.get_books(book_name)
    for book in book_data:
        BOOKS_DETAILS.append([book.name,book.author,book.format,book.link])

    for num in range(len(BOOKS_DETAILS)):
        print(num,BOOKS_DETAILS[num][0])

    which_book = int(input("which book do you want(enter the number): "))


    print("Name:", BOOKS_DETAILS[which_book][0])
    print("Author:", BOOKS_DETAILS[which_book][1])
    print("Format:", BOOKS_DETAILS[which_book][2])
    print("Link:", BOOKS_DETAILS[which_book][3])
    print()



