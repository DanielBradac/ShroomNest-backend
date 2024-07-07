# Periodic errand which turns humidifier, light, etc. on and off if it is set to automatic
def run_errand(sensor_data, hum_settings, ip_settings, log_manager, init_run):
    try:      
        if init_run:
            on_off = "ON" if hum_settings.humidifier_on else "OFF"
            log_manager.log_event("info", f"INIT: Humidifier {on_off}", f"Turning humidifier {on_off} on init run")
            hum_settings.toggle_humidifier(ip_settings.humidifier_ip, hum_settings.humidifier_on)
            return
        
        if (hum_settings.humidifier_on and hum_settings.last_humidity != 0):
            # Humidity hasn't got up and the humidifier is on? Maybe it is out of water
            if (sensor_data.humidity < 90 and hum_settings.last_humidity >= sensor_data.humidity):
                log_manager.report_out_of_water(hum_settings.last_humidity, sensor_data.humidity)
                
            # Humidity went severly up, humidifier for sure is not out of water
            if (hum_settings.last_humidity + 2 < sensor_data.humidity):
                log_manager.reset_out_of_water_calls()
             
        hum_settings.last_humidity = sensor_data.humidity
        
        if hum_settings.is_automatic():
            if sensor_data.humidity < hum_settings.range_from and not hum_settings.humidifier_on:
                formatted_message = f"Turning humidifier ON. Humidity: {sensor_data.humidity} %, target range: {hum_settings.range_from} % - {hum_settings.range_to} %"
                
                log_manager.log_event("info", "AUTO: Humidifier ON", formatted_message)
                hum_settings.toggle_humidifier(ip_settings.humidifier_ip, True)
            
            elif sensor_data.humidity > hum_settings.range_to and hum_settings.humidifier_on:
                formatted_message = f"Turning humidifier OFF. Humidity: {sensor_data.humidity} %, target range: {hum_settings.range_from} % - {hum_settings.range_to} %"

                log_manager.log_event("info", "AUTO: Humidifier OFF", formatted_message)
                hum_settings.toggle_humidifier(ip_settings.humidifier_ip, False)
         
    except Exception as e:
        log_manager.log_event("error", "Humidifier Error", str(e))