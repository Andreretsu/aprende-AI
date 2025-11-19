from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
import os
from gtts import gTTS
import random
import time

# Lista expandida de palavras para praticar (sem repetição)
PALAVRAS_PRATICA = [
    # Palavras básicas
    'casa', 'bola', 'gato', 'cachorro', 'livro', 'mesa', 'cadeira', 'porta', 'janela', 'carro',
    'sol', 'lua', 'estrela', 'céu', 'nuvem', 'chuva', 'vento', 'mar', 'rio', 'lago',
    'água', 'fogo', 'terra', 'ar', 'pedra', 'areia', 'montanha', 'floresta', 'árvore', 'flor',
    
    # Emoções e sentimentos
    'amor', 'paz', 'feliz', 'alegria', 'triste', 'raiva', 'medo', 'calma', 'sonho', 'esperança',
    
    # Família
    'mãe', 'pai', 'filho', 'filha', 'bebê', 'avó', 'avô', 'irmão', 'irmã', 'família',
    
    # Cores
    'azul', 'verde', 'vermelho', 'amarelo', 'rosa', 'roxo', 'preto', 'branco', 'cinza', 'laranja',
    
    # Animais
    'pássaro', 'peixe', 'leão', 'tigre', 'elefante', 'macaco', 'cavalo', 'vaca', 'porco', 'galinha',
    'rato', 'coelho', 'urso', 'lobo', 'raposa', 'cobra', 'sapo', 'borboleta', 'abelha', 'formiga',
    
    # Comidas
    'pão', 'leite', 'arroz', 'feijão', 'carne', 'frango', 'peixe', 'ovo', 'queijo', 'manteiga',
    'maçã', 'banana', 'laranja', 'uva', 'melancia', 'morango', 'tomate', 'batata', 'cenoura', 'alface',
    
    # Objetos do dia a dia
    'telefone', 'relógio', 'sapato', 'roupa', 'camisa', 'calça', 'vestido', 'chapéu', 'bolsa', 'chave',
    'prato', 'copo', 'garfo', 'faca', 'colher', 'panela', 'fogão', 'geladeira', 'cama', 'sofá',
    
    # Ações
    'andar', 'correr', 'pular', 'dormir', 'comer', 'beber', 'falar', 'ouvir', 'ver', 'tocar',
    'ler', 'escrever', 'desenhar', 'pintar', 'cantar', 'dançar', 'jogar', 'estudar', 'trabalhar', 'brincar'
]

# Variável global para controlar palavras já usadas
palavras_usadas = []

def home(request):
    """Página inicial do projeto"""
    return render(request, 'core/home.html')

