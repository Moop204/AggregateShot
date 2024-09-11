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
        "https://www.ritzcinemas.com.au/now-showing/monday",
        "https://www.ritzcinemas.com.au/now-showing/tuesday",
        "https://www.ritzcinemas.com.au/now-showing/wednesday",
        "https://www.ritzcinemas.com.au/now-showing/thursday",
        "https://www.ritzcinemas.com.au/now-showing/friday",
    ]

    def parse(self, response):
        """
        This function is the callback used by the Scrapy Spider to
        scrape the relevant data from the Ritz Cinemas website.

        It yields a dictionary for each film, with the title of the film,
        the day of the week, and the screenings for that film on that day.
        """
        FILM_SELECTOR = ".Movie"
        DAY_SELECTOR = ".swiper-slide .Selected::text"
        for film_block in response.css(FILM_SELECTOR):
            film_details = film_block.css(".Wrapper")
            # Select the title of the film in the href attribute
            TITLE_SELECTOR = ".Title a::text"
            screenings = film_block.css(".Tickets .Sessions .Time::text").getall()

            yield {
                "title": filterTitle(film_details.css(TITLE_SELECTOR).extract_first()),
                "day": response.css(DAY_SELECTOR).extract_first(),
                "screenings": list(map(regularTimeToStandard, screenings)),
            }
