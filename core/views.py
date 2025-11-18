from django.shortcuts import render
from django.http import JsonResponse
import speech_recognition as sr # Exemplo da lib de IA (teria que instalar)

def home(request):
    # Apenas mostra o HTML
    return render(request, 'index.html')

def processar_audio(request):
    if request.method == 'POST':
        # 1. Pega o arquivo de áudio enviado pelo JS
        audio_file = request.FILES.get('audio_data')

        if not audio_file:
            return JsonResponse({'erro': 'Nenhum áudio recebido'}, status=400)

        # --- AQUI ENTRARIA SUA IA (Exemplo Simulado) ---
        # recognizer = sr.Recognizer()
        # audio = sr.AudioFile(audio_file)
        # texto = recognizer.recognize_google(audio, language='pt-BR')
        
        # Simulando uma resposta da IA para o teste:
        texto_reconhecido = "Casa" 
        acertou = True
        # -----------------------------------------------

        # 2. Retorna um JSON (não um HTML)
        return JsonResponse({
            'texto': texto_reconhecido,
            'acertou': acertou,
            'mensagem': 'Parabéns! Você leu corretamente.'
        })
    
    return JsonResponse({'erro': 'Método não permitido'}, status=405)
