import requests, json
from datetime import datetime, date, timedelta
from Tkinter import *
import tkMessageBox

# OpenweatherMaps API key
api_key = '5c9447dde0bd171a53e6d95b9ff3597f' 
# variable used to debug
debug = 0 

def get_current_data(entered_location):
	"""
	Extracts current weather data from openweathermaps API based on the entered location
	Args:
		entered_location: location for the current data is required
	
	Returns:
		j: json object which has the current weather data

	Raises:
		ValueError: raises an server error if the entered location is not present in the json file
	"""
	entered_location = entered_location.lower()
	# to check if the data is present in file, if present checks its age, if too old replace with new
	try: 
		# flag set when data is too old and new to be replaced with a new one
		flag = 0
		f = open("current", "r")
		counter = 0
		for line in f:
			j = json.loads(line)
			if j["list"][0]["name"].lower()==entered_location:
				flag = 1
				if ((datetime.utcnow()-datetime(1970, 1, 1)).total_seconds()-j["list"][0]["dt"])<=1000:
					if debug:
						print json.dumps(j, indent=4)
					f.close()
					return j
				else:
					break
			counter += 1
		f.close()
	except:
		if debug:
			print "ERROR !! Unable to open file !!\n"
		pass
	api_base_link = 'http://api.openweathermap.org/data/2.5/find?q='
	remaining_link = '&units=metric&appid='
	try:
		if debug:
			print "Fetching Data....\n"
		# request to the server to get weather data
		r = requests.get(api_base_link+entered_location+remaining_link+api_key)
	except:
		raise
	j = json.loads(r.text)
	if debug:
		print json.dumps(j, indent=4)
	try:
		j["list"][0]["name"] = entered_location
		if j['count']==0:
			raise ValueError("Server Error")
	except:
		raise ValueError("Server Error")
	if j['cod']!='200':
		raise Exception("ERROR !! Not a valid location !!")
		
	if flag:
		# since flag is set so previous data needs to be modified
		if debug:
			print json.dumps(j, indent=4)
			print "Note !! Previous data found but it was very old !!\n"
		try:
			f = open("current", "r")
			lst = f.readlines()
			f.close()
			lst[counter] = str(json.dumps(j)+"\n")
			f = open("current", "w")
			f.writelines(lst)
			f.close()
		except:
			if debug:
				print "ERROR !! Unable to open file. flag is set !!"
	else:
		# no previous data, so appending the json object with new data
		if debug:
			print json.dumps(j, indent=4)
			print "Note !! Previous data was not found !!\n"
		try:
			f = open("current", "a")
			f.write(json.dumps(j)+"\n")
			f.close()
		except:
			if debug:
				print "ERROR !! Not able to open file. flag is not set !!"
	return j

def get_forecast_data(entered_location):
	"""
	Extracts predicted weather data from openweathermaps API based on the entered location for next 4 days
	Args:
		entered_location: location for the current data is required
	
	Returns:
		j: json object which has the current weather data

	Raises:
		ValueError: raises an server error if the entered location is not present in the json file
	"""
	entered_location = entered_location.lower()
	# to check if the data is present in file, if present checks its age, if too old replace with new
	try: 
		# flag set when data is too old and new to be replaced with a new one
		flag = 0
		f = open("data", "r")
		counter = 0
		for line in f:
			j = json.loads(line)
			if j["city"]["name"].lower()==entered_location:
				flag = 1
				today = date.today().isoformat()
				if today==j["list"][0]["dt_txt"].split()[0]:
					if debug:
						print "** Found in file **"
						print json.dumps(j, indent=4)
					f.close()
					return j
				else:
					break
			counter += 1
		f.close()
	except:
		if debug:
			print "ERROR !! Not able to open file !!\n"
		pass
	api_base_link= 'http://api.openweathermap.org/data/2.5/forecast?q='
	remaining_link = '&units=metric&appid='
	try:
		if debug:
			print "Fetching Data....\n"
		# request to the server to get weather data
		r = requests.get(api_base_link+entered_location+remaining_link+api_key)
	except:
		raise
	j = json.loads(r.text)
	try:
		j["city"]["name"] = entered_location
		if j['cnt']==0:
			raise ValueError("Server Error")
	except:
		raise ValueError("Server Error")
	if j['cod']!='200':
		raise Exception("Not a valid entered_locationation")
	
	if flag:
		# since flag is set so previous data needs to be modified
		if debug:
			print json.dumps(j, indent=4)
			print "Note !! Previous data found but it was very old !!\n"
			
		try:
			f = open("data", "r")
			lst = f.readlines()
			f.close()
			lst[counter] = str(json.dumps(j)+"\n")
			f = open("data", "w")
			f.writelines(lst)
			f.close()
		except:
			if debug:
				print "ERROR !! Unable to open file, flag is set !!"
			pass
	else:
		# no previous data, so appending the json object with new data
		if debug:
			print json.dumps(j, indent=4)
			print "Note !! Previous data was not found !!\n"
		try:
			f = open("data", "a")
			f.write(json.dumps(j)+"\n")
			f.close()
		except:
			if debug:
				print "ERROR !! Unable to open file, flag is not set !!"
			pass
	return j
	
