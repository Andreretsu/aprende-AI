import wave
import json
import os
from dotenv import load_dotenv
from django.http import JsonResponse, FileResponse
from django.shortcuts import render
from vosk import Model, KaldiRecognizer
from gtts import gTTS
from google import genai
from django.views.decorators.csrf import csrf_exempt
from pydub import AudioSegment


#load_dotenv()
#client = genai.Client()

# carregar modelo do vosk 1x só
vosk_model = Model("model")  


def index(request):
    return render(request, "index.html")


def transcribe(path):
    wf = wave.open(path, "rb")
    rec = KaldiRecognizer(vosk_model, wf.getframerate())
    text = ""

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            text = json.loads(rec.Result()).get("text", "")

    return text


def ai_answer(prompt):
    response = client.models.generate_content(
    model="gemini-2.5-flash", contents=prompt
    )
    print(response.text)
    return response.text


def synthesize(text):
    if not text or not text.strip():
        text = "Não foi possível gerar áudio."
    tts = gTTS(text, lang="pt")
    tts.save("response.mp3")
    return "response.mp3"



def convert_to_wav(input_path, output_path="input.wav"):
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(16000)
    audio.export(output_path, format="wav")
    return output_path

@csrf_exempt
def talk(request):
    try:
        audio_file = request.FILES["audio"]

        # salva arquivo original (webm)
        with open("input.webm", "wb") as f:
            for chunk in audio_file.chunks():
                f.write(chunk)

        # converte para wav
        wav_path = convert_to_wav("input.webm", "input.wav")

        # STT
        prompt = transcribe(wav_path)
        print("PROMPT DO USUARIO: ", prompt)

        if not prompt.strip():
            reply = "Não consegui te ouvir, pode repetir?"
        else:
            reply = prompt
            # IA (Gemini)
            #reply = ai_answer(prompt)

        # TTS
        path = synthesize(reply) #aqui seria a reply

        return FileResponse(open(path, "rb"), content_type="audio/mpeg")

    except Exception as e:
        print("\n\nERRO >>>", e, "\n\n")
        return JsonResponse({"error": str(e)}, status=500)


# Create your views here.
