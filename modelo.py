import json
import time
from pathlib import Path

import pulp


def carregar_instancia_json(caminho):
    """
    Lê uma instância própria em formato JSON.
    """
    with caminho.open("r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    elementos = dados["elementos"]
    conjuntos = dados["conjuntos"]

    return elementos, conjuntos


def carregar_instancia_orlib(caminho):
    """
    Lê uma instância no formato padrão da OR-Library.
    """
    with caminho.open("r", encoding="utf-8") as arquivo:
        dados = [int(valor) for valor in arquivo.read().split()]

    posicao = 0

    # Número de elementos (linhas)
    m = dados[posicao]
    posicao += 1

    # Número de conjuntos (colunas)
    n = dados[posicao]
    posicao += 1

    # Custos dos n conjuntos
    custos = dados[posicao:posicao + n]
    posicao += n

    # Elementos cobertos por cada conjunto
    cobertura = {
        j: []
        for j in range(1, n + 1)
    }

    # Para cada elemento, a OR-Library informa
    # quais conjuntos conseguem cobri-lo.
    for elemento in range(1, m + 1):
        quantidade = dados[posicao]
        posicao += 1

        colunas = dados[posicao:posicao + quantidade]
        posicao += quantidade

        for coluna in colunas:
            cobertura[coluna].append(elemento)

    elementos = list(range(1, m + 1))

    conjuntos = []

    for j in range(1, n + 1):
        conjuntos.append({
            "id": f"S{j}",
            "custo": custos[j - 1],
            "cobre": cobertura[j],
        })

    return elementos, conjuntos


def carregar_instancia(caminho):
    """
    Identifica automaticamente o formato da instância.
    """
    caminho = Path(caminho)

    if caminho.suffix.lower() == ".json":
        return carregar_instancia_json(caminho)

    if caminho.suffix.lower() == ".txt":
        return carregar_instancia_orlib(caminho)

    raise ValueError(
        f"Formato de instância não suportado: {caminho.suffix}"
    )


def validar_instancia(elementos, conjuntos):
    """
    Valida se todos os elementos aparecem em pelo menos um conjunto.
    """
    cobertos = set()

    for conjunto in conjuntos:
        cobertos.update(conjunto["cobre"])

    nao_cobertos = [elemento for elemento in elementos if elemento not in cobertos]

    if nao_cobertos:
        raise ValueError(
            "Instância inválida. Os seguintes elementos não são cobertos "
            f"por nenhum conjunto: {nao_cobertos}"
        )


def criar_solver():
    """
    Utiliza o solver HiGHS.
    """
    return pulp.HiGHS(msg=False), "HiGHS"


def resolver_set_covering(caminho_instancia):
    """
    Monta e resolve o modelo matemático do Set Covering Problem.
    """
    elementos, conjuntos = carregar_instancia(caminho_instancia)
    validar_instancia(elementos, conjuntos)

    # Quantidade de valores 1 na matriz de cobertura.
    total_incidencias = sum(
        len(conjunto["cobre"])
        for conjunto in conjuntos
    )

    # Densidade da matriz A.
    total_posicoes = len(elementos) * len(conjuntos)

    densidade = (
        (total_incidencias / total_posicoes) * 100
        if total_posicoes > 0
        else 0
    )

    problema = pulp.LpProblem(
        "Set_Covering_Problem",
        pulp.LpMinimize
    )

    # x_j = 1 se o conjunto j for escolhido; 0 caso contrário.
    x = {
        conjunto["id"]: problema.add_variable(
            f"x_{conjunto['id']}",
            cat=pulp.LpBinary,
        )
        for conjunto in conjuntos
    }

    # Função objetivo: minimizar o custo total dos conjuntos selecionados.
    problema += pulp.lpSum(
        conjunto["custo"] * x[conjunto["id"]]
        for conjunto in conjuntos
    ), "Custo_Total"

    # Restrição: cada elemento deve ser coberto por pelo menos um conjunto.
    for elemento in elementos:
        conjuntos_que_cobrem = [
            x[conjunto["id"]]
            for conjunto in conjuntos
            if elemento in conjunto["cobre"]
        ]

        problema += (
            pulp.lpSum(conjuntos_que_cobrem) >= 1,
            f"Cobertura_Elemento_{elemento}",
        )

    solver, nome_solver = criar_solver()

    inicio = time.perf_counter()
    stats = problema.solve(solver)
    fim = time.perf_counter()

    status = stats.status_str

    # Informações específicas fornecidas diretamente pelo HiGHS.
    info_highs = None

    try:
        info_highs = problema.solverModel.getInfo()
    except Exception:
        pass

    resultado = {
        "status": status,
        "solver": nome_solver,

        # Tempos
        "tempo_segundos": fim - inicio,
        "tempo_solver_segundos": stats.time,

        # Dimensões
        "numero_elementos": len(elementos),
        "numero_conjuntos": len(conjuntos),
        "numero_variaveis": stats.num_variables,
        "numero_restricoes": stats.num_constraints,

        # Estrutura da matriz
        "total_incidencias": total_incidencias,
        "densidade_percentual": round(densidade, 6),

        # Resultado da otimização
        "custo_otimo": None,
        "quantidade_selecionados": 0,
        "conjuntos_escolhidos": [],

        # Informações do método exato
        "melhor_limite": stats.best_bound,
        "gap_absoluto": stats.gap_abs,
        "gap_relativo": stats.gap_rel,

        # Informações nativas do HiGHS
        "nos_branch_and_bound": (
            getattr(info_highs, "mip_node_count", None)
            if info_highs is not None
            else None
        ),

        "iteracoes_simplex": (
            getattr(info_highs, "simplex_iteration_count", None)
            if info_highs is not None
            else None
        ),
    }

    if status == "Optimal":
        resultado["custo_otimo"] = round(
    pulp.value(problema.objective),
    6
)

        for conjunto in conjuntos:
            id_conjunto = conjunto["id"]

            if pulp.value(x[id_conjunto]) > 0.5:
                resultado["conjuntos_escolhidos"].append(
                    {
                        "id": id_conjunto,
                        "custo": conjunto["custo"],
                        "cobre": conjunto["cobre"],
                    }
                )
                
        resultado["quantidade_selecionados"] = len(
            resultado["conjuntos_escolhidos"]
        )

    return resultado
