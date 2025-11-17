# Resumo das Correções Aplicadas

## Correções Realizadas

### 1. Inversão de Estatísticas ✅
**Problema**: Quando os jogadores eram alternados (para dar chance justa), as estatísticas não eram invertidas, causando tempos negativos e dados incorretos.

**Correção**: Agora, quando os jogadores são trocados, as estatísticas também são invertidas:
- `player1_time` do jogo vira `player2_time` do experimento
- `player2_time` do jogo vira `player1_time` do experimento

### 2. Reset de `_last_stats` ✅
**Problema**: A variável global `_last_stats` não era resetada, fazendo com que Random "visitasse nós" (pegava valores do jogador anterior).

**Correção**: 
- `_last_stats` é resetado antes de cada jogada
- `random_player` define explicitamente `nodes_visited = 0`
- Se não houver estatísticas, usa 0 como padrão

### 3. Aumento do Número de Jogos ✅
**Mudança**: Aumentamos o número de jogos para melhor confiança estatística:
- Experiment 1: 20, 15, 10, 8 jogos (antes: 15, 10, 8, 5)
- Experiment 2: 15, 10, 8, 6 jogos (antes: 8, 5, 3, 2)

## Observações Importantes

### AI_Random e AI_Minimax
**Ambas apontam para `search.choose_move`**, então são a mesma IA completa (Minimax + Alpha-Beta + Iterative Deepening). Isso explica por que você não consegue ganhar de nenhuma das duas - ambas são a IA completa!

- `AI_Dummy`: Loop infinito (para testar timeout) - por isso é ruim e demora
- `AI_Random` e `AI_Minimax`: Ambas são a IA completa - por isso são fortes

## Próximos Passos

1. Rodar experimentos novamente com as correções
2. Preencher relatório com os novos resultados
3. Documentar testes manuais

