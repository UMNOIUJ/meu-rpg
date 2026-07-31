"""
====================================
ENGINE RPG v2.0
Arquivo: guarda.py

Responsabilidade:
- Gerenciar guardas ativas.
- Interpretar guardas vindas do cache NocoDB.
- Controlar duração.
- Fornecer bônus defensivos.
- Fornecer reações defensivas.

Não:
- Calcula dano.
- Resolve combate.
- Acessa NocoDB diretamente.
- Modifica HP/SAN.

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
# Classe Guarda
# ==========================================================


class Guarda:


    def __init__(self, dados):


        self.id = dados.get(
            "Id"
        )


        self.nome = dados.get(
            "Nome",
            ""
        )


        self.descricao = dados.get(
            "Descrição",
            ""
        )


        self.ativa = converter_bool(
            dados.get(
                "Ativa",
                True
            )
        )


        self.duracao = converter_numero(
            dados.get(
                "Duração",
                1
            ),
            1
        )


        self.turnos_restantes = self.duracao



        self.permanente = converter_bool(
            dados.get(
                "Permanente",
                False
            )
        )



        self.bonus_defesa = converter_numero(
            dados.get(
                "Bônus Defesa",
                0
            )
        )



        self.reducao_dano_percentual = converter_numero(
            dados.get(
                "Redução Dano %",
                0
            )
        )


        self.reducao_dano_fixo = converter_numero(
            dados.get(
                "Redução Dano Fixo",
                0
            )
        )



        self.permite_desvio = converter_bool(
            dados.get(
                "Permite Desvio",
                False
            )
        )


        self.valor_desvio = converter_numero(
            dados.get(
                "Valor Desvio",
                0
            )
        )



        self.permite_contra_ataque = converter_bool(
            dados.get(
                "Permite Contra Ataque",
                False
            )
        )


        self.bonus_contra_ataque = converter_numero(
            dados.get(
                "Bônus Contra Ataque",
                0
            )
        )



        self.penetra_defesa = converter_bool(
            dados.get(
                "Penetra Defesa",
                False
            )
        )


        self.condicao = dados.get(
            "Condição"
        )


        self.dados = dados





# ==========================================================
# Buscar guarda
# ==========================================================


def buscar_guarda(nome):


    guardas = cache.listar(
        "guardas"
    )



    for dados in guardas.values():


        if dados.get(
            "Nome"
        ) == nome:


            return Guarda(
                dados
            )



    return None





# ==========================================================
# Ativar
# ==========================================================


def ativar_guarda(
        personagem,
        guarda):


    if isinstance(
            guarda,
            dict):

        guarda = Guarda(
            guarda
        )



    personagem.guarda_ativa = guarda


    return guarda





# ==========================================================
# Remover
# ==========================================================


def remover_guarda(personagem):


    personagem.guarda_ativa = None





# ==========================================================
# Atualizar duração
# ==========================================================


def atualizar_guarda(personagem):


    guarda = getattr(
        personagem,
        "guarda_ativa",
        None
    )


    if not guarda:

        return



    if guarda.permanente:

        return



    guarda.turnos_restantes -= 1



    if guarda.turnos_restantes <= 0:

        remover_guarda(
            personagem
        )





# ==========================================================
# Verificar
# ==========================================================


def possui_guarda(personagem):


    return getattr(
        personagem,
        "guarda_ativa",
        None
    ) is not None





# ==========================================================
# Defesa
# ==========================================================


def obter_bonus_defesa(personagem):


    if not possui_guarda(
            personagem):

        return 0



    return personagem.guarda_ativa.bonus_defesa





def obter_reducao(personagem):


    if not possui_guarda(
            personagem):

        return {

            "Percentual": 0,

            "Fixo": 0

        }



    guarda = personagem.guarda_ativa


    return {

        "Percentual":

            guarda.reducao_dano_percentual,


        "Fixo":

            guarda.reducao_dano_fixo

    }





# ==========================================================
# Reações
# ==========================================================


def permite_desvio(personagem):


    return (

        possui_guarda(personagem)

        and

        personagem.guarda_ativa.permite_desvio

    )





def valor_desvio(personagem):


    if not permite_desvio(
            personagem):

        return 0



    return personagem.guarda_ativa.valor_desvio





def permite_contra_ataque(personagem):


    return (

        possui_guarda(personagem)

        and

        personagem.guarda_ativa.permite_contra_ataque

    )





def bonus_contra_ataque(personagem):


    if not permite_contra_ataque(
            personagem):

        return 0



    return personagem.guarda_ativa.bonus_contra_ataque  