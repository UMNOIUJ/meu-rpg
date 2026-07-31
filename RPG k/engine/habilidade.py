"""
====================================
ENGINE RPG v2.0
Arquivo: habilidade.py

Estado:
- MODO FINAL
- Arquivo estabilizado.
- Não alterar arquitetura sem solicitação explícita.

Responsabilidade:
- Buscar habilidades no cache.
- Validar recursos.
- Interpretar dados.
- Calcular resultados usando calculos.py.
- Preparar efeitos vinculados.
- Retornar execução.

Não:
- Resolve embates.
- Escolhe ações.
- Controla turnos.
- Calcula acerto diretamente.
- Aplica efeitos diretamente.
- Acessa NocoDB.

====================================
"""


from database import cache


from engine.calculos import (
    calcular_dano,
    calcular_dano_san,
    aplicar_critico
)





# ======================================================
# Cache
# ======================================================


def obter_lista_cache(nome):


    if hasattr(cache, nome):

        return getattr(cache, nome)()



    return cache.listar(nome)





# ======================================================
# Buscar habilidade
# ======================================================


def buscar_habilidade(nome):


    habilidades = obter_lista_cache(
        "habilidades"
    )


    if isinstance(
            habilidades,
            dict):

        habilidades = habilidades.values()



    for habilidade in habilidades:


        if habilidade.get(
                "Nome"
        ) == nome:


            return habilidade



    return None





# ======================================================
# Conversão
# ======================================================


def converter_numero(valor, padrao=0):


    try:


        if isinstance(valor, str):

            valor = valor.replace(
                "d",
                ""
            ).replace(
                "D",
                ""
            )


        return int(valor)



    except (
        TypeError,
        ValueError
    ):


        return padrao





def obter_id(valor):


    if not isinstance(valor, dict):

        return valor



    return valor.get(
        "Id",
        valor.get(
            "id"
        )
    )





# ======================================================
# SAN
# ======================================================


def verificar_custo_san(usuario, habilidade):


    custo = converter_numero(

        habilidade.get(
            "Custo SAN",
            0
        )

    )



    if custo <= 0:

        return True



    return getattr(

        usuario,

        "san_atual",

        0

    ) >= custo





def consumir_san(usuario, habilidade):


    custo = converter_numero(

        habilidade.get(
            "Custo SAN",
            0
        )

    )



    if custo <= 0:

        return



    if hasattr(

            usuario,

            "perder_san"):


        usuario.perder_san(

            custo

        )





# ======================================================
# Efeitos vinculados
# ======================================================


def buscar_efeitos_habilidade(habilidade):


    resultado = []



    registros = obter_lista_cache(

        "habilidade_efeitos"

    )



    if isinstance(

            registros,

            dict):


        registros = registros.values()



    id_habilidade = obter_id(

        habilidade

    )



    for registro in registros:


        if obter_id(

                registro.get(

                    "Habilidade"

                )

        ) != id_habilidade:


            continue



        efeito = registro.get(

            "Efeito"

        )



        if efeito:

            resultado.append(

                efeito

            )



    return resultado





# ======================================================
# Cálculo de dano
# ======================================================


def calcular_dano_habilidade(

        habilidade,

        acertos):


    return calcular_dano(


        dano_base=habilidade.get(

            "Dano",

            0

        ),


        quantidade_dados=habilidade.get(

            "Quantidade Dados",

            0

        ),


        tipo_dado=habilidade.get(

            "Tipo Dado",

            0

        ),


        quantidade_acertos=acertos


    )





def calcular_san_habilidade(

        habilidade,

        acertos):


    return calcular_dano_san(


        dano_base=habilidade.get(

            "Dano SAN",

            0

        ),


        quantidade_dados=habilidade.get(

            "Quantidade Dados SAN",

            0

        ),


        tipo_dado=habilidade.get(

            "Tipo Dado SAN",

            0

        ),


        quantidade_acertos=acertos


    )





# ======================================================
# Executar habilidade
# ======================================================


def executar_habilidade(

        usuario,

        alvo,

        nome_habilidade,

        resultado_execucao):


    habilidade = buscar_habilidade(

        nome_habilidade

    )



    if not habilidade:


        return {

            "Erro":

                "Habilidade inexistente"

        }





    if not habilidade.get(

            "Ativa",

            True):


        return {

            "Erro":

                "Habilidade inativa"

        }





    if not verificar_custo_san(

            usuario,

            habilidade):


        return {

            "Nome":

                nome_habilidade,


            "Erro":

                "SAN insuficiente",


            "Dano":

                0

        }





    consumir_san(

        usuario,

        habilidade

    )





    acertos = resultado_execucao.get(

        "Acertos",

        0

    )


    critico = resultado_execucao.get(

        "Critico",

        False

    )


    parcial = resultado_execucao.get(

        "Parcial",

        False

    )





    if acertos <= 0:


        return {


            "Nome":

                habilidade.get(

                    "Nome"

                ),


            "Usuario":

                usuario,


            "Alvo":

                alvo,


            "Acertos":

                0,


            "Dano":

                0,


            "Dano SAN":

                0,


            "Efeitos":

                [],


            "Critico":

                critico,


            "Parcial":

                parcial

        }





    dano = calcular_dano_habilidade(

        habilidade,

        acertos

    )



    dano_san = calcular_san_habilidade(

        habilidade,

        acertos

    )





    dano_final = dano.get(

        "Dano Final",

        dano.get(

            "Dano",

            0

        )

    )





    if critico:


        dano_final = aplicar_critico(

            dano_final

        )





    return {


        "Nome":

            habilidade.get(

                "Nome"

            ),


        "Usuario":

            usuario,


        "Alvo":

            alvo,


        "Acertos":

            acertos,


        "Dano":

            dano_final,


        "Dano SAN":

            dano_san.get(

                "Dano SAN",

                0

            ),


        "Efeitos":

            buscar_efeitos_habilidade(

                habilidade

            ),


        "Critico":

            critico,


        "Parcial":

            parcial,


        "Detalhes":

            dano.get(

                "Detalhes",

                []

            )

    }