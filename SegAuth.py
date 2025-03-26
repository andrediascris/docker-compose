#Ative autenticação no mongod
  mongod --auth

#Crie um usuário administrador:
  use admin;
  db.createUser({
     user: "admin",
     pwd: "adminCorp",
     roles: [{ role: "root", db: "admin" }]
});
#Conecte-se com autenticação em PyMongo:
  client = MongoClient("mongodb://admin:adminCorp@node1:27017/admin")


#Configure o MongoDB para usar os certificados:

  mongod --sslMode requireSSL --sslPEMKeyFile /path/to/cert.pem