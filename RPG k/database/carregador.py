"""
====================================
ENGINE RPG v2.0
Arquivo: carregador.py

Responsabilidade:
- Carregar dados do NocoDB.
- Centralizar leitura do banco.
- Converter dados para formato do cache.

Não:
- Calcula regras.
- Executa combate.
- Modifica personagens.

====================================
"""


from database.nocodb import buscar_tabela

from config import TABELAS





# ==========================================================
# Conversão para cache
# ==========================================================


def preparar_registros(registros):


    if not registros:

        return {}





    resultado = {}





    for registro in registros:


        if not isinstance(

                registro,

                dict

        ):

            continue





        chave = registro.get(

            "Id",

            registro.get(

                "id"

            )

        )





        if chave is None:

            continue





        resultado[chave] = registro





    return resultado





# ==========================================================
# Base
# ==========================================================


def carregar_tabela(nome):


    try:


        tabela = TABELAS.get(

            nome

        )





        if not tabela:


            print(

                f"Tabela não configurada: {nome}"

            )


            return {}





        registros = buscar_tabela(

            tabela

        )





        return preparar_registros(

            registros

        )





    except Exception as erro:


        print(

            f"Erro carregando {nome}: {erro}"

        )


        return {}





# ==========================================================
# Personagens
# ==========================================================


def carregar_personagens():


    return carregar_tabela(

        "personagens"

    )





# ==========================================================
# Habilidades
# ==========================================================


def carregar_habilidades():


    return carregar_tabela(

        "habilidades"

    )





# ==========================================================
# Relações
# ==========================================================


def carregar_personagem_habilidades():


    return carregar_tabela(

        "personagem_habilidades"

    )





def carregar_personagem_efeitos():


    return carregar_tabela(

        "personagem_efeitos"

    )





def carregar_habilidade_efeitos():


    return carregar_tabela(

        "habilidade_efeitos"

    )





def carregar_habilidade_acoes():


    return carregar_tabela(

        "habilidade_acoes"

    )





# ==========================================================
# Efeitos
# ==========================================================


def carregar_efeitos():


    return carregar_tabela(

        "efeitos"

    )





# ==========================================================
# Guardas
# ==========================================================


def carregar_guardas():


    return carregar_tabela(

        "guardas"

    )





# ==========================================================
# Sistema
# ==========================================================


def carregar_combos():


    return carregar_tabela(

        "combos"

    )





def carregar_condicoes():


    return carregar_tabela(

        "condicoes"

    )





def carregar_estados():


    return carregar_tabela(

        "estados"

    )





def carregar_tipos():


    return carregar_tabela(

        "tipos"

    )





def carregar_interacoes():


    return carregar_tabela(

        "interacoes"

    )





# ==========================================================
# Combate
# ==========================================================


def carregar_combates():


    return carregar_tabela(

        "combates"

    )





def carregar_participantes_combate():


    return carregar_tabela(

        "participantes_combate"

    )





def carregar_acoes_combate():


    return carregar_tabela(

        "acoes_combate"

    )





def carregar_eventos():


    return carregar_tabela(

        "eventos"

    )





def carregar_dados_combate():


    return carregar_tabela(

        "dados_combate"

    )





# ==========================================================
# Comandos
# ==========================================================


def carregar_comandos():


    return carregar_tabela(

        "comandos"

    )