import copy
import random
import itertools
import numpy as np

final_size = 50
number_of_sets = 1


def initial_state() -> tuple:
    suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    cards = []
    for i in range(0, number_of_sets):
        for suit, value in itertools.product(suits, values):
            cards.append((suit, value))
    player0 = []
    player1 = []
    random.shuffle(cards)
    card = cards.pop()
    player0.append(card)
    card = cards.pop()
    player0.append(card)
    card = cards.pop()
    player1.append(card)
    card = cards.pop()
    player1.append(card)
    list_total = [cards, player0, player1]
    dic = {"stand": 0, "BlackJack": False, "Boom": False}
    list_total.append(dic)
    tuple1 = (0, list_total)
    return tuple1


def game_over(state: tuple) -> bool:
    test = copy.deepcopy(state[1])
    if (test[3])["BlackJack"]:
        return True
    elif (test[3])["Boom"]:
        return True
    elif (test[3])["stand"] == 2:
        return True
    else:
        return False


def cardscore(value):
    if value in ["Jack", "Queen", "King"]:
        return 10
    if value in ["2", "3", "4", "5", "6", "7", "8", "9", "10"]:
        return int(value)
    if value == "Ace":
        return 1


def handscore_ace_adjusted(total: int, list1: list) -> int:
    y = 0
    for x in list1:
        if x[1] == "Ace":
            y = y + 1
    for ace in range(y):
        if total < final_size - 9:
            total += 10
    return total


def calculate_score(list1: list) -> int:
    sum_value = 0
    for x in list1:
        sum_value = sum_value + cardscore(x[1])
    final_score = handscore_ace_adjusted(sum_value, list1)
    return final_score


def calculate_score1(list1: list) -> int:
    sum_value = 0
    for x in list1:
        sum_value = sum_value + cardscore(x[1])
    return sum_value


def blackjack(list1: list) -> bool:  # GHHHHHHHHHHHHH
    sum_value = calculate_score(list1)
    if sum_value == final_size:
        return True
    else:
        return False


def boom(list1: list) -> bool:  # GHHHHHHHHHHHHH
    sum_value = calculate_score(list1)
    if sum_value > final_size:
        return True
    else:
        return False


def current_player(board: list) -> int:
    if (board[3])["stand"] == 0:
        return 0
    else:
        return 1


def opposite_player(p: int) -> int:
    if p == 1:
        return 0
    if p == 0:
        return 1


def play_turn(move: str, new_list: list) -> tuple:
    board = copy.deepcopy(new_list)

    if move == "Hit" and (board[3])["stand"] == 0:
        random.shuffle(board[0])
        card = board[0].pop()
        board[1].append(card)
        (board[3])["BlackJack"] = blackjack(board[1])
        (board[3])["Boom"] = boom(board[1])
        new = current_player(board)
        if (board[3])["BlackJack"]:
            new_tuple = (new, board)
            return new_tuple
        if (board[3])["Boom"]:
            new_tuple = (new, board)
            return new_tuple
    elif move == "Hit" and (board[3])["stand"] == 1:
        random.shuffle(board[0])
        card = board[0].pop()
        board[2].append(card)
        (board[3])["BlackJack"] = blackjack(board[2])
        (board[3])["Boom"] = boom(board[2])
        new = current_player(board)
        if (board[3])["BlackJack"]:
            new_tuple = (new, board)
            return new_tuple
        if (board[3])["Boom"]:
            new_tuple = (new, board)
            return new_tuple
    else:
        (board[3])["stand"] = (board[3])["stand"] + 1
        new = 1

    new_tuple = (new, board)
    return new_tuple


def winner_of(list1: list) -> int:
    board = copy.deepcopy(list1)
    if (board[3])["BlackJack"]:
        return current_player(board)
    elif (board[3])["Boom"]:
        return opposite_player(current_player(board))
    elif calculate_score(board[1]) > calculate_score(board[2]):
        return 0
    else:
        return 1


def is_tied(list1: list) -> bool:
    board = copy.deepcopy(list1)
    if calculate_score(board[1]) == calculate_score(board[2]):
        return True
    else:
        return False


def score_in(state: tuple) -> float:  # GHHHHHHHHHHHHH important ------------------------
    if final_size == 21:
        per = 0.86
    elif final_size == 50:
        per = 0.9
    elif final_size == 70:
        per = 0.92
    elif final_size == 90:
        per = 0.94
    else:
        per = 0.96
    list1 = copy.deepcopy(state[1])
    a = current_player(list1)
    if a == 0:
        if final_size * per > calculate_score(list1[1]):
            return final_size * per - calculate_score(list1[1])
        else:
            return calculate_score(list1[1]) - final_size
    else:
        if final_size * per > calculate_score(list1[2]):
            return final_size * per - calculate_score(list1[2])
        else:
            return calculate_score(list1[2]) - final_size


