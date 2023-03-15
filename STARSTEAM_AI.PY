import speech_recognition as sr
from playsound import playsound
from voicevox import Client
from googletrans import Translator
import asyncio
from pygame import mixer
import time
import keyboard 
from setting import Key
import logging
import shutil
import os
import datetime

r = sr.Recognizer()
translator = Translator()
getkey = Key()

logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


async def main():
    async with Client() as client:
        with sr.Microphone() as source: 
            playsound("./sound.wav")
            audio = r.record(source, duration=3)
            playsound("./sound.wav")

            try:
                text = r.recognize_google(audio, language="th")
            except:
                text = "ขอโทษค่ะ"

        translation = translator.translate(text, src='th', dest='ja')
        
        
        print("TH : " + text)
        print("JA : " + translation.text)

        audio_query = await client.create_audio_query(
            translation.text, speaker=20 #20 #11
        )
        with open('./output.wav', "wb") as f:
            f.write(await audio_query.synthesis())

    now = datetime.datetime.now()
    new_filename = "output_{}_{}.wav".format(now.strftime("%Y-%m-%d"), now.strftime("%H-%M-%S"))
    os.rename("output.wav", new_filename)

    old_path = "./"+new_filename
    new_path = "./cache/"+new_filename
    shutil.move(old_path, new_path)

    # mixer.init(devicename = 'CABLE Input (VB-Audio Virtual Cable)')
    mixer.init()
    mixer.music.load('./cache/'+new_filename)
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(1)
    
    

try:
    print("Change Thai Voice To Japanese Anime Voice System")
    print("DEV. : STARSTEAM_X")
    print(f"PUSH THE {getkey} KEY")

    while True :
        if __name__ == "__main__":
            if keyboard.is_pressed(getkey): 
                asyncio.run(main())
            time.sleep(0.1)
        time.sleep(0.1)
        
except Exception as e:
    print(f"Error: {e}")
    logging.error(str(e))