# Set Covering Problem - Programação Linear Inteira

Projeto inicial para o trabalho de Programação Linear Inteira.

## Problema

O Set Covering Problem (SCP) busca selecionar conjuntos com o menor custo total possível, garantindo que todos os elementos do universo sejam cobertos por pelo menos um conjunto selecionado.

## Tecnologias

- Python
- PuLP
- HiGHS
- CBC como fallback

## Estrutura

```text
set-covering-pli/
├── main.py
├── modelo.py
├── requirements.txt
├── README.md
├── .vscode/
│   └── settings.json
└── instancias/
    └── facil.json
```

## Como executar no VS Code

### 1. Abra a pasta do projeto

No VS Code:

```text
File > Open Folder
```

Selecione a pasta `set-covering-pli`.

### 2. Crie um ambiente virtual

No terminal do VS Code:

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute

```bash
python main.py
```

Por padrão, o programa utiliza:

```text
instancias/facil.json
```

Também é possível informar outra instância:

```bash
python main.py instancias/outra_instancia.json
```

## Formato das instâncias

Exemplo:

```json
{
  "elementos": [1, 2, 3],
  "conjuntos": [
    {
      "id": "S1",
      "custo": 10,
      "cobre": [1, 2]
    },
    {
      "id": "S2",
      "custo": 8,
      "cobre": [2, 3]
    }
  ]
}
```

Cada conjunto possui:

- `id`: identificador;
- `custo`: custo de selecionar o conjunto;
- `cobre`: elementos cobertos pelo conjunto.

## Modelo matemático

Variável binária:

```text
x_j = 1 se o conjunto j for escolhido
x_j = 0 caso contrário
```

Função objetivo:

```text
min Σ c_j * x_j
```

Restrições:

```text
Σ a_ij * x_j >= 1
```

para cada elemento `i`.

## Próxima etapa

A instância atual serve para validar a implementação.

As instâncias Fácil, Média e Difícil definitivas deverão ser calibradas para apresentar crescimento real de dificuldade e tempo de processamento.
