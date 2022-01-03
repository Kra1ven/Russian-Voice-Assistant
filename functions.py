import keyboard
import subprocess
import win32con   
from win32gui import PostMessage, GetForegroundWindow
from time import sleep
import pyowm
import geocoder

class functions(object):

	def typeText(txt):
		keyboard.write(txt, delay=0.1)

	def copyAll():
		keyboard.press_and_release('ctrl+a, ctrl+c')

	def runApp(app):
		subprocess.run(f"cmd /c start {app}", shell=False)

	def closeApp(handle):
		PostMessage(handle,win32con.WM_CLOSE,0,0)

	def getWeather():
		g = geocoder.ip('me')
		owm = pyowm.OWM("85623e53736a17f4c27f7d48ba0a86e5")
		mgr = owm.weather_manager()
		observation = mgr.weather_at_place(f'{g.city}, {g.country}')
		w = observation.weather
		w.temperature('celsius') 
		return w.temperature('celsius')

	def screenshot():
		keyboard.press_and_release('Alt + PrtScn')
		