from pymongo import MongoClient, ReadPreference
from util import conexao

def selecionar_opcao():
    print("Selecione uma opção de leitura:")
    print("(1) PRIMARY_PREFERRED")
    print("(2) SECONDARY")
    print("(3) SECONDARY_PREFERRED")
    print("(4) NEAREST")
    print("**Digite qualquer outra tecla pra voltar")
    
    opcao = int(input("Digite o número da opção desejada: "))

    if opcao == 1:
        return ReadPreference.PRIMARY_PREFERRED
    elif opcao == 2:
        return ReadPreference.SECONDARY
    elif opcao == 3:
        return ReadPreference.SECONDARY_PREFERRED
    elif opcao == 4:
        return ReadPreference.NEAREST
    else:
        return None

def read_from_secondary(uri, db, table):
    read_pref = selecionar_opcao()
    if not read_pref:
        print("Voltando ao menu principal...")
        return
    
    if read_pref == ReadPreference.NEAREST:
        uri = conexao.selecionar_mais_proximo()

    if read_pref != ReadPreference.PRIMARY_PREFERRED:
        secundarios = conexao.selecionar_secundarios()
        if not secundarios:
            print("Nenhum nó secundário disponível.")
            return
        uri = secundarios[0]  

    client = MongoClient(uri, read_preference=read_pref)
    database = client[db]
    colecao = database[table]

    print("🔍 Buscando documentos...")

    try:
        servidor = read_pref.name.capitalize()
        server_info = client.address
        print(f"Leitura realizada com preferência: {servidor}")
        print(f"Conectado em: {server_info}")
    except Exception as e:
        print("Não foi possível identificar o host da leitura:", e)

    try:
        resultado = colecao.find()
        for doc in resultado:
            print(doc)
    except Exception as e:
        print("Falha ao consultar documentos:", e)

    try:
        hello = client.admin.command("hello")
        if hello.get("isWritablePrimary", False):
            print("\nLeitura caiu no primário!")
        else:
            print("\nLeitura foi feita em um nó secundário.")
    except:
        pass