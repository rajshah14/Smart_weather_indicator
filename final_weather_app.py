# -*- coding: utf-8 -*-
from weather_final import * 
import re 
import tkMessageBox


def do_operation():
    """
    Function to collect the data from the API, based on the location entered.
    Creates a tkinter window to display both current and 4 days, predicted data.
    Returns dictionry having current and predicted weather data.
    """
    city = entry.get()
    try:
        low_value = 0
        high_value = len(all_city_list)-1
        while low_value <= high_value:
            mid = (low_value + high_value)/2
            if (all_city_list[mid].lower()) == city.lower():
                break
            elif (all_city_list[mid].lower()) < city.lower():
                low_value = mid+1
            else:
                high_value = mid-1
        if low_value <= high_value:
            all_weather_data = get_data(city)
        else:
            raise Exception("Invalid location")
    except requests.exceptions.ConnectionError:
        tkMessageBox.showwarning("Alert", "Computer not Connected to internet")
        raise
    except ValueError:
        print 'Entered'
        tkMessageBox.showwarning("Alert", "Server Error")
        raise
    except:
        print "invalid"
        tkMessageBox.showwarning("Alert", "Invalid City!!")
        raise
    main = Toplevel()
    main.geometry('450x450+200+200')
    city_name = city
    main.title(city_name)
    main.geometry("{0}x{1}+0+0".format(main.winfo_screenwidth(), main.winfo_screenheight()))
    main.resizable(width=False, height=False)
    screen_width = main.winfo_screenwidth()
    screen_height = main.winfo_screenheight()

    temp = all_weather_data['today']['temp']
    temp_min = all_weather_data['today']['min']
    temp_max = all_weather_data['today']['max']
    temp = str(temp) + "°C"
    temp_min = "Min : " + str(temp_min) + "°C"
    temp_max = "Max : " + str(temp_max) + "°C"

    canvas = Canvas(main, width=1920, height=1080)
    canvas.create_image(0, 0, anchor=NW, image=background)
    canvas.create_text(screen_width/2, screen_height*0.066667, text=city, fill="white", font="Rockwell 60 italic")
    canvas.create_image(screen_width/2, screen_height*0.066667*3.5)
    canvas.create_text(screen_width/2, screen_height*6*0.066667, text=temp, fill="white", font="Times 40 ")
    canvas.create_text(screen_width*0.066667*4, screen_height*5.5*0.066667, text=temp_min, fill="white",
                       font="Times 30")
    canvas.create_text(screen_width*0.066667*11, screen_height*5.5*0.066667, text=temp_max, fill="white",
                       font="Times 30")
    canvas.create_text(screen_width/2, screen_height*7.2*0.066667, text=all_weather_data['today']['desc'], fill="white",
                       font="Times 40")
    canvas.create_line(screen_width/5, screen_height*8*0.066667, screen_width/1.2, screen_height*8*0.066667,
                       fill="white", width=0.1)
    canvas.create_text(screen_width/3.8, screen_height*9*0.066667, text=all_weather_data[1]['day'], fill="white",
                       font="Times 20 bold")
    canvas.create_text(screen_width/2.3, screen_height*9*0.066667, text=all_weather_data[2]['day'], fill="white",
                       font="Times 20 bold")
    canvas.create_text(screen_width/1.65, screen_height*9*0.066667, text=all_weather_data[3]['day'], fill="white",
                       font="Times 20 bold")
    canvas.create_text(screen_width/1.3, screen_height*9*0.066667, text=all_weather_data[4]['day'], fill="white",
                       font="Times 20 bold")
    canvas.create_text(screen_width/3.8, screen_height*11*0.066667, text=all_weather_data[1]['min'], fill="white",
                       font="Times 17 bold")
    canvas.create_text(screen_width/2.3, screen_height*11*0.066667, text=all_weather_data[2]['min'], fill="white",
                       font="Times 17 bold")
    canvas.create_text(screen_width/1.65, screen_height*11*0.066667, text=all_weather_data[3]['min'], fill="white",
                       font="Times 17 bold")
    canvas.create_text(screen_width/1.3, screen_height*11*0.066667, text=all_weather_data[4]['min'], fill="white",
                       font="Times 17 bold")
    canvas.create_text(screen_width/3.8, screen_height*11.5*0.066667, text=all_weather_data[1]['max'], fill="white",
                       font="Times 17 bold")
    canvas.create_text(screen_width/2.3, screen_height*11.5*0.066667, text=all_weather_data[2]['max'], fill="white",
                       font="Times 17 bold")
    canvas.create_text(screen_width/1.65, screen_height*11.5*0.066667, text=all_weather_data[3]['max'], fill="white",
                       font="Times 17 bold")
    canvas.create_text(screen_width/1.3, screen_height*11.5*0.066667, text=all_weather_data[4]['max'], fill="white",
                       font="Times 17 bold")
    canvas.pack()
    bulb_value = all_weather_data['today']['desc']
    bulb_glow(bulb_value)
    return


