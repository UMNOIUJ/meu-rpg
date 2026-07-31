class Combate:


    def __init__(
        self,
        nocodb
    ):


        self.nocodb = nocodb

        self.turno = 1



    def escolher_personagem(
        self,
        personagens
    ):


        vivos = [

            p for p in personagens

            if p.esta_vivo()

        ]


        for i,p in enumerate(
            vivos,
            1
        ):


            print(

                i,
                "-",
                p.nome,
                f"{p.hp_atual}/{p.hp_maximo}"

            )


        escolha = int(
            input(
                "Quem age: "
            )
        )


        return vivos[
            escolha-1
        ]



    def escolher_habilidade(
        self,
        personagem
    ):


        for i,h in enumerate(
            personagem.habilidades,
            1
        ):


            print(

                i,
                "-",
                h.nome

            )


        escolha = int(

            input(
                "Habilidade: "
            )

        )


        return personagem.habilidades[
            escolha-1
        ]



    def escolher_alvo(
        self,
        personagens
    ):


        vivos = [

            p for p in personagens

            if p.esta_vivo()

        ]


        for i,p in enumerate(
            vivos,
            1
        ):


            print(

                i,
                "-",
                p.nome

            )



        escolha = int(

            input(
                "Alvo: "
            )

        )


        return vivos[
            escolha-1
        ]



    def atacar(
        self,
        atacante,
        defensor,
        habilidade
    ):



        if not atacante.pode_agir():

            return



        print(

            atacante.nome,

            "usa",

            habilidade.nome

        )



        hp_antes = defensor.hp_atual



        interacao = self.nocodb.buscar_interacao(

            habilidade.tipo,

            defensor.defesa

        )



        dano = habilidade.dano



        resultado = "Normal"



        if interacao:


            resultado = interacao.get(

                "Resultado",

                "Normal"

            )


            dano += int(

                interacao.get(

                    "Dano",

                    0

                )

                or 0

            )


            dano += int(

                interacao.get(

                    "Dano Psíquico",

                    0

                )

                or 0

            )



            if interacao.get(

                "Atordoado",

                False

            ):


                defensor.atordoado = True



        defensor.receber_dano(
            dano
        )



        atacante.perder_sanidade(

            habilidade.custo_san

        )



        hp_depois = defensor.hp_atual



        status = "Normal"


        if defensor.morto:

            status = "Morto"


        elif defensor.atordoado:

            status = "Atordoado"



        print(

            "Dano causado:",

            dano

        )



        print(

            defensor.mostrar()

        )



        # SALVAR LOG


        self.nocodb.salvar_log_combate(

            {


            "Turno":

            self.turno,


            "Atacante":

            atacante.nome,


            "Alvo":

            defensor.nome,


            "Habilidade":

            habilidade.nome,


            "Dano":

            dano,


            "Resultado":

            resultado,


            "Dano SAN":

            habilidade.custo_san,


            "HP Antes":

            hp_antes,


            "HP Depois":

            hp_depois,


            "Status":

            status


            }

        )