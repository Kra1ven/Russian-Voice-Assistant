import queue
import sounddevice as sd
import vosk
import sys
from timeit import default_timer as timer
from intents import intents as intent_cls
from win32gui import GetForegroundWindow
import config


t0 = ""
t1 = ""
spotted = False


def getWords(intents):
	main_keys = intents.keys()
	sents = []
	for i in main_keys:
		if i != 'smalltalk_res':
			lower_keys = intents[i].keys()
			for j in lower_keys:
				sents += intents[i][j]

	return tuple(sents)

def wakeword():

	global t0, t1, spotted
	
	q = queue.Queue()
	device_info = sd.query_devices(None, 'input')
	samplerate = int(device_info['default_samplerate'])
	model = vosk.Model("model")

	def callback(indata, frames, time, status):
		if status:
			print(status, file=sys.stderr)
		q.put(bytes(indata))

	intent_cls.initLoad()
	words = getWords(config.intents)
	string = '", "'.join(words)
	handle = GetForegroundWindow()

	with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=None, dtype='int16', channels=1, callback=callback):
		rec = vosk.KaldiRecognizer(model, samplerate, f'["{string}", "лиза", "[unk]"]')

		while True:

			data = q.get()
			if rec.AcceptWaveform(data):
				x = rec.Result()
				text = intent_cls.strToDict(x)['text'].replace("лиза", "").replace("[unk]", "")

				if "лиза" in x and text != "" or config.free_mode and text != "":
					t1 = timer()
					print(t1-t0)
					spotted = False

					print(text)

					main_intent = intent_cls.getMainIntent(text)
					print(handle)

					print(main_intent)
					if main_intent != "":
						intent = intent_cls.processMainIntent(main_intent, text, handle)

			else:
				y = rec.PartialResult()
				print(y)

				if "лиза" in y or config.free_mode:
					if not spotted:
						handle = GetForegroundWindow()
						spotted = True
						t0 = timer()

wakeword()
