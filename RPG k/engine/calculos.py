"""
====================================
ENGINE RPG v2.0
Arquivo: calculos.pyEstado:
- MODO FINAL
- Arquivo estabilizado.
- Não alterar arquitetura sem solicitação explícita.
Responsabilidade:
- Realizar cálculos matemáticos da engine.
- Calcular dano.
- Calcular dano SAN.
- Calcular escudos.
- Aplicar reduções.
- Aplicar defesa.
- Determinar críticos.

Não:
- Consulta banco.
- Procura dados.
- Modifica personagens.
- Resolve combate.
- Executa habilidades.

====================================
"""


from engine.dados import (
    rolar_dados,
    teste_percentual
)





# ==========================================================
# Conversões
# ==========================================================


def converter_numero(valor, padrao=0):


    try:

        return int(valor)


    except (TypeError, ValueError):

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
# Bônus
# ==========================================================


def somar_bonus(*bonus):


    total = 0


    for valor in bonus:

        total += converter_numero(valor)


    return total





# ==========================================================
# Crítico
# ==========================================================


def calcular_critico(chance):


    return teste_percentual(

        converter_numero(chance)

    )





def aplicar_critico(

        dano,

        multiplicador=2):


    dano = converter_numero(

        dano

    )


    multiplicador = converter_numero(

        multiplicador,

        2

    )


    return dano * multiplicador





# ==========================================================
# Escudo
# ==========================================================


def calcular_escudo(

        valor_fixo=0,

        quantidade_dados=0,

        tipo_dado=0,

        bonus=0):


    total = converter_numero(

        valor_fixo

    )


    detalhes = []



    quantidade_dados = converter_numero(

        quantidade_dados

    )


    tipo_dado = converter_numero(

        tipo_dado

    )



    if quantidade_dados > 0 and tipo_dado > 0:


        resultado = rolar_dados(

            quantidade_dados,

            tipo_dado

        )


        total += resultado["Total"]


        detalhes = resultado["Rolagens"]





    total += converter_numero(

        bonus

    )



    if total < 0:

        total = 0



    return {


        "Escudo":

            total,


        "Rolagens":

            detalhes


    }





# ==========================================================
# Defesa
# ==========================================================


def aplicar_defesa(

        dano,

        defesa=0):


    resultado = (

        converter_numero(dano)

        -

        converter_numero(defesa)

    )



    if resultado < 0:

        resultado = 0



    return resultado





# ==========================================================
# Redução
# ==========================================================


def aplicar_reducao(

        dano,

        reducao_percentual=0,

        reducao_fixa=0):


    dano = converter_numero(

        dano

    )


    percentual = converter_numero(

        reducao_percentual

    )


    fixa = converter_numero(

        reducao_fixa

    )



    dano -= int(

        dano *

        percentual /

        100

    )


    dano -= fixa



    if dano < 0:

        dano = 0



    return dano





# ==========================================================
# Penetração
# ==========================================================


def aplicar_penetracao(

        defesa,

        penetra=False):


    if converter_bool(

        penetra

    ):

        return 0



    return converter_numero(

        defesa

    )





# ==========================================================
# Escudo absorvendo dano
# ==========================================================


def aplicar_escudo(

        dano,

        escudo):


    dano = converter_numero(

        dano

    )


    escudo = converter_numero(

        escudo

    )



    if escudo <= 0:


        return {


            "Dano":

                dano,


            "Escudo":

                0


        }





    if dano <= escudo:


        return {


            "Dano":

                0,


            "Escudo":

                escudo - dano


        }





    return {


        "Dano":

            dano - escudo,


        "Escudo":

            0


    }





# ==========================================================
# Dano
# ==========================================================


def calcular_dano(

        dano_base=0,

        quantidade_dados=0,

        tipo_dado=0,

        bonus=0,

        quantidade_acertos=1):


    total = 0


    detalhes = []



    quantidade = max(

        1,

        converter_numero(

            quantidade_acertos,

            1

        )

    )





    for numero in range(quantidade):


        dano = converter_numero(

            dano_base

        )


        rolagens = []



        dados = converter_numero(

            quantidade_dados

        )


        faces = converter_numero(

            tipo_dado

        )





        if dados > 0 and faces > 0:


            resultado = rolar_dados(

                dados,

                faces

            )


            dano += resultado["Total"]


            rolagens = resultado["Rolagens"]





        dano += converter_numero(

            bonus

        )



        if dano < 0:

            dano = 0



        total += dano



        detalhes.append({

            "Acerto":

                numero + 1,


            "Rolagens":

                rolagens,


            "Dano":

                dano

        })





    return {


        "Dano":

            total,


        "Dano Final":

            total,


        "Acertos":

            quantidade,


        "Detalhes":

            detalhes


    }





# ==========================================================
# Dano SAN
# ==========================================================


def calcular_dano_san(

        dano_base=0,

        quantidade_dados=0,

        tipo_dado=0,

        bonus=0,

        quantidade_acertos=1):


    resultado = calcular_dano(

        dano_base,

        quantidade_dados,

        tipo_dado,

        bonus,

        quantidade_acertos

    )



    return {


        "Dano SAN":

            resultado["Dano"],


        "Acertos":

            resultado["Acertos"],


        "Detalhes":

            resultado["Detalhes"]


    }