def get_data(entered_location):
	"""
	Used to get the weather details required for our project...
	Returns a dictionary from which details can be extracted easily...
	"""
	try:
		all_weather_data = {}
		current_weather_data = get_current_data(entered_location)
		predicted_weather_data = get_forecast_data(entered_location)
		
		#setting up the weather data dictionary

		#name of the location
		all_weather_data["name"] = current_weather_data["list"][0]["name"]
		all_weather_data["today"] = {}
		#get the current temperature
		all_weather_data["today"]["temp"] = current_weather_data["list"][0]["main"]["temp"]
		#get the max. temperature 
		all_weather_data["today"]["max"] = all_weather_data["today"]["temp"]
		#get the min. temperature
		all_weather_data["today"]["min"] = all_weather_data["today"]["temp"]
		#get the weather description
		all_weather_data["today"]["desc"] = current_weather_data["list"][0]["weather"][0]["description"]
		
		today = date.today()
		today_date = today
		t = timedelta(1)
		for i in range(1, 7):
			today_date = today_date+t
			s = today_date.strftime("%a")
			all_weather_data[i] = {}
			#name of the day of the week
			all_weather_data[i]["day"] = s
			#max. temperature
			all_weather_data[i]["max"] = '' 
			#min. temperature
			all_weather_data[i]["min"] = ''
		today_date = today

		counter = 0
		f = 1
		# storing max. and min. temp in the weather data dictionary
		for i in predicted_weather_data["list"]:
			if f:
				if today_date.isoformat()>i["dt_txt"].split()[0]:
					pass
				else:
					f=0
			elif today_date.isoformat()==i["dt_txt"].split()[0]:
				if today_date==today:
					x = all_weather_data['today']
				else:
					x = all_weather_data[counter]
				if x['max']=='':
					x['max'] = i["main"]["temp_max"]
					x['min'] = i['main']['temp_min']
				else:
					x['max'] = max(x['max'], i["main"]["temp_max"])
					x['min'] = min(x['min'], i['main']['temp_min'])
			else:
				counter += 1
				today_date = today_date+t
				x = all_weather_data[counter]
				x['max'] = i["main"]["temp_max"]
				x['min'] = i['main']['temp_min']
				x['description'] = i['weather'][0]['description']
		
		return all_weather_data
	except:
		raise

def cities():
	"""
	returns a list of valid locations, used to validate if the location entered by user is valid
	"""
	f = open('city.list.json', 'r')
	lst = []
	for line in f:
		j = json.loads(line)
		lst.append(j['name']+','+j['country'])
	return lst

def message_window(message_to_print, color):
	"""
	used to create a message window based on the current weatehr data
	background color emulates the hue of the light bulb, and it changes with the
	:param message_to_print: appropriate weather condition message
	:param color: bulb color
	"""
	window = Tk()
	#window.configure(background='red')

	def close_window():
		"""
		close the message window on press of a button
		"""
		window.destroy()
	frame = Frame(window, bg=color, width=5000, height=6000)
	l1 = Label(frame, text= message_to_print, font= "Verdana 16 bold")
	l1.pack()
	frame.pack()
	button = Button (frame, text = "Proceed to predicted data",command = close_window)
	button.pack(side= 'bottom')
	window.mainloop()


