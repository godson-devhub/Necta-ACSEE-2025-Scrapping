import logging

log = logging.getLogger("necta")
log.setLevel(logging.INFO)
log.propagate = False
log.handlers.clear()

class _PrintHandler(logging.Handler):
    def emit(self, record):
        try:
            print(self.format(record))
        except:
            pass

fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

ph = _PrintHandler()
ph.setFormatter(fmt)
log.addHandler(ph)

fh = logging.FileHandler("logs/necta_scraper.log", encoding="utf-8")
fh.setFormatter(fmt)
log.addHandler(fh)