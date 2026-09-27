from pathlib import Path
import csv

from modelo import resolver_set_covering


INSTANCIAS = [
    {
        "nivel": "Fácil",
        "arquivo": "facil_scp41.txt",
    },
    {
        "nivel": "Média",
        "arquivo": "media_scpa1.txt",
    },
    {
        "nivel": "Difícil",
        "arquivo": "dificil_scpnre1.txt",
    },
]


def main():
    pasta_projeto = Path(__file__).resolve().parent
    pasta_instancias = pasta_projeto / "instancias"
    pasta_resultados = pasta_projeto / "resultados"

    pasta_resultados.mkdir(exist_ok=True)

    resultados = []

    print("\n" + "=" * 85)
    print("COMPARATIVO - SET COVERING PROBLEM")
    print("=" * 85)

    for instancia in INSTANCIAS:
        caminho = pasta_instancias / instancia["arquivo"]

        print(f"\nResolvendo instância {instancia['nivel']}...")
        print(f"Arquivo: {instancia['arquivo']}")

        resultado = resolver_set_covering(caminho)

        resultado["nivel"] = instancia["nivel"]
        resultado["arquivo"] = instancia["arquivo"]

        resultados.append(resultado)

        print(
            f"Status={resultado['status']} | "
            f"Custo={resultado['custo_otimo']} | "
            f"Tempo={resultado['tempo_segundos']:.6f}s"
        )

    print("\n" + "=" * 85)

    cabecalho = (
        f"{'Nível':<10}"
        f"{'Elem.':>8}"
        f"{'Conj.':>8}"
        f"{'Sel.':>8}"
        f"{'Dens.%':>10}"
        f"{'Custo':>10}"
        f"{'Tempo(s)':>12}"
        f"{'Nós B&B':>12}"
    )

    print(cabecalho)
    print("-" * 85)

    for resultado in resultados:
        custo = resultado["custo_otimo"]

        if custo is None:
            custo_texto = "-"
        else:
            custo_texto = f"{custo:.2f}"

        nos = resultado["nos_branch_and_bound"]

    nos_texto = (
        str(nos)
        if nos is not None
        else "-"
    )

    print(
        f"{resultado['nivel']:<10}"
        f"{resultado['numero_elementos']:>8}"
        f"{resultado['numero_conjuntos']:>8}"
        f"{resultado['quantidade_selecionados']:>8}"
        f"{resultado['densidade_percentual']:>10.4f}"
        f"{custo_texto:>10}"
        f"{resultado['tempo_segundos']:>12.4f}"
        f"{nos_texto:>12}"
    )

    print("=" * 85)

    caminho_csv = pasta_resultados / "comparativo.csv"

    with caminho_csv.open(
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as arquivo_csv:

        campos = [
            "nivel",
            "arquivo",

            "numero_elementos",
            "numero_conjuntos",
            "numero_variaveis",
            "numero_restricoes",

            "quantidade_selecionados",

            "total_incidencias",
            "densidade_percentual",

            "custo_otimo",

            "tempo_segundos",
            "tempo_solver_segundos",

            "melhor_limite",
            "gap_absoluto",
            "gap_relativo",

            "nos_branch_and_bound",
            "iteracoes_simplex",

            "status",
            "solver",
        ]

        writer = csv.DictWriter(
            arquivo_csv,
            fieldnames=campos,
        )

        writer.writeheader()

        for resultado in resultados:
            writer.writerow({
                campo: resultado[campo]
                for campo in campos
            })

    print(f"\nResultados salvos em: {caminho_csv}")


if __name__ == "__main__":
    main()