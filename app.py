from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# --- Tic Tac Toe logic (Minimax with Backtracking Visualization) ---

WIN_COMBOS = [
    [0,1,2], [3,4,5], [6,7,8],
    [0,3,6], [1,4,7], [2,5,8],
    [0,4,8], [2,4,6]
]

def check_winner(board):
    for a, b, c in WIN_COMBOS:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if None not in board:
        return "Draw"
    return None

def minimax(board, is_max, depth=0, trace=None):
    """Minimax with explicit backtracking trace"""
    if trace is None:
        trace = []

    result = check_winner(board)
    if result == "O": return 10, trace
    if result == "X": return -10, trace
    if result == "Draw": return 0, trace

    if is_max:
        best = -float("inf")
        for i in range(9):
            if board[i] is None:
                board[i] = "O"
                trace.append(f"{'|  '*depth}Try O at {i}")
                score, trace = minimax(board, False, depth + 1, trace)
                board[i] = None  # <-- backtrack
                trace.append(f"{'|  '*depth}Backtrack from O at {i}")
                best = max(best, score)
        return best, trace
    else:
        best = float("inf")
        for i in range(9):
            if board[i] is None:
                board[i] = "X"
                trace.append(f"{'|  '*depth}Try X at {i}")
                score, trace = minimax(board, True, depth + 1, trace)
                board[i] = None  # <-- backtrack
                trace.append(f"{'|  '*depth}Backtrack from X at {i}")
                best = min(best, score)
        return best, trace

def best_move(board):
    best_score = -float("inf")
    move = -1
    trace = []
    for i in range(9):
        if board[i] is None:
            board[i] = "O"
            trace.append(f"AI tries O at {i}")
            score, trace = minimax(board, False, 1, trace)
            board[i] = None
            trace.append(f"AI backtracks from O at {i}")
            if score > best_score:
                best_score = score
                move = i
    return move, trace


# --- Routes ---

@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/move", methods=["POST"])
def move():
    data = request.get_json()
    board = [x if x in ("X", "O") else None for x in data["board"]]
    move_index, trace = best_move(board)
    return jsonify({"move": move_index, "trace": trace})


if __name__ == "__main__":
    app.run(debug=True)

