from typing import List, Tuple, Optional, Dict
import time
import math
import random

ROWS, COLS = 6, 7
EMPTY, P1, P2 = 0, 1, 2

# -----------------------------------------------------------------------------
# Utilidades de tabuleiro (PRONTAS)
# -----------------------------------------------------------------------------
def copy_board(board: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in board]

def valid_moves(board: List[List[int]]) -> List[int]:
    """Retorna as colunas ainda jogáveis (topo vazio)."""
    return [c for c in range(COLS) if board[0][c] == EMPTY]

def make_move(board: List[List[int]], col: int, player: int) -> Optional[List[List[int]]]:
    """Retorna um novo tabuleiro aplicando a gravidade na coluna col; None se inválido."""
    if col < 0 or col >= COLS or board[0][col] != EMPTY:
        return None
    nb = copy_board(board)
    for r in reversed(range(ROWS)):
        if nb[r][col] == EMPTY:
            nb[r][col] = player
            return nb
    return None

def winner(board: List[List[int]]) -> int:
    """0 se ninguém venceu; 1 ou 2 se há 4 em linha."""
    # Horizontais
    for r in range(ROWS):
        for c in range(COLS - 3):
            x = board[r][c]
            if x != EMPTY and x == board[r][c+1] == board[r][c+2] == board[r][c+3]:
                return x
    # Verticais
    for c in range(COLS):
        for r in range(ROWS - 3):
            x = board[r][c]
            if x != EMPTY and x == board[r+1][c] == board[r+2][c] == board[r+3][c]:
                return x
    # Diag ↘
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            x = board[r][c]
            if x != EMPTY and x == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3]:
                return x
    # Diag ↗
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            x = board[r][c]
            if x != EMPTY and x == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3]:
                return x
    return 0

def is_full(board: List[List[int]]) -> bool:
    return all(board[0][c] != EMPTY for c in range(COLS))

def terminal(board: List[List[int]]) -> Tuple[bool, int]:
    """(é_terminal, vencedor) com vencedor=0 para empate/indefinido."""
    w = winner(board)
    if w != 0:
        return True, w
    if is_full(board):
        return True, 0
    return False, 0

def other(player: int) -> int:
    return P1 if player == P2 else P2

# -----------------------------------------------------------------------------
# ÚNICO PONTO A SER IMPLEMENTADO PELOS ALUNOS
# -----------------------------------------------------------------------------

def evaluate(board: List[List[int]], player: int) -> float:
    """
    Avalia o tabuleiro do ponto de vista do jogador.
    Retorna um valor positivo se a posição é favorável ao jogador.
    
    Componentes da heurística:
    1. Valorização do centro (colunas centrais são mais valiosas)
    2. Contagem de sequências (duplas e triplas)
    """
    opponent = other(player)
    score = 0.0
    
    # 1. Valorização do centro
    # Colunas centrais (2, 3, 4) são mais valiosas
    center_cols = [2, 3, 4]
    for c in center_cols:
        for r in range(ROWS):
            if board[r][c] == player:
                # Quanto mais central, mais pontos
                if c == 3:  # Coluna central
                    score += 3.0
                else:  # Colunas 2 e 4
                    score += 2.0
            elif board[r][c] == opponent:
                # Penalizar peças do oponente no centro
                if c == 3:
                    score -= 3.0
                else:
                    score -= 2.0
    
    # 2. Contagem de sequências
    # Contar sequências de 2 e 3 peças do jogador
    def count_sequences(length: int, p: int) -> int:
        """Conta sequências de 'length' peças do jogador p."""
        count = 0
        # Horizontais
        for r in range(ROWS):
            for c in range(COLS - length + 1):
                seq = [board[r][c+i] for i in range(length)]
                if seq.count(p) == length and seq.count(EMPTY) == 0:
                    count += 1
        # Verticais
        for c in range(COLS):
            for r in range(ROWS - length + 1):
                seq = [board[r+i][c] for i in range(length)]
                if seq.count(p) == length and seq.count(EMPTY) == 0:
                    count += 1
        # Diagonais ↘
        for r in range(ROWS - length + 1):
            for c in range(COLS - length + 1):
                seq = [board[r+i][c+i] for i in range(length)]
                if seq.count(p) == length and seq.count(EMPTY) == 0:
                    count += 1
        # Diagonais ↗
        for r in range(length - 1, ROWS):
            for c in range(COLS - length + 1):
                seq = [board[r-i][c+i] for i in range(length)]
                if seq.count(p) == length and seq.count(EMPTY) == 0:
                    count += 1
        return count
    
    # Sequências de 2 peças: peso 1
    score += count_sequences(2, player) * 1.0
    score -= count_sequences(2, opponent) * 1.0
    
    # Sequências de 3 peças: peso 10 (muito mais importante)
    score += count_sequences(3, player) * 10.0
    score -= count_sequences(3, opponent) * 10.0
    
    return score

