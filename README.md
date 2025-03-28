# **O que é um cluster**:question:

O cluster é um conjunto de servidores interconectados que trabalham em conjunto
fornecendo mais disponibilidade, escalabilidade e desempenho para aplicações.O
cluster pode ser usado em banco de dados, computação distribuída e
armazenamento de dados .
No banco de dados, ele pode ser usado para distribuição da carga de trabalho entre
vários nós, garantindo redundância e replicação para evitar falhas e melhorar o
desempenho

## O que é MongoDB :question:
MongoDB é um sistema de gerenciamento de banco de dados NoSQL (Not Only
SQL) de código aberto e orientado a documentos.

## Como o MongoDB Trabalha com Clusters :question:
Replica Set (Alta Disponibilidade)
Um Replica Set é um grupo de servidores MongoDB que mantém cópias idênticas
dos dados para garantir tolerância a falhas. Ele é composto por:

* Primária: O nó principal que recebe operações de escrita e leitura.

* Secundárias: Nós secundários que replicam os dados do nó primário e
podem ser promovidos a primário caso ele falhe.

* Arbiter (Opcional): Um nó que não armazena dados, mas participa das
eleições para escolher um novo primário em caso de falha.

**Vantagens:**

* :heavy_check_mark: Redundância e segurança contra falhas.

* :heavy_check_mark: Failover automático (se o primário falhar, um secundário assume).

* :heavy_check_mark: Melhor distribuição de carga para leitura (se configurado corretamente).


### Sharding (Escalabilidade Horizontal)
O Sharding é o método do MongoDB para distribuir dados em múltiplos servidores
para suportar grandes volumes de dados e melhorar o desempenho. Ele funciona
da seguinte maneira:

* Shards: Servidores que armazenam pedaços do banco de dados.

* Config Servers: Armazenam metadados sobre os shards e ajudam a
coordenar a distribuição dos dados.

* Query Router (mongos): Encaminhar consultas para os shards apropriados.

**Vantagens:**

* :heavy_check_mark: Permite lidar com grandes volumes de dados.

* :heavy_check_mark: Balanceamento de carga entre servidores.

* :heavy_check_mark: Escalabilidade horizontal (adicionando mais máquinas conforme necessário).

<img src="https://github.com/user-attachments/assets/866f921a-a473-40c1-b48b-7e7d577146d5" width="500px"/>


# :computer: **docker-compose**
No terminal para criar a rede docker 

   	 docker network create mongoCluster

### Configura uma rede chamada mongoCluster para que todos os contêineres se comuniquem.

## Iniciando nó primário

   	 docker run -d --name node1 --network mongoCluster -p 27017:27017 mongo:6 mongod --replSet myReplicaSet --bind_ip localhost,mongo1

## Nós secundários

	docker run -d --rm -p 27018:27017 --name node2 --network cluster mongodb/mongodb-community-server:latest --replSet replicaSet --bind_ip localhost,node2
	docker run -d --rm -p 27019:27017 --name node3 --network cluster mongodb/mongodb-community-server:latest --replSet replicaSet --bind_ip localhost,node3
	docker run -d --rm -p 27020:27017 --name node4 --network cluster mongodb/mongodb-community-server:latest --replSet replicaSet --bind_ip localhost,node4

#### -d --> indica que este contêiner deve ser executado no modo desanexado (em segundo plano).
#### --name --> indica o nome do contêiner. Este se tornará o nome do host desta máquina.
#### -p --> indica o mapeamento de porta. Qualquer solicitação de entrada na porta 27017 em sua máquina será redirecionada para a porta 27017 no contêiner.
#### --network --> indica qual rede Docker usar. Todos os contêineres na mesma rede podem ver uns aos outros.
#### mongodb/mongodb-community-server:latest --> é a imagem que será usada pelo Docker. Esta imagem é o servidor MongoDB Community 
#### --bind_ip: Define os endereços IP que o MongoDB pode escutar.

## Inicializar o conjunto de réplicas

	docker exec -it mongo1 mongosh --eval "rs.initiate({ _id: 'myReplicaSet', members: [ { _id: 0, host: 'mongo1' }, { _id: 1, host: 'mongo2' }, { _id: 2, host: 'mongo3' } ] })"

### docker exec -it: Executa um comando dentro de um contêiner em execução.
### mongosh: Inicia o shell interativo do MongoDB.
### rs.initiate: Inicializa o conjunto de réplicas com os membros especificados.

## Verificar o status do cluster :+1:
 	docker exec -it mongo1 mongosh --eval "rs.status()"
### Este comando exibe o status do conjunto de réplicas, incluindo quais nós estão ativos e sincronizados.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Outras possiveis funcionalidades para o cluster

## Leitura distribuída: 
A leitura distribuída permite que consultas sejam realizadas nos nós secundários do cluster,
aliviando a carga do nó primário e aumentando a capacidade de leitura.
from pymongo import MongoClient

	# Conectar ao cluster MongoDB
	client = MongoClient(
   		"mongodb://node1:27017,node2:27018,node3:27019,node4:27020/?replicaSet=replicaSet",
    		read_preference="secondary"  # Configura a leitura em nós secundários
	)

	# Selecionar o banco de dados
	db = client["SistemaCorp"]

	# Fazer uma consulta no nó secundário
	resultado = db.cliente.find()

	# Exibir os resultados
	for documento in resultado:
  	    print(documento)
       
### O MongoClient é usado para se conectar ao cluster.

## Escrita resiliente:
Escrita resiliente garante que os dados sejam escritos de forma confiável,
mesmo em um ambiente de replicação, com tolerância a falhas.
Você pode usar o write concern para controlar o nível de garantia na escrita.
	
 	from pymongo import MongoClient
	# Conectar ao cluster MongoDB
	client = MongoClient(
    		"mongodb://node1:27017,node2:27018,node3:27019,node4:27020/?replicaSet=replicaSet"
	)

	# Selecionar o banco de dados e a coleção
	db = client["SistemaCorp"]
	colecao = db["cliente"]

	# Configurar escrita com write concern
	colecao = cliente.with_options(write_concern={"w": "majority", "j": True})

	# Inserir dados com garantia de escrita resiliente
	documento = {"nome": "Escrita Resiliente", "status": "ativo"}
	resultado = cliente.insert_one(documento)
	
	# Exibir confirmação da operação
	print(f"Documento inserido com ID: {resultado.inserted_id}")
 
## Write Concern:
### w: "majority": Exige que a escrita seja confirmada na maioria dos nós do conjunto de réplicas. 
### Isso garante alta disponibilidade e consistência.
## Configuração de write concern em uma coleção:
### O método with_options() permite definir configurações de escrita específicas
### para a coleção minhaColecao, aplicando o write concern.
## Inserção de dados:
### insert_one(): Realiza a escrita do documento, respeitando as garantias definidas pelo write concern.

## Backup e restore automáticos
### Automatizar backups e restaurações ajuda a proteger os dados em caso de falhas ou perdas.

## :lock: Segurança e autenticação: 
### Configure autenticação no MongoDB para proteger os dados e use SSL/TLS para criptografia. 
	#Ative autenticação no mongod
	mongod --auth

	#Crie um usuário administrador:
	use admin;
	db.createUser({
   	   user: "admin",
   	   pwd: "adminCorp",
    	   roles: [{ role: "root", db: "admin" }]
	});
### SSL/TLS com Docker Desktop:
### Configure o MongoDB para usar os certificados
	mongod --sslMode requireSSL --sslPEMKeyFile /path/to/cert.pem
#### Compass permite autenticação e conexões seguras via SSL diretamente na interface.
