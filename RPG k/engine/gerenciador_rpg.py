from combate import Combate
from motor_combate import MotorCombate


class GerenciadorRPG:


    def __init__(self, noco):

        self.noco = noco

        self.combate = None

        self.motor = None

        self.personagens = {}



    # ======================================
    # PERSONAGENS
    # ======================================


    def carregar_personagem(self, nome):

        if nome in self.personagens:

            return self.personagens[nome]


        personagem = self.noco.carregar_personagem(

            nome

        )


        if personagem:

            self.personagens[

                personagem.nome

            ] = personagem


        return personagem




    def buscar_personagem(self, nome):

        return self.personagens.get(

            nome

        )




    def limpar_personagens(self):

        self.personagens.clear()



    # ======================================
    # COMBATE
    # ======================================


    def iniciar_combate(self, nome):


        dados = self.noco.criar_combate(

            nome

        )


        if not dados:

            return {

                "Erro":

                "Não foi possível criar combate"

            }



        id_combate = dados.get(

            "Id",

            dados.get(

                "id"

            )

        )


        if not id_combate:

            return {

                "Erro":

                "Combate sem ID"

            }



        self.combate = Combate(

            self.noco,

            id_combate

        )


        self.motor = MotorCombate(

            self.noco,

            self.combate

        )


        return self.combate





    def carregar_combate(self, id_combate):


        if self.combate:


            if self.combate.id_combate == id_combate:

                return self.combate




        dados = self.noco.buscar_combate(

            id_combate

        )


        if not dados:

            return {

                "Erro":

                "Combate não encontrado"

            }




        self.combate = Combate(

            self.noco,

            id_combate

        )


        self.motor = MotorCombate(

            self.noco,

            self.combate

        )


        self.personagens.clear()



        participantes = self.noco.buscar_participantes_combate(

            id_combate

        )



        for participante in participantes:


            personagem_data = participante.get(

                "Personagem",

                []

            )


            if not personagem_data:

                continue



            nome = personagem_data[0].get(

                "Nome"

            )



            ordem = participante.get(

                "Ordem",

                0

            )



            personagem = self.carregar_personagem(

                nome

            )


            if personagem:


                self.motor.adicionar_personagem(

                    personagem,

                    ordem

                )



        return self.combate





    def adicionar_personagem_combate(
        self,
        personagem,
        ordem=0
    ):


        personagem_obj = self.carregar_personagem(

            personagem

        )


        if not personagem_obj:


            return {

                "Erro":

                "Personagem não encontrado"

            }




        if not self.motor:


            return {

                "Erro":

                "Nenhum combate ativo"

            }




        self.motor.adicionar_personagem(

            personagem_obj,

            ordem

        )


        return personagem_obj





    def finalizar_combate(self):


        if self.combate:


            self.noco.finalizar_combate(

                self.combate.id_combate

            )



        if self.motor:


            self.motor.finalizar()



        self.combate = None

        self.motor = None

        self.personagens.clear()





    # ======================================
    # TURNOS
    # ======================================


    def iniciar_turnos(self):


        if not self.motor:

            return {

                "Erro":

                "Nenhum combate ativo"

            }


        return self.motor.iniciar()




    def escolher_turno(self, personagem):


        if not self.motor:

            return False



        alvo = self.buscar_personagem(

            personagem

        )


        if not alvo:

            alvo = self.carregar_personagem(

                personagem

            )



        if not alvo:

            return False



        return self.motor.definir_turno(

            alvo

        )





    def finalizar_turno(self):


        if not self.motor:

            return None


        return self.motor.finalizar_turno()




    def nova_rodada(self):


        if not self.motor:

            return None


        return self.motor.nova_rodada()




    # ======================================
    # HABILIDADES
    # ======================================


    def usar_habilidade(
        self,
        atacante_nome,
        alvo_nome,
        habilidade_nome
    ):


        if not self.combate:


            return {

                "Erro":

                "Nenhum combate ativo"

            }




        atacante = self.buscar_personagem(

            atacante_nome

        )


        alvo = self.buscar_personagem(

            alvo_nome

        )



        if not atacante:

            atacante = self.carregar_personagem(

                atacante_nome

            )


        if not alvo:

            alvo = self.carregar_personagem(

                alvo_nome

            )




        if not atacante or not alvo:


            return {

                "Erro":

                "Personagem não encontrado"

            }




        habilidade = atacante.buscar_habilidade(

            habilidade_nome

        )



        if not habilidade:


            return {

                "Erro":

                "Habilidade não encontrada"

            }




        rodada = 1


        if self.motor:

            rodada = self.motor.rodada




        resultado = self.combate.atacar(

            atacante,

            alvo,

            habilidade,

            rodada

        )




        self.noco.salvar_personagem(

            atacante

        )


        self.noco.salvar_personagem(

            alvo

        )



        return resultado





    # ======================================
    # INFORMAÇÕES
    # ======================================


    def estado_combate(self):


        if not self.motor:


            return {

                "Erro":

                "Nenhum combate ativo"

            }



        return self.motor.resumo()