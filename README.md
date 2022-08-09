# bato_to_scraper
Python web scraper using BeautifulSoup that downloads images from the bato.to manga site.
Images are sorted by chapter and numbered to allow for manga from your computer instead of
their site.

## Usage

```bash
bato_io_scraper.py -n <name> -l <link> -c <chapter> [-o]

# -n is the name of the series
# -l is the full path to the series
# -c is the chapter to start scraping at
# -o overwrites any existing files with the same names
```

