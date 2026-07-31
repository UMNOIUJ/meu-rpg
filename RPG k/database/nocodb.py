"""
====================================
ENGINE RPG v2.0
Arquivo: nocodb.py

Responsabilidade:
- Comunicação direta com NocoDB.
- Buscar registros.
- Criar registros.
- Atualizar registros.
- Remover registros.

Este arquivo NÃO:
- Possui regras de combate.
- Calcula dano.
- Manipula personagens.
- Controla turnos.

Toda lógica deve usar este arquivo
ou o cache.
====================================
"""

import requests


from config import (
    NOCODB_URL,
    NOCODB_TOKEN
)





# ==========================================================
# Cabeçalho
# ==========================================================


def cabecalho():

    return {

        "xc-token": NOCODB_TOKEN,

        "Content-Type": "application/json"

    }





# ==========================================================
# URL
# ==========================================================


def url_tabela(tabela):


    base = NOCODB_URL.rstrip("/")



    if base.endswith("/api/v2"):


        return (

            f"{base}/tables/{tabela}/records"

        )



    return (

        f"{base}/api/v2/tables/{tabela}/records"

    )





# ==========================================================
# Buscar tabela completa
# ==========================================================


def buscar_tabela(tabela):


    registros = []


    offset = 0


    limite = 1000



    while True:


        try:


            resposta = requests.get(


                url_tabela(tabela),


                headers=cabecalho(),


                params={


                    "limit": limite,


                    "offset": offset


                },


                timeout=30


            )



        except Exception as erro:


            print(

                "Erro conexão NocoDB:",

                erro

            )


            return registros





        if resposta.status_code != 200:


            print(

                f"Erro buscar tabela {tabela}:",

                resposta.text

            )


            return registros





        dados = resposta.json()



        pagina = dados.get(

            "list",

            []

        )



        registros.extend(

            pagina

        )





        if len(pagina) < limite:


            break





        offset += limite





    return registros





# ==========================================================
# Buscar por ID
# ==========================================================


def buscar_por_id(tabela, id_registro):


    try:


        resposta = requests.get(


            f"{url_tabela(tabela)}/{id_registro}",


            headers=cabecalho(),


            timeout=30


        )



    except Exception:


        return None





    if resposta.status_code != 200:


        return None





    return resposta.json()





# ==========================================================
# Criar registro
# ==========================================================


def criar_registro(tabela, dados):


    try:


        resposta = requests.post(


            url_tabela(tabela),


            headers=cabecalho(),


            json=dados,


            timeout=30


        )



    except Exception as erro:


        print(

            "Erro criar registro:",

            erro

        )


        return None





    if resposta.status_code not in (

        200,

        201

    ):


        print(

            f"Erro criar registro {tabela}:",

            resposta.text

        )


        return None





    return resposta.json()





# ==========================================================
# Atualizar registro
# ==========================================================


def atualizar(tabela, id_registro, dados):


    try:


        resposta = requests.patch(


            f"{url_tabela(tabela)}/{id_registro}",


            headers=cabecalho(),


            json=dados,


            timeout=30


        )



    except Exception as erro:


        print(

            "Erro atualizar:",

            erro

        )


        return False





    if resposta.status_code not in (

        200,

        201

    ):


        print(

            f"Erro atualizar {tabela}:",

            resposta.text

        )


        return False





    return True





# ==========================================================
# Deletar registro
# ==========================================================


def deletar_registro(tabela, id_registro):


    try:


        resposta = requests.delete(


            f"{url_tabela(tabela)}/{id_registro}",


            headers=cabecalho(),


            timeout=30


        )



    except Exception:


        return False





    return resposta.status_code in (

        200,

        204

    )





# ==========================================================
# Buscar filtrado
# ==========================================================


def buscar_filtrado(tabela, campo, valor):


    return [


        registro


        for registro in buscar_tabela(tabela)


        if registro.get(campo) == valor


    ]





# ==========================================================
# Primeiro registro
# ==========================================================


def buscar_primeiro(tabela, campo, valor):


    registros = buscar_filtrado(


        tabela,


        campo,


        valor


    )



    if registros:


        return registros[0]





    return None





# ==========================================================
# Atualização em lote
# ==========================================================


def atualizar_varios(tabela, registros):


    resultados = []



    for registro in registros:



        id_registro = registro.get(


            "Id",


            registro.get(

                "id"

            )

        )



        if not id_registro:


            continue





        dados = registro.copy()



        dados.pop(

            "Id",

            None

        )


        dados.pop(

            "id",

            None

        )





        resultados.append(


            atualizar(


                tabela,


                id_registro,


                dados


            )

        )





    return resultados





# ==========================================================
# Teste conexão
# ==========================================================


def testar_conexao():


    try:


        resposta = requests.get(


            NOCODB_URL,


            headers=cabecalho(),


            timeout=10


        )


        return resposta.status_code < 500





    except Exception:


        return False