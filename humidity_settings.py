import requests

# mode - "auto"/"manual"
class HumiditySettings:    
    def __init__(self, range_from: float, range_to: float, mode: String, humidifier_on: Boolean):
        self.validate(range_from, range_to, mode)
        
        self.range_from = range_from
        self.range_to = range_to
        self.mode = mode
        self.humidifier_on = humidifier_on
        
    def validate(self, range_from: float, range_to: float, mode: String):
        if range_from < 0 or range_to > 100:
            raise ValueError("range_from must be in interval <0;100>")
        if range_to < 0 or range_to > 100:
            raise ValueError("range_to must be in interval <0;100>")
        if range_from >= range_to:
            raise ValueError("range_from must be lower than range_to")
        if mode != "auto" and mode != "manual":
            raise ValueError("mode must be 'manual' or 'auto'")
    
    def serialize(self):
        return {
            "rangeFrom": self.range_from,
            "rangeTo": self.range_to,
            "mode": self.mode,
            "humidifierOn": self.humidifier_on
        }
    
    def update_from_json(self, json: String, humidifier_ip: String):
        range_from = self.range_from
        range_to = self.range_to
        mode = self.mode
        humidifier_on = self.humidifier_on
        
        if "range_from" in json:
            range_from = json["rangeFrom"]
        if "range_to" in json:
            range_to = json["rangeTo"]
        if "mode" in json:
            mode = json["mode"]
        if "humidifier_on" in json:
            humidifier_on = json["humidifierOn"]
            
        self.validate(range_from, range_to, mode)
        
        self.range_from = range_from
        self.range_to = range_to
        self.mode = mode
        
        if (not self.is_automatic()):
            self.toggle_humidifier(humidifier_ip, humidifier_on) 
    
    def is_automatic(self):
        return self.mode == "auto"
    
    def toggle_humidifier(self, humidifier_ip: String, on: Boolean):
        url = "http://" + humidifier_ip + "/cm?cmnd=Power%20" + ("On" if on else "Off")
        
        response = requests.post(url)
        if response.status_code != 200:
            raise Exception("Unable to toggle humidifier, status code: " + response.status_code + ", raw response: " + response.text)
        
        resp_json = response.json()
        if "POWER" in resp_json:
            if on and resp_json["POWER"] == "ON":
                self.humidifier_on = True
                return
            if not on and resp_json["POWER"] == "OFF":
                self.humidifier_on = False
                return
            raise Exception("Unable to toggle humidifier: invalid response in correlation to toggle setting (on = " + on +"), raw response: " + response.text)
            
        else:
            raise Exception("Unable to toggle humidifier: invalid response, raw response: " + response.text)
        
        
        


