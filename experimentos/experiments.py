"""
Script para executar experimentos comparativos entre diferentes algoritmos.
Coleta métricas conforme especificado nas instruções do TP2.
"""

import time
import random
from typing import List, Tuple, Dict
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from search import (
    choose_move, valid_moves, make_move, terminal, winner, 
    EMPTY, P1, P2, ROWS, COLS, copy_board
)

def play_game(player1_func, player2_func, config1: Dict, config2: Dict, 
              max_moves: int = 42, timeout_per_move: float = 10.0) -> Tuple[int, Dict]:
    """
    Executa uma partida completa entre dois jogadores.
    
    Retorna:
        (vencedor, estatísticas) onde vencedor é 0 (empate), 1 ou 2
    """
    board = [[EMPTY] * COLS for _ in range(ROWS)]
    stats = {
        'moves': 0,
        'player1_time': [],
        'player2_time': [],
        'player1_nodes': [],
        'player2_nodes': []
    }
    
    turn = P1
    for move_num in range(max_moves):
        # Verificar se o jogo terminou
        is_term, winner_player = terminal(board)
        if is_term:
            return winner_player, stats
        
        # Escolher jogada com timeout
        start_time = time.time()
        global _last_stats
        _last_stats = {}  # Resetar antes de cada jogada para evitar contaminação
        col = 0
        try:
            if turn == P1:
                col = player1_func(board, turn, config1)
                elapsed = (time.time() - start_time) * 1000
                if elapsed > timeout_per_move * 1000:
                    print(f"  AVISO: Jogada do P1 demorou {elapsed:.0f}ms (timeout: {timeout_per_move*1000:.0f}ms)")
                stats['player1_time'].append(elapsed)
                if 'nodes_visited' in _last_stats:
                    stats['player1_nodes'].append(_last_stats['nodes_visited'])
                else:
                    stats['player1_nodes'].append(0)  # Se não houver estatísticas, usar 0
            else:
                col = player2_func(board, turn, config2)
                elapsed = (time.time() - start_time) * 1000
                if elapsed > timeout_per_move * 1000:
                    print(f"  AVISO: Jogada do P2 demorou {elapsed:.0f}ms (timeout: {timeout_per_move*1000:.0f}ms)")
                stats['player2_time'].append(elapsed)
                if 'nodes_visited' in _last_stats:
                    stats['player2_nodes'].append(_last_stats['nodes_visited'])
                else:
                    stats['player2_nodes'].append(0)  # Se não houver estatísticas, usar 0
        except Exception as e:
            print(f"  ERRO na jogada: {e}")
            # Em caso de erro, escolher primeira jogada válida
            legal = valid_moves(board)
            col = legal[0] if legal else 0
        
        # Aplicar jogada
        new_board = make_move(board, col, turn)
        if new_board is None:
            # Jogada inválida, o outro jogador vence
            return other(turn), stats
        board = new_board
        stats['moves'] += 1
        
        # Alternar turno
        turn = P2 if turn == P1 else P1
    
    # Empate
    return 0, stats

def other(player: int) -> int:
    return P1 if player == P2 else P2

def random_player(board: List[List[int]], turn: int, config: Dict) -> int:
    """Jogador aleatório para comparação."""
    global _last_stats
    _last_stats = {'nodes_visited': 0}  # Random não visita nós
    legal = valid_moves(board)
    if not legal:
        return 0
    return random.choice(legal)

# Variável global para armazenar estatísticas da última jogada
_last_stats = {}

def minimax_player(board: List[List[int]], turn: int, config: Dict) -> int:
    """Jogador usando Minimax (sem Alfa-Beta)."""
    from search import minimax
    max_depth = int(config.get("max_depth", 5))
    stats = {'nodes_visited': 0}
    
    legal = valid_moves(board)
    if not legal:
        return 0
    
    best_value = float('-inf')
    best_move = legal[0]
    
    for col in legal:
        new_board = make_move(board, col, turn)
        if new_board is not None:
            value = minimax(new_board, depth=1, max_depth=max_depth, 
                          player=turn, is_maximizing=False, stats=stats)
            if value > best_value:
                best_value = value
                best_move = col
    
    # Armazenar estatísticas
    global _last_stats
    _last_stats = {'nodes_visited': stats['nodes_visited']}
    
    return best_move

def alphabeta_player(board: List[List[int]], turn: int, config: Dict) -> int:
    """Jogador usando Minimax com Alfa-Beta (sem Iterative Deepening)."""
    from search import minimax_alphabeta
    max_depth = int(config.get("max_depth", 5))
    stats = {'nodes_visited': 0, 'pruned': 0}
    
    legal = valid_moves(board)
    if not legal:
        return 0
    
    best_value = float('-inf')
    best_move = legal[0]
    alpha = float('-inf')
    beta = float('inf')
    
    for col in legal:
        new_board = make_move(board, col, turn)
        if new_board is not None:
            value = minimax_alphabeta(new_board, depth=1, max_depth=max_depth, 
                                    player=turn, is_maximizing=False, 
                                    alpha=alpha, beta=beta, stats=stats)
            if value > best_value:
                best_value = value
                best_move = col
            alpha = max(alpha, best_value)
    
    # Armazenar estatísticas
    global _last_stats
    _last_stats = {
        'nodes_visited': stats['nodes_visited'],
        'pruned_nodes': stats.get('pruned', 0)
    }
    
    return best_move

