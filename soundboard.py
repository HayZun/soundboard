#!/usr/bin/python3
from flask import Flask, request, redirect, url_for
from gtts import gTTS
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    audio_file = request.files['audio_file']
    #verifier que le fichier audio est un MP3
    if audio_file.filename.split('.')[-1] != 'mp3':          
      #c'est pas un audio
      return redirect('/')
    else:
      titre = audio_file.filename.split('.')[0]
      audio_file.save(f'./sons/{titre}.mp3')
      return redirect('/')
    
@app.route('/stop', methods=['POST'])
def stop():
    print("stop")
    os.system("killall vlc")
    return redirect('/')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('Convertir en audio') == 'Convertir en audio':
            text = request.form['text']
            language = request.form['language']
            filename = 'audio.mp3'
            tts = gTTS(text=text, lang=language)
            tts.save(filename)
            os.system("cvlc --gain 1 --play-and-exit audio.mp3")
            os.remove("audio.mp3")
            return redirect('/')
        else:
            son = "'" + list(request.form.keys())[0] + ".mp3" + "'"
            print(f"{son}")
            os.system(f"cvlc --gain 1 --play-and-exit ./sons/{son}")
            return redirect('/')
    else:
        return HTML()

def HTML():
    
    header = '''
          <head>
    <title>Freeda</title>
    <style>
      body {
        text-align: center;
        font-family: Arial, sans-serif;
        background-color: #f2f2f2;
      }
      
      h1 {
        color: #4d4d4d;
        margin-top: 50px;
      }
      
      form {
        margin-top: 30px;
      }
      
      label {
        display: block;
        margin-top: 10px;
        color: #4d4d4d;
        font-weight: bold;
      }
      
      textarea {
        width: 80%;
        height: 150px;
        margin-top: 10px;
        padding: 5px;
        border-radius: 5px;
        border: 1px solid #ccc;
        font-family: Arial, sans-serif;
      }
      
      select {
        margin-top: 10px;
        padding: 5px;
        border-radius: 5px;
        border: 1px solid #ccc;
        font-family: Arial, sans-serif;
      }
      
      input[type="submit"] {
        margin-top: 20px;
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
      }
      
      input[type="submit"]:hover {
        background-color: #3e8e41;
      }
      
      .error {
        color: red;
        font-weight: bold;
        margin-top: 10px;
      }
    </style>
  </head>
        <body>
            <h1>Freeda</h1>
            <form method="post">
                <label for="text">Texte à convertir en audio :</label><br>
                <textarea id="text" name="text" rows="4" cols="50"></textarea><br>
                <label for="language">Langue :</label>
                <select id="language" name="language">
                        <option value="fr">French</option>
                        <option value="af">Afrikaans</option>
                        <option value="ar">Arabic</option>
                        <option value="bg">Bulgarian</option>
                        <option value="bn">Bengali</option>
                        <option value="bs">Bosnian</option>
                        <option value="ca">Catalan</option>
                        <option value="cs">Czech</option>
                        <option value="da">Danish</option>
                        <option value="de">German</option>
                        <option value="el">Greek</option>
                        <option value="en">English</option>
                        <option value="es">Spanish</option>
                        <option value="et">Estonian</option>
                        <option value="fi">Finnish</option>
                        <option value="gu">Gujarati</option>
                        <option value="hi">Hindi</option>
                        <option value="hr">Croatian</option>
                        <option value="hu">Hungarian</option>
                        <option value="id">Indonesian</option>
                        <option value="is">Icelandic</option>
                        <option value="it">Italian</option>
                        <option value="iw">Hebrew</option>
                        <option value="ja">Japanese</option>
                        <option value="jw">Javanese</option>
                        <option value="km">Khmer</option>
                        <option value="kn">Kannada</option>
                        <option value="ko">Korean</option>
                        <option value="la">Latin</option>
                        <option value="lv">Latvian</option>
                        <option value="ml">Malayalam</option>
                        <option value="mr">Marathi</option>
                        <option value="ms">Malay</option>
                        <option value="my">Myanmar (Burmese)</option>
                        <option value="ne">Nepali</option>
                        <option value="nl">Dutch</option>
                        <option value="no">Norwegian</option>
                        <option value="pl">Polish</option>
                        <option value="pt">Portuguese</option>
                        <option value="ro">Romanian</option>
                        <option value="ru">Russian</option>
                        <option value="si">Sinhala</option>
                        <option value="sk">Slovak</option>
                        <option value="sq">Albanian</option>
                        <option value="sr">Serbian</option>
                        <option value="su">Sundanese</option>
                        <option value="sv">Swedish</option>
                        <option value="sw">Swahili</option>
                        <option value="ta">Tamil</option>
                        <option value="te">Telugu</option>
                        <option value="th">Thai</option>
                        <option value="tl">Filipino</option>
                        <option value="tr">Turkish</option>
                        <option value="uk">Ukrainian</option>
                        <option value="ur">Urdu</option>
                        <option value="vi">Vietnamese</option>
                        <option value="zh-CN">Chinese (Simplified)</option>
                        <option value="zh-TW">Chinese (Mandarin/Taiwan)</option>
                        <option value="zh">Chinese (Mandarin)</option>
                </select><br>
                <input type="submit" name= "Convertir en audio" value="Convertir en audio">
            </form>
            <form method="post">'''


            #<form method="post">'''

    #récupérer les noms des fichiers dans le dossier sons
    but = []

    for file in os.listdir("sons"):
        if file.endswith(".mp3"):
            but.append(file[:-4])

    boutons = ''

    #créer les boutons
    for i in but:
        boutons += '<button type="submit" name="{}" value="{}">{}</button>'.format(i, i, i)

    stop = '''
    <form method="POST" action="/stop" style="display:none">
      <input type="hidden" name="image_clickee" value="True">
      <input type="submit" id="submit">
    </form>
    <img src="/static/stop.png"  onclick="document.getElementById('submit').click()">'''
    
    upload = '''</form>
    <form action="http://127.0.0.1:5000/upload" method="post" enctype="multipart/form-data">
              <input type="file" name="audio_file">
              <input type="submit" value="Upload">
            </form>
            <div id="button-container">
            </div>
        </body>'''
    
    return header + boutons + upload + stop

if __name__ == '__main__':
    app.run(debug=True)
