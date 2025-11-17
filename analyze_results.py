"""
Script para analisar os resultados dos experimentos e identificar problemas.
"""

import json

with open('experiment_results.json', 'r') as f:
    results = json.load(f)

print("="*70)
print("ANÁLISE DOS RESULTADOS DOS EXPERIMENTOS")
print("="*70)

# Problemas identificados
problems = []

# EXPERIMENTO 1: Minimax vs Random
print("\n1. EXPERIMENTO 1: Minimax vs Random")
print("-" * 70)
for depth, data in results['experiment_1'].items():
    print(f"\nProfundidade {depth}:")
    print(f"  Vitórias Minimax: {data['player1_wins']}/{data['total_games']} ({data['player1_wins']/data['total_games']*100:.1f}%)")
    print(f"  Tempo médio Minimax: {data['player1_avg_time']:.2f} ms")
    print(f"  Tempo médio Random: {data['player2_avg_time']:.2f} ms")
    print(f"  Nós visitados Minimax: {data['player1_avg_nodes']:.1f}")
    print(f"  Nós visitados Random: {data['player2_avg_nodes']:.1f}")
    
    # Verificar problemas
    if data['player2_avg_time'] < 0:
        problems.append(f"EXP1-Depth{depth}: Tempo negativo do Random ({data['player2_avg_time']:.2f} ms)")
    if data['player1_wins'] == 0 and depth != "2":
        problems.append(f"EXP1-Depth{depth}: Minimax não ganhou nenhuma partida (esperado ganhar todas)")
    if data['player1_avg_nodes'] < data['player2_avg_nodes']:
        problems.append(f"EXP1-Depth{depth}: Random visitou mais nós que Minimax (não faz sentido)")

# EXPERIMENTO 2: Alpha-Beta vs Minimax
print("\n\n2. EXPERIMENTO 2: Alpha-Beta vs Minimax")
print("-" * 70)
for depth, data in results['experiment_2'].items():
    print(f"\nProfundidade {depth}:")
    print(f"  Vitórias Alpha-Beta: {data['player1_wins']}/{data['total_games']}")
    print(f"  Vitórias Minimax: {data['player2_wins']}/{data['total_games']}")
    print(f"  Tempo médio Alpha-Beta: {data['player1_avg_time']:.2f} ms")
    print(f"  Tempo médio Minimax: {data['player2_avg_time']:.2f} ms")
    print(f"  Nós visitados Alpha-Beta: {data['player1_avg_nodes']:.1f}")
    print(f"  Nós visitados Minimax: {data['player2_avg_nodes']:.1f}")
    
    # Verificar problemas
    if data['player1_avg_time'] < 0 or data['player2_avg_time'] < 0:
        problems.append(f"EXP2-Depth{depth}: Tempo negativo (AB: {data['player1_avg_time']:.2f}, MM: {data['player2_avg_time']:.2f})")
    if data['player1_avg_nodes'] > data['player2_avg_nodes']:
        problems.append(f"EXP2-Depth{depth}: Alpha-Beta visitou MAIS nós que Minimax (deveria visitar MENOS devido à poda)")
    if data['total_games'] < 5:
        problems.append(f"EXP2-Depth{depth}: Poucos jogos ({data['total_games']}) - resultados podem não ser confiáveis")

# EXPERIMENTO 3: Iterative Deepening vs Alpha-Beta
print("\n\n3. EXPERIMENTO 3: Iterative Deepening vs Alpha-Beta")
print("-" * 70)
for time_limit, data in results['experiment_3'].items():
    print(f"\nLimite de tempo {time_limit}ms:")
    print(f"  Vitórias ID: {data['player1_wins']}/{data['total_games']} ({data['player1_wins']/data['total_games']*100:.1f}%)")
    print(f"  Vitórias AB: {data['player2_wins']}/{data['total_games']} ({data['player2_wins']/data['total_games']*100:.1f}%)")
    print(f"  Tempo médio ID: {data['player1_avg_time']:.2f} ms")
    print(f"  Tempo médio AB: {data['player2_avg_time']:.2f} ms")
    print(f"  Nós visitados ID: {data['player1_avg_nodes']:.1f}")
    print(f"  Nós visitados AB: {data['player2_avg_nodes']:.1f}")
    
    # Verificar problemas
    if data['player1_avg_time'] > int(time_limit) * 2:
        problems.append(f"EXP3-Time{time_limit}: ID está usando mais que o dobro do tempo limite ({data['player1_avg_time']:.2f} ms vs {time_limit} ms)")
    if data['player2_avg_time'] > int(time_limit) * 2:
        problems.append(f"EXP3-Time{time_limit}: AB está usando mais que o dobro do tempo limite ({data['player2_avg_time']:.2f} ms vs {time_limit} ms)")

# Resumo de problemas
print("\n\n" + "="*70)
print("PROBLEMAS IDENTIFICADOS:")
print("="*70)
if problems:
    for i, problem in enumerate(problems, 1):
        print(f"{i}. {problem}")
else:
    print("Nenhum problema crítico identificado!")

print("\n" + "="*70)
print("ANÁLISE DE VALIDADE:")
print("="*70)

# Verificar se os resultados fazem sentido teoricamente
print("\n✓ Experiment 1: Minimax vs Random")
print("  - Minimax deveria ganhar todas ou quase todas as partidas: OK" if all(d['player1_wins'] == d['total_games'] for d in results['experiment_1'].values()) else "  - PROBLEMA: Minimax não ganhou todas as partidas")
print("  - Nós visitados devem aumentar exponencialmente com profundidade: OK" if results['experiment_1']['2']['player1_avg_nodes'] < results['experiment_1']['3']['player1_avg_nodes'] < results['experiment_1']['4']['player1_avg_nodes'] else "  - PROBLEMA: Padrão de nós visitados não é exponencial")

print("\n✓ Experiment 2: Alpha-Beta vs Minimax")
print("  - Alpha-Beta deveria visitar MENOS nós que Minimax: ", end="")
ab_better = all(d['player1_avg_nodes'] < d['player2_avg_nodes'] for d in results['experiment_2'].values())
print("OK" if ab_better else "PROBLEMA - Alpha-Beta está visitando mais nós!")

print("\n✓ Experiment 3: Iterative Deepening vs Alpha-Beta")
print("  - ID deveria ter desempenho similar ou melhor que AB: OK" if results['experiment_3']['1000']['player1_wins'] >= results['experiment_3']['1000']['player2_wins'] else "  - PROBLEMA: ID não está performando bem")

