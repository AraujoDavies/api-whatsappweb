from flash_models import flash_personalizado_pinbet
import schedule
import time

import logging

logging.basicConfig(
  level=logging.WARNING,
  encoding='utf-8',
  format='%(asctime)s - %(levelname)s: %(message)s',
)


# envios schedulados
flash_personalizado_pinbet()

schedule.every(15).minutes.do(flash_personalizado_pinbet)

while True:
    schedule.run_pending()
    time.sleep(30)