"""
====================================
ENGINE RPG v1.0
Arquivo: combo.py

Responsabilidade:
Gerenciar combos de habilidades.

Não:
- Calcula dano.
- Executa habilidade.
- Resolve combate.
- Acessa NocoDB diretamente.

====================================
"""


import random



from database.carregador import carregar_combos

from engine.condicao import verificar_condicao



# ==========================================================
# Conversões
# ==========================================================


def converter_bool(
        valor):


    if isinstance(
            valor,
            bool):

        return valor



    if valor is None:

        return False



    return str(
        valor
    ).lower().strip() in (

        "true",

        "1",

        "sim",

        "yes"

    )



def converter_numero(
        valor,
        padrao=0):


    try:

        return int(valor)

    except:

        return padrao



# ==========================================================
# Buscar combos disponíveis
# ==========================================================


def procurar_combos(
        habilidade,
        contexto):


    combos = carregar_combos()


    encontrados = []



    for combo in combos:



        origem = combo.get(

            "Habilidade Origem"

        )



        if isinstance(
                origem,
                dict):


            origem = origem.get(

                "Nome"

            )



        if origem != habilidade:

            continue



        if verificar_condicao(

                combo.get(
                    "Condição"
                ),

                contexto

        ):


            encontrados.append(

                combo

            )



    return encontrados



# ==========================================================
# Buscar combo específico
# ==========================================================


def buscar_combo(
        habilidade_origem,
        habilidade_destino):


    for combo in carregar_combos():


        origem = combo.get(

            "Habilidade Origem"

        )


        destino = combo.get(

            "Habilidade Destino"

        )



        if isinstance(
                origem,
                dict):


            origem = origem.get(
                "Nome"
            )



        if isinstance(
                destino,
                dict):


            destino = destino.get(
                "Nome"
            )



        if (

            origem == habilidade_origem

            and

            destino == habilidade_destino

        ):


            return combo



    return None



# ==========================================================
# Obter próxima habilidade
# ==========================================================


def obter_proxima_habilidade(
        combo):


    destino = combo.get(

        "Habilidade Destino"

    )


    if isinstance(
            destino,
            dict):


        return destino.get(

            "Nome"

        )


    return destino



# ==========================================================
# Ordem do combo
# ==========================================================


def verificar_ordem(
        combo,
        ordem_atual):


    ordem = converter_numero(

        combo.get(

            "Ordem",

            0

        )

    )


    return ordem == ordem_atual



# ==========================================================
# Chance do combo
# ==========================================================


def verificar_chance(
        combo,
        resultado=None):


    chance = converter_numero(

        combo.get(

            "Chance",

            100

        ),

        100

    )



    if resultado is not None:


        return resultado <= chance



    rolagem = random.randint(

        1,

        100

    )


    return rolagem <= chance



# ==========================================================
# Obrigatório
# ==========================================================


def combo_obrigatorio(
        combo):


    return converter_bool(

        combo.get(

            "Obrigatório",

            False

        )

    )



# ==========================================================
# Executar seleção de combo
# ==========================================================


def selecionar_combo(
        habilidade,
        contexto,
        ordem=0):


    combos = procurar_combos(

        habilidade,

        contexto

    )



    validos = []



    for combo in combos:



        if verificar_ordem(

                combo,

                ordem

        ):


            if verificar_chance(

                    combo

            ):


                validos.append(

                    combo

                )



    if not validos:

        return None



    # Prioriza combos obrigatórios

    for combo in validos:


        if combo_obrigatorio(

                combo

        ):


            return combo



    return validos[0]



# ==========================================================
# Resolver cadeia de combos
# ==========================================================


def montar_combo(
        habilidade_inicial,
        contexto):


    cadeia = []


    atual = habilidade_inicial


    ordem = 0



    while True:



        combo = selecionar_combo(

            atual,

            contexto,

            ordem

        )



        if not combo:

            break



        destino = obter_proxima_habilidade(

            combo

        )



        if not destino:

            break



        cadeia.append(

            destino

        )


        atual = destino


        ordem += 1



    return cadeia