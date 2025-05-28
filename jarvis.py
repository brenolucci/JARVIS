import whisper
import sounddevice as sd
import numpy as np
import openai
import pyttsx3
import os
from scipy.io.wavfile import write
from dotenv import load_dotenv

# Carrega chave da OpenAI
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Inicializa Whisper
model = whisper.load_model("base")  # ou "tiny", "small", "medium", "large"

# Inicializa TTS
engine = pyttsx3.init()

def falar(texto):
    engine.say(texto)
    engine.runAndWait()
    

def gravar_audio(duracao=5, fs=16000):
    print("🎙️ Gravando...")
    audio = sd.rec(int(duracao * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    write("audio.wav", fs, audio)
    print("✅ Gravação finalizada.")
    return "audio.wav"

def transcrever_audio(caminho_audio):
    print("🧠 Transcrevendo com Whisper...")
    resultado = model.transcribe(caminho_audio, language="pt")
    texto = resultado["text"]
    print("Você disse:", texto)
    return texto.lower()

def perguntar_ao_chatgpt(pergunta):
    resposta = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é Jarvis, um assistente pessoal educado e inteligente."},
            {"role": "user", "content": pergunta}
        ]
    )
    return resposta.choices[0].message.content

# Loop principal
if __name__ == "__main__":
    falar("Jarvis está pronto. Diga 'Jarvis' para me chamar.")
    jarvis_ativo = False
    while True:
        caminho_audio = gravar_audio(duracao=5)
        texto = transcrever_audio(caminho_audio)

        if not texto.strip():
            continue

        if not jarvis_ativo:
            if "jarvis" in texto:
                jarvis_ativo = True
                falar("Estou ouvindo. Pode falar.")
        else:
            if "sair" in texto or "desligar" in texto:
                falar("Até mais!")
                jarvis_ativo = False
            else:
                resposta = perguntar_ao_chatgpt(texto)
                print("🤖 Jarvis:", resposta)
                falar(resposta)
