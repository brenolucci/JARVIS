import openai
from dotenv import load_dotenv

# Carrega chave da OpenAI e inicializa o cliente usando a env OPENAI_API_KEY
load_dotenv()
client = openai.OpenAI()

jarvisAtivo = True

def perguntar_ao_chatgpt(pergunta):
    resposta = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é Jarvis, um assistente pessoal educado e inteligente."},
            {"role": "user", "content": pergunta}
        ]
    )
    return resposta.choices[0].message.content


if __name__ == "__main__":
    while jarvisAtivo == True:
        
        pergunta = input('Digite sua pergunta: ')
        if pergunta == "sair":
            break

        resposta = perguntar_ao_chatgpt(pergunta)
        print("Resposta: ", resposta)