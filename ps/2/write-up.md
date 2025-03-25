# write-up

For this assignment I decided to scrape <https://quotes.toscrape.com/>.
I began by exploring the site in my browser's debugger view and taking
note of HTML elements of interest and the URL format of pages. After a
bit of exploration, I realized that each page of the site had the format
of `https://quotes.toscrape.com/page/{page}/`, where `{page}` is a
positive integer. I also noticed that all quotes were `div`s with the
`quote` class.

## Scraping

To scrape the site I wrote up a quick loop to iterate over a specified
amount of pages. I used the [`requests`] library to pull each of the
pages of the site along with the [`beautifulsoup4`] library to parse
each of the HTML tags. I also added support to stop scraping once I've
exhausted pages with quotes as the site successfully returns empty pages
past a certain index. Once scraped, I dumped my constructed database to
a JSON file consisting of a list of dictionaries with keys for the
author of the quote, the quote itself, and any tags associated with the
quote.

## Querying

To query the database, I loaded the JSON file into memory and simply
compared query authors and tags to all entries. If a user specifies both
authors and tags, then the query will only include quotes that satisfy
both.

### "Interesting" Queries

```
$ ./query.py --authors 'Mark Twain'
[
    {
        "author": "Mark Twain",
        "text": "Good friends, good books, and a sleepy conscience: this is the ideal life.",
        "tags": [
            "books",
            "contentment",
            "friends",
            "friendship",
            "life"
        ]
    },
    {
        "author": "Mark Twain",
        "text": "I have never let my schooling interfere with my education.",
        "tags": [
            "education"
        ]
    },
    {
        "author": "Mark Twain",
        "text": "\u2032Classic\u2032 - a book which people praise and don't read.",
        "tags": [
            "books",
            "classic",
            "reading"
        ]
    },
    {
        "author": "Mark Twain",
        "text": "The fear of death follows from the fear of life. A man who lives fully is prepared to die at any time.",
        "tags": [
            "death",
            "life"
        ]
    },
    {
        "author": "Mark Twain",
        "text": "A lie can travel half way around the world while the truth is putting on its shoes.",
        "tags": [
            "misattributed-mark--tagswain",
            "truth"
        ]
    },
    {
        "author": "Mark Twain",
        "text": "Never tell the truth to people who are not worthy of it.",
        "tags": [
            "truth"
        ]
    }
]
```

```
$ ./query.py --tags truth
[
    {
        "author": "George Carlin",
        "text": "The reason I talk to myself is because I\u2019m the only one whose answers I accept.",
        "tags": [
            "humor",
            "insanity",
            "lies",
            "lying",
            "self-indulgence",
            "truth"
        ]
    },
    {
        "author": "Mark Twain",
        "text": "A lie can travel half way around the world while the truth is putting on its shoes.",
        "tags": [
            "misattributed-mark--tagswain",
            "truth"
        ]
    },
    {
        "author": "J.K. Rowling",
        "text": "The truth.\" Dumbledore sighed. \"It is a beautiful and terrible thing, and should therefore be treated with great caution.",
        "tags": [
            "truth"
        ]
    },
    {
        "author": "Mark Twain",
        "text": "Never tell the truth to people who are not worthy of it.",
        "tags": [
            "truth"
        ]
    }
]
```

```
$ ./query.py --authors 'Albert Einstein' --tags mistakes
[
    {
        "author": "Albert Einstein",
        "text": "Anyone who has never made a mistake has never tried anything new.",
        "tags": [
            "mistakes"
        ]
    }
]
```

[`beautifulsoup4`]: https://pypi.org/project/beautifulsoup4/
[`requests`]: https://pypi.org/project/requests/