def iterative_deepening_player(board: List[List[int]], turn: int, config: Dict) -> int:
    """Jogador usando Iterative Deepening (usa choose_move atual)."""
    # choose_move já usa Iterative Deepening, mas não retorna stats
    # Vamos usar uma versão que coleta estatísticas
    from search import minimax_alphabeta, valid_moves, make_move, order_moves
    import time
    
    max_time_ms = int(config.get("max_time_ms", 2000))
    max_depth = int(config.get("max_depth", 10))
    start = time.time()
    
    def time_exceeded():
        return max_time_ms > 0 and (time.time() - start) * 1000.0 >= max_time_ms
    
    legal = valid_moves(board)
    if not legal:
        return 0
    
    stats = {'nodes_visited': 0, 'pruned': 0}
    best_move = legal[0]
    best_value = float('-inf')
    final_depth = 1
    
    # Iterative Deepening
    for current_depth in range(1, max_depth + 1):
        if time_exceeded():
            break
        
        depth_stats = {'nodes_visited': 0, 'pruned': 0}
        depth_best_value = float('-inf')
        depth_best_move = best_move
        alpha = float('-inf')
        beta = float('inf')
        
        ordered_moves = order_moves(board, legal, turn)
        for col in ordered_moves:
            if time_exceeded():
                break
            
            new_board = make_move(board, col, turn)
            if new_board is not None:
                value = minimax_alphabeta(new_board, depth=1, max_depth=current_depth, 
                                        player=turn, is_maximizing=False, 
                                        alpha=alpha, beta=beta, stats=depth_stats)
                if value > depth_best_value:
                    depth_best_value = value
                    depth_best_move = col
                alpha = max(alpha, depth_best_value)
        
        if not time_exceeded() or current_depth == 1:
            best_move = depth_best_move
            best_value = depth_best_value
            final_depth = current_depth
            stats['nodes_visited'] += depth_stats['nodes_visited']
            stats['pruned'] += depth_stats.get('pruned', 0)
        else:
            break
    
    global _last_stats
    _last_stats = {
        'nodes_visited': stats['nodes_visited'],
        'pruned_nodes': stats.get('pruned', 0),
        'depth_reached': final_depth
    }
    
    return best_move

def run_experiment(name: str, player1_func, player2_func, 
                  config1: Dict, config2: Dict, num_games: int = 10) -> Dict:
    """
    Executa um experimento: num_games partidas entre dois jogadores.
    
    Retorna estatísticas agregadas.
    """
    print(f"\n{'='*60}")
    print(f"Experimento: {name}")
    print(f"{'='*60}")
    
    results = {
        'player1_wins': 0,
        'player2_wins': 0,
        'draws': 0,
        'player1_avg_time': 0.0,
        'player2_avg_time': 0.0,
        'player1_avg_nodes': 0.0,
        'player2_avg_nodes': 0.0,
        'total_games': num_games
    }
    
    all_p1_times = []
    all_p2_times = []
    all_p1_nodes = []
    all_p2_nodes = []
    
    for game_num in range(1, num_games + 1):
        print(f"Jogo {game_num}/{num_games}...", end=" ", flush=True)
        game_start = time.time()
        
        # Alternar quem começa
        if game_num % 2 == 1:
            winner, stats = play_game(player1_func, player2_func, config1, config2, timeout_per_move=15.0)
            # Estatísticas já estão na ordem correta
            all_p1_times.extend(stats.get('player1_time', []))
            all_p2_times.extend(stats.get('player2_time', []))
            all_p1_nodes.extend(stats.get('player1_nodes', []))
            all_p2_nodes.extend(stats.get('player2_nodes', []))
        else:
            winner, stats = play_game(player2_func, player1_func, config2, config1, timeout_per_move=15.0)
            # Inverter resultado do jogo
            if winner == P1:
                winner = P2
            elif winner == P2:
                winner = P1
            # Inverter estatísticas também (player1 e player2 foram trocados)
            all_p1_times.extend(stats.get('player2_time', []))  # player2 do jogo = player1 do experimento
            all_p2_times.extend(stats.get('player1_time', []))  # player1 do jogo = player2 do experimento
            all_p1_nodes.extend(stats.get('player2_nodes', []))
            all_p2_nodes.extend(stats.get('player1_nodes', []))
        
        game_time = time.time() - game_start
        if game_time > 60:  # Se o jogo demorou mais de 1 minuto
            print(f" (demorou {game_time:.1f}s)", end="")
        
        if winner == P1:
            results['player1_wins'] += 1
        elif winner == P2:
            results['player2_wins'] += 1
        else:
            results['draws'] += 1
        
        print(f"Vencedor: {winner if winner else 'Empate'}")
    
    # Calcular médias
    if all_p1_times:
        results['player1_avg_time'] = sum(all_p1_times) / len(all_p1_times)
    if all_p2_times:
        results['player2_avg_time'] = sum(all_p2_times) / len(all_p2_times)
    if all_p1_nodes:
        results['player1_avg_nodes'] = sum(all_p1_nodes) / len(all_p1_nodes)
    if all_p2_nodes:
        results['player2_avg_nodes'] = sum(all_p2_nodes) / len(all_p2_nodes)
    
    # Imprimir resultados
    print(f"\nResultados:")
    print(f"  Vitórias Jogador 1: {results['player1_wins']} ({results['player1_wins']/num_games*100:.1f}%)")
    print(f"  Vitórias Jogador 2: {results['player2_wins']} ({results['player2_wins']/num_games*100:.1f}%)")
    print(f"  Empates: {results['draws']} ({results['draws']/num_games*100:.1f}%)")
    print(f"  Tempo médio J1: {results['player1_avg_time']:.2f} ms")
    print(f"  Tempo médio J2: {results['player2_avg_time']:.2f} ms")
    print(f"  Estados médios J1: {results['player1_avg_nodes']:.1f}")
    print(f"  Estados médios J2: {results['player2_avg_nodes']:.1f}")
    
    return results

