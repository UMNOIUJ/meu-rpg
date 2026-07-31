"""
====================================
ENGINE RPG v2.0
Arquivo: main.py

Responsabilidade:
- Iniciar a Engine RPG.
- Carregar NocoDB.
- Preparar cache.
- Iniciar sistema USO RPG.

====================================
"""

from database.inicializador import iniciar_engine
from engine.comando import ComandoUSO


def iniciar():

    print()
    print("==============================")
    print("       USO RPG v2.0")
    print("==============================")
    print()


    sucesso = iniciar_engine()


    from database import cache


    print()
    print("===== TESTE NOCODB =====")


    print()
    print("COMBATES:")
    print(
        cache.listar("combates")
    )


    print()
    print("PARTICIPANTES:")
    print(
        cache.listar("participantes_combate")
    )


    print()
    print("COMANDOS:")
    print(
        cache.listar("comandos")
    )


    print()
    print("PERSONAGENS:")
    print(
        cache.listar("personagens")
    )


    print()
    print("========================")



    if not sucesso:

        print()
        print("Erro ao iniciar engine.")
        return



    print()
    print("Engine carregada.")
    print()



    sistema = ComandoUSO()


    sistema.iniciar()



if __name__ == "__main__":

    iniciar()