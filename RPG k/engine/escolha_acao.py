# escolha_acao.py


from personagem import habilidades_personagem






def mostrar_habilidades(

        personagem_id):


    habilidades = habilidades_personagem(

        personagem_id

    )



    print()



    for indice, habilidade in enumerate(

            habilidades,

            1):


        print(

            indice,

            "-",

            habilidade["Nome"]

        )



    return habilidades






def escolher_habilidade(

        personagem_id):


    habilidades = mostrar_habilidades(

        personagem_id

    )



    escolha = int(

        input(

            "Escolha a habilidade: "

        )

    )



    return habilidades[

        escolha - 1

    ]["Nome"]