"""Create a uniform logger & prevent duplicate loggers of the same name to be created
Loggers must be imported first(before other impor[has to do with subImports incorrectly setting up lower level loggers first]) 
otherwise the logger file name may be incorrect"""
import logging
import os

class Logger(object):
    logger = ""
    
    @staticmethod
    def getLogger(__file_, loggerOutput = 's', logLvl = logging.DEBUG, logMode = "w"):
        """logger output s = stream only, f = file only, (else:*) b = both"""
        if Logger.logger == "":
            logName = str(os.path.basename(__file_))
            logName = logName.replace(".py", "")
            
            Logger.logger = logging.getLogger(logName)
            Logger.logger.setLevel(logLvl)
            
            formatter = logging.Formatter("[%(asctime)s] [%(module)20s.py] [%(funcName)20s] [%(levelname)7s%(lineno)4s]: %(message)s", 
                                          datefmt="%Y-%b-%d %H:%M:%S") # %H:%M:%S
            fileHandler = logging.FileHandler(logName + ".log", mode = logMode)
            fileHandler.setFormatter(formatter)
            
            streamHandler = logging.StreamHandler()
            streamHandler.setFormatter(formatter)
        
            if loggerOutput == 's':
                Logger.logger.addHandler(streamHandler)
            elif loggerOutput == 'f':
                Logger.logger.addHandler(fileHandler)
            else:
                Logger.logger.addHandler(fileHandler)
                Logger.logger.addHandler(streamHandler)
            
            Logger.logger.info("=======================================")
            Logger.logger.info("New Log Entry into log: " + logName)
            Logger.logger.info("=======================================")
        return Logger.logger

if __name__ == "__main__":
    logger = Logger.getLogger(__file__, 's', logging.DEBUG, "a")
    logger = Logger.getLogger(__file__, 's', logging.DEBUG, "a") #trying to create a seccond logger of the same type (Shouldnt be created)
    logger.debug("Testing logger setup")
    print("done")