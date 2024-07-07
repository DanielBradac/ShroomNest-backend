class IPSettings:
    def __init__(self, humidifier_ip: String = "192.168.0.130"):
        self.humidifier_ip = humidifier_ip
    
    def serialize(self):
        return {
            "humidifierIp": self.humidifier_ip
        }
    
    def update_from_json(self, json: String):
        if "humidifierIp" in json:
            self.humidifier_ip = json["humidifierIp"]