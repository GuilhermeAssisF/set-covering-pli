from pathlib import Path
from urllib.request import urlretrieve


URL_BASE = "https://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/"

INSTANCIAS = {
    "facil_scp41.txt": "scp41.txt",
    "media_scpa1.txt": "scpa1.txt",
    "dificil_scpnre1.txt": "scpnre1.txt",
}


def main():
    pasta_projeto = Path(__file__).resolve().parent
    pasta_instancias = pasta_projeto / "instancias"

    pasta_instancias.mkdir(exist_ok=True)

    print("=" * 60)
    print("DOWNLOAD DAS INSTÂNCIAS - OR-LIBRARY")
    print("=" * 60)

    for nome_local, nome_origem in INSTANCIAS.items():
        destino = pasta_instancias / nome_local

        if destino.exists():
            print(f"[OK] {nome_local} já existe.")
            continue

        url = URL_BASE + nome_origem

        print(f"Baixando {nome_origem}...")

        urlretrieve(url, destino)

        print(f"[OK] Salvo como {nome_local}")

    print("=" * 60)
    print("Download concluído.")


if __name__ == "__main__":
    main()