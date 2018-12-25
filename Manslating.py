
from google.cloud import texttospeech
from flask import Flask, render_template
import os
import speech_recognition as sr
import subprocess

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "ManslatingSecrets.json"

app = Flask(__name__)

@app.route("/home")
def home():
    return render_template("home.html")

## rendering the HTML page which has the button
@app.route('/json')
def json():
    return render_template('json.html')

## background process happening without any refreshing
@app.route('/background_process_test')
def background_process_test():
    manslate()
    return "nothing"

def explicit():
    from google.cloud import storage

    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json(
        'ManslatingSecrets.json')

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)

def create_wav_audio_file(text, out_filename):
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)

    # TODO: Make voice more manly

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # The response's audio_content is binary.
    with open(out_filename, 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        # print('Audio content written to file "{0}.wav"'.format(out_filename))

def say_from_file(audio_file):
    subprocess.call(['afplay', audio_file])

test_filename = "manslation_test.wav"

r = sr.Recognizer()
mic = sr.Microphone()

def manslate():
    with mic as source:
        # r.adjust_for_ambient_noise(source)
        print('Ready. Go!\n')
        audio = r.listen(source)
        print('...thanks! Transcribing...\n')
        transcript = r.recognize_google(audio)
        print('Transcription: {0}\n'.format(transcript))
        print("...done. Creating Manslation...\n")
        create_wav_audio_file(transcript, test_filename)
        print("...done. Speaking Manslation...\n")
        say_from_file(test_filename)
        print("...done! :-)")

if __name__ == "__main__":
    app.run(debug=True)
    
### Page exists on googlemanslate.com and says "Welcome to Google Manslate! Press this button to start:" (button)
### Button calls manslate function from this script.
### On button press, display message: "Please speak!"
### Then run line 80 in this script "audio = r.listen(source)"
### After line 82 runs (transcript = r.recognize_google(audio)), display message: "Manslating..."
### After line 85 runs (create_wav_audio_file(transcript, test_filename)), display message: "Speaking Manslation!"
### After line 87 runs (say_from_file(test_filename)), display message: "Enjoy being heard :-)"