def minimax(board: List[List[int]], depth: int, max_depth: int, player: int, 
            is_maximizing: bool, stats: Dict) -> float:
    """
    Algoritmo Minimax com profundidade limitada.
    
    Retorna o valor da posição do ponto de vista do jogador maximizador.
    stats é um dicionário mutável para contar estados visitados.
    """
    stats['nodes_visited'] = stats.get('nodes_visited', 0) + 1
    
    # Verificar estado terminal
    is_terminal, winner_player = terminal(board)
    if is_terminal:
        if winner_player == player:
            return float('inf')  # Vitória do jogador
        elif winner_player == other(player):
            return float('-inf')  # Derrota do jogador
        else:
            return 0.0  # Empate
    
    # Se atingiu profundidade máxima, usar heurística
    if depth >= max_depth:
        if is_maximizing:
            return evaluate(board, player)
        else:
            return -evaluate(board, other(player))
    
    # Obter jogadas válidas
    legal_moves = valid_moves(board)
    if not legal_moves:
        return 0.0  # Sem jogadas (empate)
    
    if is_maximizing:
        # Maximizador: escolhe o maior valor
        max_value = float('-inf')
        for col in legal_moves:
            new_board = make_move(board, col, player)
            if new_board is not None:
                value = minimax(new_board, depth + 1, max_depth, player, False, stats)
                max_value = max(max_value, value)
        return max_value
    else:
        # Minimizador: escolhe o menor valor
        min_value = float('inf')
        opponent = other(player)
        for col in legal_moves:
            new_board = make_move(board, col, opponent)
            if new_board is not None:
                value = minimax(new_board, depth + 1, max_depth, player, True, stats)
                min_value = min(min_value, value)
        return min_value

def minimax_alphabeta(board: List[List[int]], depth: int, max_depth: int, player: int, 
                     is_maximizing: bool, alpha: float, beta: float, stats: Dict) -> float:
    """
    Algoritmo Minimax com poda Alfa-Beta.
    
    Retorna o valor da posição do ponto de vista do jogador maximizador.
    stats é um dicionário mutável para contar estados visitados.
    alpha: melhor valor que o maximizador pode garantir
    beta: melhor valor que o minimizador pode garantir
    """
    stats['nodes_visited'] = stats.get('nodes_visited', 0) + 1
    
    # Verificar estado terminal
    is_terminal, winner_player = terminal(board)
    if is_terminal:
        if winner_player == player:
            return float('inf')  # Vitória do jogador
        elif winner_player == other(player):
            return float('-inf')  # Derrota do jogador
        else:
            return 0.0  # Empate
    
    # Se atingiu profundidade máxima, usar heurística
    if depth >= max_depth:
        if is_maximizing:
            return evaluate(board, player)
        else:
            return -evaluate(board, other(player))
    
    # Obter jogadas válidas
    legal_moves = valid_moves(board)
    if not legal_moves:
        return 0.0  # Sem jogadas (empate)
    
    if is_maximizing:
        # Maximizador: escolhe o maior valor
        max_value = float('-inf')
        for col in legal_moves:
            new_board = make_move(board, col, player)
            if new_board is not None:
                value = minimax_alphabeta(new_board, depth + 1, max_depth, player, 
                                        False, alpha, beta, stats)
                max_value = max(max_value, value)
                alpha = max(alpha, max_value)
                
                # Poda Beta: se o valor é maior que beta, o minimizador não escolherá este caminho
                if beta <= alpha:
                    stats['pruned'] = stats.get('pruned', 0) + 1
                    break  # Poda: não precisa explorar mais
        return max_value
    else:
        # Minimizador: escolhe o menor valor
        min_value = float('inf')
        opponent = other(player)
        for col in legal_moves:
            new_board = make_move(board, col, opponent)
            if new_board is not None:
                value = minimax_alphabeta(new_board, depth + 1, max_depth, player, 
                                        True, alpha, beta, stats)
                min_value = min(min_value, value)
                beta = min(beta, min_value)
                
                # Poda Alfa: se o valor é menor que alpha, o maximizador não escolherá este caminho
                if beta <= alpha:
                    stats['pruned'] = stats.get('pruned', 0) + 1
                    break  # Poda: não precisa explorar mais
        return min_value

