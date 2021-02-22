from math import pow

#########################################
#            MQ135 GAS SENSOR           #
#########################################
__ADC = None
__ADC_RES = 1023


def __get_correction_factor(temperature, humidity):
    """Calculates the correction factor for ambient air temperature and relative humidity
    Based on the linearization of the temperature dependency curve
    under and above 20 degrees Celsius, assuming a linear dependency on humidity,
    provided by Balk77 https://github.com/GeorgK/MQ135/pull/6/files
    0.00035  - 'CORA' Parameters to model temperature and humidity dependence
    0.02718  - 'CORB'
    1.39538  - 'CORC'
    0.0018   - 'CORD'
    -0.003333333  - 'CORE'
    -0.001923077  - 'CORF'
    1.130128205   - 'CORG'
    """
    if temperature < 20:
        return 0.00035 * temperature * temperature - 0.02718\
               * temperature + 1.39538 - (humidity - 33.) * 0.0018
    return -0.003333333 * temperature + -0.001923077 * humidity + 1.130128205


def __get_resistance():
    """
    Returns the resistance of the sensor in kOhms // -1 if not value got in pin
    10.0 - 'RLOAD' The load resistance on the board
    """
    global __ADC, __ADC_RES
    if __ADC is None:
        from machine import ADC
        from LogicalPins import get_pin_on_platform_by_key
        if 'esp8266' in platform:
            __ADC = ADC(get_pin_on_platform_by_key('co2'))       # 1V measure range
            __ADC_RES = 1023
        else:
            __ADC = ADC(Pin(get_pin_on_platform_by_key('co2')))
            __ADC.atten(ADC.ATTN_11DB)                          # 3.3V measure range
            __ADC_RES = 4095
    value = __ADC.read()
    if value == 0:
        return -1
    return (1023./value - 1.) * 10.0


def __get_corrected_resistance(temperature, humidity):
    """Gets the resistance of the sensor corrected for temperature/humidity"""
    return __get_resistance()/__get_correction_factor(temperature, humidity)


def __get_corrected_ppm(temperature, humidity):
    """
    Returns the ppm of CO2 sensed (assuming only CO2 in the air)
    corrected for temperature/humidity
    76.63       - 'RZERO' Calibration resistance at atmospheric CO2 level
    116.6020682 - 'PARA' parameters for calculating ppm of CO2 from sensor resistance
    2.769034857 - 'PARB'
    """
    return 116.6020682 * pow((__get_corrected_resistance(temperature, humidity)\
                                           / 76.63), -2.769034857)


def measure_mq135(temperature=None, humidity=None):
    """
    CO2 Gas Concentration - Parts-per-million - PPM
    -> 1ppm = 0.0001% gas.
    Concentration evaluation:
        250-400ppm      Normal background concentration in outdoor ambient air
        400-1,000ppm    Concentrations typical of occupied indoor spaces with good air exchange
        1,000-2,000ppm  Complaints of drowsiness and poor air.
        2,000-5,000 ppm Headaches, sleepiness and stagnant, stale, stuffy air. Poor concentration, loss of attention, increased heart rate and slight nausea may also be present.
        5,000ppm        Workplace exposure limit (as 8-hour TWA) in most jurisdictions.
        >40,000 ppm     Exposure may lead to serious oxygen deprivation resulting in permanent brain damage, coma, even death.
    """
    if temperature is None or humidity is None:
        print("Missing mandatory parameters: temperature and/or humidity")
        return

    try:
        status = 'n/a'
        ppm = __get_corrected_ppm(temperature, humidity)
        if ppm <= 1000:
            status = 'PERFECT'
        elif ppm <= 2000:
            status = 'POOR'
        elif ppm <= 4000:
            status = "WARNING"
        elif ppm > 4000:
            status = "CRITICAL"
        return "{} - {}".format(ppm, status)
    except Exception as e:
        return "measure_mq135 ERROR: {}".format(e)


def help():
    return 'measure_mq135(temp, hum)'

