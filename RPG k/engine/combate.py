"""
====================================
ENGINE RPG v2.0

Arquivo: combate.py

Estado:
- MODO FINAL
- Arquivo estabilizado.
- Não alterar arquitetura sem solicitação explícita.
====================================

Este arquivo NÃO:
- Calcula dano.
- Resolve embates.
- Executa habilidades diretamente.
- Acessa NocoDB.

====================================
"""


from engine.turno import Turno
from engine.motor_combate import MotorCombate
from engine.efeito import atualizar_efeitos
from engine.comando import ComandoUSO





class Combate:



    def __init__(

            self,

            participantes):


        self.participantes = participantes


        self.turno_atual = 1


        self.finalizado = False


        self.historico = []


        self.resultados = []


        self.comando = ComandoUSO()


        self.motor = MotorCombate(

            self

        )





# ======================================================
# Iniciar combate
# ======================================================


    def iniciar(self):


        print("==============================")

        print("       COMBATE INICIADO")

        print("==============================")


        print()



        nomes = " VS ".join(

            [

                personagem.nome

                for personagem in self.participantes

            ]

        )



        print(nomes)

        print()



        while not self.finalizado:



            turno = Turno(

                self,

                self.comando,

                self.turno_atual

            )



            acoes = turno.executar()



            self.executar_acoes_turno(

                acoes

            )



            turno.finalizar()



            self.finalizar_turno()



            self.verificar_estado()



            if not self.finalizado:

                self.proximo_turno()





        print()

        print("==============================")

        print("COMBATE FINALIZADO")

        print("==============================")









# ======================================================
# Executar ações do turno
# ======================================================


    def executar_acoes_turno(

            self,

            acoes):


        if not acoes:

            return []



        self.motor.limpar()



        for acao in acoes:


            self.motor.adicionar_acao(

                acao

            )





        resultados = self.motor.executar_acoes()



        self.resultados.extend(

            resultados

        )



        self.motor.limpar()



        return resultados









# ======================================================
# Finalizar turno
# ======================================================


    def finalizar_turno(self):


        for personagem in self.participantes:



            atualizar_efeitos(

                personagem

            )



            self.atualizar_guardas(

                personagem

            )









# ======================================================
# Guardas
# ======================================================


    def atualizar_guardas(

            self,

            personagem):


        guarda = getattr(

            personagem,

            "guarda_ativa",

            None

        )



        if not guarda:

            return





        if isinstance(

                guarda,

                dict):


            if guarda.get(

                "Permanente",

                False

            ):

                return



            guarda["Turnos Restantes"] = guarda.get(

                "Turnos Restantes",

                0

            ) - 1



            if guarda["Turnos Restantes"] <= 0:

                personagem.guarda_ativa = None



            return







        if getattr(

                guarda,

                "permanente",

                False):

            return





        guarda.duracao -= 1





        if guarda.duracao <= 0:


            personagem.guarda_ativa = None









# ======================================================
# Próximo turno
# ======================================================


    def proximo_turno(self):


        self.turno_atual += 1







# ======================================================
# Alvos válidos
# ======================================================


    def obter_alvos_validos(

            self,

            atacante):


        return [

            personagem

            for personagem in self.participantes

            if personagem != atacante

            and personagem.esta_vivo()

        ]









# ======================================================
# Vitória
# ======================================================


    def verificar_estado(self):


        vivos = [

            personagem

            for personagem in self.participantes

            if personagem.esta_vivo()

        ]





        if len(vivos) <= 1:


            self.finalizado = True



            print()



            if vivos:


                print(

                    f"{vivos[0].nome} venceu!"

                )


            else:


                print(

                    "Todos foram derrotados."

                )











# ======================================================
# Eventos
# ======================================================


    def registrar_evento(

            self,

            evento):


        self.historico.append(

            evento

        )


        print()

        print("==============================")

        print(evento)

        print("==============================")











# ======================================================
# Participantes
# ======================================================


    def obter_participantes(self):


        return self.participantes