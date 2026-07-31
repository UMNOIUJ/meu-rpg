"""
====================================
ENGINE RPG v2.0
Arquivo: cache.py

Responsabilidade:

- Centralizar dados carregados do NocoDB.
- Manter estado temporário da engine.
- Evitar múltiplas chamadas ao banco.
- Servir como memória da sessão.

Não:

- Faz cálculos.
- Resolve combate.
- Executa habilidades.
- Controla turnos.
- Acessa regras de jogo.

====================================
"""





# ==========================================================
# CACHE PRINCIPAL
# ==========================================================


dados = {

    # Tabelas NocoDB

    "personagens": {},

    "habilidades": {},

    "personagem_habilidades": {},

    "efeitos": {},

    "personagem_efeitos": {},

    "habilidade_efeitos": {},

    "habilidade_acoes": {},

    "guardas": {},

    "combos": {},

    "condicoes": {},

    "estados": {},

    "tipos": {},

    "interacoes": {},

    "combates": {},

    "participantes_combate": {},

    "acoes_combate": {},

    "eventos": {},

    "dados_combate": {},

    "comandos": {},


    # Estado da engine

    "combate": None,

    "turno": None,

    "rodada": 0,


    # Controle

    "carregado": False

}





# ==========================================================
# INICIAR CACHE
# ==========================================================


def iniciar_cache():

    limpar_cache()





# ==========================================================
# LIMPAR CACHE
# ==========================================================


def limpar_cache():

    global dados


    dados = {

        "personagens": {},

        "habilidades": {},

        "personagem_habilidades": {},

        "efeitos": {},

        "personagem_efeitos": {},

        "habilidade_efeitos": {},

        "habilidade_acoes": {},

        "guardas": {},

        "combos": {},

        "condicoes": {},

        "estados": {},

        "tipos": {},

        "interacoes": {},

        "combates": {},

        "participantes_combate": {},

        "acoes_combate": {},

        "eventos": {},

        "dados_combate": {},

        "comandos": {},


        "combate": None,

        "turno": None,

        "rodada": 0,


        "carregado": False

    }





# ==========================================================
# CARREGAR DADOS
# ==========================================================


def carregar(tipo, registros):


    if registros is None:

        registros = {}





    if isinstance(registros, list):


        convertido = {}



        for registro in registros:


            if isinstance(registro, dict):


                chave = registro.get(

                    "Id"

                )


                if chave is not None:

                    convertido[chave] = registro



        registros = convertido





    dados[tipo] = registros





# ==========================================================
# ADICIONAR DADOS
# ==========================================================


def adicionar(tipo, chave, valor):


    if tipo not in dados:

        dados[tipo] = {}



    dados[tipo][chave] = valor





# ==========================================================
# OBTER UM REGISTRO
# ==========================================================


def obter(tipo, chave):


    tabela = dados.get(

        tipo,

        {}

    )



    if isinstance(tabela, dict):

        return tabela.get(chave)



    return None





# ==========================================================
# LISTAR TABELA COMPLETA
# ==========================================================


def listar(tipo):


    return dados.get(

        tipo,

        {}

    )





# ==========================================================
# REMOVER
# ==========================================================


def remover(tipo, chave):


    tabela = dados.get(tipo)



    if isinstance(tabela, dict):

        tabela.pop(

            chave,

            None

        )





# ==========================================================
# ATALHOS DE TABELAS
# ==========================================================


def personagens():

    return _lista("personagens")





def habilidades():

    return _lista("habilidades")





def personagem_habilidades():

    return _lista("personagem_habilidades")





def efeitos():

    return _lista("efeitos")





def personagem_efeitos():

    return _lista("personagem_efeitos")





def habilidade_efeitos():

    return _lista("habilidade_efeitos")





def habilidade_acoes():

    return _lista("habilidade_acoes")





def guardas():

    return _lista("guardas")





def combos():

    return _lista("combos")





def condicoes():

    return _lista("condicoes")





def estados():

    return _lista("estados")





def tipos():

    return _lista("tipos")





def interacoes():

    return _lista("interacoes")





def combates():

    return _lista("combates")





def participantes_combate():

    return _lista("participantes_combate")





def acoes_combate():

    return _lista("acoes_combate")





def eventos():

    return _lista("eventos")





def comandos():

    return _lista("comandos")





def _lista(tipo):


    tabela = dados.get(

        tipo,

        {}

    )



    if isinstance(tabela, dict):

        return tabela.values()



    if isinstance(tabela, list):

        return tabela



    return []





# ==========================================================
# CONTROLE DE CARREGAMENTO
# ==========================================================


def marcar_carregado():

    dados["carregado"] = True





def esta_carregado():

    return dados.get(

        "carregado",

        False

    )





# ==========================================================
# CONTROLE DE COMBATE
# ==========================================================


def iniciar_combate(combate):


    dados["combate"] = combate


    dados["rodada"] = 1





def finalizar_combate():


    dados["combate"] = None


    dados["turno"] = None


    dados["rodada"] = 0





def atualizar_turno(turno):


    dados["turno"] = turno





def proxima_rodada():


    dados["rodada"] += 1





def estado_combate():


    return dados.get(

        "combate"

    )





# ==========================================================
# DEBUG
# ==========================================================


def mostrar_cache():


    return dados