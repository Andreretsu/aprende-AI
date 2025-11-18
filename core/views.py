import os
import speech_recognition as sr
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from pydub import AudioSegment
from .ai_tutor import perguntar_ao_tutor

# --- CONFIGURAÇÃO BLINDADA DO FFMPEG ---
caminho_ffmpeg = str(settings.BASE_DIR)
os.environ["PATH"] += os.pathsep + caminho_ffmpeg
AudioSegment.converter = os.path.join(caminho_ffmpeg, "ffmpeg.exe")
AudioSegment.ffmpeg = os.path.join(caminho_ffmpeg, "ffmpeg.exe")
AudioSegment.ffprobe = os.path.join(caminho_ffmpeg, "ffprobe.exe")
# ---------------------------------------

def home(request):
    return render(request, 'index.html')

def processar_audio(request):
    if request.method == 'POST':
        audio_file = request.FILES.get('audio_data')
        
        if not audio_file:
            return JsonResponse({'erro': 'Nenhum áudio recebido'}, status=400)

        arquivo_webm = "temp_audio.webm"
        arquivo_wav = "temp_audio.wav"

        try:
            # 1. Salvar
            with open(arquivo_webm, 'wb+') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)

            # 2. Converter
            print("🔄 Convertendo áudio...")
            track = AudioSegment.from_file(arquivo_webm)
            track = track.set_frame_rate(16000).set_channels(1)
            
            # --- TRUQUE 1: Aumentar o volume (Gain) ---
            # Se seu mic for baixo, isso ajuda. (+10 decibéis)
            track = track + 10 
            
            track.export(arquivo_wav, format="wav")

            texto_usuario = ""
            resposta_ia = ""

            # 3. Reconhecer
            r = sr.Recognizer()
            with sr.AudioFile(arquivo_wav) as source:
                # --- TRUQUE 2: Calibrar Ruído ---
                # Ele escuta 0.5s de "silêncio" para entender o ambiente
                print("🔇 Calibrando ruído de fundo...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                
                print("🎤 Ouvindo...")
                audio_data = r.record(source)
                
                print("🧠 Enviando para Google...")
                # show_all=False garante que ele retorne só o melhor texto
                texto_usuario = r.recognize_google(audio_data, language='pt-BR')
                print(f"🗣️ Texto: {texto_usuario}")

            # 4. IA
            if texto_usuario:
                resposta_ia = perguntar_ao_tutor(texto_usuario)

            return JsonResponse({
                'texto': texto_usuario,
                'mensagem': resposta_ia
            })

        except sr.UnknownValueError:
            print("❌ Google não entendeu nada.")
            return JsonResponse({'mensagem': 'Não entendi. Fale um pouco mais alto.', 'texto': '???'})
        
        except Exception as e:
            print(f"❌ ERRO: {e}")
            return JsonResponse({'mensagem': 'Erro técnico.', 'texto': 'Erro'})
            
        finally:
            # --- TRUQUE 3: MODO ESPIÃO ---
            # Comentei a limpeza para você poder ouvir o arquivo.
            # Quando estiver tudo perfeito, você descomenta isso aqui.
            
            # if os.path.exists(arquivo_webm): os.remove(arquivo_webm)
            # if os.path.exists(arquivo_wav): os.remove(arquivo_wav)
            pass
    
    return JsonResponse({'erro': 'Método não permitido'}, status=405)