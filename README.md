## docker-compose
No terminal para criar a rede docker 

   	 docker network create mongoCluster

# Configura uma rede chamada mongoCluster para que todos os contêineres se comuniquem.

## Iniciando nó primário

   	 docker run -d --name node1 --network mongoCluster -p 27017:27017 mongo:6 mongod --replSet myReplicaSet --bind_ip localhost,mongo1

## Nós secundários

	docker run -d --rm -p 27018:27017 --name node2 --network cluster mongodb/mongodb-community-server:latest --replSet replicaSet --bind_ip localhost,node2
	docker run -d --rm -p 27019:27017 --name node3 --network cluster mongodb/mongodb-community-server:latest --replSet replicaSet --bind_ip localhost,node3
	docker run -d --rm -p 27020:27017 --name node4 --network cluster mongodb/mongodb-community-server:latest --replSet replicaSet --bind_ip localhost,node4

# -d --> indica que este contêiner deve ser executado no modo desanexado (em segundo plano).
# --name --> indica o nome do contêiner. Este se tornará o nome do host desta máquina.
# -p --> indica o mapeamento de porta. Qualquer solicitação de entrada na porta 27017 em sua máquina será redirecionada para a porta 27017 no contêiner.
# --network --> indica qual rede Docker usar. Todos os contêineres na mesma rede podem ver uns aos outros.
# mongodb/mongodb-community-server:latest --> é a imagem que será usada pelo Docker. Esta imagem é o servidor MongoDB Community 
# --bind_ip: Define os endereços IP que o MongoDB pode escutar.

## Inicializar o conjunto de réplicas

	docker exec -it mongo1 mongosh --eval "rs.initiate({ _id: 'myReplicaSet', members: [ { _id: 0, host: 'mongo1' }, { _id: 1, host: 'mongo2' }, { _id: 2, host: 'mongo3' } ] })"

# docker exec -it: Executa um comando dentro de um contêiner em execução.
# mongosh: Inicia o shell interativo do MongoDB.
# rs.initiate: Inicializa o conjunto de réplicas com os membros especificados.

Verificar o status do cluster
 	docker exec -it mongo1 mongosh --eval "rs.status()"
# Este comando exibe o status do conjunto de réplicas, incluindo quais nós estão ativos e sincronizados.
