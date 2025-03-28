from pymongo import MongoClient
from util import conexao, definir_config
from . import LeituraDistribuida, EscritaResiliente, BackupAutomatico

def menu():
    Dados = None
    print("Selecione uma configuração:")
    print("(0) definir configurações (começar por aqui)")
    print("(1) Leitura Distribuida")
    print("(2) Escrita resiliente")
    print("(3) Backup e restore automáticos ")
    print("**Digite qualquer outra tecla pra encerrar")
    opcao = input("escolha: ")
    
    primario_uri = conexao.selecionar_primario()
    primario = MongoClient(primario_uri) 

    try:
        Dados = definir_config.carregar_config()
    except:
        if opcao != "0":
            print("dados necessarios ainda não definidos, entrando na opção '(0) definir configurações (começar por aqui)'")
            definir_config.definir_config()
            Dados = definir_config.carregar_config()
            menu()
    

    if opcao == "0":
        definir_config.definir_config()
        print("\n\n\n")
        menu()
    elif opcao == "1":
        print("\n\n\n")
        LeituraDistribuida.read_from_secondary(primario, Dados.db, Dados.table)
        print("\n\n\n")
        menu()
    elif opcao == "2":
        document = EscritaResiliente.criar_document()
        EscritaResiliente.writeconcern(primario, Dados.db, Dados.table, document)
        print("\n\n\n")
        menu()
    elif opcao == "3":
        hora = input("Digite um horario hh:mm -> ")
        BackupAutomatico.iniciar_agendador_em_thread(hora, Dados.backup, Dados.mongodump)
        print("\n\n\n")
        menu()
    else:
        print("encerrando...")
        return None
