import logging
import logging.config

logging.config.fileConfig("logger/loggingConfig.ini")

# create logger
screen_log = logging.getLogger("root")
main_log = logging.getLogger("smoot_light")
exception_log = logging.getLogger("exception")

#test code -- won't work unless file is imported by a file from the directory above this "logger" directory
#main_log.debug("debug mesage")
#main_log.info("info message")
#main_log.warn("warn message")
#main_log.error("error message")
#main_log.critical("critical message")
#exception_log.critical("hi")
#screen_log.error("whoa")

