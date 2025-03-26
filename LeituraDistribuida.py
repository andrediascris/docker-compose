from pymongo import MongoClient

#Conectar ao cluster MongoDB
client = MongoClient(
  "mongodb://node1:27017,node2:27018,node3:27019,node4:27020/?replicaSet=replicaSet",
   read_preference="secondary"  # Configura a leitura em nós secundários
)

#Selecionar o banco de dados
db = client["SistemaCorp"]

#Fazer uma consulta no nó secundário
resultado = db.cliente.find()

#Exibir os resultados
for documento in resultado:
  print(documento)