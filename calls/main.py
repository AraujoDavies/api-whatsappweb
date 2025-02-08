from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import pandas as pd
import requests
import json
import logging
import schedule
import time


logging.basicConfig(
  level=logging.WARNING,
  encoding='utf-8',
  format='%(asctime)s - %(levelname)s: %(message)s',
)

load_dotenv()
engine = create_engine(os.getenv('DATABASE_URI'))


def envio(chat_name, mensagem):
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


def flash_diario():
  with engine.begin() as conn:
      data = conn.execute(text('SELECT * FROM academia.flash;')).fetchall()

  df = pd.DataFrame(data)

  mensagem = '*Flash diário*\n\n'
  for index in df.index:
      for col in df.columns:
          mensagem += f"{col}: {df[col][index]}\n"
      mensagem += '\n'

  CHAT_NAME = 'Sla'
  for i in range(5):
    enviado = envio(CHAT_NAME, mensagem)
    if enviado == "SUCESSO": 
      break
  
  logging.warning('flash_diario: %s', enviado) 


# envios schedulados
flash_diario()

schedule.every(2).hours.do(flash_diario)

while True:
    schedule.run_pending()
    time.sleep(1)