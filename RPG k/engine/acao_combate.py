# acao_combate.py


from nocodb import criar_registro

from config import TABELAS






def registrar_acao(

        combate,

        personagem,

        habilidade,

        dano,

        dano_san,

        resultado):



    dados = {


        "Combate":

            combate,


        "Personagem":

            personagem,


        "Habilidade Escolhida":

            habilidade,


        "Dano":

            dano,


        "Dano SAN":

            dano_san,


        "Resultado":

            resultado

    }




    return criar_registro(

        TABELAS["acoes"],

        dados

    )