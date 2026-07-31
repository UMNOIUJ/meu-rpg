# engine/defesa.py


from engine.efeito import obter_bonus_efeitos







def obter_tipo_ataque(habilidade):


    return habilidade.get(

        "Tipo",

        "Normal"

    )









def obter_defesas(personagem):


    if hasattr(

            personagem,

            "defesas"):


        return personagem.defesas



    return []











def encontrar_defesa(

        personagem,

        tipo_ataque):


    defesas = obter_defesas(

        personagem

    )





    for defesa in defesas:



        if defesa.get(

                "Tipo"

        ) == tipo_ataque:



            return defesa






    return None











def aplicar_defesa(

        dano,

        habilidade,

        alvo):



    tipo_ataque = obter_tipo_ataque(

        habilidade

    )





    defesa = encontrar_defesa(

        alvo,

        tipo_ataque

    )






    reducao = 0







    if defesa:


        reducao = defesa.get(

            "Reducao",

            0

        )









    try:


        reducao = float(

            reducao

        )


    except:


        reducao = 0







    # buffs e debuffs de defesa


    bonus_defesa = obter_bonus_efeitos(

        alvo,

        "Defesa"

    )



    reducao += bonus_defesa







    if reducao < 0:


        reducao = 0







    if reducao > 100:


        reducao = 100







    dano_final = dano - (

        dano *

        reducao /

        100

    )







    if dano_final < 0:


        dano_final = 0







    return int(

        dano_final

    )