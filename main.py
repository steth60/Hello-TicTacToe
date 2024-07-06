import random
import time

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("---------")

def check_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or \
           all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or \
       all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def is_full(board):
    return all(cell != ' ' for row in board for cell in row)

def get_empty_cells(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']

def evaluate_board(board, player, opponent):
    score = 0
    
    # Check rows, columns, and diagonals
    lines = (
        board + # rows
        list(map(list, zip(*board))) + # columns
        [[board[i][i] for i in range(3)]] + # main diagonal
        [[board[i][2-i] for i in range(3)]] # other diagonal
    )
    
    for line in lines:
        player_count = line.count(player)
        opponent_count = line.count(opponent)
        empty_count = line.count(' ')
        
        if player_count == 3:
            score += 100
        elif player_count == 2 and empty_count == 1:
            score += 10
        elif player_count == 1 and empty_count == 2:
            score += 1
        
        if opponent_count == 2 and empty_count == 1:
            score -= 10
    
    # Prefer center and corners
    if board[1][1] == player:
        score += 5
    for corner in [(0,0), (0,2), (2,0), (2,2)]:
        if board[corner[0]][corner[1]] == player:
            score += 3
    
    return score

def minimax(board, depth, alpha, beta, is_maximizing, player, opponent):
    if check_winner(board, player):
        return 1000 - depth
    if check_winner(board, opponent):
        return -1000 + depth
    if is_full(board):
        return 0
    if depth >= 5:  # Limit depth for faster computation
        return evaluate_board(board, player, opponent)

    if is_maximizing:
        best_score = float('-inf')
        for i, j in get_empty_cells(board):
            board[i][j] = player
            score = minimax(board, depth + 1, alpha, beta, False, player, opponent)
            board[i][j] = ' '
            best_score = max(score, best_score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = float('inf')
        for i, j in get_empty_cells(board):
            board[i][j] = opponent
            score = minimax(board, depth + 1, alpha, beta, True, player, opponent)
            board[i][j] = ' '
            best_score = min(score, best_score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score

def ai_move(board, player, opponent):
    best_score = float('-inf')
    best_moves = []
    alpha = float('-inf')
    beta = float('inf')
    
    for i, j in get_empty_cells(board):
        board[i][j] = player
        score = minimax(board, 0, alpha, beta, False, player, opponent)
        board[i][j] = ' '
        
        if score > best_score:
            best_score = score
            best_moves = [(i, j)]
        elif score == best_score:
            best_moves.append((i, j))
    
    # Randomly choose from the best moves
    return random.choice(best_moves)

def play_game():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    players = ['X', 'O']
    
    print("New game starting!")
    print_board(board)
    time.sleep(2)
    
    for turn in range(9):
        current_player = players[turn % 2]
        opponent = players[(turn + 1) % 2]
        
        print(f"\nAI {current_player} is thinking...")
        time.sleep(1)
        
        row, col = ai_move(board, current_player, opponent)
        board[row][col] = current_player
        
        print(f"AI {current_player} makes a move:")
        print_board(board)
        
        if check_winner(board, current_player):
            print(f"AI {current_player} wins!")
            return current_player
        
        if is_full(board):
            print("It's a tie!")
            return "Tie"
        
        time.sleep(2)

    print("It's a tie!")
    return "Tie"

def print_scoreboard(results, games_played):
    print("\n--- Current Scoreboard ---")
    print(f"Games played: {games_played}")
    print(f"AI X wins: {results['X']} ({results['X']/games_played*100:.1f}%)")
    print(f"AI O wins: {results['O']} ({results['O']/games_played*100:.1f}%)")
    print(f"Ties: {results['Tie']} ({results['Tie']/games_played*100:.1f}%)")
    print("-------------------------")

def main():
    games_to_play = 5
    results = {"X": 0, "O": 0, "Tie": 0}
    
    for game in range(games_to_play):
        print(f"\n=== Game {game + 1} ===")
        result = play_game()
        results[result] += 1
        print_scoreboard(results, game + 1)
        time.sleep(3)
    
    print("\n=== Final Results ===")
    print_scoreboard(results, games_to_play)
    
    if results["X"] > results["O"]:
        print("AI X is the overall winner!")
    elif results["O"] > results["X"]:
        print("AI O is the overall winner!")
    else:
        print("The tournament ends in a tie!")

# Run the main function
main()
