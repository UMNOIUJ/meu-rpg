"""
====================================
ENGINE RPG v2.0
Arquivo: acao.py

Responsabilidade:
- Representar uma ação escolhida no turno.
- Guardar dados da ação.
- Preparar ação para o MotorCombate.


Estado:
- MODO FINAL
- Arquivo estabilizado.
- Não alterar arquitetura sem solicitação explícita.

Não:
- Calcula dano.
- Resolve embates.
- Compara ataque e defesa.
- Executa habilidade.
- Aplica efeitos.
- Controla combos.
- Acessa NocoDB.
- Controla turnos.

====================================
"""





# ==========================================================
# Classe Ação
# ==========================================================


class Acao:




    def __init__(

            self,

            usuario,

            alvo,

            tipo,

            nome=None):


        self.usuario = usuario


        self.alvo = alvo


        self.tipo = tipo


        self.nome = nome


        self.resultado = None





# ==========================================================
# Preparar ação
# ==========================================================


    def preparar(self):


        return {


            "Tipo":

                self.tipo,



            "Usuario":

                self.usuario,



            "Alvo":

                self.alvo,



            "Nome":

                self.nome



        }





# ==========================================================
# Executar preparação
# ==========================================================


    def executar(self):


        return self.preparar()





# ==========================================================
# Registrar resultado
# ==========================================================


    def definir_resultado(

            self,

            resultado):


        self.resultado = resultado





# ==========================================================
# Obter resultado
# ==========================================================


    def obter_resultado(self):


        return self.resultado





# ==========================================================
# Verificar execução
# ==========================================================


    def foi_realizada(self):


        if not self.resultado:


            return False





        return self.resultado.get(

            "Sucesso",

            False

        )





# ==========================================================
# Representação
# ==========================================================


    def dados(self):


        return {


            "Usuario":

                self.usuario.nome

                if self.usuario

                else None,



            "Alvo":

                self.alvo.nome

                if self.alvo

                else None,



            "Tipo":

                self.tipo,



            "Nome":

                self.nome



        }