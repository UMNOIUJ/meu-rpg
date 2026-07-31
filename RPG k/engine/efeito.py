"""
====================================
ENGINE RPG v2.0
Arquivo: efeito.py

Responsabilidade:
Gerenciar efeitos ativos.

Não:
- Calcula dano.
- Resolve combate.
- Executa habilidades.
- Acessa NocoDB diretamente.

====================================
"""


from database import cache





# ==========================================================
# Conversões
# ==========================================================


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





def converter_numero(valor, padrao=0):


    try:

        return int(valor)


    except (TypeError, ValueError):

        return padrao





# ==========================================================
# Criar efeito
# ==========================================================


def criar_efeito(efeito, stacks=1):


    duracao = converter_numero(

        efeito.get(
            "Duração",
            0
        )

    )



    return {


        "Id":

            efeito.get(
                "Id"
            ),



        "Nome":

            efeito.get(
                "Nome",
                ""
            ),



        "Tipo":

            efeito.get(
                "Tipo"
            ),



        "Valor":

            converter_numero(

                efeito.get(
                    "Valor",
                    0
                )

            ),



        "Duração":

            duracao,



        "Turnos Restantes":

            duracao,



        "Stacks":

            converter_numero(
                stacks,
                1
            ),



        "Máximo Stack":

            converter_numero(

                efeito.get(
                    "Máximo Stack",
                    1
                ),

                1

            ),



        "Permanente":

            converter_bool(

                efeito.get(
                    "Permanente",
                    False
                )

            ),



        "Ativo":

            True,


        "Dados":

            efeito

    }





# ==========================================================
# Aplicar efeito
# ==========================================================


def aplicar_efeito(personagem, efeito):


    if not efeito:

        return False



    nome = efeito.get(
        "Nome"
    )


    if not nome:

        return False





    if not hasattr(
            personagem,
            "efeitos"):

        personagem.efeitos = []





    for ativo in personagem.efeitos:



        if ativo.get(
                "Nome"
        ) == nome:



            max_stack = converter_numero(

                ativo.get(
                    "Máximo Stack",
                    1
                ),

                1

            )



            stacks = converter_numero(

                ativo.get(
                    "Stacks",
                    1
                ),

                1

            )



            if stacks < max_stack:

                ativo["Stacks"] = stacks + 1





            if not ativo.get(

                    "Permanente",

                    False

            ):


                ativo["Turnos Restantes"] = converter_numero(

                    efeito.get(
                        "Duração",
                        ativo.get(
                            "Turnos Restantes",
                            0
                        )
                    )

                )



            return True





    personagem.efeitos.append(

        criar_efeito(

            efeito

        )

    )



    return True





# ==========================================================
# Aplicar por nome
# ==========================================================


def aplicar_efeito_por_nome(personagem, nome):


    efeitos = cache.listar(

        "efeitos"

    )



    for efeito in efeitos.values():



        if efeito.get(
                "Nome"
        ) == nome:



            return aplicar_efeito(

                personagem,

                efeito

            )



    return False





# ==========================================================
# Remover efeito
# ==========================================================


def remover_efeito(personagem, nome):


    personagem.efeitos = [

        efeito

        for efeito in personagem.efeitos

        if efeito.get(
            "Nome"
        ) != nome

    ]





# ==========================================================
# Atualizar duração
# ==========================================================


def atualizar_efeitos(personagem):


    remover = []



    for efeito in personagem.efeitos:



        if efeito.get(
                "Permanente",
                False
        ):

            continue





        efeito["Turnos Restantes"] = converter_numero(

            efeito.get(
                "Turnos Restantes",
                0
            )

        ) - 1





        if efeito["Turnos Restantes"] <= 0:


            remover.append(

                efeito.get(
                    "Nome"
                )

            )





    for nome in remover:


        remover_efeito(

            personagem,

            nome

        )





# ==========================================================
# Verificar efeito
# ==========================================================


def possui_efeito(personagem, nome):


    return any(

        efeito.get(
            "Nome"
        ) == nome

        for efeito in personagem.efeitos

    )





# ==========================================================
# Obter bônus
# ==========================================================


def obter_bonus_efeitos(personagem, tipo_bonus):


    total = 0



    for efeito in personagem.efeitos:



        if efeito.get(
                "Tipo"
        ) == tipo_bonus:



            total += (

                converter_numero(

                    efeito.get(
                        "Valor",
                        0
                    )

                )

                *

                converter_numero(

                    efeito.get(
                        "Stacks",
                        1
                    ),

                    1

                )

            )



    return total





# ==========================================================
# Estados
# ==========================================================


def obter_estados(personagem):


    return [

        efeito.get(
            "Nome"
        )

        for efeito in personagem.efeitos

        if efeito.get(
            "Tipo"
        ) == "Estado"

    ]





# ==========================================================
# Limpar efeitos
# ==========================================================


def limpar_efeitos(personagem):


    personagem.efeitos.clear()





# ==========================================================
# Buscar efeitos da habilidade
# ==========================================================


def obter_efeitos_habilidade(habilidade, tabela=None):


    resultado = []



    if tabela is None:

        tabela = cache.listar(

            "habilidade_efeitos"

        ).values()





    for registro in tabela:



        relacao = registro.get(

            "Habilidade"

        )



        if isinstance(
                relacao,
                dict):

            nome = relacao.get(
                "Nome"
            )


        else:

            nome = relacao





        if nome != habilidade:

            continue





        efeito = registro.get(

            "Efeito"

        )



        if isinstance(
                efeito,
                dict):

            resultado.append(
                efeito
            )



    return resultado





# ==========================================================
# Aplicar efeitos da habilidade
# ==========================================================


def aplicar_efeitos_habilidade(personagem, habilidade, tabela=None):


    aplicados = []



    efeitos = obter_efeitos_habilidade(

        habilidade,

        tabela

    )



    for efeito in efeitos:



        if aplicar_efeito(

            personagem,

            efeito

        ):


            aplicados.append(

                efeito.get(
                    "Nome"
                )

            )



    return aplicados