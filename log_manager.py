from utils import local_time_formatted

# How many log messages can there be in a single list - we don't have RAM to spare
MAX_LOG_SIZE = 100

class LogManager:
    info: List[LogMessage] = []
    warning: List[LogMessage] = []
    error: List[LogMessage] = []
    out_of_water_calls = 0
    
    def purge_logs(self):
        self.info: List[LogMessage] = []
        self.warning = []
        self.error = []
        self.out_of_water_calls = 0
    
    def add_message(self, list: List[LogMessage], message: LogMessage):
        if (len(list) >= MAX_LOG_SIZE):
            list.pop(0)
        list.append(message)
        
    def log_event(self, category: str, header: str, message: str):
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
    def __init__(self, header: str, message: str):
        self.header = header
        self.message = message
        
        self.timestamp = local_time_formatted()
        
    def serialize(self):
        return {
            "timestamp": self.timestamp,
            "header": self.header,
            "message": self.message
        }
        
        
