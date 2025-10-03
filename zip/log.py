import logging 

class ScraperLog:
    def __init__(self, scraper_name: str):
        logging.basicConfig(
            filename=f'{scraper_name}.log',
            level=logging.DEBUG,
            format='%(asctime)s - %(message)s',
            datefmt='%d-%b-%y %H:%M:%S' 
        )
        self.logger = logging.getLogger(scraper_name)

    def info(self, *args, **kwargs):
        return self.logger.info(*args, **kwargs)