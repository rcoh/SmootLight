from logging import Formatter

class UTF8LogFormatter(Formatter):
    def format(self, record):
        try:
            return Formatter.format(self, record)
        except Exception, e:
            return Formatter.format(self, record).encode('utf8')
