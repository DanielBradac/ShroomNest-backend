# Periodic errand which turns humidifier, light, etc. on and off if it is set to automatic

def run_errand(sensor_data, hum_settings, ip_settings, log_manager, errand_per, init_run):
    try:      
        if init_run:
            on_off = "ON" if hum_settings.humidifier_on else "OFF"
            log_manager.log_event("info", f"INIT: Switching humidifier {on_off}", f"Switching humidifier {on_off} on init run")
            hum_settings.toggle_humidifier(ip_settings.humidifier_ip, hum_settings.humidifier_on, log_manager)
            return
        
        if (hum_settings.humidifier_on and hum_settings.last_humidity != 0):
            # Humidity hasn't got up and the humidifier is on? Maybe it is out of water
            if (sensor_data.humidity < 90 and hum_settings.last_humidity >= sensor_data.humidity):
                log_manager.report_out_of_water(hum_settings.last_humidity, sensor_data.humidity)
                
            # Humidity went severly up, humidifier for sure is not out of water
            if (hum_settings.last_humidity + 2 < sensor_data.humidity):
                log_manager.reset_out_of_water_calls()
             
        hum_settings.last_humidity = sensor_data.humidity
        
        # Auto run
        if hum_settings.is_automatic():
            if sensor_data.humidity < hum_settings.range_from and not hum_settings.humidifier_on:
                log_manager.log_event("info", "AUTO: Switching humidifier ON", f"Switching humidifier ON. Humidity: {sensor_data.humidity} %, target range: {hum_settings.range_from} % - {hum_settings.range_to} %")
                hum_settings.toggle_humidifier(ip_settings.humidifier_ip, True, log_manager)
            
            elif sensor_data.humidity > hum_settings.range_to and hum_settings.humidifier_on:
                log_manager.log_event("info", "AUTO: Switching humidifier OFF", f"Switching humidifier OFF. Humidity: {sensor_data.humidity} %, target range: {hum_settings.range_from} % - {hum_settings.range_to} %")
                hum_settings.toggle_humidifier(ip_settings.humidifier_ip, False, log_manager)
            return
        
        # Periodic run
        if hum_settings.is_periodic():
            if hum_settings.humidifier_on:
                hum_settings.run_time += errand_per
            else:
                hum_settings.wait_time += errand_per
                
            if (hum_settings.run_time >= hum_settings.run_per or hum_settings.wait_time >= hum_settings.wait_per):
                toggle_on = not hum_settings.humidifier_on
                
                if toggle_on:
                    log_manager.log_event("info", "PERIOD: Switching humidifier ON", f"Switching humidifier ON. Wait time is over, wait period: {hum_settings.wait_per} s, current wait time: {hum_settings.wait_time} s")
                else:
                    log_manager.log_event("info", "PERIOD: Switching humidifier OFF", f"Switching humidifier OFF. Run time is over, run period: {hum_settings.run_per} s, current run time: {hum_settings.run_time} s")
                                        
                hum_settings.toggle_humidifier(ip_settings.humidifier_ip, toggle_on, log_manager)
                hum_settings.reset_periodic_timers()
         
    except Exception as e:
        log_manager.log_event("error", "Humidifier Error", str(e))


    