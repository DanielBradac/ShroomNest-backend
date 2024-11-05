class IPSettings:
    def __init__(self, humidifier_ip: str = "192.168.1.180", fan_ip: str = "192.168.1.181"):
        self.humidifier_ip = humidifier_ip
        self.fan_ip = fan_ip
    
    def serialize(self):
        return {
            "humidifierIp": self.humidifier_ip,
            "fanIp": self.fan_ip
        }
    
    def update_from_json(self, json: str):
        if "humidifierIp" in json:
            self.humidifier_ip = json["humidifierIp"]
        if "fanIp" in json:
            self.fan_ip = json["fanIp"]