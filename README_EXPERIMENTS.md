# Scripts de Experimentos - TP2

## Como executar os experimentos

### Pré-requisitos
- Ambiente virtual ativado: `source tp2-env/bin/activate`
- Dependências instaladas: `pip install -r requirements.txt`

### Executar todos os experimentos
```bash
python experiments.py
```

Isso executará:
1. **Experimento 1**: Minimax vs Aleatório (profundidades 2, 3, 4, 5)
2. **Experimento 2**: Alfa-Beta vs Minimax (profundidades 2, 3, 4, 5)
3. **Experimento 3**: Iterative Deepening vs Alfa-Beta (limites 1s e 2s)

### Resultados
Os resultados são salvos em `experiment_results.json` e também impressos no terminal.

### Métricas coletadas
- Taxa de vitória (%)
- Tempo médio por jogada (ms)
- Média de estados visitados
- Profundidade média atingida (para Iterative Deepening)

## Teste manual no navegador

1. Inicie o servidor:
```bash
cd tp2-jogos
source tp2-env/bin/activate
python server.py
```

2. Abra no navegador: `http://localhost:5001`

3. Configure os jogadores e parâmetros na interface web

4. Jogue e observe o comportamento da IA

## Notas
- Os experimentos podem demorar alguns minutos para completar
- Ajuste `num_games` no script se quiser mais/fewer partidas por experimento
- Para experimentos mais rápidos, reduza o número de jogos ou profundidades

