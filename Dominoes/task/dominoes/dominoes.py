import random
import operator


dominoes = []
stock = []
player = []
computer = []
stock = []
snake = []
status = ""


def start_game():
    global dominoes
    global stock
    global player
    global computer
    global stock

    random.shuffle(dominoes)

    player = random.sample(dominoes, k=7)
    dominoes = [i for i in dominoes if not i in player]

    computer = random.sample(dominoes, k=7)
    stock = [i for i in dominoes if not i in computer]
    find_snake()


def main():
    global dominoes

    x = 0
    y = 0

    for i in range(28):
        while y < 7:
            dominoes.append([x, y])
            y = y + 1
        else:
            x = x + 1
            y = x


def find_snake():
    global snake
    global player
    global computer
    global status

    x = 6

    while x >= 0:
        y = x
        list_search = [x, y]
        if list_search in player:
            snake.append(list_search)
            player.remove(list_search)
            status = "computer"
            return
        elif list_search in computer:
            snake.append(list_search)
            computer.remove(list_search)
            status = "player"
            return
        x = x - 1
    else:
        start_game()


def check_game(current):
    global status
    global player
    global computer
    global snake

    if len(current) == 0:
        if status == "player":
            print_me()
            print("\nStatus: The game is over. You won!")
            exit()
        else:
            print_me()
            print("\nStatus: The game is over. The computer won!")
            exit()
    elif len(snake) > 6 and snake[0][0] == snake[-1][-1]:
        if sum(x.count(snake[0][0]) for x in snake) == 8:
            print("Status: The game is over. It's a draw!")
            exit()
        else:
            return True
    else:
        return True


def try_opposite(move):
    move = move - move * 2
    gameplay(move, computer)

def gameplay(move, active):
    global status
    global stock
    global snake
    global player
    global computer

    current = active
    isNeedToEscape = False
    if move == 0:
        if len(stock) != 0:
            i = random.sample(stock, k=1)
            current.extend(i)
            stock.remove(current[-1])
    elif move > 0:
        move = move - 1
        if snake[-1][-1] not in current[move]:
            if status == "player":
                print("Illegal move. Please try again")
                activate_pl()
            else:
                isNeedToEscape = True
                try_opposite(move + 1)
        if isNeedToEscape == False:
            if snake[-1][-1] == current[move][-1]:
                snake.append(current[move][::-1])
            else:
                snake.append(current[move])
            current.remove(current[move])
    else:
        move = abs(move) - 1
        if snake[0][0] not in current[move]:
            if status == "player":
                print("Illegal move. Please try again")
                activate_pl()
            else:
                isNeedToEscape = True
        if isNeedToEscape == False:
            if snake[0][0] == current[move][0]:
                snake.insert(0, current[move][::-1])
            else:
                snake.insert(0, current[move])
            current.remove(current[move])

    if check_game(current) == True and isNeedToEscape == False:
        if status == "player":
            player = current
            status = "computer"
        elif status == "computer":
            computer = current
            status = "player"
        next_turn()


def validate(move):
    global player

    try:
        int(move)
        if abs(int(move)) <= len(player):
            return True
        else:
            return False
    except ValueError:
        return False


def activate_pl():
    global player

    move = input()
    if validate(move) == True:
        gameplay(int(move), player)
    else:
        print("Invalid input. Please try again.")
        activate_pl()

def domino_structure(dominos, struct):
  for domino in dominos:
    for value in domino:
      struct[value] += 1

def get_value(comp, struct):
  comp_dict = {}
  i = 0
  for domino in comp:

    my_sum = struct[domino[0]]
    my_sum += struct[domino[1]]
    comp_dict.update({i: my_sum})
    i += 1

  a = dict(sorted(comp_dict.items(), key=operator.itemgetter(1), reverse=True))
  return a

def make_move(a):
    i = 0
    while i < len(a):
        gameplay((a[i] + 1), computer)
        i = i + 1
    else:
        i = 0
        gameplay(i, computer)


def comp_turn():
    dicts = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0}

    domino_structure(computer, dicts)
    domino_structure(snake, dicts)
    a = get_value(computer, dicts)
    make_move(list(a.keys()))


def activate_comp():
    input()
    comp_turn()




def print_me():
    global player
    global computer
    global stock
    global snake

    print("======================================================================")
    print(f"Stock size: {len(stock)}")
    print(f"Computer pieces: {len(computer)}")
    print("\n")

    if len(snake) < 7:
        print(*snake)
    else:
        print(str(snake[0]) + str(snake[1]) + str(snake[2]) + "..." + str(snake[-3]) + str(snake[-2]) + str(snake[-1]))
    print("\n")
    print("Your pieces:")
    if len(player) > 0:
        for i, d in enumerate(player):
            print(f"{i + 1}:{d}")
    else:
        print("\n")


def next_turn():
    global status
    print_me()

    if status == "player":
        print("\nStatus: It's your turn to make a move. Enter your command.")
        activate_pl()
    elif status == "computer":
        print("\nStatus: Computer is about to make a move. Press Enter to continue...")
        activate_comp()


main()
start_game()
next_turn()
