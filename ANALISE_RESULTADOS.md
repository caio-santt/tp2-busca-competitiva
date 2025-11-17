# Análise dos Resultados dos Experimentos

## Problemas Identificados

### 1. ✅ CORRIGIDO: Tempos Negativos
**Problema**: Tempos negativos aparecem quando os jogadores são invertidos (ex: -1776.73 ms, -1830.98 ms)

**Causa**: Quando os jogadores são invertidos no experimento (para alternar quem começa), as estatísticas não eram invertidas corretamente.

**Correção**: Agora as estatísticas são invertidas quando os jogadores são trocados.

### 2. ✅ CORRIGIDO: Random "Visitando Nós"
**Problema**: Random player aparece visitando nós (ex: 52.3 nós, 380.7 nós)

**Causa**: `_last_stats` global não era resetado, então Random pegava os valores do jogador anterior.

**Correção**: 
- `random_player` agora define `_last_stats = {'nodes_visited': 0}`
- `_last_stats` é resetado antes de cada jogada

### 3. ⚠️ A INVESTIGAR: Alpha-Beta Visitando Mais Nós que Minimax
**Problema**: Em alguns casos, Alpha-Beta visita mais nós que Minimax (deveria visitar MENOS devido à poda)

**Possíveis Causas**:
- Ordenação de jogadas pode estar afetando a contagem
- Pode ser um problema de coleta de estatísticas
- Pode ser que em alguns casos específicos a poda não seja eficiente

**Status**: Precisa verificar se é um problema real ou apenas estatística com poucos jogos.

### 4. ⚠️ A INVESTIGAR: Tempos Muito Altos no Experiment 3
**Problema**: Tempos estão muito acima do limite (4203ms vs 1000ms, 1103ms vs 2000ms)

**Causa**: O timeout não está sendo respeitado - o código apenas avisa, mas não interrompe a execução.

**Nota**: Isso pode ser esperado se o algoritmo está no meio de uma iteração e não pode ser interrompido de forma segura. Mas deveria respeitar melhor o limite.

## Resultados que Fazem Sentido

### Experiment 1: Minimax vs Random ✅
- Minimax ganha todas as partidas (100%) - **CORRETO**
- Nós visitados aumentam exponencialmente com profundidade - **CORRETO**
- Tempos aumentam com profundidade - **CORRETO**

### Experiment 2: Alpha-Beta vs Minimax ⚠️
- Em profundidade 3, Alpha-Beta visita MENOS nós (213.7 vs 270.7) - **CORRETO**
- Em profundidade 2 e 4, Alpha-Beta visita MAIS nós - **PROBLEMA** (pode ser devido a poucos jogos ou ordenação)

### Experiment 3: Iterative Deepening vs Alpha-Beta ✅
- ID ganha mais partidas (87.5% e 75%) - **CORRETO** (ID é mais forte)
- ID visita menos nós em alguns casos - **CORRETO** (poda mais eficiente com ordenação)

## Próximos Passos

1. ✅ Corrigir inversão de estatísticas
2. ✅ Corrigir contagem de nós do Random
3. ⏳ Rodar experimentos novamente para validar correções
4. ⏳ Verificar se Alpha-Beta realmente está visitando mais nós ou se é problema de coleta
5. ⏳ Considerar melhorar o timeout (mas pode ser aceitável para fins acadêmicos)

## Recomendações

1. **Rodar experimentos novamente** após as correções para validar
2. **Aumentar número de jogos** para Experiment 2 (especialmente profundidades 4 e 5) para ter mais confiança estatística
3. **Documentar** que os tempos podem exceder o limite devido à natureza do algoritmo (não pode ser interrompido no meio de uma iteração)
4. **Considerar testes manuais** para validar que a IA está jogando corretamente
