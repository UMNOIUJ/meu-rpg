"""
====================================
ENGINE RPG v2.0
Arquivo: motor_combate.py

Estado:
- MODO FINAL
- Arquivo estabilizado.
- Não alterar arquitetura sem solicitação explícita.

Responsabilidade:
- Executar ações escolhidas no USO RPG.
- Encaminhar ações para habilidades.
- Organizar resultados.
- Registrar eventos do combate.

Este arquivo NÃO:
- Controla turnos.
- Escolhe ações.
- Calcula dano diretamente.
- Resolve embates separados.
- Aplica efeitos diretamente.
- Acessa NocoDB.

====================================
"""


from engine.habilidade import (
    buscar_habilidade,
    executar_habilidade
)





# ======================================================
# Motor de Combate
# ======================================================


class MotorCombate:



    def __init__(self, combate):

        self.combate = combate

        self.acoes = []

        self.resultados = []





# ======================================================
# Obter valor da ação
# ======================================================


    def obter_valor_acao(self, acao, chave):


        if isinstance(acao, dict):

            campos = {

                "tipo": "Tipo",

                "nome": "Nome",

                "alvo": "Alvo",

                "usuario": "Usuario"

            }


            return acao.get(

                campos.get(

                    chave,

                    chave

                )

            )



        return getattr(

            acao,

            chave,

            None

        )





# ======================================================
# Receber ações
# ======================================================


    def adicionar_acao(self, acao):


        self.acoes.append(

            acao

        )


        return acao





# ======================================================
# Executar uma ação
# ======================================================


    def executar_acao(self, acao):


        tipo = self.obter_valor_acao(

            acao,

            "tipo"

        )



        if tipo != "HABILIDADE":


            return {

                "Erro":

                    "Tipo de ação não suportado"

            }





        usuario = self.obter_valor_acao(

            acao,

            "usuario"

        )



        alvo = self.obter_valor_acao(

            acao,

            "alvo"

        )



        nome = self.obter_valor_acao(

            acao,

            "nome"

        )





        if not usuario or not alvo or not nome:


            return {

                "Erro":

                    "Ação incompleta"

            }





        habilidade = buscar_habilidade(

            nome

        )



        if not habilidade:


            return {

                "Erro":

                    "Habilidade não encontrada"

            }





        resultado = executar_habilidade(

            usuario,

            alvo,

            nome

        )



        self.registrar_evento(

            resultado

        )



        return resultado





# ======================================================
# Executar todas ações
# ======================================================


    def executar_acoes(self):


        self.resultados.clear()



        for acao in self.acoes:


            resultado = self.executar_acao(

                acao

            )



            self.resultados.append(

                resultado

            )



        return self.resultados





# ======================================================
# Eventos
# ======================================================


    def registrar_evento(self, evento):


        if hasattr(

                self.combate,

                "registrar_evento"):


            self.combate.registrar_evento(

                evento

            )





# ======================================================
# Limpeza
# ======================================================


    def limpar(self):


        self.acoes.clear()


        self.resultados.clear()





# ======================================================
# Status
# ======================================================


    def status(self):


        return {


            "Ações":

                len(

                    self.acoes

                ),



            "Resultados":

                len(

                    self.resultados

                )


        }