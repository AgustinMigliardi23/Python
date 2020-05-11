import arrange_data
import datetime as dt
import os
import tkinter as tk

def get_colour(days):
    sky = [0, 0, 0]
    for day in days:
        skies = day[3][1]
        if skies == "pocas nubes":
            sky[0] += 1
        elif skies == "ninguna nube":
            sky[0] += 1
        elif skies == "nubes aisladas":
            sky[1] += 1
        elif skies == "muchas nubes":
            sky[2] += 1
        elif skies == "nubes dispersas":
            sky[1] += 1
    if sky.index(max(sky)) == 0:
        colour = "#f1fa41"
    elif sky.index(max(sky)) == 1:
        colour = "#a9bfd6"
    else:
        colour = "#3e4b59"
    return colour

def get_temp(days):
    temp = 0
    for day in days:
        temp += int(day[1][0])
    temp = int(temp/len(days))
    return str(temp)

def get_rain_chances(days):
    humidity = float(get_humidity(days))
    sky_desc = get_sky(days)

    sky_const = 0
    humidity_const = 0
    bias = 30

    sky = sky_desc.split(",")
    if sky[0] == "Despejado":
        sky_const = 0
        bias = 0
    elif sky[1] == " con pocas nubes":
        sky_const = 0.5
    elif sky[1] == " con nubes aisladas":
        sky_const = 0.8
    elif sky[1] == " totalmente nublado":
        sky_const = 1.1
    
    if humidity > 50:
        humidity_const = 0.6
    elif humidity > 70:
        humidity_const = 0.8
    else:
        humidity_const = 1
    
    return str(round(sky_const*humidity_const*humidity + bias, 2))

def get_feels_like(days):
    temp = 0
    for day in days:
        temp += int(day[1][1])
    temp = int(temp/len(days))
    return str(temp)

def get_humidity(days):
    humidity = 0
    for day in days:
        humidity += int(day[2])
    humidity = humidity / len(days)
    return str(humidity)

def get_day(day):
    date = day[0][0].weekday()
    if date == 0:
        return "Lunes"
    elif date == 1:
        return "Martes"
    elif date == 2:
        return "Miercles"
    elif date == 3:
        return "Jueves"
    elif date == 4:
        return "Viernes"
    elif date == 5:
        return "Sabado"
    else:
        return "Domingo"

def get_sky(days):
    sky = [0, 0, 0]
    shorty = [0, 0]
    final = ""
    
    for day in days:
        skies = day[3][1]
        if skies == "pocas nubes":
            sky[0] += 1
        elif skies == "ninguna nube":
            sky[0] += 1
        elif skies == "nubes aisladas":
            sky[1] += 1
        elif skies == "muchas nubes":
            sky[2] += 1
        elif skies == "nubes dispersas":
            sky[1] += 1
        short = day[3][0]
        if short == "Despejado":
            shorty[0] += 1
        elif short == "Nublado":
            shorty[1] += 1
    
    if shorty.index(max(shorty)) == 0:
        final += "Despejado, "
    else:
        final += "Nublado, "
    if sky.index(max(sky)) == 0:
        final += "con pocas nubes"
    elif sky.index(max(sky)) == 1:
        final += "con nubes aisladas"
    else:
        final += " totalmente nublado"
    return final

def add_day(root, relwidth, relx, day):
    colour = get_colour(day)
    frame = tk.Frame(root, bg=colour)
    frame.place(relwidth=relwidth, relheight=0.2, relx=relx, rely=0.8)

    day_text = get_day(day)
    day_label = tk.Label(frame, width=10, text= day_text, anchor="center", bg=colour, fg="black", font=("Courier", 12))
    day_label.pack()

    temp_text = get_temp(day)
    temp = tk.Label(frame, width=10, text= temp_text + "°", anchor="center", bg=colour, fg="black", font=("Courier", 30))
    temp.pack()


def main_day(day, root):
    colour = get_colour(day)

    day_text = get_day(day)
    day_text += " " + str(day[0][0].day) + "/" + str(day[0][0].month) + "/" + str(day[0][0].year)

    frame = tk.Frame(root, bg=colour)
    frame.place(relwidth=1, relheight=0.8, relx=0, rely=0)

    place_text = "Buenos Aires"
    place = tk.Label(frame, width=30, text= place_text, anchor="w", bg=colour, fg="black", font=("Courier", 30))
    place.place(relwidth=0.475, relheight=0.115, relx=0, rely=0)

    day_label = tk.Label(frame, width=60, text= day_text, anchor="w", bg=colour, fg="black", font=("Courier", 15))
    day_label.place(relwidth=0.3, relheight=0.07, relx=0, rely=0.115)

    sky_text = get_sky(day)
    sky = tk.Label(frame, width=80, text= sky_text, anchor="w", bg=colour, fg="black", font=("Courier", 10))
    sky.place(relwidth=0.5, relheight=0.05, relx=0, rely=0.185)

    temp_text = get_temp(day)
    temp = tk.Label(frame, width=30, text= temp_text + "°", anchor="w", bg=colour, fg="black", font=("Courier", 60))
    temp.place(relwidth=0.25, relheight=0.3, relx=0, rely=0.3)

    rain_chamce_text = "Chances de lluvia: %" + get_rain_chances(day)
    humidity = tk.Label(frame, width=30, text= rain_chamce_text, anchor="e", bg=colour, fg="black", font=("Courier", 15))
    humidity.place(relwidth=0.5, relheight=0.1, relx=0.5, rely=0.3)
    
    fl_text = "Sensacion termica: " + get_feels_like(day) +"°"
    fl = tk.Label(frame, width=30, text= fl_text, anchor="e", bg=colour, fg="black", font=("Courier", 15))
    fl.place(relwidth=0.5, relheight=0.1, relx=0.5, rely=0.4)

    humidity_text = "Humedad del %" + get_humidity(day)
    humidity = tk.Label(frame, width=30, text= humidity_text, anchor="e", bg=colour, fg="black", font=("Courier", 15))
    humidity.place(relwidth=0.5, relheight=0.1, relx=0.4, rely=0.5)

    button = tk.Button(frame, text='Refresh', padx=10, pady=5, fg="white", bg="purple", command=(lambda : refresh(root)))
    button.place(relwidth=0.15, relheight=0.1, relx=0.85, rely=0)

def refresh(root):
    root.destroy()
    draw_app()

def draw_app():
    root = tk.Tk()

    root.title('Weather')
    canvas = tk.Canvas(root, width=600, height=350, bg="#5e80d6") 
    canvas.pack()

    data = arrange_data.arrange_data()

    if data == "No Internet":
        connection_error = tk.Label(root, width=30, text= "Connection Error", anchor="e", bg="white", fg="black", font=("Courier", 30))
        connection_error.place(relwidth=0.8, relheight=0.3, relx=0, rely=0)
    else:
        count = 0
        for day in data:
            add_day(root, 1/len(data), count, day)
            count += 1 / len(data)
        
        # refresh_button(root)
        
        main_day(data[0], root)

    root.mainloop()

draw_app()