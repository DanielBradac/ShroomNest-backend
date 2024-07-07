import time

from utils import local_time_formatted

# How many log messages can there be in a single list - we don't have RAM to spare
MAX_LOG_SIZE = 20
# if the worker reports this amout of out of water calls, we log it
MAX_OUT_OF_WATER_CALLS = 5

class LogManager:
    info: List[LogMessage] = []
    warning: List[LogMessage] = []
    error: List[LogMessage] = []
    out_of_water_calls = 0
    
    def report_out_of_water(self, last_humidity, new_humidity):
        if (self.out_of_water_calls < MAX_OUT_OF_WATER_CALLS):
            self.out_of_water_calls += 1
            
        if (self.out_of_water_calls == MAX_OUT_OF_WATER_CALLS):
            formatted_message = f"Humidifier might be out of water. Humidity last errand: {last_humidity} %, now: {new_humidity} %"
            self.log_event("warning", "Humidifier out of water", formatted_message)
            # We will wait until the log purge or reset - one out of water message is enough
            self.out_of_water_calls += 1

    def reset_out_of_water_calls(self):
        self.out_of_water_calls = 0
    
    def purge_logs(self):
        self.info: List[LogMessage] = []
        self.warning = []
        self.error = []
        self.out_of_water_calls = 0
    
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
        
        self.timestamp = local_time_formatted()
        
    def serialize(self):
        return {
            "timestamp": self.timestamp,
            "header": self.header,
            "message": self.message
        }
        
        
