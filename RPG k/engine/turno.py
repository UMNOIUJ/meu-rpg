"""
====================================
ENGINE RPG v2.0
Arquivo: turno.py


Estado:
- MODO FINAL
- Arquivo estabilizado.
- Não alterar arquitetura sem solicitação explícita.

Responsabilidade
- Controlar fluxo do turno.
- Controlar ordem dos participantes.
- Receber comandos externos.
- Criar ações.
- Guardar ações pendentes.

Este arquivo NÃO:
- Calcula dano.
- Resolve embates.
- Executa habilidades.
- Aplica efeitos.
- Controla regras de combate.
- Acessa NocoDB.

====================================
"""


from engine.acao import Acao





class Turno:



    def __init__(

            self,

            combate,

            comando,

            numero=1):


        self.combate = combate

        self.comando = comando

        self.numero = numero


        self.participantes = self.organizar_ordem()


        self.indice_atual = 0


        self.acoes = []





# ======================================================
# Organizar ordem
# ======================================================


    def organizar_ordem(self):


        participantes = []



        for participante in self.combate.participantes:



            if isinstance(

                    participante,

                    dict):


                personagem = participante.get(

                    "Personagem"

                )


            else:


                personagem = participante





            if not personagem:

                continue



            if not personagem.esta_vivo():

                continue





            participantes.append(

                personagem

            )





        return sorted(

            participantes,

            key=lambda personagem:

                getattr(

                    personagem,

                    "ordem_combate",

                    0

                ),

            reverse=True

        )





# ======================================================
# Participante atual
# ======================================================


    def participante_atual(self):


        if not self.participantes:

            return None





        if self.indice_atual >= len(

                self.participantes):

            return None





        return self.participantes[

            self.indice_atual

        ]





# ======================================================
# Receber ação
# ======================================================


    def receber_acao(

            self,

            dados):


        personagem = self.participante_atual()



        if not personagem:

            return None





        if dados is None:

            dados = {

                "Tipo":

                    "PASSAR"

            }





        acao = Acao(

            usuario=personagem,

            alvo=dados.get(

                "Alvo"

            ),

            tipo=dados.get(

                "Tipo"

            ),

            nome=dados.get(

                "Nome"

            )

        )





        self.acoes.append(

            acao

        )





        self.indice_atual += 1





        return acao





# ======================================================
# Executar coleta de turno
# ======================================================


    def executar(self):


        print()

        print("==============================")

        print(

            f"TURNO {self.numero}"

        )

        print("==============================")

        print()





        while self.participante_atual():



            personagem = self.participante_atual()



            print()

            print(

                f"Vez de {personagem.nome}"

            )





            dados = self.comando.escolher_acao(

                personagem,

                self.combate

            )





            acao = self.receber_acao(

                dados

            )





            if acao:


                print()

                print(

                    f"{personagem.nome} escolheu: {acao.tipo}"

                )





                if acao.nome:


                    print(

                        f"Ação: {acao.nome}"

                    )







        return self.ordenar_acoes()





# ======================================================
# Obter ações
# ======================================================


    def obter_acoes(self):


        return self.acoes





# ======================================================
# Ordenar ações
# ======================================================


    def ordenar_acoes(self):


        self.acoes.sort(

            key=lambda acao:


                getattr(

                    acao.usuario,

                    "ordem_combate",

                    0

                ),

            reverse=True

        )



        return self.acoes





# ======================================================
# Limpar turno
# ======================================================


    def finalizar(self):


        self.indice_atual = 0


        self.acoes.clear()