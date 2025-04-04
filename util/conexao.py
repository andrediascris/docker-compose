
import subprocess
import json
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure

def listar_portas_dos_mongos():
    try:
        resultado = subprocess.check_output('docker ps --format "{{json .}}"', shell=True)

        linhas = resultado.decode("utf-8").strip().splitlines()
        
        portas = []

        for linha in linhas:
            container = json.loads(linha)
            if "mongo" in container["Image"].lower():
                porta_map = container["Ports"]
                if "->27017" in porta_map:
                    externa = porta_map.split(":")[1].split("->")[0]
                    portas.append(int(externa))

        return portas

    except Exception as e:
        print(f"Erro ao listar containers Docker: {e}")
        return []

def encontrar_primario(portas):
    for porta in portas:
        uri_sem_auth = f"mongodb://localhost:{porta}/?directConnection=true&serverSelectionTimeoutMS=2000"
        try:
            client = MongoClient(uri_sem_auth)
            info = client.admin.command("hello")

            if info.get("isWritablePrimary") or info.get("ismaster"):
                print(f"[OK] PRIMARY encontrado: {uri_sem_auth}")
                return uri_sem_auth

        except OperationFailure as auth_error:
            print(f"Porta {porta} exige autenticação.")
            # Tenta com credenciais padrão
            uri_com_auth = f"mongodb://admin:adminCorp@localhost:{porta}/admin?directConnection=true&serverSelectionTimeoutMS=2000"

            try:
                client = MongoClient(uri_com_auth)
                info = client.admin.command("hello")

                if info.get("isWritablePrimary") or info.get("ismaster"):
                    print(f"PRIMARY com autenticação: {uri_com_auth}")
                    return uri_com_auth

            except Exception as e:
                print(f"Erro ao tentar autenticar na porta {porta}: {e}")
                print("Verifique se a URL está correta e se o usuário/senha existem.")

        except ServerSelectionTimeoutError:
            print(f"[x] Sem resposta em localhost:{porta}")
        except Exception as e:
            print(f"[!] Erro inesperado em {porta}: {e}")

    return None


def selecionar_secundarios():
    portas = listar_portas_dos_mongos()
    secundarios = []
    for porta in portas:
        uri = f"mongodb://localhost:{porta}/?directConnection=true&serverSelectionTimeoutMS=2000"
        try:
            client = MongoClient(uri)
            status = client.admin.command("replSetGetStatus")

            # Verifica qual membro é "self" e se é secundário
            for member in status["members"]:
                if member.get("self") and member["stateStr"] == "SECONDARY":
                    print(f"[OK] SECONDARY encontrada: {uri}")
                    secundarios.append(uri)
        except Exception as e:
            print(f"[!] Erro inesperado em {porta}: {e}")
    
    return secundarios

def selecionar_mais_proximo():
    portas = listar_portas_dos_mongos()
    menor_ping = float("inf")
    uri_mais_proxima = None

    for porta in portas:
        uri = f"mongodb://localhost:{porta}/?directConnection=true&serverSelectionTimeoutMS=2000"
        try:
            client = MongoClient(uri)
            status = client.admin.command("replSetGetStatus")

            for member in status["members"]:
                if member.get("self"):
                    ping = member.get("pingMs", 9999)
                    if ping < menor_ping:
                        menor_ping = ping
                        uri_mais_proxima = uri
        except Exception as e:
            print(f"[!] Erro ao verificar ping em {porta}: {e}")

    if uri_mais_proxima:
        print(f"Nó mais próximo selecionado com ping de {menor_ping}ms: {uri_mais_proxima}")
    else:
        print("Nenhum nó mais próximo encontrado.")

    return uri_mais_proxima


def selecionar_primario():
    portas = listar_portas_dos_mongos()
    print(f"Portas encontradas: {portas}")
    uri_primario = encontrar_primario(portas)

    if uri_primario:
        client = MongoClient(uri_primario)
        print(uri_primario)
        return uri_primario
        
    else:
        return "nenhuma instancia primaria encontrada"