def choose_move(board: List[List[int]], turn: int, config: Dict) -> Tuple[int, Dict]:
    """
    Decide a coluna (0..6) para jogar agora.

    Parâmetros:
      - board: matriz 6x7 com valores {0,1,2}
      - turn: 1 ou 2
      - config: {"max_time_ms": int, "max_depth": int}

    Retorna:
      - col: int (0..6)
    """
    max_time_ms = int(config.get("max_time_ms"))
    max_depth = int(config.get("max_depth"))
    turn = int(turn)

    print(f"AI choose_move called with max_time_ms={max_time_ms}, max_depth={max_depth}, player={turn}")
    
    start = time.time()

    # Função auxiliar para checar tempo decorrido   
    def time_exceeded():
        return max_time_ms > 0 and (time.time() - start) * 1000.0 >= max_time_ms
    
    legal = valid_moves(board)

    move = 0
    if not legal:
        # Sem jogadas: devolve 0 por convenção (servidor lida com isso)
        return move
    
    # Usar Minimax com poda Alfa-Beta para escolher a melhor jogada
    stats = {'nodes_visited': 0, 'pruned': 0}
    best_value = float('-inf')
    best_move = legal[0]  # Fallback: primeira jogada válida
    
    # Inicializar alpha e beta
    alpha = float('-inf')
    beta = float('inf')
    
    for col in legal:
        new_board = make_move(board, col, turn)
        if new_board is not None:
            # Avaliar esta jogada com Minimax Alfa-Beta
            # Começamos com is_maximizing=False porque o próximo turno é do oponente
            value = minimax_alphabeta(new_board, depth=1, max_depth=max_depth, 
                                    player=turn, is_maximizing=False, 
                                    alpha=alpha, beta=beta, stats=stats)
            
            if value > best_value:
                best_value = value
                best_move = col
            
            # Atualizar alpha (melhor valor que o maximizador pode garantir)
            alpha = max(alpha, best_value)
    
    move = best_move
    
    # Retornar informações sobre a busca (útil para experimentos)
    info = {
        'nodes_visited': stats['nodes_visited'],
        'pruned_nodes': stats.get('pruned', 0),
        'method': 'minimax_alphabeta',
        'depth': max_depth
    }
    
    return move

def choose_move_infinity(board: List[List[int]], turn: int, config: Dict) -> Tuple[int, Dict]:
    """
    Decide a coluna (0..6) para jogar agora.

    Parâmetros:
      - board: matriz 6x7 com valores {0,1,2}
      - turn: 1 ou 2
      - config: {"max_time_ms": int, "max_depth": int}

    Retorna:
      - col: int (0..6)
    """
    max_time_ms = int(config.get("max_time_ms"))
    max_depth = int(config.get("max_depth"))
    turn = int(turn)

    print(f"AI choose_move called with max_time_ms={max_time_ms}, max_depth={max_depth}, player={turn}")
    
    start = time.time()

    # Função auxiliar para checar tempo decorrido   
    def time_exceeded():
        return max_time_ms > 0 and (time.time() - start) * 1000.0 >= max_time_ms
    
    legal = valid_moves(board)

    move = 0
    if not legal:
        # Sem jogadas: devolve 0 por convenção (servidor lida com isso)
        return move
    
    # VERSÃO INICIAL: escolhe aleatoriamente entre as jogadas legais
    i = 0
    while True:
        i += 1

    return move