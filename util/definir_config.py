import json
import os
from collections import namedtuple

def definir_config():
    db = input("Digite o nome do banco: ")
    table = input("Digite o nome da tabela: ")
    url_backup = input("Digite a url de backup")
    url_mongodump = input("Digite o caminho da pasta do mongodb-database-tools (caso o sistema não encontre o mongodump e o voce tenha o mongodb-database-tools instalado) ")
    
    config = {
        "db": db,
        "table": table,
        "backup": url_backup,
        "mongodump": url_mongodump
    }

   
    caminho_pasta = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    os.makedirs(caminho_pasta, exist_ok=True)

   
    caminho_arquivo = os.path.join(caminho_pasta, "dados.json")

   
    with open(caminho_arquivo, "w") as f:
        json.dump(config, f, indent=4)

    print(f"✅ Configurações salvas em: {caminho_arquivo}")


import json
import os

def carregar_config():
    caminho_arquivo = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "dados.json"))

    try:
        with open(caminho_arquivo, "r") as f:
            config = json.load(f)
            Config = namedtuple("Config", ["db", "table", "backup", "mongodump"])
            return Config(
                db=config["db"],
                table=config["table"],
                backup=config.get("backup"),
                mongodump=config.get("mongodump")
            )
    except FileNotFoundError:
        print("Arquivo de configuração não encontrado.")
        return None
    except KeyError as e:
        print(f"Erro na estrutura do arquivo JSON. Campo faltando: {e}")
        return None