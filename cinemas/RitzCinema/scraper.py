import scrapy


def regularTimeToStandard(time):
    [time, amOrPm] = time.split(" ")
    [hour, minute] = time.split(":")
    if amOrPm == "PM":
        hour = int(hour) + 12
    return f"{hour}:{minute}"


def filterTitle(title):
    if "(" in title:
        bracket_index = title.index("(")
        if title[bracket_index + 1 : bracket_index + 5].isdigit():
            title = title[: title.index(")") + 1]
        else:
            title = title[: title.index("(")]
    return title


class RitzSpider(scrapy.Spider):
    name = "ritz-spider"
    start_urls = [
        "https://www.ritzcinemas.com.au/now-showing/Monday",
        "https://www.ritzcinemas.com.au/now-showing/Tuesday",
        "https://www.ritzcinemas.com.au/now-showing/Wednesday",
        "https://www.ritzcinemas.com.au/now-showing/Thursday",
        "https://www.ritzcinemas.com.au/now-showing/Friday",
    ]

    def parse(self, response):
        """
        This function is the callback used by the Scrapy Spider to
        scrape the relevant data from the Ritz Cinemas website.

        It yields a dictionary for each film, with the title of the film,
        the day of the week, and the screenings for that film on that day.
        """
        FILM_SELECTOR = ".Movie"
        for film_block in response.css(FILM_SELECTOR):
            film_details = film_block.css(".Wrapper")
            # Select the title of the film in the href attribute
            TITLE_SELECTOR = ".Title a::text"
            screenings = film_block.css(".Tickets .Sessions .Time::text").getall()

            yield {
                "title": filterTitle(film_details.css(TITLE_SELECTOR).extract_first()),
                "day": response.request.url.split("/")[-1],
                "screenings": list(map(regularTimeToStandard, screenings)),
            }
