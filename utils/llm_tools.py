from 





import requests
import json

url = "http://localhost:11434/api/chat"

payload = json.dumps({
  "model": "gemma3",
  "messages": [
    {
      "role": "system",
      "content": "Você é um auxiliar administrativo, seu nome é Peão, você está responsável por análisar as mensagens que recebemos no whatsapp da empresa e identifcar quais mensagens foram enviadas para o destinatario errado, com base no que o destinatario respondeu, o usuário mandará um json para você no formato { \"telefone\": \" 5585992058133\", \"message\": \"ola este numero nao me pertence, favor retirar da sua lista\" }, ao concluir a análise, caso identifique que está errado, retornar somente um json, por exemplo: { \"telefone\": \" 5585992058133\", \"status\": \"errado\"}, Caso não identifique que o número está errado, responda somente um False"
    },
    {
      "role": "user",
      "content": " {\"numero\": \"558590909292\", \"mensagem\": \"Dia! Esse contato não a essa pessoa da mensagem!}"
    }
  ],
  "stream": False
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
