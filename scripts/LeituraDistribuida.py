from pymongo import ReadPreference

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

def read_from_secondary(client, db, table):
    read_pref = selecionar_opcao()

    if not read_pref:
        print("Voltando ao menu principal...")
        return

    database = client.get_database(db, read_preference=read_pref)
    colecao = database[table]

    resultado = colecao.find()

    for documento in resultado:
        print(documento)
