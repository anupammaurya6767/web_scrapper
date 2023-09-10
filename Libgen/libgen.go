package main

import (
	"errors"
	"fmt"
	"log"
	"net/http"
	"strings"

	"github.com/PuerkitoBio/goquery"
)

func linkToGet(link string) ([2]string, error) {
	res, err := http.Get(link)
	if err != nil {
		return [2]string{}, err
	}
	defer res.Body.Close()

	if res.StatusCode != 200 {
		return [2]string{}, errors.New("Request failed with status: " + res.Status)
	}

	doc, err := goquery.NewDocumentFromReader(res.Body)
	if err != nil {
		return [2]string{}, err
	}

	linkHref, _ := doc.Find("td#info a:eq(1)").Attr("href")
	imgLinkSrc, _ := doc.Find("td#info img[alt=cover]").Attr("src")
	imgLink := "http://library.lol" + imgLinkSrc

	return [2]string{linkHref, imgLink}, nil
}

type Book struct {
	Name     string `json:"name"`
	Author   string `json:"author"`
	Size     string `json:"size"`
	Format   string `json:"format"`
	Link     string `json:"link"`
	Language string `json:"language"`
}

type LibGen struct{}

func (lg *LibGen) getBooks(bookName string) ([]Book, error) {
	const results = 10
	const mainres = 25

	if bookName == "" || len(bookName) < 3 {
		return nil, errors.New("Title Too Short")
	}

	bookName = strings.ReplaceAll(bookName, " ", "+")
	url := fmt.Sprintf("http://libgen.is/search.php?req=%s&lg_topic=libgen&open=0&view=simple&res=%d&phrase=1&column=def", bookName, mainres)

	res, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer res.Body.Close()

	if res.StatusCode != 200 {
		return nil, errors.New("Request failed with status: " + res.Status)
	}

	doc, err := goquery.NewDocumentFromReader(res.Body)
	if err != nil {
		return nil, err
	}

	if strings.Contains(doc.Text(), "Search string must contain minimum 3 characters..") {
		return nil, errors.New("Title Too Short")
	}

	var Books []Book
	objKeys := []string{"name", "author", "size", "format", "link", "language"}

	table := doc.Find("table").Eq(2)
	tableRows := table.Find("tr")
	for i := 1; i < tableRows.Length() && len(Books) < results; i++ {
		row := tableRows.Eq(i)
		tableDatas := row.Find("td")
		bookName := tableDatas.Eq(2).Text()
		author := tableDatas.Eq(1).Text()
		link, _ := tableDatas.Eq(9).Find("a").Attr("href")
		linkInfo, err := linkToGet(link)
		if err != nil {
			log.Println("Error in linkToGet:", err)
			continue
		}
		language := tableDatas.Eq(6).Text()
		size := tableDatas.Eq(7).Text()
		typeOfIt := tableDatas.Eq(8).Text()

		if (typeOfIt != "pdf" && typeOfIt != "epub") || language != "English" {
			continue
		}

		book := Book{
			Name:     bookName,
			Author:   author,
			Size:     size,
			Format:   typeOfIt,
			Link:     linkInfo[0],
			Language: linkInfo[1],
		}

		Books = append(Books, book)
	}

	if len(Books) >= 1 {
		return Books, nil
	} else {
		return nil, errors.New("No results found")
	}
}

func main() {
	libGenScraper := &LibGen{}
	bookName := "Python" // Replace with the desired book name
	bookData, err := libGenScraper.getBooks(bookName)
	if err != nil {
		log.Println("Error:", err)
		return
	}

	for _, book := range bookData {
		fmt.Println("Name:", book.Name)
		fmt.Println("Author:", book.Author)
		fmt.Println("Size:", book.Size)
		fmt.Println("Format:", book.Format)
		fmt.Println("Link:", book.Link)
		fmt.Println("Language:", book.Language)
		fmt.Println()
	}
}
