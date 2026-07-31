class InteracaoCombate:


    def __init__(
        self,
        dados
    ):


        # ======================================
        # RESULTADO DA INTERAÇÃO
        # ======================================

        self.resultado = dados.get(
            "Resultado",
            "Normal"
        )



        # ======================================
        # MODIFICADORES DE DANO
        # ======================================

        self.dano = float(
            dados.get(
                "Dano",
                1
            )
        )


        self.dano_san = int(
            dados.get(
                "Dano SAN",
                0
            )
        )


        self.dano_psiquico = int(
            dados.get(
                "Dano Psíquico",
                0
            )
        )



        # ======================================
        # DEFESA E ACERTO
        # ======================================

        self.bonus_defesa = int(
            dados.get(
                "Bônus de Defesa",
                dados.get(
                    "Bônus Defesa",
                    0
                )
            )
        )


        self.bonus_acerto = int(
            dados.get(
                "Bônus de Acerto",
                0
            )
        )



        # ======================================
        # MECÂNICAS ESPECIAIS
        # ======================================

        self.penetra_defesa = bool(
            dados.get(
                "Penetra Defesa",
                False
            )
        )


        self.desvio = bool(
            dados.get(
                "Desvio",
                False
            )
        )


        self.contra_ataque = bool(
            dados.get(
                "Contra Ataque",
                False
            )
        )



        # ======================================
        # VALORES ESPECIAIS
        # ======================================

        self.valor_desvio = int(
            dados.get(
                "Valor Desvio",
                0
            )
        )


        self.valor_critico = int(
            dados.get(
                "Valor Crítico",
                20
            )
        )



    # ======================================
    # MODIFICAR ACERTO
    # ======================================


    def modificar_acerto(
        self,
        valor
    ):


        return valor + self.bonus_acerto





    # ======================================
    # CALCULAR DANO
    # ======================================


    def calcular_dano(
        self,
        dano
    ):


        return dano * self.dano





    # ======================================
    # CALCULAR DEFESA
    # ======================================


    def calcular_defesa(
        self,
        defesa
    ):


        if self.penetra_defesa:

            return 0



        return defesa + self.bonus_defesa





    # ======================================
    # VERIFICAR DESVIO
    # ======================================


    def permite_desvio(
        self
    ):


        return self.desvio





    # ======================================
    # VALOR DE DESVIO
    # ======================================


    def calcular_desvio(
        self,
        valor
    ):


        if not self.desvio:

            return valor



        return valor + self.valor_desvio





    # ======================================
    # CONTRA ATAQUE
    # ======================================


    def permite_contra_ataque(
        self
    ):


        return self.contra_ataque





    # ======================================
    # CRÍTICO
    # ======================================


    def eh_critico(
        self,
        resultado=None
    ):


        if self.resultado.lower() == "crítico".lower():

            return True



        if resultado is not None:


            return resultado >= self.valor_critico



        return 