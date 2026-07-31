"""
====================================
ENGINE RPG v2.0
Arquivo: inicializador.py

Responsabilidade:
- Iniciar cache.
- Carregar dados do NocoDB.
- Preparar engine para uso.

Não:
- Controla combate.
- Calcula regras.
- Executa habilidades.
- Manipula lógica de jogo.

====================================
"""


from database import cache


from database.carregador import (

    carregar_personagens,

    carregar_habilidades,

    carregar_personagem_habilidades,

    carregar_efeitos,

    carregar_personagem_efeitos,

    carregar_habilidade_efeitos,

    carregar_habilidade_acoes,

    carregar_guardas,

    carregar_combos,

    carregar_condicoes,

    carregar_estados,

    carregar_tipos,

    carregar_interacoes,

    carregar_combates,

    carregar_participantes_combate,

    carregar_acoes_combate,

    carregar_eventos,

    carregar_dados_combate,

    carregar_comandos

)





# ==========================================================
# Inicializar Engine
# ==========================================================


def iniciar_engine():


    cache.iniciar_cache()



    carregadores = {


        "personagens":

            carregar_personagens,


        "habilidades":

            carregar_habilidades,


        "personagem_habilidades":

            carregar_personagem_habilidades,


        "efeitos":

            carregar_efeitos,


        "personagem_efeitos":

            carregar_personagem_efeitos,


        "habilidade_efeitos":

            carregar_habilidade_efeitos,


        "habilidade_acoes":

            carregar_habilidade_acoes,


        "guardas":

            carregar_guardas,


        "combos":

            carregar_combos,


        "condicoes":

            carregar_condicoes,


        "estados":

            carregar_estados,


        "tipos":

            carregar_tipos,


        "interacoes":

            carregar_interacoes,


        "combates":

            carregar_combates,


        "participantes_combate":

            carregar_participantes_combate,


        "acoes_combate":

            carregar_acoes_combate,


        "eventos":

            carregar_eventos,


        "dados_combate":

            carregar_dados_combate,


        "comandos":

            carregar_comandos

    }





    sucesso = True





    for nome, funcao in carregadores.items():


        try:


            registros = funcao()



            if registros is None:


                registros = {}



            cache.carregar(

                nome,

                registros

            )



            print(

                f"Carregado: {nome}"

            )



        except Exception as erro:


            print()

            print(

                f"Erro carregando {nome}:"

            )

            print(

                erro

            )


            cache.carregar(

                nome,

                {}

            )


            sucesso = False





    cache.marcar_carregado()



    return sucesso