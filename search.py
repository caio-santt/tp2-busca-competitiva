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
    
    # VERSÃO INICIAL: escolhe aleatoriamente entre as jogadas legais
    move = random.choice(legal)

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