def message_window(message_to_print, color):
    """
    used to create a message window based on the current weather data
    background color emulates the hue of the light bulb, and it changes with the
    :param message_to_print: appropriate weather condition message
    :param color: bulb color
    """
    window = Tk()
    window.title('Smart_Weather_Indicator')

    def close_window():
        """
        close the message window on press of a button
        """
        window.destroy()

    frame = Frame(window, bg=color, width=5000, height=6000)
    message_label = Label(frame, text=message_to_print, font="Times 11 bold")
    message_label.pack()
    frame.pack()
    button = Button(frame, text="OK", command=close_window)
    button.pack(side='bottom')
    window.mainloop()


def bulb_glow(bulb_value):
    """
    Gets the weather description, based on that changes the weather bulb color
    :param bulb_value: weather description of the location
    """
    weather_dictionary = {'good_day_conditions': ['clear day', 'clouds', 'Sky is Clear'],
                          'thunderstorm_conditions': ['thunderstorm with light rain', 'thunderstorm with rain',
                                                      'thunderstorm with heavy rain', 'light thunderstorm',
                                                      'thunderstorm with light drizzle', 'thunderstorm with drizzle',
                                                      'thunderstorm with heavy drizzle'],
                          'drizzle_conditions': ['light intensity drizzle', 'drizzle', 'heavy intensity drizzle',
                                                 'light intensity drizzle rain', 'drizzle rain',
                                                 'shower rain and drizzle', 'heavy shower rain and drizzle',
                                                 'shower drizzle'],
                          'rain_conditions': ['light rain', 'moderate rain', 'freezing rain',
                                              'light intensity shower rain', 'shower rain'],
                          'snow_conditions': ['light snow', 'light rain and snow', 'rain and snow', 'light shower snow',
                                              'shower snow'],
                          'atmosphere_conditions': ['mist', 'smoke', 'haze', 'sand,dust whirls', 'fog', 'sand', 'dust',
                                                    'volcanic ash', 'squalls'],
                          'clear_conditions': ['clear sky'],
                          'clouds_conditions': ['few clouds', 'scattered clouds', 'broken clouds', 'overcast clouds'],
                          'extreme_hot_cold_conditions': ['hot', 'cold', 'windy'],
                          'normal_conditions': ['calm', 'light breeze', 'gentle breeze', 'moderate breeze',
                                                'fresh breeze', 'strong breeze', 'high wind,near gale', 'gale',
                                                'severe gale'],
                          'extreme_conditions': ['violent storm', 'hurricane', 'storm', 'tornado', 'tropical storm',
                                                 'hail', 'heavy intensity shower rain', 'ragged shower rain',
                                                 'heavy intensity rain', 'very heavy rain', 'extreme rain',
                                                 'freezing rain', 'thunderstorm with heavy rain', 'heavy thunderstorm',
                                                 'thunderstorm with heavy drizzle']}
    if bulb_value in weather_dictionary['extreme_conditions']:
        message_to_print = "please take extreme caution, it is extremely " + bulb_value + " outside.....glow red bulb"
        message_window(message_to_print, '#FF0000')
    else:
        if bulb_value in weather_dictionary['thunderstorm_conditions']:
            message_to_print = "Hey, it is" + bulb_value + " outside, please take appropriate precautions...." \
                                                           "consider going out only if necessary"
            message_window(message_to_print, '#A9A9A9')
        elif bulb_value in weather_dictionary['drizzle_conditions']:
            message_to_print = "Hey, it is" + bulb_value + " outside.....you should enjoy outside, but don't forget " \
                                                           "to carry rain wear"
            message_window(message_to_print, '#AFEEEE')
        elif bulb_value in weather_dictionary['rain_conditions']:
            message_to_print = "Hey, it is going to be " + bulb_value + " outside.....you should go outside with " \
                                                                         "precautions and appropriate rain wear"
            message_window(message_to_print, '#0000CD')
        elif bulb_value in weather_dictionary['snow_conditions']:
            message_to_print = "Hey, it is going to be " + bulb_value + " outside.....you should be extremely " \
                                                                        "cautious. Drive slowly and carefully"
            message_window(message_to_print, '#DCDCDC')
        elif bulb_value in weather_dictionary['atmosphere_conditions']:
            message_to_print = "Hey, it is going to be " + bulb_value + " outside..."
            message_window(message_to_print, '#808080')
        elif bulb_value in weather_dictionary['clear_conditions']:
            message_to_print = "Hey, it is going to be " + bulb_value + " outside.....its a really good weather to " \
                                                                        "go on the beach !!"
            message_window(message_to_print, '#00BFFF')
        elif bulb_value in weather_dictionary['clouds_conditions']:
            message_to_print = "Hey, it is going to be " + bulb_value + " outside.....don;t fret and enjoy a good " \
                                                                        "walk outside"
            message_window(message_to_print, '#708090')
        elif bulb_value in weather_dictionary['extreme_hot_cold_conditions']:
            message_to_print = "Hey, it is going to be " + bulb_value + " outside....go out only if needed"
            message_window(message_to_print, '#FF8C00')
        else:
            message_to_print = "Hey, it is going to be " + bulb_value + " outside....."
            message_window(message_to_print, '#FFFFFF')


