import os
import schedule
import time

def backup():
    os.system("mongodump --host=node1 --port=27017 --out=/path/to/backup")

# Agendando o backup para rodar todos os dias às 2 da manhã
schedule.every().day.at("02:00").do(backup)

while True:
    schedule.run_pending()
    time.sleep(1)