@api_view(['POST'])
def stt_view(request):
    """Speech-to-Text usando Google Speech Recognition (online)"""
    print("=" * 50)
    print("=== INÍCIO STT ===")
    
    audio_file = request.FILES.get('audio')
    palavra_esperada = request.data.get('palavra_esperada', '').lower().strip()
    
    print(f"Arquivo recebido: {audio_file}")
    print(f"Palavra esperada: {palavra_esperada}")
    
    if not audio_file:
        print("ERRO: Nenhum arquivo de áudio enviado")
        return Response({'error': 'Nenhum arquivo de áudio enviado'}, status=400)
    
    temp_audio = 'temp_original.wav'
    temp_converted = 'temp_converted.wav'
    
    try:
        print("1. Salvando arquivo...")
        with open(temp_audio, 'wb') as f:
            f.write(audio_file.read())
        print(f"   Arquivo salvo: {os.path.getsize(temp_audio)} bytes")
        
        print("2. Convertendo áudio...")
        from pydub import AudioSegment
        audio = AudioSegment.from_file(temp_audio)
        audio = audio.set_frame_rate(16000)
        audio = audio.set_channels(1)
        audio = audio.set_sample_width(2)
        audio.export(temp_converted, format='wav')
        print(f"   Áudio convertido: {os.path.getsize(temp_converted)} bytes")
        
        print("3. Iniciando reconhecimento...")
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        
        # Abre e fecha o arquivo corretamente
        audio_file_obj = sr.AudioFile(temp_converted)
        with audio_file_obj as source:
            print("   Ajustando para ruído ambiente...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("   Gravando áudio...")
            audio_data = recognizer.record(source)
        
        # Aguarda para garantir que o arquivo foi fechado
        time.sleep(0.3)
        
        print("   Enviando para Google Speech Recognition...")
        try:
            texto_completo = recognizer.recognize_google(audio_data, language='pt-BR').lower().strip()
            print(f"   ✅ Reconhecido: '{texto_completo}'")
        except sr.UnknownValueError:
            print("   ⚠️ Google não entendeu o áudio")
            time.sleep(0.5)
            
            try:
                if os.path.exists(temp_audio):
                    os.remove(temp_audio)
                if os.path.exists(temp_converted):
                    os.remove(temp_converted)
            except Exception as e:
                print(f"   Aviso ao deletar: {e}")
                
            return Response({
                'transcricao': '',
                'acertou': False,
                'mensagem': 'Nenhuma fala detectada. Fale mais alto e claramente.'
            })
        except sr.RequestError as e:
            print(f"   ❌ Erro de conexão: {e}")
            time.sleep(0.5)
            
            try:
                if os.path.exists(temp_audio):
                    os.remove(temp_audio)
                if os.path.exists(temp_converted):
                    os.remove(temp_converted)
            except Exception as e:
                print(f"   Aviso ao deletar: {e}")
                
            return Response({
                'error': 'Erro ao conectar com o serviço de reconhecimento. Verifique sua internet.'
            }, status=500)
        
        print("4. Limpando arquivos temporários...")
        time.sleep(0.5)
        
        try:
            if os.path.exists(temp_audio):
                os.remove(temp_audio)
            if os.path.exists(temp_converted):
                os.remove(temp_converted)
        except Exception as e:
            print(f"   Aviso: Não conseguiu deletar arquivos temporários: {e}")
        
        print("5. Verificando resposta...")
        palavras_detectadas = texto_completo.split()
        acertou = (
            palavra_esperada == texto_completo or 
            palavra_esperada in palavras_detectadas or
            any(palavra_esperada in palavra for palavra in palavras_detectadas)
        )
        
        print(f"   Palavra esperada: '{palavra_esperada}'")
        print(f"   Acertou: {acertou}")
        print("=" * 50)
        
        return Response({
            'transcricao': texto_completo,
            'palavra_esperada': palavra_esperada,
            'acertou': acertou,
            'mensagem': '🎉 Parabéns! Você acertou!' if acertou else f'❌ Você disse "{texto_completo}". Tente novamente.'
        })
        
    except Exception as e:
        print(f"❌ ERRO FATAL: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        
        time.sleep(0.5)
        
        try:
            if os.path.exists(temp_audio):
                os.remove(temp_audio)
            if os.path.exists(temp_converted):
                os.remove(temp_converted)
        except Exception as cleanup_error:
            print(f"   Erro ao limpar: {cleanup_error}")
            
        return Response({'error': f'Erro ao processar áudio: {str(e)}'}, status=500)

@api_view(['POST'])
def tts_view(request):
    """Text-to-Speech: Converte texto em áudio"""
    texto = request.data.get('texto')
    if not texto:
        return Response({'error': 'Texto não enviado'}, status=400)
    
    try:
        tts = gTTS(text=texto, lang='pt')
        audio_path = 'saida.mp3'
        tts.save(audio_path)
        
        with open(audio_path, 'rb') as f:
            audio_data = f.read()
        
        os.remove(audio_path)
        
        return HttpResponse(audio_data, content_type='audio/mpeg')
        
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def nova_palavra(request):
    """Retorna uma palavra aleatória SEM REPETIÇÃO"""
    global palavras_usadas
    
    if len(palavras_usadas) >= len(PALAVRAS_PRATICA):
        palavras_usadas = []
    
    palavras_disponiveis = [p for p in PALAVRAS_PRATICA if p not in palavras_usadas]
    palavra = random.choice(palavras_disponiveis)
    palavras_usadas.append(palavra)
    
    return Response({
        'palavra': palavra,
        'progresso': f'{len(palavras_usadas)}/{len(PALAVRAS_PRATICA)}'
    })

@api_view(['POST'])
def resetar_palavras(request):
    """Reseta o progresso de palavras"""
    global palavras_usadas
    palavras_usadas = []
    return Response({'mensagem': 'Progresso resetado com sucesso!'})
