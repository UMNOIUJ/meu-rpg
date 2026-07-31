"""
====================================
ENGINE RPG v1.0
Arquivo: condicao.py

Responsabilidade:
Verificar condições de habilidades,
combos e efeitos.

Não:
- Calcula dano.
- Executa ações.
- Acessa NocoDB diretamente.

====================================
"""


from engine.efeito import possui_efeito



# ==========================================================
# Auxiliares
# ==========================================================


def normalizar_nome(
        valor):


    if not valor:

        return ""


    return str(valor).upper().strip()



def obter_personagem(
        contexto,
        chave):


    return contexto.get(
        chave
    )



def esta_vivo(
        personagem):


    if not personagem:

        return False



    if hasattr(
            personagem,
            "esta_vivo"
    ):

        return personagem.esta_vivo()



    return personagem.hp_atual > 0




# ==========================================================
# Verificar condição
# ==========================================================


def verificar_condicao(
        condicao,
        contexto):


    if not condicao:

        return False



    nome = normalizar_nome(
        condicao
    )



    usuario = obter_personagem(

        contexto,

        "Usuario"

    )


    alvo = obter_personagem(

        contexto,

        "Alvo"

    )


    resultado = contexto.get(

        "Resultado",

        {}

    )



    # ======================================================
    # Básicas
    # ======================================================


    if nome == "SEMPRE":

        return True



    # ======================================================
    # Resultado do ataque
    # ======================================================


    if nome == "ACERTO":

        return resultado.get(

            "Acertou",

            False

        )



    if nome == "ERRO":

        return not resultado.get(

            "Acertou",

            False

        )



    if nome == "PARCIAL":

        return resultado.get(

            "Parcial",

            False

        )



    if nome == "CRITICO":

        return resultado.get(

            "Critico",

            False

        )



    # ======================================================
    # Embate
    # ======================================================


    if nome == "EMBATE_VENCIDO":

        return resultado.get(

            "Embate"

        ) == "VENCIDO"



    if nome == "EMBATE_PERDIDO":

        return resultado.get(

            "Embate"

        ) == "PERDIDO"



    # ======================================================
    # Estado alvo
    # ======================================================


    if nome == "ALVO_VIVO":

        return esta_vivo(
            alvo
        )



    if nome == "ALVO_MORTO":

        return alvo is not None and not esta_vivo(
            alvo
        )



    # ======================================================
    # Vida
    # ======================================================


    if nome == "HP_MENOR_50":


        if not alvo:

            return False



        return (

            alvo.hp_atual

            <=

            alvo.hp_maximo / 2

        )



    if nome == "HP_MAIOR_50":


        if not alvo:

            return False



        return (

            alvo.hp_atual

            >

            alvo.hp_maximo / 2

        )



    if nome == "HP_CHEIO":


        if not alvo:

            return False



        return alvo.hp_atual == alvo.hp_maximo



    if nome == "HP_BAIXO":


        if not alvo:

            return False



        return alvo.hp_atual < alvo.hp_maximo



    # ======================================================
    # SAN
    # ======================================================


    if nome == "SAN_MENOR_50":


        if not alvo:

            return False



        return (

            alvo.san_atual

            <=

            alvo.san_maxima / 2

        )



    if nome == "SAN_MAIOR_50":


        if not alvo:

            return False



        return (

            alvo.san_atual

            >

            alvo.san_maxima / 2

        )



    if nome == "SAN_CHEIA":


        if not alvo:

            return False



        return alvo.san_atual == alvo.san_maxima



    # ======================================================
    # Efeitos
    # ======================================================


    if nome == "POSSUI_EFEITO":


        if not alvo:

            return False



        return len(
            alvo.efeitos
        ) > 0




    if nome == "NÃO_POSSUI_EFEITO":


        if not alvo:

            return False



        return len(
            alvo.efeitos
        ) == 0



    # ======================================================
    # Efeito específico
    # ======================================================


    if nome.startswith(
        "EFEITO:"
    ):


        if not alvo:

            return False



        nome_efeito = condicao.split(
            ":",
            1
        )[1].strip()



        return possui_efeito(

            alvo,

            nome_efeito

        )



    # ======================================================
    # Guarda
    # ======================================================


    if nome == "POSSUI_GUARDA":


        if not alvo:

            return False



        return alvo.possui_guarda()



    if nome == "SEM_GUARDA":


        if not alvo:

            return False



        return not alvo.possui_guarda()



    # ======================================================
    # Combo
    # ======================================================


    if nome == "PRIMEIRO_ACERTO":


        return contexto.get(

            "PrimeiroAcerto",

            False

        )



    if nome == "ULTIMO_ACERTO":


        return contexto.get(

            "UltimoAcerto",

            False

        )



    if nome == "PRIMEIRA_HABILIDADE":


        return contexto.get(

            "PrimeiraHabilidade",

            False

        )



    if nome == "ULTIMA_HABILIDADE":


        return contexto.get(

            "UltimaHabilidade",

            False

        )



    # ======================================================
    # Desconhecida
    # ======================================================


    return False