def experiment_1_minimax_vs_random():
    """Experimento 1: Minimax vs Aleatório (profundidades 2, 3, 4, 5)"""
    print("\n" + "="*60)
    print("EXPERIMENTO 1: Minimax vs Aleatório")
    print("="*60)
    
    results = {}
    # Aumentar número de jogos para melhor confiança estatística
    num_games_map = {2: 20, 3: 15, 4: 10, 5: 8}  # Mais jogos para melhor estatística
    
    for depth in [2, 3, 4, 5]:
        config_minimax = {'max_depth': depth, 'max_time_ms': 3000}  # Timeout mais rígido
        config_random = {}
        
        result = run_experiment(
            f"Minimax (depth={depth}) vs Aleatório",
            minimax_player,
            random_player,
            config_minimax,
            config_random,
            num_games=num_games_map[depth]
        )
        results[depth] = result
    
    return results

def experiment_2_alphabeta_vs_minimax():
    """Experimento 2: Alfa-Beta vs Minimax (profundidades 2, 3, 4, 5)"""
    print("\n" + "="*60)
    print("EXPERIMENTO 2: Alfa-Beta vs Minimax (sem poda)")
    print("="*60)
    
    results = {}
    num_games_map = {2: 15, 3: 10, 4: 8, 5: 6}  # Mais jogos para melhor comparação
    
    for depth in [2, 3, 4, 5]:
        config = {'max_depth': depth, 'max_time_ms': 3000}
        
        result = run_experiment(
            f"Alfa-Beta (depth={depth}) vs Minimax (depth={depth})",
            alphabeta_player,  # Alfa-Beta sem ID
            minimax_player,  # Minimax sem poda
            config,
            config,
            num_games=num_games_map[depth]
        )
        results[depth] = result
    
    return results

def experiment_3_iterative_vs_alphabeta():
    """Experimento 3: Iterative Deepening vs Alfa-Beta (limites 1s e 2s)"""
    print("\n" + "="*60)
    print("EXPERIMENTO 3: Iterative Deepening vs Alfa-Beta")
    print("="*60)
    
    results = {}
    for time_limit_ms in [1000, 2000]:
        config_id = {'max_depth': 10, 'max_time_ms': time_limit_ms}  # ID com limite de tempo
        config_ab = {'max_depth': 4, 'max_time_ms': time_limit_ms}  # AB fixo (profundidade 4, reduzida)
        
        result = run_experiment(
            f"Iterative Deepening ({time_limit_ms}ms) vs Alfa-Beta fixo depth=4 ({time_limit_ms}ms)",
            iterative_deepening_player,  # Usa Iterative Deepening
            alphabeta_player,  # Alfa-Beta com profundidade fixa
            config_id,
            config_ab,
            num_games=8  # Reduzido para acelerar
        )
        results[time_limit_ms] = result
    
    return results

if __name__ == "__main__":
    print("="*60)
    print("EXECUTANDO EXPERIMENTOS DO TP2")
    print("="*60)
    
    # Executar experimentos
    exp1_results = experiment_1_minimax_vs_random()
    exp2_results = experiment_2_alphabeta_vs_minimax()
    exp3_results = experiment_3_iterative_vs_alphabeta()
    
    print("\n" + "="*60)
    print("TODOS OS EXPERIMENTOS CONCLUÍDOS")
    print("="*60)
    
    # Salvar resultados em arquivo
    results_file = os.path.join(os.path.dirname(__file__), 'experiment_results.json')
    import json
    all_results = {
        'experiment_1': exp1_results,
        'experiment_2': exp2_results,
        'experiment_3': exp3_results
    }
    
    with open('experiment_results.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print("\nResultados salvos em 'experiment_results.json'")
