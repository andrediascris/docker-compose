import os
import subprocess
import schedule
import time
import threading

import os

def executar_backup(backup_path, mongodump_path):
    print("🗃️ Tentando executar mongodump padrão...")

    try:
        subprocess.run(
            ["mongodump", "--host=localhost", "--port=27017", f"--out={backup_path}"],
            check=True
        )
        print("Backup concluído com mongodump do sistema.")
    except FileNotFoundError:
        print("mongodump não está no PATH. Tentando com caminho completo...")
        try:
            subprocess.run(
                [mongodump_path, "--host=localhost", "--port=27017", f"--out={backup_path}"],
                check=True
            )
            print("Backup concluído com caminho alternativo.")
        except Exception as e:
            print("Falha ao realizar o backup com caminho alternativo.")
            print(f"Erro: {e}")
    except Exception as e:
        print("Falha ao realizar o backup com mongodump padrão.")
        print(f"Erro: {e}")



def iniciar_agendador_em_thread(hora="00:00", backup_path="", mongodump_path=""):
    def agendar():
        schedule.every().day.at(hora).do(executar_backup, backup_path, mongodump_path)

        print(f"🔄 Backup agendado para todos os dias às {hora}. Rodando em segundo plano...")
        while True:
            schedule.run_pending()
            time.sleep(1)

    thread = threading.Thread(target=agendar, daemon=True)
    thread.start()
