"""
====================================
ENGINE RPG v2.0
Arquivo: embate.py

Responsabilidade:
- Representar confronto entre ação ofensiva e alvo.
- Resolver disputa de acerto.
- Determinar crítico.
- Gerar dados para habilidade.py.
Arquivo: embate.py

Estado:
- MODO FINAL
- Arquivo estabilizado.
- Não alterar arquitetura sem solicitação explícita.

Não:
- Calcula dano.
- Executa habilidade.
- Aplica efeitos.
- Controla turnos.
- Acessa NocoDB.

====================================
"""


from engine.calculos import calcular_critico
from engine.dados import rolar_dados





class Embate:



    def __init__(

            self,

            atacante,

            defensor,

            habilidade):


        self.atacante = atacante

        self.defensor = defensor

        self.habilidade = habilidade or {}

        self.resultado = None





# ======================================================
# Resolver embate
# ======================================================


    def resolver(self):


        if not self.atacante or not self.defensor:


            self.resultado = {


                "Sucesso":

                    False,


                "Acertos":

                    0,


                "Critico":

                    False,


                "Parcial":

                    False


            }


            return self.resultado





        acertos = self.calcular_acertos()


        critico = self.verificar_critico()



        self.resultado = {


            "Sucesso":

                acertos > 0,


            "Atacante":

                self.atacante,


            "Defensor":

                self.defensor,


            "Habilidade":

                self.habilidade,


            "Acertos":

                acertos,


            "Critico":

                critico,


            "Parcial":

                self.verificar_parcial(

                    acertos

                )


        }



        return self.resultado





# ======================================================
# Acertos
# ======================================================


    def calcular_acertos(self):


        quantidade = self.converter_numero(

            self.habilidade.get(

                "Acertos",

                1

            ),

            1

        )



        total = 0



        for _ in range(quantidade):


            ataque = self.rolar_acerto()


            defesa = self.rolar_defesa()



            if ataque > defesa:

                total += 1




        return total





# ======================================================
# Rolagem ataque
# ======================================================


    def rolar_acerto(self):


        dado = self.converter_numero(

            self.habilidade.get(

                "Dado Acerto",

                20

            ),

            20

        )



        resultado = rolar_dados(

            1,

            dado

        )



        if isinstance(resultado, dict):

            return resultado.get(

                "Total",

                0

            )


        return resultado





# ======================================================
# Defesa
# ======================================================


    def rolar_defesa(self):


        if hasattr(

                self.defensor,

                "obter_defesa"):


            return self.defensor.obter_defesa()



        defesa = getattr(

            self.defensor,

            "defesa",

            0

        )



        return self.converter_numero(

            defesa

        )





# ======================================================
# Parcial
# ======================================================


    def verificar_parcial(

            self,

            acertos):


        ativo = self.habilidade.get(

            "Parcial",

            False

        )



        if isinstance(

                ativo,

                str):


            ativo = ativo.lower() in (

                "true",

                "1",

                "sim"

            )



        return ativo and acertos == 0





# ======================================================
# Crítico
# ======================================================


    def verificar_critico(self):


        chance = self.habilidade.get(

            "Critico",

            self.habilidade.get(

                "Chance Crítico",

                0

            )

        )



        return calcular_critico(

            self.converter_numero(

                chance

            )

        )





# ======================================================
# Conversão
# ======================================================


    def converter_numero(

            self,

            valor,

            padrao=0):


        try:


            if isinstance(

                    valor,

                    str):


                valor = valor.replace(

                    "d",

                    ""

                ).replace(

                    "D",

                    ""

                )



            return int(valor)



        except (

            TypeError,

            ValueError

        ):


            return padrao





# ======================================================
# Resultado
# ======================================================


    def obter_resultado(self):

        return self.resultado





# ======================================================
# Informações
# ======================================================


    def dados(self):


        return {


            "Atacante":

                self.atacante.nome

                if self.atacante

                else None,


            "Defensor":

                self.defensor.nome

                if self.defensor

                else None,


            "Habilidade":

                self.habilidade.get(

                    "Nome"

                )

        }





# ======================================================
# Compatibilidade antiga
# ======================================================


def resolver_embate(embate):


    if isinstance(

            embate,

            Embate):


        return embate.resolver()



    objeto = Embate(

        embate.get(

            "Atacante"

        ),

        embate.get(

            "Defensor"

        ),

        embate.get(

            "Habilidade"

        )

    )



    return objeto.resolver()