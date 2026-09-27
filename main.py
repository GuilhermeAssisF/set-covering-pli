from pathlib import Path
import argparse

from modelo import resolver_set_covering


def imprimir_resultado(resultado):
    print("\n" + "=" * 60)
    print("SET COVERING PROBLEM - RESULTADO")
    print("=" * 60)

    print(f"Status: {resultado['status']}")
    print(f"Solver: {resultado['solver']}")
    print(f"Elementos: {resultado['numero_elementos']}")
    print(f"Conjuntos: {resultado['numero_conjuntos']}")
    print(f"Tempo: {resultado['tempo_segundos']:.6f} s")

    if resultado["status"] != "Optimal":
        print("\nNão foi encontrada uma solução ótima.")
        return

    print(f"Custo ótimo: {resultado['custo_otimo']:.2f}")

    print("\nConjuntos escolhidos:")

    for conjunto in resultado["conjuntos_escolhidos"]:
        print(
            f"  - {conjunto['id']}: "
            f"custo={conjunto['custo']} | "
            f"cobre={conjunto['cobre']}"
        )

    print("=" * 60)


def main():
    pasta_projeto = Path(__file__).resolve().parent
    instancia_padrao = pasta_projeto / "instancias" / "facil.json"

    parser = argparse.ArgumentParser(
        description="Resolve uma instância do Set Covering Problem."
    )

    parser.add_argument(
        "instancia",
        nargs="?",
        default=str(instancia_padrao),
        help="Caminho para o arquivo JSON da instância.",
    )

    args = parser.parse_args()

    resultado = resolver_set_covering(args.instancia)
    imprimir_resultado(resultado)


if __name__ == "__main__":
    main()
