import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer, time, event
from google.cloud import texttospeech
from gtts import gTTS

try:
	os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="key.json"
	google_api = True
except:
	google_api = False

class audio():
	
	def playAudio(file = "output.mp3"):
		mixer.init()
		mixer.music.load(file)
		mixer.music.play()
		while mixer.music.get_busy():
			time.Clock().tick(10)
		mixer.quit()
		os.remove("output.mp3")

	def createTTS(text):
		if google_api:
			client = texttospeech.TextToSpeechClient()
		
			synthesis_input = texttospeech.SynthesisInput(text=text)
		
			voice = texttospeech.VoiceSelectionParams(
			    language_code="ru-RU", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE, name="ru-RU-Wavenet-A")
		
			audio_config = texttospeech.AudioConfig(
			    audio_encoding=texttospeech.AudioEncoding.MP3, pitch=1.7, speaking_rate=1.05)
		
			response = client.synthesize_speech(
			    input=synthesis_input, voice=voice, audio_config=audio_config)
		
			with open("output.mp3", "wb") as out:
			    out.write(response.audio_content)

		else:
			tts = gTTS(text, 'ru', 'ru')
			tts.save("output.mp3")