def final_evaluate(state):
    return score_in(state)


def valid_actions(state: tuple) -> list:  # GHHHHHHHHHHHHH
    list1 = []
    result = copy.deepcopy(state[1])
    if current_player(result) == 0:
        if calculate_score(result[1]) < final_size:
            list1.append("Hit")
            list1.append("stand")
    else:
        if calculate_score(result[2]) < final_size:
            list1.append("Hit")
            list1.append("stand")
    return list1


def baseline_ai(state):
    actions = valid_actions(state)
    random.shuffle(actions)
    ac = actions.pop()
    a, b = perform_action(ac, state)
    return a, b


def string_of(board: list) -> str:
    str1 = "Player0: \n"
    for x in board[1]:
        str1 = str1 + str(x)
    a = calculate_score(board[1])
    str1 = str1 + "current score:" + str(a) + "\n"
    str2 = "Player1:\n(player1's first card is not revealed now)"
    for y in (board[2])[1:]:
        str2 = str2 + str(y)
    b = cardscore(((board[2])[1])[1])
    str2 = str2 + "current score:" + str(b) + "\n"
    str3 = str1 + str2
    return str3


def string_of_final(board: list) -> str:
    str1 = "Player0: \n"
    for x in board[1]:
        str1 = str1 + str(x)
    a = calculate_score(board[1])
    str1 = str1 + "current score:" + str(a) + "\n"
    str2 = "Player1: \n"
    for y in board[2]:
        str2 = str2 + str(y)
    b = calculate_score(board[2])
    str2 = str2 + "current score:" + str(b) + "\n"
    str3 = str1 + str2
    return str3


def get_user_action(state):
    actions = list(map(str, valid_actions(state)))
    player, board = state
    prompt = "Player %d, choose an action (%s): " % (player, ",".join(actions))
    while True:
        action = input(prompt)
        if action in actions:
            return action
        print("Invalid action, try again.")


def perform_action(action, state):
    player, board = state
    new_player, new_board = play_turn(action, board)
    return new_player, new_board


def minimax(state, max_depth, evaluate):
    # returns chosen child state, utility

    # base cases
    if game_over(state):
        return None, score_in(state)
    if max_depth == 0:
        return None, evaluate(state)

    # recursive case
    children = [perform_action(action, state) for action in valid_actions(state)]
    results = [minimax(child, max_depth - 1, evaluate) for child in children]

    _, utilities = zip(*results)
    player, board = state
    if player == 0:
        action2 = np.argmax(utilities)
    if player == 1:
        action2 = np.argmin(utilities)
    return children[action2], utilities[action2]


if __name__ == "__main__":

    max_depth1 = 1
    final_size = int(input("Please select the size(21, 50, 70, 90, 100): "))
    number_of_sets = int(input("How many decks do you want(If the size is greater than 50, it is recommended to "
                               "choose 2 decks of cards or more)(1,2,3,4): "))
    model1 = input("Player0, please select the model(human, baseline-AI, or tree-based-AI): ")
    model2 = input("Player1, please select the model(human, baseline-AI, or tree-based-AI): ")
    print("\n")
    state1 = initial_state()
    while not game_over(state1):
        playerr, boardd = state1
        if playerr == 0:
            print(string_of(boardd))
            if model1 == "human":
                action1 = get_user_action(state1)
                state1 = perform_action(action1, state1)
            elif model1 == "baseline-AI":
                print("--- baseline AI --->")
                g, h = baseline_ai(state1)
                state1 = (g, h)
            else:
                print("--- tree-base-AI --->")
                state1, _ = minimax(state1, max_depth1, final_evaluate)
        else:
            print(string_of_final(boardd))
            if model2 == "human":
                action1 = get_user_action(state1)
                state1 = perform_action(action1, state1)
            elif model2 == "baseline-AI":
                print("--- baseline AI --->")
                g, h = baseline_ai(state1)
                state1 = (g, h)
            else:
                print("--- tree-base-AI --->")
                state1, _ = minimax(state1, max_depth1, final_evaluate)

    playerr, boardd = state1
    print(string_of_final(boardd))
    if is_tied(boardd):
        print("Game over, it is tied.")
    else:
        winner = winner_of(boardd)
        print("Game over, player %d wins." % winner)

    score = score_in(state1)
    print("Final score: %d" % score)
