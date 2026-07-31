# engine/status.py



class Status:


    def __init__(

            self,

            nome,

            tipo="neutro",

            valor=0,

            duracao=1,

            stacks=1,

            stack_max=1):


        self.nome = nome


        self.tipo = tipo


        self.valor = valor


        self.duracao = duracao


        self.stacks = stacks


        self.stack_max = stack_max







    def adicionar_stack(self):


        if self.stacks < self.stack_max:


            self.stacks += 1


            return True



        return False







    def remover_stack(self):


        if self.stacks > 0:


            self.stacks -= 1


            return True



        return False







    def reduzir_duracao(self):


        if self.duracao > 0:


            self.duracao -= 1





        return self.duracao







    def expirou(self):


        return self.duracao <= 0







    def multiplicador(self):


        return self.valor * self.stacks







    def dados(self):


        return {


            "Nome": self.nome,


            "Tipo": self.tipo,


            "Valor": self.valor,


            "Duração": self.duracao,


            "Stacks": self.stacks,


            "Stack Máximo": self.stack_max

        }