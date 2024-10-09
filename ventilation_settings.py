import requests

# mode - "manual"/"period"
# manual - manual fan toggle
# period - periodic turning on and off

# wait_per - time between every toggle of fan in period mode, in seconds
# run_per - for how long should the fan be toggled on in period mode, in seconds
# fan_on - is the fan currently on?

class VentilationSettings:    
    def __init__(self, wait_per: int, run_per: int, mode: String, fan_on: Boolean):
        self.validate(wait_per, run_per, mode)
        
        self.wait_per = wait_per
        self.run_per = run_per
        self.mode = mode
        self.fan_on = fan_on
        
        self.reset_periodic_timers()
    
    def validate(self, wait_per: int, run_per: int, mode: String):
        if wait_per < 0:
            raise ValueError("wait_per must be a positive number")
        if run_per < 0:
            raise ValueError("run_per must be a positive number")
        if mode != "manual" and mode != "period":
            raise ValueError("mode must be 'manual' or 'period'")
    
    def serialize(self):
        return {
            "waitPer": self.wait_per,
            "runPer": self.run_per,
            "mode": self.mode,
            "fanOn": self.fan_on,
            "runTime": self.run_time,
            "waitTime": self.wait_time
        }
    
    def update_from_json(self, json: String, fan_ip: String, log_manager):
        mode = self.mode
        fan_on = self.fan_on
        wait_per = self.wait_per
        run_per = self.run_per
        
        if "mode" in json:
            mode = json["mode"]
        if "fanOn" in json:
            fan_on = json["fanOn"]
        if "waitPer" in json:
            wait_per = json["waitPer"]
        if "runPer" in json:
            run_per = json["runPer"]
            
        self.validate(wait_per, run_per, mode)
        self.mode = mode
        self.wait_per = wait_per
        self.run_per = run_per
        
        if (self.is_manual()):
            on_off = "ON" if fan_on else "OFF"
            log_manager.log_event("info", f"Fan - MANUAL", f"Manual toggle {on_off}")
            self.toggle_fan(fan_ip, fan_on, log_manager)
            
        if (not self.is_periodic()):
            self.reset_periodic_timers()
    
    def is_manual(self):
        return self.mode == "manual"
    
    def is_periodic(self):
        return self.mode == "period"
    
    def reset_periodic_timers(self):
        self.wait_time = 0
        self.run_time = 0
    
    def toggle_fan(self, fan_ip: String, on: Boolean, log_manager):
        url = f"http://{fan_ip}/cm?cmnd=Power%20{'On' if on else 'Off'}"
        try:
            response = requests.post(url)
        except Exception as e:
            raise Exception(f"Unable to toggle fan, error: {str(e)}")
            
        if response.status_code != 200:
            raise Exception(f"Unable to toggle fan, status code: {response.status_code}, raw response: {response.text}")
        
        resp_json = response.json()
        if "POWER" in resp_json:
            if on and resp_json["POWER"] == "ON":
                self.fan_on = True
            elif not on and resp_json["POWER"] == "OFF":
                self.fan_on = False
            else:
                raise Exception(f"Unable to toggle fan: invalid response in correlation to toggle setting (on = {on}), raw response: {response.text}")
            log_manager.log_event("info", "Fan TOGGLE DONE", f"Fan switched {"ON" if on else "OFF"}")
            return
        
        raise Exception(f"Unable to toggle fan: invalid response, raw response: {response.text}")
