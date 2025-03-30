***
***Apresentação e explicação do que é um cluster e como o MongoDB trabalha
***
Oque é
- Cluster é um conjunto de servidores ou instancias mongoDB que armazenam os mesmos dados
- Isso resulta em redundância, aumentando a disponibilidade dos dados
- Caso falhe um servidor, temos os outros
- Replicação assíncrona
- Configuração Altamente recomendada para a maioria dos ambientes de produção

---
***Como funciona?
- existe um nó primários e vários nós secundários 
- primários recebe as escritas e leituras por padrão
- secundários replicam os dados do primário

![[Pasted image 20250323023015.png]]

* Temos o Heartbeat que fica verificando se os nós ainda estão de pé
* Se um primário cair, um secundário assume seu lugar

![[Pasted image 20250323023052.png]]


**Em caso de queda
- Quando um primário não se comunica com os outros membros do set por mais do que o período predefinido (10 segundos)
- um secundário elegível solicita uma eleição para se nomear como o novo primário para retomar as operações normais.

![[Pasted image 20250323023731.png]]

***

**Interessante saber!

Existe um tipo de nó especial, chamado "Arbiter" (Opcional): Um nó que não armazena dados, mas participa das eleições para escolher um novo primário em caso de falha.
![[Pasted image 20250329162146.png]]