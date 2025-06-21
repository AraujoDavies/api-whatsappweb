from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import requests
import json


load_dotenv('pass.env')
engine = create_engine(os.getenv('DATABASE_URI_PROD'))


def envio(chat_name, mensagem):
  """
    Envio no whatsapp com API.
  """
  for i in range(2):
    try:
      # abrir whatsapp -> Response: Browser is open OR browser already running
      url = "http://localhost:8910/start?phone_number=2"
      response = requests.request("GET", url)
      if "Browser is open" not in response.text and "browser already running" not in response.text:
        return f'Erro ao abrir chrome: {response.text}'

      # encontrar o chat -> Response: Chat found.
      url = "http://localhost:8910/find-chat"
      payload = json.dumps({
        "phone_number": "2",
        "chat_name": chat_name
      })
      response = requests.request("POST", url, data=payload)
      if 'Chat found.' not in response.text:
        return f'Erro ao localizar chat: {response.text}'

      # enviar a mensagem -> response: Message sended
      url = "http://localhost:8910/send-message"
      payload = json.dumps({
        "phone_number": "2",
        "message": mensagem
      })
      response = requests.request("POST", url, data=payload)
      if 'Message sended' not in response.text:
        return f'Erro ao enviar mensagem: {response.text}'
      
      return "SUCESSO"
    except:
      pass

  return 'EXCEPT'