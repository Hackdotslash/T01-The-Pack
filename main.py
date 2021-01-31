import record
import voice2text
import requests
import moviepy.editor as mp
import shutil
import os
import time
from flask import Flask
from google_trans_new import google_translator
translator = google_translator()
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def translate(text):
    return translator.translate(text)

@app.route("/detect")
def main():
    file_name = "temp.wav"
    shutil.rmtree("data/")
    os.mkdir("data")

    record.record(file_name)

    spoken_text = voice2text.retrieve_transcript("temp.wav")
    print(spoken_text)
    spoken_text = translate(spoken_text)

    list_words = [a.lower().strip("!,.?") for a in spoken_text.split()]

    modified_urls = [ i + "/" + i + "-abc.mp4" if len(i) == 1 else i[0] + "/" + i + ".mp4" if i != "bye" else "bye-wave.mp4" for i in list_words]

    # Read URLs from handspeak.com
    for i, url in enumerate(modified_urls):
        r = requests.get("https://handspeak.com/word/" + url)
        print("https://handspeak.com/word/" + url)
        if r.text[:15] == "<!DOCTYPE html>":
            letters = list(list_words[i])
            c = []
            for l in letters:
                if l.isalpha():
                    c.append(mp.VideoFileClip("letters/%s-abc.mp4" % l).resize(height=320, width=240).speedx(factor=2))
            f = mp.concatenate_videoclips(c, method="compose")
            f.write_videofile("data/%d.mp4" % i)
        else:
            f = open("data/%d.mp4" % i, 'wb')
            for chunk in r.iter_content(chunk_size=255):
                if chunk:
                    f.write(chunk)
            f.close()

    clips = []
    for j in range(len(modified_urls)):
        clips.append(mp.VideoFileClip("data/%d.mp4" % j).resize(height=320, width=240))

    final_clip = mp.concatenate_videoclips(clips, method="compose")

    final_clip.write_videofile("public/final_clip.mp4")
    time.sleep(1)
    return spoken_text

@app.route('/realtime')
def realtime():
    text='sky'
    url = text[0]+'/'+ text +'.mp4'
    r = requests.get("https://handspeak.com/word/" + url)
    f = open("data/%s.mp4" % text, 'wb')
    for chunk in r.iter_content(chunk_size=255):
        if chunk:
            f.write(chunk)
    f.close()
    return 'done'


if __name__ == "__main__":
	app.run(host='127.0.0.1',port=6789)