def match_entered_text(fieldValue, acListEntry):
    pattern = re.compile(re.escape(fieldValue) + '.*', re.IGNORECASE)
    return re.match(pattern, acListEntry)


class AutocompleteEntry(Entry):
    """
    It is used while entering the data in the text box for getting name of the location.
    Predicts the closest matches of the names of the city based on the letters entered by the user.
    Allow user to scroll through the list of closest matches using up and down arrow keys on the keyboard.
    """
    def __init__(self, all_city_list, *args, **kwargs):
        if 'listboxLength' in kwargs:
            self.listboxLength = kwargs['listboxLength']
            del kwargs['listboxLength']
        else:
            self.listboxLength = 8

        if 'matchesFunction' in kwargs:
            self.matchesFunction = kwargs['matchesFunction']
            del kwargs['matchesFunction']
        else:
            def match_entered_text(fieldValue, acListEntry):
                pattern = re.compile('.*' + re.escape(fieldValue) + '.*', re.IGNORECASE)
                return re.match(pattern, acListEntry)

            self.matchesFunction = match_entered_text

        Entry.__init__(self, *args, **kwargs)
        self.focus()
        self.all_city_list = all_city_list
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()
        self.var.trace('w', self.changed)
        self.bind("<Return>", self.selection)
        self.bind("<Up>", self.moveUp)
        self.bind("<Down>", self.moveDown)
        self.listboxUp = False

    def changed(self, name, index, mode):
        if self.var.get() == '':
            if self.listboxUp:
                self.listbox.destroy()
                self.listboxUp = False
        else:
            words = self.comparison()
            if words:
                if not self.listboxUp:
                    self.listbox = Listbox(width=self["width"], height=self.listboxLength)
                    self.listbox.bind("<Button-1>", self.selection)
                    self.listbox.bind("<Right>", self.selection)
                    self.listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                    self.listboxUp = True

                self.listbox.delete(0, END)
                for w in words:
                    self.listbox.insert(END, w)
            else:
                if self.listboxUp:
                    self.listbox.destroy()
                    self.listboxUp = False

    def selection(self, event):
        if self.listboxUp:
            self.var.set(self.listbox.get(ACTIVE))
            self.listbox.destroy()
            self.listboxUp = False
            self.icursor(END)

    def moveUp(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]

            if index != '0':
                self.listbox.selection_clear(first=index)
                index = str(int(index) - 1)

                self.listbox.see(index)
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

    def moveDown(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]

            if index != END:
                self.listbox.selection_clear(first=index)
                index = str(int(index) + 1)

                self.listbox.see(index)
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

    def comparison(self):
        lst = []
        low_value = 0
        high_value = len(self.all_city_list)-1
        s = self.var.get().lower()
        while low_value <= high_value:
            mid = (low_value + high_value)/2
            if (self.all_city_list[mid].lower()).startswith(s):
                break
            elif (self.all_city_list[mid].lower()) < s:
                low_value = mid+1
            else:
                high_value = mid-1
        if (self.all_city_list[mid].lower()).startswith(s):
            lst.append(self.all_city_list[mid])
            low_value = mid-1
            while low_value >= 0 and self.all_city_list[low_value].lower().startswith(s):
                lst.append(self.all_city_list[low_value])
                low_value -= 1
            high_value = mid+1
            while high_value < len(self.all_city_list) and self.all_city_list[high_value].lower().startswith(s):
                lst.append(self.all_city_list[high_value])
                high_value += 1
        return lst


def erase_default_data():
    entry.selection_range(0, END)

if __name__ == '__main__':
    all_city_list = list(set(cities()))
    all_city_list.sort()
    window = Tk()
    window.geometry("320x180+600+400")
    window.title('Smart_Weather_Indicator')
    background = PhotoImage(file="wallpaper.gif")
    back_label = Label(window, image=background)
    back_label.place(x=0, y=0, relwidth=1, relheight=1)
    entry = AutocompleteEntry(all_city_list, window, listboxLength=6, width=32, matchesFunction=match_entered_text)
    entry.insert(END, 'Enter Your City Here ....')
    entry.place(relx=0.5, rely=0.2, anchor=N)
    button = PhotoImage(file="button.gif")
    my_button = Button(text="", command=do_operation, width=20, height=20, image=button, compound=RIGHT, relief=RIDGE)\
        .place(relx=0.5, rely=0.7, anchor=S)
    window.mainloop()
