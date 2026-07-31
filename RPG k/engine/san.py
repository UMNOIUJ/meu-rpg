# engine/san.py





def aplicar_custo_san(

        personagem,

        habilidade):


    custo = habilidade.get(

        "Custo SAN",

        0

    )


    try:

        custo = int(custo)

    except:

        custo = 0






    if custo <= 0:


        return 0







    personagem.perder_san(

        custo

    )



    return custo







def aplicar_dano_san(

        personagem,

        valor):


    try:

        valor = int(valor)

    except:

        valor = 0






    if valor <= 0:


        return 0






    personagem.perder_san(

        valor

    )



    return valor







def recuperar_san(

        personagem,

        valor):


    try:

        valor = int(valor)

    except:

        valor = 0






    personagem.san_atual += valor






    if personagem.san_atual > personagem.san_maximo:


        personagem.san_atual = personagem.san_maximo






    return valor







def verificar_san_baixa(

        personagem,

        limite):


    return personagem.san_atual <= limite