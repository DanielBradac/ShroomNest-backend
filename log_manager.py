import time

# How many log messages can there be in a single list - we don't have RAM to spare
MAX_LOG_SIZE = 10

class LogManager:
    info: List[LogMessage] = []
    warning: List[LogMessage] = []
    error: List[LogMessage] = []
        
    def purge_logs(self):
        self.info: List[LogMessage] = []
        self.warning = []
        self.error = []
    
    def add_message(self, list: List[LogMessage], message: LogMessage):
        if (len(list) >= MAX_LOG_SIZE):
            list.pop(0)
        list.append(message)
        
    def log_event(self, category: String, header: String, message: String):
        if (category == "info"):
            self.add_message(self.info, LogMessage(header, message))
        elif (category == "warning"):
            self.add_message(self.warning, LogMessage(header, message))
        else:
            self.add_message(self.error, LogMessage(header, message))
    
    def serialize(self):
        return {
            "info": list(map(LogMessage.serialize, self.info)),
            "warning": list(map(LogMessage.serialize, self.warning)),
            "error": list(map(LogMessage.serialize, self.error)),
        }

class LogMessage:
    def __init__(self, header: String, message: String):
        self.header = header
        self.message = message
        
        lt = time.localtime()
        self.timestamp = f"{lt[0]:04}-{lt[1]:02}-{lt[2]:02} {lt[3]:02}:{lt[4]:02}:{lt[5]:02}"
        
    def serialize(self):
        return {
            "timestamp": self.timestamp,
            "header": self.header,
            "message": self.message
        }
        
        
