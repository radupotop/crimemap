class BaseScraper():

    def __init__(self):
        if not self.type:
            raise NotImplementedError('Scraper should have a type property')
        if not self.scrape:
            raise NotImplementedError('Scraper should have a scrape method')
