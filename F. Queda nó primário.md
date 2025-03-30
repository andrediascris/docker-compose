Derrubar nó primário
**Use apenas um desses seguintes comandos para derrubar apenas o nó primário
```
docker stop node1
```

```
docker stop node2
```

```
docker stop node3
```

```
docker stop node4
```

---
Após a queda

Tente inserir
```
db.cliente.insertOne({codigo:6, nome: "Esdras"});
```
-> vai dar erro, pois o nó caiu

Verificar quem é o novo nó primário
```
docker exec -it node4 mongosh --eval "rs.status()"
```

---

**no novo nó primário
```
db.cliente.insertOne({codigo:6, nome: "Teresa Maria"});
```

---
Verificar a nova inserção nos nós secundários

```
use sistemaCorp
```

```
db.cliente.find()
```