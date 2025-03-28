from pymongo import MongoClient

#Incompleto e cortado do projeto!!!

def criar_usuario_admin(client):
    db = client["admin"]

    try:
        usuarios = db.command("usersInfo")["users"]
        if any(user["user"] == "admin" for user in usuarios):
            db.command("dropUser", "admin")
            print("Usuário 'admin' anterior removido.")
        else:
            print("ℹUsuário 'admin' ainda não existe, prosseguindo com criação.")
    except Exception as e:
        print("Erro ao verificar/remover usuário anterior:", e)

    try:
        db.command("createUser", "admin",
            pwd="adminCorp",
            roles=[{"role": "root", "db": "admin"}]
        )
        print("Usuário administrador criado com sucesso.")
    except Exception as e:
        print(f"Erro ao criar usuário: {e}")
