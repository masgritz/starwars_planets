# Star Wars Planets REST API

Essa é uma API REST desenvolvida em Python 3 utilizando Flask (https://github.com/pallets/flask), flask_restplus (https://github.com/noirbizarre/flask-restplus) e PyMongo (https://github.com/mongodb/mongo-python-driver) com o objetivo de gerenciar planetas do universo de Star Wars. Inclui funções para inserir, excluir e buscar planetas. Também possuí integração com o SWAPI (https://swapi.co) para inserir o número de aparições do planeta nos filmes da saga.

## Instalação

É necessário apenas a instalação das depedências com o [pip](https://pip.pypa.io/en/stable/).

```bash
pip install requirements.txt
```

## Modo de Uso

Para iniciar a API, execute o comando:
```python
python3 app.py
```
Ele pode ser acessada através do endereço ```https://127.0.0.1:5000```.
```python
https://127.0.0.1:5000/planets # Método GET: lista todos os planetas cadastrados no banco de dados

https://127.0.0.1:5000/planets # Método POST: cadastra um novo planeta no banco de dados

https://127.0.0.1:5000/planets/name/<nome_do_planeta> # Método GET: busca um planeta pelo nome

https://127.0.0.1:5000/planets/id/<id_do_planeta> # Método GET: busca um planeta pelo id

https://127.0.0.1:5000/planets/name/<nome_do_planeta> # Método DELETE: remove um planeta com nome correspondente

https://127.0.0.1:5000/planets/id/<id_do_planeta> # Método DELETE: remove um planeta com id correspondente
```
## Licença
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
