# TP2: Busca Competitiva - Ligue-4 (Connect Four)

Projeto de implementação de um agente de IA para jogar **Ligue-4 (Connect Four)** utilizando algoritmos de busca adversarial.

## 📋 Sobre o Projeto

Este projeto faz parte do Trabalho Prático 2 (TP2) da disciplina de Inteligência Artificial. O objetivo é implementar e comparar diferentes algoritmos de busca adversarial:

- **Minimax** com profundidade limitada e função heurística
- **Poda Alfa-Beta** para otimização
- **Iterative Deepening** com limite de tempo

## 🎮 O Jogo

Ligue-4 é um jogo de tabuleiro 6×7 onde dois jogadores alternam jogadas, tentando formar uma linha de 4 peças na horizontal, vertical ou diagonal.

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8+
- pip

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/caio-santt/tp2-busca-competitiva.git
cd tp2-busca-competitiva
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv tp2-env
source tp2-env/bin/activate  # No Windows: tp2-env\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute o servidor:
```bash
python server.py
```

5. Abra no navegador:
```
http://localhost:5001
```

## 📁 Estrutura do Projeto

```
tp2-jogos/
├── search.py          # Implementação do agente de IA (arquivo principal)
├── server.py          # Servidor Flask
├── requirements.txt   # Dependências Python
├── static/           # Arquivos estáticos (CSS, JS)
├── templates/        # Templates HTML
└── README.md         # Este arquivo
```

## 🎯 Funcionalidades

- **Jogar contra a IA**: Modo humano vs IA
- **IA vs IA**: Observar partidas entre agentes
- **Controles configuráveis**: Ajustar profundidade máxima e tempo por jogada
- **Visualização em tempo real**: Interface web com p5.js

## 🔧 Implementação

O arquivo `search.py` contém a função principal `choose_move()` que deve ser implementada com os algoritmos de busca adversarial.

### Função Principal

```python
def choose_move(board: List[List[int]], turn: int, config: Dict) -> Tuple[int, Dict]:
    """
    Decide a coluna (0..6) para jogar agora.
    
    Parâmetros:
      - board: matriz 6x7 com valores {0,1,2}
      - turn: 1 ou 2 (jogador da vez)
      - config: {"max_time_ms": int, "max_depth": int}
    
    Retorna:
      - col: int (0..6) - coluna escolhida
    """
```

## 📊 Experimentos

O projeto inclui experimentos comparativos entre diferentes algoritmos e configurações, documentados no relatório final.

## 📝 Licença

Este é um projeto acadêmico desenvolvido para fins educacionais.

## 👤 Autor

Desenvolvido como parte do TP2 da disciplina de Inteligência Artificial.

---

**Status**: Em desenvolvimento 🚧
