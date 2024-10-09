# Periodic errand which turns humidifier, fan, etc. on and off if it is set to automatic/periodic
def run_errand(sensor_data, hum_settings, vent_settings, ip_settings, log_manager, errand_per, init_run):
    # We turn everything off on init run
    if init_run:
        try:
            log_manager.log_event("info", "Humidifier - INIT", "Switching humidifier OFF on init run")
            hum_settings.toggle_humidifier(ip_settings.humidifier_ip, False, log_manager)
        except Exception as e:
            log_manager.log_event("error", "Worker Error - Humidifier", str(e))
            
        try:
            log_manager.log_event("info", "Fan - INIT", "Switching fan OFF on init run")
            vent_settings.toggle_fan(ip_settings.fan_ip, False, log_manager)
        except Exception as e:
            log_manager.log_event("error", "Worker Error - Fan", str(e))
            
        return
        
    try:
        update_humidifier_state(sensor_data, hum_settings, ip_settings, log_manager, errand_per)
    except Exception as e:
        log_manager.log_event("error", "Worker Error - Humidifier", str(e))
        
    try:
        update_fan_state(vent_settings, ip_settings, log_manager, errand_per)
    except Exception as e:
        log_manager.log_event("error", "Worker Error - Fan", str(e))


# Check on humidifier based on its settings and current sensor data
def update_humidifier_state(sensor_data, hum_settings, ip_settings, log_manager, errand_per):
    if (hum_settings.humidifier_on and hum_settings.last_humidity != 0):
        # Humidity hasn't got up and the humidifier is on? Maybe it is out of water
        if (sensor_data.humidity < 90 and hum_settings.last_humidity >= sensor_data.humidity):
            log_manager.report_out_of_water(hum_settings.last_humidity, sensor_data.humidity)
                
         # Humidity went up a lot, humidifier for sure is not out of water
        if (hum_settings.last_humidity + 0.3 < sensor_data.humidity):
            log_manager.reset_out_of_water_calls()
             
    hum_settings.last_humidity = sensor_data.humidity
        
    # Auto run
    if hum_settings.is_automatic():
        if sensor_data.humidity < hum_settings.range_from and not hum_settings.humidifier_on:
            log_manager.log_event("info", "Humidifier - AUTO", f"Switching humidifier ON. Humidity: {sensor_data.humidity} %, target range: {hum_settings.range_from} % - {hum_settings.range_to} %")
            hum_settings.toggle_humidifier(ip_settings.humidifier_ip, True, log_manager)
            
        elif sensor_data.humidity > hum_settings.range_to and hum_settings.humidifier_on:
            log_manager.log_event("info", "Humidifier - AUTO", f"Switching humidifier OFF. Humidity: {sensor_data.humidity} %, target range: {hum_settings.range_from} % - {hum_settings.range_to} %")
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
                log_manager.log_event("info", "Humidifier - PERIOD", f"Switching humidifier ON. Wait time is over, wait period: {hum_settings.wait_per} s, current wait time: {hum_settings.wait_time} s")
            else:
                log_manager.log_event("info", "Humidifier - PERIOD", f"Switching humidifier OFF. Run time is over, run period: {hum_settings.run_per} s, current run time: {hum_settings.run_time} s")
                                        
            hum_settings.toggle_humidifier(ip_settings.humidifier_ip, toggle_on, log_manager)
            hum_settings.reset_periodic_timers()

# Check on fan - shouldn't we turn it on?
def update_fan_state(vent_settings, ip_settings, log_manager, errand_per):
    # Periodic run
        if vent_settings.is_periodic():
            if vent_settings.fan_on:
                vent_settings.run_time += errand_per
            else:
                vent_settings.wait_time += errand_per
                
            if (vent_settings.run_time >= vent_settings.run_per or vent_settings.wait_time >= vent_settings.wait_per):
                toggle_on = not vent_settings.fan_on
                
                if toggle_on:
                    log_manager.log_event("info", "Fan - PERIOD", f"Switching fan ON. Wait time is over, wait period: {vent_settings.wait_per} s, current wait time: {vent_settings.wait_time} s")
                else:
                    log_manager.log_event("info", "Fan - PERIOD", f"Switching fan OFF. Run time is over, run period: {vent_settings.run_per} s, current run time: {vent_settings.run_time} s")
                                        
                vent_settings.toggle_fan(ip_settings.fan_ip, toggle_on, log_manager)
                vent_settings.reset_periodic_timers()
    