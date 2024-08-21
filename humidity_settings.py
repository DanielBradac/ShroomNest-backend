import requests

# mode - "auto"/"manual"/"period"
# auto - automatic humidifier setting according to current humidity and set humidity range
# manual - manual humidifier toggle
# period - periodic turning on and off

# range_from - low end of desired humidity in C
# range_to - high end of desired humidity in C
# wait_per - time between every toggle of humidifier in period mode, in seconds
# run_per - for how long should the humidifier be toggled on in period mode, in seconds
# humidifier_on - is the humidifier currently on?

class HumiditySettings:    
    def __init__(self, range_from: float, range_to: float, wait_per: int, run_per: int, mode: String, humidifier_on: Boolean):
        self.validate(range_from, range_to, wait_per, run_per, mode)
        
        self.range_from = range_from
        self.range_to = range_to
        self.wait_per = wait_per
        self.run_per = run_per
        self.mode = mode
        self.humidifier_on = humidifier_on
        
        self.last_humidity = 0
        self.reset_periodic_timers()
    
    def validate(self, range_from: float, range_to: float, wait_per: int, run_per: int, mode: String):
        if range_from < 0 or range_to > 100:
            raise ValueError("range_from must be in interval <0;100>")
        if range_to < 0 or range_to > 100:
            raise ValueError("range_to must be in interval <0;100>")
        if range_from >= range_to:
            raise ValueError("range_from must be lower than range_to")
        if wait_per < 0:
            raise ValueError("wait_per must be a positive number")
        if run_per < 0:
            raise ValueError("run_per must be a positive number")
        if mode != "auto" and mode != "manual" and mode != "period":
            raise ValueError("mode must be 'manual', 'auto' or 'period'")
    
    def serialize(self):
        return {
            "rangeFrom": self.range_from,
            "rangeTo": self.range_to,
            "waitPer": self.wait_per,
            "runPer": self.run_per,
            "mode": self.mode,
            "humidifierOn": self.humidifier_on,
            "runTime": self.run_time,
            "waitTime": self.wait_time
        }
    
    def update_from_json(self, json: String, humidifier_ip: String, log_manager):
        range_from = self.range_from
        range_to = self.range_to
        mode = self.mode
        humidifier_on = self.humidifier_on
        wait_per = self.wait_per
        run_per = self.run_per
        
        if "rangeFrom" in json:
            range_from = json["rangeFrom"]
        if "rangeTo" in json:
            range_to = json["rangeTo"]
        if "mode" in json:
            mode = json["mode"]
        if "humidifierOn" in json:
            humidifier_on = json["humidifierOn"]
        if "waitPer" in json:
            wait_per = json["waitPer"]
        if "runPer" in json:
            run_per = json["runPer"]
            
        self.validate(range_from, range_to, wait_per, run_per, mode)
        
        self.range_from = range_from
        self.range_to = range_to
        self.mode = mode
        self.wait_per = wait_per
        self.run_per = run_per
        
        if (self.is_manual()):
            on_off = "ON" if humidifier_on else "OFF"
            log_manager.log_event("info", f"MANUAL: Switching humidifier {on_off}", f"Manual toggle {on_off}")
            self.toggle_humidifier(humidifier_ip, humidifier_on, log_manager)
            
        if (not self.is_periodic()):
            self.reset_periodic_timers()
    
    def is_automatic(self):
        return self.mode == "auto"
    
    def is_manual(self):
        return self.mode == "manual"
    
    def is_periodic(self):
        return self.mode == "period"
    
    def reset_periodic_timers(self):
        self.wait_time = 0
        self.run_time = 0
    
    def toggle_humidifier(self, humidifier_ip: String, on: Boolean, log_manager):
        url = f"http://{humidifier_ip}/cm?cmnd=Power%20{'On' if on else 'Off'}"
        try:
            response = requests.post(url)
        except Exception as e:
            raise Exception(f"Unable to toggle humidifier, error: {str(e)}")
            
        if response.status_code != 200:
            raise Exception(f"Unable to toggle humidifier, status code: {response.status_code}, raw response: {response.text}")
        
        resp_json = response.json()
        if "POWER" in resp_json:
            if on and resp_json["POWER"] == "ON":
                self.humidifier_on = True
            elif not on and resp_json["POWER"] == "OFF":
                self.humidifier_on = False
            else:
                raise Exception(f"Unable to toggle humidifier: invalid response in correlation to toggle setting (on = {on}), raw response: {response.text}")
            log_manager.log_event("info", "Humidifier TOGGLE DONE", f"Humidifier switched {"ON" if on else "OFF"}")
            return
        
        raise Exception(f"Unable to toggle humidifier: invalid response, raw response: {response.text}")
