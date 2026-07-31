"""
====================================
ENGINE RPG v2.0
Arquivo: comando.py

Responsabilidade:

- Controlar entrada do jogador.
- Criar dados de ações do turno.
- Interface USO RPG.
- Iniciar fluxo principal do sistema.

Não:

- Calcula dano.
- Executa habilidade.
- Resolve embates.
- Acessa NocoDB.
- Controla regras.

====================================
"""


from database import cache
from engine.personagem import Personagem





class ComandoUSO:



    def __init__(self):

        pass





# ==========================================================
# Entrada principal USO RPG
# ==========================================================


    def iniciar(self):


        while True:


            print()

            print("==============================")

            print("          USO RPG")

            print("==============================")

            print()


            print("1 - Iniciar combate")

            print("2 - Listar personagens")

            print("0 - Sair")

            print()



            escolha = input(

                "Escolha: "

            ).strip()





            if escolha == "1":


                combate = self.escolher_combate()



                if not combate:


                    print()

                    print(

                        "Combate inválido."

                    )

                    continue





                combate.iniciar()





            elif escolha == "2":


                self.listar_personagens()





            elif escolha == "0":


                print()

                print(

                    "Encerrando USO RPG."

                )

                break





            else:


                print()

                print(

                    "Comando inválido."

                )









# ==========================================================
# Escolher combate do NocoDB
# ==========================================================


    def escolher_combate(self):


        from engine.combate import Combate



        registros = cache.listar(

            "combates"

        )



        if isinstance(

                registros,

                dict):


            registros = list(

                registros.values()

            )





        if not registros:


            print(

                "Nenhum combate encontrado."

            )


            return None





        print()

        print("==============================")

        print("          COMBATES")

        print("==============================")

        print()



        for indice, combate in enumerate(

                registros,

                1):


            nome = combate.get(

                "Nome",

                f"Combate {indice}"

            )


            print(

                f"{indice} - {nome}"

            )





        escolha = input(

            "Escolha combate: "

        ).strip()





        try:


            combate_dados = registros[

                int(escolha) - 1

            ]



        except Exception:


            return None





        participantes = self.carregar_participantes_combate(

            combate_dados.get(

                "Id"

            )

        )





        if len(participantes) < 2:


            print()

            print(

                "Combate sem participantes suficientes."

            )


            return None





        return Combate(

            participantes

        )









# ==========================================================
# Carregar participantes do combate
# ==========================================================


    def carregar_participantes_combate(

            self,

            id_combate):


        registros = cache.listar(

            "participantes_combate"

        )



        if isinstance(

                registros,

                dict):


            registros = registros.values()





        participantes = []





        for registro in registros:



            combate = registro.get(

                "Combate"

            )



            combate_id = None





            if isinstance(

                    combate,

                    dict):


                combate_id = combate.get(

                    "Id"

                )



            elif isinstance(

                    combate,

                    list) and combate:


                combate_id = combate[0].get(

                    "Id"

                )



            else:


                combate_id = combate





            if combate_id != id_combate:


                continue





            personagem = registro.get(

                "Personagem"

            )





            dados_personagem = None





            if isinstance(

                    personagem,

                    dict):


                dados_personagem = personagem



            elif isinstance(

                    personagem,

                    list) and personagem:


                dados_personagem = personagem[0]





            if not dados_personagem:


                continue





            participantes.append(

                Personagem(

                    dados_personagem

                )

            )





        return participantes







# ==========================================================
# Listar personagens
# ==========================================================


    def listar_personagens(self):


        print()

        print("==============================")

        print("        PERSONAGENS")

        print("==============================")

        print()



        personagens = cache.listar(

            "personagens"

        )



        if isinstance(

                personagens,

                dict):


            personagens = personagens.values()



        personagens = list(

            personagens

        )





        if not personagens:


            print(

                "Nenhum personagem encontrado."

            )

            return





        for indice, personagem in enumerate(

                personagens,

                1):


            print(

                f"{indice} - {personagem.get('Nome')}"

            )









# ==========================================================
# Escolher ação
# ==========================================================


    def escolher_acao(

            self,

            personagem,

            combate):


        print()

        print("==============================")

        print("          USO RPG")

        print("==============================")

        print()



        print(

            f"Jogador: {personagem.nome}"

        )



        print()

        print("1 - Passar")

        print("2 - Guarda")

        print("3 - Habilidade")

        print()



        escolha = input(

            "Escolha: "

        ).strip()





        if escolha == "1":


            return {


                "Tipo":

                    "PASSAR",


                "Usuario":

                    personagem


            }





        if escolha == "2":


            nome = input(

                "Nome da guarda: "

            ).strip()



            return {


                "Tipo":

                    "GUARDA",


                "Nome":

                    nome,


                "Usuario":

                    personagem


            }





        if escolha == "3":


            nome = input(

                "Nome da habilidade: "

            ).strip()



            alvo = self.escolher_alvo(

                personagem,

                combate

            )



            return {


                "Tipo":

                    "HABILIDADE",


                "Nome":

                    nome,


                "Usuario":

                    personagem,


                "Alvo":

                    alvo


            }





        return {


            "Tipo":

                "PASSAR",


            "Usuario":

                personagem


        }









# ==========================================================
# Escolher alvo
# ==========================================================


    def escolher_alvo(

            self,

            personagem,

            combate):


        alvos = combate.obter_alvos_validos(

            personagem

        )



        if not alvos:


            return None





        print()

        print("Alvos:")





        for indice, alvo in enumerate(

                alvos,

                1):


            print(

                f"{indice} - {alvo.nome}"

            )





        while True:


            escolha = input(

                "Escolha alvo: "

            ).strip()





            try:


                escolha = int(

                    escolha

                )



                if 1 <= escolha <= len(alvos):


                    return alvos[

                        escolha - 1

                    ]



            except ValueError:


                pass





            print(

                "Alvo inválido."

            )