from pymongo import MongoClient

#Conectar ao cluster MongoDB
client = MongoClient(
    "mongodb://node1:27017,node2:27018,node3:27019,node4:27020/?replicaSet=replicaSet"
)
#Selecionar o banco de dados e a coleção
db = client["SistemaCorp"]
colecao = db["cliente"]

#Configurar escrita com write concern
colecao = cliente.with_options(write_concern={"w": "majority", "j": True})
# Inserir dados com garantia de escrita resiliente
documento = {"nome": "Escrita Resiliente", "status": "ativo"}
resultado = cliente.insert_one(documento)
	
# Exibir confirmação da operação
print(f"Documento inserido com ID: {resultado.inserted_id}")