conectar compass com as urls copiadas

```
mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.4.2
```

```
mongodb://127.0.0.1:27018/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.4.2
```

```
mongodb://127.0.0.1:27019/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.4.2
```

```
mongodb://127.0.0.1:27020/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.4.2
```

| Palavra                        | Função                                                                                                         |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| mongodb://                     | Protocolo usado para conectar ao MongoDB                                                                       |
| 127.0.0.1:27017                | Endereço IP e porta do servidor MongoDB (localhost + porta padrão 27017)                                       |
| ?directConnection=true         | Diz ao cliente que ele deve se conectar diretamente a esse host, e não tentar replicar ou descobrir outros nós |
| &serverSelectionTimeoutMS=2000 | Tempo limite (em milissegundos) para o cliente tentar selecionar um servidor (2 segundos aqui)                 |
| &appName=mongosh+2.4.2         | Nome da aplicação cliente (nesse caso, mongosh versão 2.4.2) — apenas informativo/logs<br>                     |

----------------------------------------------------
**No primário

```
use sistemaCorp
```
-> Mudar para o banco de dados sistemaCorp ou cria-lo caso ele não exista

Inserções
```
db.cliente.insertOne({codigo:1, nome: "Lucas Henrique Soares"});
```
-> Comando para inserir um documento na coleção "cliente"

```
db.cliente.insertOne({codigo:2, nome: "André Cristiano Dias Raymundo"});
```

```
db.cliente.insertOne({codigo:3, nome: "Julia Cesarini Schmidt De Siqueira"});
```

```
db.cliente.insertOne({codigo:4, nome: "Diego Leme Pires"});
```

```
db.cliente.insertOne({codigo:5, nome: "Julia Mel"});
```

Verificar tabelas adicionadas
```
db.cliente.find()
```


----------------------------------------------------
 **Nos Secundario**
 
```
use sistemaCorp
```

```
db.cliente.findOne()
```
-> comando para encontrar um único cliente
