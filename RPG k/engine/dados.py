"""
====================================
ENGINE RPG v2.0
Arquivo: dados.py

Responsabilidade:
- Interpretar tipos de dados.
- Realizar rolagens.
- Validar entradas.
- Centralizar toda aleatoriedade da engine.

Este arquivo NÃO:
- Calcula dano.
- Aplica efeitos.
- Consulta banco.
- Imprime mensagens.

====================================
"""

import random
import re





# ==========================================================
# Conversões
# ==========================================================


def converter_numero(valor, padrao=0):


    if valor is None:

        return padrao



    if isinstance(valor, int):

        return valor



    texto = str(valor).strip().upper()



    texto = texto.replace(

        "D",

        ""

    )



    try:

        return int(texto)



    except ValueError:

        return padrao





def converter_bool(valor):


    if isinstance(valor, bool):

        return valor



    if valor is None:

        return False



    return str(valor).lower().strip() in (

        "true",

        "1",

        "sim",

        "yes"

    )





# ==========================================================
# Interpretar dado
# ==========================================================


def interpretar_dado(valor):


    """
    Aceita:

    D20
    d20
    20


    Retorna:

    20
    """



    lados = converter_numero(

        valor,

        20

    )



    if lados <= 0:

        lados = 20



    return lados





# ==========================================================
# Rolagens simples
# ==========================================================


def rolar_unico(tipo_dado):


    lados = interpretar_dado(

        tipo_dado

    )



    if lados <= 1:

        return 1



    return random.randint(

        1,

        lados

    )





def rolar_dados(

        quantidade,

        tipo_dado):


    quantidade = converter_numero(

        quantidade,

        1

    )



    if quantidade < 1:

        quantidade = 1



    resultados = []



    for _ in range(quantidade):


        resultados.append(

            rolar_unico(

                tipo_dado

            )

        )



    return {


        "Rolagens":

            resultados,


        "Total":

            sum(resultados)

    }





# ==========================================================
# Expressões
# ==========================================================


def interpretar_expressao(expressao):


    """
    Interpreta:

    2D6
    1D20
    D8


    Retorna:

    {
        Quantidade: 2,
        Tipo: 6
    }

    """



    if expressao is None:


        return {


            "Quantidade":

                1,


            "Tipo":

                20

        }





    texto = str(expressao).upper().strip()



    regex = r"^(\d*)D(\d+)$"



    encontrado = re.match(

        regex,

        texto

    )



    if encontrado:



        quantidade = encontrado.group(1)



        tipo = encontrado.group(2)



        if quantidade == "":


            quantidade = 1



        return {


            "Quantidade":

                int(quantidade),



            "Tipo":

                int(tipo)

        }





    return {


        "Quantidade":

            1,



        "Tipo":

            interpretar_dado(

                texto

            )

    }





def rolar_expressao(expressao):


    dados = interpretar_expressao(

        expressao

    )



    resultado = rolar_dados(

        dados["Quantidade"],

        dados["Tipo"]

    )



    return {


        "Expressao":

            expressao,



        "Rolagens":

            resultado["Rolagens"],



        "Total":

            resultado["Total"]

    }





# ==========================================================
# Testes
# ==========================================================


def teste_percentual(chance):


    chance = converter_numero(

        chance

    )



    if chance <= 0:

        return False



    if chance >= 100:

        return True



    return rolar_unico(

        100

    ) <= chance





def comparar_rolagens(

        valor_a,

        valor_b):


    if valor_a > valor_b:

        return "ATACANTE"



    if valor_b > valor_a:

        return "DEFENSOR"



    return "EMPATE"





# ==========================================================
# Sorteio simples
# ==========================================================


def escolher_aleatorio(lista):


    if not lista:

        return None



    return random.choice(

        lista

    )