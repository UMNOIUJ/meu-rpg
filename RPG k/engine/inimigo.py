# engine/inimigo.py


from engine.personagem import Personagem




class Inimigo(Personagem):


    def __init__(

            self,

            dados):


        super().__init__(

            dados

        )


        self.tipo = dados.get(

            "Tipo",

            "Inimigo"

        )


        self.nivel = dados.get(

            "Nivel",

            1

        )


        self.ataques = []






    def adicionar_habilidade(

            self,

            habilidade):


        self.ataques.append(

            habilidade

        )







    def remover_habilidade(

            self,

            habilidade):


        if habilidade in self.ataques:


            self.ataques.remove(

                habilidade

            )







    def informacoes(self):


        return {


            "Nome":

                self.nome,


            "Tipo":

                self.tipo,


            "HP":

                self.hp_atual,


            "HP Máximo":

                self.hp_maximo,


            "SAN":

                self.san_atual,


            "Status":

                self.status


        }