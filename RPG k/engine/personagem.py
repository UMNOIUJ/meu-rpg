"""
====================================
ENGINE RPG v2.0
Arquivo: personagem.py

Status:
- MODO FINAL
- Arquivo estabilizado.
- Não alterar arquitetura sem solicitação explícita.

Responsabilidade:
- Representar personagens da engine.
- Controlar atributos básicos.
- Controlar HP/SAN.
- Controlar efeitos ativos.
- Controlar guarda ativa.
- Fornecer dados para combate.
- Buscar habilidades vinculadas pelo cache.

Este arquivo NÃO:
- Calcula dano.
- Resolve embates.
- Executa habilidades.
- Acessa NocoDB diretamente.
- Controla turnos.

====================================
"""


from database import cache





# ==========================================================
# Conversões
# ==========================================================


def converter_numero(valor, padrao=0):

    try:

        return int(valor)

    except (TypeError, ValueError):

        return padrao





def converter_bool(valor):

    if isinstance(valor, bool):

        return valor


    if valor is None:

        return False


    return str(valor).lower().strip() in (

        "true",
        "1",
        "sim",
        "yes"

    )





# ==========================================================
# Classe Personagem
# ==========================================================


class Personagem:


    def __init__(self, dados):


        self.id = dados.get(
            "Id"
        )


        self.nome = dados.get(
            "Nome",
            ""
        )


        self.dados = dados



        # --------------------------
        # Recursos
        # --------------------------


        self.hp_maximo = converter_numero(

            dados.get(

                "HP",

                dados.get(

                    "HP Máximo",

                    100

                )

            ),

            100

        )


        self.hp_atual = converter_numero(

            dados.get(

                "HP Atual",

                self.hp_maximo

            ),

            self.hp_maximo

        )



        self.san_maxima = converter_numero(

            dados.get(

                "SAN",

                dados.get(

                    "SAN Máxima",

                    100

                )

            ),

            100

        )


        self.san_atual = converter_numero(

            dados.get(

                "SAN Atual",

                self.san_maxima

            ),

            self.san_maxima

        )





        # --------------------------
        # Combate
        # --------------------------


        self.ordem_combate = converter_numero(

            dados.get(

                "Ordem",

                0

            )

        )


        self.defesa = converter_numero(

            dados.get(

                "Defesa",

                10

            ),

            10

        )


        self.ataque = converter_numero(

            dados.get(

                "Ataque",

                0

            )

        )





        # --------------------------
        # Estado
        # --------------------------


        self.efeitos = []


        self.guarda_ativa = None


        self.vivo = True





# ==========================================================
# Estado
# ==========================================================


    def esta_vivo(self):

        return (

            self.hp_atual > 0

            and

            self.vivo

        )





    def morrer(self):

        self.hp_atual = 0

        self.vivo = False





# ==========================================================
# HP
# ==========================================================


    def receber_dano(self, dano):


        dano = converter_numero(
            dano
        )


        if dano < 0:

            dano = 0



        self.hp_atual -= dano



        if self.hp_atual <= 0:

            self.hp_atual = 0

            self.morrer()



        return dano





    def curar(self, valor):


        valor = converter_numero(
            valor
        )


        self.hp_atual += valor



        if self.hp_atual > self.hp_maximo:

            self.hp_atual = self.hp_maximo



        return valor





# ==========================================================
# SAN
# ==========================================================


    def perder_san(self, valor):


        valor = converter_numero(
            valor
        )


        self.san_atual -= valor



        if self.san_atual < 0:

            self.san_atual = 0



        return valor





    def recuperar_san(self, valor):


        valor = converter_numero(
            valor
        )


        self.san_atual += valor



        if self.san_atual > self.san_maxima:

            self.san_atual = self.san_maxima



        return valor





# ==========================================================
# Defesa
# ==========================================================


    def obter_defesa(self):


        defesa = self.defesa


        guarda = self.guarda_ativa



        if not guarda:

            return defesa



        if isinstance(guarda, dict):

            defesa += converter_numero(

                guarda.get(

                    "Bônus Defesa",

                    0

                )

            )


        else:

            defesa += converter_numero(

                getattr(

                    guarda,

                    "bonus_defesa",

                    0

                )

            )



        return defesa





# ==========================================================
# Turnos
# ==========================================================


    def inicio_turno(self):

        pass





    def fim_turno(self):

        pass





# ==========================================================
# Efeitos
# ==========================================================


    def adicionar_efeito(self, efeito):

        self.efeitos.append(
            efeito
        )





    def remover_efeito(self, nome):


        self.efeitos = [

            efeito

            for efeito in self.efeitos

            if efeito.get(
                "Nome"
            ) != nome

        ]





# ==========================================================
# Habilidades
# ==========================================================


    def habilidades(self):


        registros = cache.listar(

            "personagem_habilidades"

        )



        resultado = []



        if isinstance(registros, dict):

            registros = registros.values()



        for relacao in registros:



            personagem = relacao.get(
                "Personagem"
            )



            personagem_id = None



            if isinstance(personagem, dict):

                personagem_id = personagem.get(
                    "Id"
                )


            elif isinstance(personagem, list) and personagem:

                personagem_id = personagem[0].get(
                    "Id"
                )


            else:

                personagem_id = personagem



            if personagem_id == self.id:


                habilidade = relacao.get(
                    "Habilidade"
                )


                if habilidade:

                    resultado.append(
                        habilidade
                    )





        # Compatibilidade NocoDB M2M

        dados = self.dados.get(

            "Personagem_Habilidades",

            []

        )


        if dados:


            for habilidade in dados:

                if habilidade not in resultado:

                    resultado.append(
                        habilidade
                    )



        return resultado





    def buscar_habilidade(self, nome):


        for habilidade in self.habilidades():


            if habilidade.get(
                "Nome"
            ) == nome:

                return habilidade



        return None





# ==========================================================
# Status
# ==========================================================


    def status(self):


        guarda = None



        if self.guarda_ativa:


            if isinstance(
                self.guarda_ativa,
                dict
            ):

                guarda = self.guarda_ativa.get(
                    "Nome"
                )


            else:

                guarda = getattr(

                    self.guarda_ativa,

                    "nome",

                    None

                )



        return {


            "Nome":

                self.nome,


            "HP":

                self.hp_atual,


            "HP Máximo":

                self.hp_maximo,


            "SAN":

                self.san_atual,


            "SAN Máxima":

                self.san_maxima,


            "Vivo":

                self.esta_vivo(),


            "Efeitos":

                [

                    efeito.get(
                        "Nome"
                    )

                    for efeito in self.efeitos

                ],


            "Guarda":

                guarda

        }





# ==========================================================
# Buscar personagem
# ==========================================================


def buscar_personagem(nome):


    registros = cache.listar(

        "personagens"

    )



    if isinstance(registros, dict):

        registros = registros.values()



    for dados in registros:


        if dados.get(
            "Nome"
        ) == nome:


            return Personagem(
                dados
            )



    return None