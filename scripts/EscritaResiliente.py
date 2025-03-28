from pymongo import WriteConcern

def writeconcernVar(client, db, table):
    database = client[db]
    colecao = database.get_collection(table, write_concern=WriteConcern(w="majority", j=True))
    return colecao


def writeconcern(client, db, table, document):
    database = client[db]
    colecao = database.get_collection(table, write_concern=WriteConcern(w="majority", j=True))
    resultado = colecao.insert_one(document)
        
    print(f"✅ Documento inserido com ID: {resultado.inserted_id}")
    
def criar_document():
    print("📄 Criação de documento MongoDB")
    print("🟡 Digite 'ok' a qualquer momento para encerrar.")
    
    document = {}
    
    while True:
        var = input("📝 Nome do atributo: ")
        if var.lower() == "ok":
            break

        valor = input("🔢 Valor do atributo: ")
        if valor.lower() == "ok":
            break

        document[var] = valor  

    return document
