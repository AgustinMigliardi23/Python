import datetime as dt

KELVIN = 273.15

def parse_data_to_numbers(forecast):
    current_temp = forecast["main"]["temp"] - KELVIN
    feels_like = forecast["main"]["feels_like"] - KELVIN
    humidity = forecast["main"]["humidity"]
    main_weather = forecast["weather"][0]["main"]
    description = forecast["weather"][0]["description"]

    return current_temp, feels_like, humidity, main_weather, description

def get_verbo(day):
    today = dt.datetime.now()
    if day.day == today.day and day.hour == today.hour:
        return "es"
    else:
        return "sera"

def get_time_zone(day):
    if day.hour == 9:
        return "a la mañana"
    elif day.hour == 15:
        return "al mediodia"
    else:
        return "a la noche"

def get_start(day):
    today = dt.datetime.now()
    if day.day == today.day:
        return "Hoy "
    try:
        tommorrow = dt.datetime(today.year, today.month, today.day + 1)
    except:
        try:
            tommorrow = dt.datetime(today.year, today.month + 1, 1)
        except:
            tommorrow = dt.datetime(today.year + 1, 1, 1)
    if tommorrow.day == day.day:
        return "Mañana "
    else:
        if day.weekday() == 0:
            return "El lunes "
        elif  day.weekday() == 1:
            return "El martes "
        elif  day.weekday() == 2:
            return "El miercoles "
        elif  day.weekday() == 3:
            return "El jueves "
        elif  day.weekday() == 4:
            return "El viernes "
        elif  day.weekday() == 5:
            return "El sabado "
        elif  day.weekday() == 6:
            return "El domingo "


def get_sky(data):
    if data == "Clouds":
        return "Nublado"
    elif data == "Clear":
        return "Despejado"
    else:
        return "OJO CON ESTE QUE ES NUEVO"

def get_sky_description(data):
    if data == "few clouds":
        return "pocas nubes"
    elif data == "clear sky":
        return "pocas o ninguna nube"
    elif data == "scattered clouds":
        return "nubes aisladas"
    elif data == "overcast clouds":
        return "muchas nubes"
    elif data == "broken clouds":
        return "nubes dispersas"
    else:
        print(data)
        print("----------------")

def print_data(day, data):
    what_day = get_start(day)
    when = get_time_zone(day)
    verbo = get_verbo(day)
    sky = get_sky(data[3])
    sky_description = get_sky_description(data[4])
    temp = what_day + when + " la temperatura " + verbo + " de " + str(int(data[0])) + " grados centigrados, sensacion termica de " + str(int(data[1])) + " grados centigrados"
    humidity = "la humedad " + verbo + " de %" + str(data[2])
    weather = " y el cielo estara " + sky + " con " + sky_description
    print(temp, humidity, weather)