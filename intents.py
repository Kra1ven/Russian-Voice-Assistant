import json
import os
from process import audio
from fuzzywuzzy import process, fuzz
from functions import functions
from math import floor
import config


def createJson():
	intents_json = {
		"main": {
			"launch": ["открой приложение", "запусти приложение"],
			"close_actv": ["закрой окно", "закрой активное окно", "закрой приложение"],
			"msg": ["напиши человеку", "отправь сообщение человеку"],
			"stop": ["забей", "стоп", "отстань"],
			"search": ["найди", "поиск"],
			"weather": ["какая сейчас погода" , "погода сейчас", "погода"],
			"screenshot": ["сделай скриншот", "сделай скриншот окна"],
			"copy": ["скопируй всё", "скопируй и добавь в заметки"],
			"free_mode": ["свободный режим", "свободный режим"]
		},

		"launch": {
			"steam://run/730": ["контр страйк", "кс го", "контру", "кс"],
			"steam://run/570": ["дота", "дота 2", "доту"]
		},

		"smalltalk": {
			"how_doing": ["как у тебя дела"],
			"what_doing": ["что делаешь"]
		},

		"smalltalk_res": {
			"how_doing": ["хорошо, а у тебя?"],
			"what_doing": ["работаю беспрерывно"]
		},

		"copy": {
	 		"copy_all": ["скопируй всё", "скопируй весь текст"],
			"copy_add_note": ["скопируй и добавь в заметки", "скопируй текст добавь в заметки"]
		},

		"enable/disable": {
			"enable": ["включи", "вруби"],
			"disable": ["выключи", "выруби"]
		}
	}

	with open('intents.json', 'w', encoding='utf-8') as outfile:
		json.dump(intents_json, outfile, indent=4, ensure_ascii=False)

if not os.path.isfile("intents.json"):
	createJson()

class intents():

	def initLoad():

		with open("intents.json", encoding='utf-8') as json_file:
			config.intents = json.load(json_file)

	def strToDict(text):
		return json.loads(text)

	def extractIntent(text, intents, scorer, notify = None):
		extracted_intents = process.extract(text, intents, scorer=scorer)

		counter = 0
		check = extracted_intents[0][1]
		for intent in extracted_intents:
			if intent[1] >= check and intent[1] > 80:
				counter += 1

		if counter == 0 or counter > 1:
			if notify != None:
				audio.createTTS(notify)
				audio.playAudio()
			return ["", 0, ""]
		else:
			return extracted_intents[0]


	def getMainIntent(text):
		main_check = intents.extractIntent(text, config.intents["main"], fuzz.WRatio, None)
		smalltalk_check = intents.extractIntent(text, config.intents["smalltalk"], fuzz.WRatio, None)


		intents_check = {
			main_check[2]: main_check[0],
			"smalltalk": smalltalk_check[0]
		}

		return intents.extractIntent(text, intents_check, fuzz.WRatio, "Я вас не понимаю")[2]

	def clearKeywords(text, intent):
		for i in config.intents["main"][intent]:
			for word in i.split(" "):
				text = text.replace(word, "")
		return text

	def processMainIntent(intent, text, handle = None):

		if intent == "launch":
			text = intents.clearKeywords(text, intent)
			app = intents.extractIntent(text, config.intents[intent], fuzz.token_set_ratio, "Я не поняла что запустить")
			if app:
				functions.runApp(app[2])

		if intent == "close_actv":
			functions.closeApp(handle)

		if intent == "smalltalk":
			tag = intents.extractIntent(text, config.intents[intent], scorer=fuzz.token_set_ratio)[2]
			ans = config.intents["smalltalk_res"][tag]

			audio.createTTS(ans[0])
			audio.playAudio()

		if intent == "weather":
			weather = functions.getWeather()

			def changeEnd(wthr):
				return f"{floor(wthr)} градус" if str(floor(wthr))[-1] == "1" else f"{floor(wthr)} градусов"

			weather_now = changeEnd(weather['temp'])

			weather_min = changeEnd(weather['temp_min'])

			text = f"Сейчас {weather_now}, минимальная температура на сегодня, {weather_min}"
			audio.createTTS(text)
			audio.playAudio()

		if intent == "screenshot":
			functions.screenshot()

		if intent == "free_mode":
			text = intents.clearKeywords(text, intent)
			intent = intents.extractIntent(text, config.intents['enable/disable'], fuzz.token_set_ratio, "Включить или выключить свободный режим")[2]
			if intent == "enable":
				config.free_mode = True
			elif intent == "disable":
				config.free_mode = False
