from combatlog import CombatLog


class Batalha:


    def __init__(
        self,
        combate
    ):

        self.combate = combate

        self.log = CombatLog()

        self.turno = 1



    def escolher_habilidade(
        self,
        habilidades
    ):

        print()

        print("Escolha uma habilidade:")

        print("----------------------")


        for i, habilidade in enumerate(
            habilidades
        ):

            print(
                f"{i + 1} - {habilidade.nome}"
            )


        escolha = int(
            input("> ")
        )


        return habilidades[
            escolha - 1
        ]



    def executar_turno(
        self,
        atacante,
        defensor,
        habilidades
    ):

        print()

        print(
            f"===== TURNO {self.turno} ====="
        )


        habilidade = self.escolher_habilidade(
            habilidades
        )


        self.log.mostrar_inicio(

            atacante,

            defensor,

            habilidade

        )


        resultado = self.combate.atacar(

            atacante,

            defensor,

            habilidade

        )


        self.log.mostrar_interacao(

            resultado

        )


        self.log.mostrar_resultado(

            defensor,

            resultado

        )


        self.turno += 1



    def acabou(
        self,
        personagem
    ):

        return personagem.hp_atual <= 0