from flash_models import flash_personalizado_weebet
import schedule
import time

import logging

logging.basicConfig(
  level=logging.WARNING,
  encoding='utf-8',
  format='%(asctime)s - %(levelname)s: %(message)s',
)


# envios schedulados
chat_name = 'Flash Pinbet'
comando_sql = "CALL pinbet.proc_flash_whatsapp_15min;"
flash_personalizado_weebet(chat_name, comando_sql)
schedule.every(15).minutes.do(flash_personalizado_weebet, chat_name=chat_name, comando_sql=comando_sql)


chat_name = 'Flash APF'
comando_sql = "CALL apostefacil.proc_flash_whatsapp_15min;"
flash_personalizado_weebet(chat_name, comando_sql)
schedule.every(15).minutes.do(flash_personalizado_weebet, chat_name=chat_name, comando_sql=comando_sql)


while True:
    schedule.run_pending()
    time.sleep(30)