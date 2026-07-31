"""
====================================
ENGINE RPG v1.0
Arquivo: executor_comandos.py

Responsabilidade:
- Ler comandos pendentes.
- Executar comandos do NocoDB.
- Atualizar estado do comando.
- Interpretar relações do NocoDB.

Não:
- Calcula dano.
- Resolve combate.
- Controla regras de habilidade.

====================================
"""


import time



class ExecutorComandos:



    def __init__(
            self,
            rpg):


        self.rpg = rpg


        self.ativo = False


        self.intervalo = 2





# ==========================================================
# Iniciar executor
# ==========================================================


    def iniciar(
            self):


        self.ativo = True



        while self.ativo:


            self.verificar()


            time.sleep(

                self.intervalo

            )





# ==========================================================
# Parar executor
# ==========================================================


    def parar(
            self):


        self.ativo = False





# ==========================================================
# Verificar comandos pendentes
# ==========================================================


    def verificar(
            self):


        comandos = self.rpg.noco.buscar_comandos_pendentes()



        for comando in comandos:


            self.executar(

                comando

            )





# ==========================================================
# Relações NocoDB
# ==========================================================


    def pegar_relacao(
            self,
            campo):


        if not campo:

            return None



        if isinstance(

                campo,

                list):


            if len(campo) > 0:


                return campo[0]



            return None



        return campo





    def pegar_valor(
            self,
            campo):


        relacao = self.pegar_relacao(

            campo

        )



        if isinstance(

                relacao,

                dict):


            return relacao.get(

                "Nome"

            )



        return relacao





# ==========================================================
# Marcar comando
# ==========================================================


    def atualizar_status(
            self,
            id_comando,
            status,
            resultado=None):


        self.rpg.noco.atualizar_status_comando(

            id_comando,

            status,

            resultado

        )





# ==========================================================
# Executar comando
# ==========================================================


    def executar(
            self,
            comando):


        id_comando = comando.get(

            "Id"

        )



        try:



            self.atualizar_status(

                id_comando,

                "Executando"

            )





            combate = self.pegar_relacao(

                comando.get(

                    "Combate"

                )

            )



            if combate:


                self.rpg.carregar_combate(

                    combate.get(

                        "Id"

                    )

                )





            tipo = comando.get(

                "Tipo"

            )



            resultado = None





# ==========================================================
# Usar habilidade
# ==========================================================


            if tipo == "Usar Habilidade":



                ator = self.pegar_relacao(

                    comando.get(

                        "Ator"

                    )

                )


                alvo = self.pegar_relacao(

                    comando.get(

                        "Alvo"

                    )

                )


                habilidade = self.pegar_relacao(

                    comando.get(

                        "Habilidade"

                    )

                )



                if not ator or not habilidade:


                    resultado = {


                        "Erro":

                            "Ator ou habilidade inválidos"

                    }



                else:


                    resultado = self.rpg.usar_habilidade(


                        ator.get(

                            "Nome"

                        ),


                        alvo.get(

                            "Nome"

                        )

                        if alvo

                        else None,


                        habilidade.get(

                            "Nome"

                        )

                    )





# ==========================================================
# Guarda
# ==========================================================


            elif tipo == "Usar Guarda":



                personagem = self.pegar_relacao(

                    comando.get(

                        "Ator"

                    )

                )


                guarda = self.pegar_relacao(

                    comando.get(

                        "Guarda"

                    )

                )



                resultado = self.rpg.usar_guarda(


                    personagem.get(

                        "Nome"

                    ),


                    guarda.get(

                        "Nome"

                    )

                )





# ==========================================================
# Finalizar turno
# ==========================================================


            elif tipo == "Finalizar Turno":



                resultado = self.rpg.finalizar_turno()





# ==========================================================
# Nova rodada
# ==========================================================


            elif tipo == "Nova Rodada":



                resultado = self.rpg.nova_rodada()





# ==========================================================
# Finalizar combate
# ==========================================================


            elif tipo == "Finalizar Combate":



                resultado = self.rpg.finalizar_combate()





# ==========================================================
# Comando desconhecido
# ==========================================================


            else:


                resultado = {


                    "Erro":

                        f"Comando desconhecido: {tipo}"

                }





            self.atualizar_status(

                id_comando,

                "Executado",

                resultado

            )





        except Exception as erro:



            self.atualizar_status(

                id_comando,

                "Erro",

                {

                    "Mensagem":

                        str(erro)

                }

            )





# ==========================================================
# Executar único comando manualmente
# ==========================================================


    def executar_agora(
            self,
            comando):


        return self.executar(

            comando

        )