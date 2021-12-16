import torch as tr
import exist_data as ed
import copy
import random
import itertools

final_size = 30
number_of_sets = 1
processed_nodes = 0
search_max_depth = 1

dic = {'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
       '9': 9, '10': 10}
HEARTS, CLUBS, SPADES, DIAMONDS = 0, 1, 2, 3
"""
data = [
    ([(HEARTS, 10), (CLUBS, 10)], 0.),
    ([(HEARTS, 10), (CLUBS, 5)], 1.),
    ([(HEARTS, 10), (CLUBS, 8)], 1.),
]
"""
data = ed.data_collected()
print("The data input of the neural network has been completed")

def state_tensor(cards):
    # cards == [..., (suit, number), ...]
    state = tr.zeros((4, 13))
    for (suit, number) in cards:
        state[suit, number - 1] = 1.
    state = state.reshape(4 * 13)  # unwrap into a long vector
    return state


inputs = tr.stack([state_tensor(hand) for (hand, _) in data])
targets = tr.tensor([score for (_, score) in data]).reshape(-1, 1)


def nn_utility(state):
    list1 = copy.deepcopy(state[1])
    list_t = []
    for ele in list1[1]:
        if ele[0] == "Hearts":
            list_t.append((0, dic[ele[1]]))
        elif ele[0] == "Clubs":
            list_t.append((1, dic[ele[1]]))
        elif ele[0] == "Spades":
            list_t.append((2, dic[ele[1]]))
        elif ele[0] == "Diamonds":
            list_t.append((3, dic[ele[1]]))
    # inputs = tr.stack([state_tensor(hand) for (hand, _) in data])

    cardnet = tr.nn.Sequential(
        tr.nn.Linear(inputs.shape[1], inputs.shape[0]),
        tr.nn.Sigmoid(),
        tr.nn.Linear(targets.shape[0], targets.shape[1])
    )

    c = float(cardnet(state_tensor(list_t)))
    return c


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
    dic1 = {"stand": 0, "BlackJack": False, "Boom": False}
    list_total.append(dic1)
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


def final_evaluate(state):
    list1 = copy.deepcopy(state[1])
    if calculate_score(list1[2]) < calculate_score(list1[1]) < final_size:
        return 1
    elif calculate_score(list1[1]) == final_size:
        return 1
    elif calculate_score(list1[2]) > final_size:
        return 1
    elif calculate_score(list1[2]) == calculate_score(list1[1]):
        return 1
    else:
        return 0


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
    player, board = copy.deepcopy(state)
    new_player, new_board = play_turn(action, board)
    return new_player, new_board


def findExp(state, evaluate, depth):
    a, b = state
    highScore = [0]
    remain_cards = copy.deepcopy(b[0])
    for card in remain_cards:
        new_b = copy.deepcopy(b)
        new_b[1].append(card)
        new_b[0].remove(card)
        new_state = (a, new_b)
        score = expectimax(new_state, evaluate, depth + 1)
        highScore[0] += float(score[0]) / float(len(remain_cards))

    return highScore


def expectimax(state, evaluate, depth):
    if game_over(state):
        return [evaluate(state)]
    if depth > search_max_depth:
        return [evaluate(state)]
    global processed_nodes
    processed_nodes += 1
    return findMax(state, evaluate, depth)


def findMax(state3, evaluate, depth):
    state = copy.deepcopy(state3)
    max_number = max((findExp(state, evaluate, depth)[0]), evaluate(state))
    if max_number == evaluate(state):
        highScore = [max_number, "stand"]
    else:
        highScore = [max_number, "Hit"]
    return highScore


if __name__ == "__main__":

    depth3 = 0
    search_max_depth = 1
    final_size = int(input("Please select the size(25, 30, 35, 40, 50): "))
    if final_size == 25 or final_size == 30 or final_size == 35 or final_size == 40 or final_size == 50:
        print("Game Start!")
    else:
        print("Invalid action, try again.")
        final_size = int(input("Please select a correct size(30, 50, 70, 90, 110): "))
    model1 = input("Player0, please select the model(human, baseline-AI, tree-based-AI or tree-nn-AI): ")
    print("\n")
    state1 = initial_state()
    while not game_over(state1):
        playerr, boardd = state1
        if playerr == 0:

            if model1 == "human":
                print(string_of(boardd))
                print("--- player0(human) --->")
                action1 = get_user_action(state1)
                state1 = perform_action(action1, state1)
            elif model1 == "baseline-AI":
                print(string_of(boardd))
                print("--- player0(baseline) --->")
                g, h = baseline_ai(state1)
                state1 = (g, h)
            elif model1 == "tree-based-AI":
                print(string_of(boardd))
                print("--- player0(tree) --->")
                statet = expectimax(state1, final_evaluate, depth3)
                state1 = perform_action(statet[1], state1)
            elif model1 == "tree-nn-AI":
                print(string_of(boardd))
                print("--- player0(tree-nn) --->")
                statet = expectimax(state1, nn_utility, depth3)
                state1 = perform_action(statet[1], state1)
            else:
                print("Invalid action, try again.")
                model1 = input("Player0, please select a correct model(human, baseline-AI, tree-based-AI or "
                               "tree-nn-AI): ")
        else:
            print(string_of_final(boardd))
            print("--- player1 --->")
            if calculate_score(boardd[2]) < (final_size * 0.8):
                action = 'Hit'
                state1 = perform_action(action, state1)
            else:
                break

    playerr, boardd = state1
    print(string_of_final(boardd))
    if is_tied(boardd):
        print("Game over, it is tied.")
    else:
        winner = winner_of(boardd)
        print("Game over, player %d wins." % winner)

    print("Player0 score: " + str(calculate_score(boardd[1])))
    print("Player1 score: " + str(calculate_score(boardd[2])))
