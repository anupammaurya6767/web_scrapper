const axios = require('axios');
const cheerio = require('cheerio');

function linkToGet(link) {
    // This function will get the URL of the image & book download direct link using the given link for book download
    return axios.get(link)
        .then(response => {
            const thHtml = cheerio.load(response.data);
            const tdAll = thHtml('td#info');
            const tdA = tdAll.find('a');
            const linkHref = tdA.eq(1).attr('href');
            const imgLinkTd = tdAll.find('img[alt="cover"]');
            const imgLinkSrc = imgLinkTd.attr('src');
            const imgLink = `http://library.lol${imgLinkSrc}`;
            return [linkHref, imgLink];
        })
        .catch(error => {
            console.error('Error in linkToGet:', error);
            throw error;
        });
}

class LibGen {
    constructor() {
        // Constructor for LibGen class (if needed)
    }

    async getBooks(bookName) {
        try {
            const Books = [];
            const results = 10;
            const mainres = 25;

            if (!bookName || bookName.length < 3) {
                throw new Error('Title Too Short');
            }

            bookName = bookName.replace(/ /g, '+');
            const url = `http://libgen.is/search.php?req=${bookName}&lg_topic=libgen&open=0&view=simple&res=${mainres}&phrase=1&column=def`;

            const response = await axios.get(url);
            const $ = cheerio.load(response.data);

            if ($('body').text().includes('Search string must contain minimum 3 characters..')) {
                throw new Error('Title Too Short');
            }

            const table = $('table').eq(2);
            const tableRows = table.find('tr');
            const objKeys = ["name", "author", "size", "format", "link", "language"];

            for (let i = 1, counter = 1; i < tableRows.length && counter <= results; i++) {
                const row = tableRows.eq(i);
                const tableDatas = row.find('td');
                const bookName = tableDatas.eq(2).text();
                const author = tableDatas.eq(1).text();
                const link = tableDatas.eq(9).find('a').attr('href');
                const [linkHref, imgLink] = await linkToGet(link);
                const language = tableDatas.eq(6).text();
                const size = tableDatas.eq(7).text();
                const typeOfIt = tableDatas.eq(8).text();

                if ((typeOfIt !== 'pdf' && typeOfIt !== 'epub') || language !== 'English') {
                    continue;
                }

                const book = {
                    name: bookName,
                    author: author,
                    size: size,
                    format: typeOfIt,
                    link: linkHref,
                    language: imgLink
                };

                Books.push(book);
                counter++;
            }

            if (Books.length >= 1) {
                return Books;
            } else {
                throw new Error('No results found');
            }
        } catch (error) {
            console.error('Error in getBooks:', error.message);
            throw error.message;
        }
    }
}

// Usage
const libGenScraper = new LibGen();
const bookName = "Python"; // Replace with the desired book name
libGenScraper.getBooks(bookName)
    .then(bookData => {
        if (Array.isArray(bookData)) {
            bookData.forEach(book => {
                console.log("Name:", book.name);
                console.log("Author:", book.author);
                console.log("Size:", book.size);
                console.log("Format:", book.format);
                console.log("Link:", book.link);
                console.log("Language:", book.language);
                console.log();
            });
        } else {
            console.error("Error:", bookData);
        }
    })
    .catch(error => {
        console.error("Unknown error occurred:", error);
    });