def bulb_glow(bulb_value):
	"""
	Gets the weather description, based on that changes the weather bulb color
	:param bulb_value: weather descrition of the location
	"""
	weather_dictionary = {'good_day_conditions':['clear day', 'clouds', 'Sky is Clear'],
						'thunderstorm_conditions':['thunderstorm with light rain', 'thunderstorm with rain', 'thunderstorm with heavy rain', 'light thunderstorm', 'thunderstorm with light drizzle', 'thunderstorm with drizzle', 'thunderstorm with heavy drizzle'], 
						'drizzle_conditions': ['light intensity drizzle', 'drizzle', 'heavy intensity drizzle', 'light intensity drizzle rain', 'drizzle rain', 'shower rain and drizzle', 'heavy shower rain and drizzle', 'shower drizzle'], 
						'rain_conditions': ['light rain', 'moderate rain', 'freezing rain', 'light intensity shower rain', 'shower rain'], 
						'snow_conditions': ['light snow', 'light rain and snow', 'rain and snow', 'light shower snow', 'shower snow'], 
						'atmosphere_conditions': ['mist', 'smoke', 'haze', 'snad,dust whirls', 'fog', 'sand', 'dust', 'volcanic ash', 'squalls'], 
						'clear_conditions': ['clear sky'], 
						'clouds_conditions': ['few clouds', 'scattered clouds', 'broken clouds', 'overcast clouds'], 
						'extreme_hot_cold_conditions': ['hot', 'cold', 'windy'], 
						'normal_conditions': ['calm', 'light breeze', 'gentle breeze', 'moderate breeze', 'fresh breeze', 'strong breeze', 'high wind,near gale', 'gale', 'severe gale'], 
						'extreme_conditions': ['violent storm', 'hurricane', 'storm', 'tornado', 'tropical storm', 'hail', 'heavy intensity shower rain','ragged shower rain', 'heavy intensity rain', 'very heavy rain', 'extreme rain','freezing rain', 'thunderstorm with heavy rain', 'heavy thunderstorm','thunderstorm with heavy drizzle']}
	if bulb_value in weather_dictionary['extreme_conditions']:
		message_to_print = "please take extreme caution, it is extremely " + bulb_value + " outside.....glow red bulb"
		message_window(message_to_print, '#FF0000')
	else:
		if bulb_value in weather_dictionary['thunderstorm_conditions']:
			message_to_print = "Hey, it is" + bulb_value + " outside, please take appropriate precautions....consider going out only if necessary"
			message_window(message_to_print, '#A9A9A9')
		elif bulb_value in weather_dictionary['drizzle_conditions']:
			message_to_print = "Hey, it is" + bulb_value + " outside.....you should enjoy outside, but don't forget to carry rain wear"
			message_window(message_to_print, '#AFEEEE')
		elif bulb_value in weather_dictionary['rain_conditions']:
			message_to_print =  "Hey, it is going to be " + bulb_value + " outside.....you should go outside with precautions and appropriate rain wear"
			message_window(message_to_print, '#0000CD')
		elif bulb_value in weather_dictionary['snow_conditions']:
			message_to_print = "Hey, it is going to be " + bulb_value + " outside.....you should be extremely cautious. Drive slowly and carefully"
			message_window(message_to_print, '#DCDCDC')
		elif bulb_value in weather_dictionary['atmosphere_conditions']:
			message_to_print = "Hey, it is going to be " + bulb_value + " outside..."
			message_window(message_to_print, '#808080')
		elif bulb_value in weather_dictionary['clear_conditions']:
			message_to_print = "Hey, it is going to be " + bulb_value + " outside.....its a really good weather to go on the beach !!"
			message_window(message_to_print, '#00BFFF')
		elif bulb_value in weather_dictionary['clouds_conditions']:
			message_to_print = "Hey, it is going to be " + bulb_value + " outside.....don;t fret and enjoy a good walk outside"
			message_window(message_to_print, '#708090')
		elif bulb_value in weather_dictionary['extreme_hot_cold_conditions']:
			message_to_print = "Hey, it is going to be " + bulb_value + " outside....go out only if needed"
			message_window(message_to_print, '#FF8C00')
		else:
			message_to_print = "Hey, it is going to be " + bulb_value + " outside....."
			message_window(message_to_print, '#FFFFFF')


if __name__=="__main__":
	cities()
	entered_location = raw_input("Enter your desired location: ")
	try:
		all_weather_data = get_data(entered_location)
		if all_weather_data['name'] == '':
			raise ValueError
		elif all_weather_data['name'].lower()!=entered_location.lower():
			print entered_location+" not found. The closest match is:"
		print
		print "Place: ", all_weather_data['name']
		print "Temp: ", all_weather_data['today']['temp']
		print "Min: ", all_weather_data['today']['min']
		print "Max: ", all_weather_data['today']['max']
		print "Description: ", all_weather_data['today']['desc']
		bulb_glow(all_weather_data['today']['desc'])
		for i in range(1, 5):
			print
			print "Day: ", all_weather_data[i]['day']
			print "Max: ", all_weather_data[i]['max']
			print "Min: ", all_weather_data[i]['min']
			print "Decription: ", all_weather_data[i]['description']	
	except requests.exceptions.ConnectionError:
		print 'Not connected'
	except:
		print 'Not a valid entered_locationation'
		raise
