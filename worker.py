# Periodic errand which turns humidifier, light, etc. on and off if it is set to automatic
def run_errand(sensor_data, hum_settings, ip_settings, log_manager, init_run):
    try:
        if init_run:
            log_manager.log_event("info", "Humidifier INIT OFF", "Turning humidifier OFF on init run")
            hum_settings.toggle_humidifier(ip_settings.humidifier_ip, False)
            return
        
        if hum_settings.is_automatic():
            if sensor_data.humidity < hum_settings.range_from and not hum_settings.humidifier_on:
                formatted_message = f"Turning ON. Humidity: {sensor_data.humidity} %, range: {hum_settings.range_from} % - {hum_settings.range_to} %"
                
                log_manager.log_event("info", "Humidifier ON", formatted_message)
                hum_settings.toggle_humidifier(ip_settings.humidifier_ip, True)
            
            elif sensor_data.humidity > hum_settings.range_to and hum_settings.humidifier_on:
                formatted_message = f"Turning OFF. Humidity: {sensor_data.humidity} %, range: {hum_settings.range_from} % - {hum_settings.range_to} %"

                log_manager.log_event("info", "Humidifier OFF", formatted_message)
                hum_settings.toggle_humidifier(ip_settings.humidifier_ip, False)
            
    except Exception as e:
        log_manager.log_event("error", "Humidifier Error", str(e))