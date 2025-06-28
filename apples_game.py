import random as rd
import getch as gh # getting an input without using the enter
import os          # to clean the console

# Describing everything we need to know about apple
class Apple:
    """
    Я решил использовать __init__ так, как при расширении проекта будет гораздо
    проще создавать новые подвиды яблок. И я так понял, использование максимального
    количества функций и классов - главная цель ООП. До код ревью от ГПТшки функции
    __init__ я не использовал так, как яблоко только одно.
    """
    def __init__(self, symbol_code, chance):
        self.appearance = chr(symbol_code) # The only thing I've found resembling an apple
        self.probability = chance          # Probability (0 - 1) of apple spawning on the cell of the field

# Doing the same thing with the player
class Player:
    """
    Тут я пошел по той же логике. Не смотря на то, что пока у нас только один игрок и
    ничего не мешает задать позицию для всего класса, я решил пойти по принципам ООП,
    и включить в класс функцию __init__, для возможного расширения проекта и для чистоты
    кода.
    """
    def __init__(self, symbol_code, field_n, field_m):
        self.appearance = chr(symbol_code)
        self.pos = [rd.randint(0, field_n - 1), rd.randint(0, field_m - 1)]
        self.score = 0

def player_placement(game_map: list, player) -> list:
    """
    player: class, which stands for player
    Просто устанавливаем внешность игрока (смайлик) на рандомную точку на карте
    """
    game_map[player.pos[0]][player.pos[1]] = player.appearance

def apple_generation(game_map: list, n: int, m: int, coin, player) -> list:
    """
    coin: class, which stands for apples
    player: class, which stands for player :)
    
    Запускаю форы, которые будут проходится по каждой клетке и с установленным
    шансом генерировать яблочки. Помимо этого запихиваем условие что в клетке нет смайлика,
    что бы наш игрок не заменился яблоком...
    """
    for i in range(n):
        for j in range(m):
            if (rd.random() <= coin.probability) and (game_map[i][j] != player.appearance): 
                game_map[i][j] = coin.appearance
    return game_map
            
# Temporary visualisation
def visualise(game_map: list):
    """
    Визуализация поля которая планировалась, как временная мера, но ипользуется по сей день
    """
    for i in game_map:
        print(*i)
    
# Check if movement will be possible inside the restricted area (list)
def out_of_bounds(n: int, m: int, future_player_pos: list) -> bool:
    """
    Проверяем выходит ли следующий ход игрока за поля или нет.
    """
    if 0 > future_player_pos[0] > n:
        return False
    elif 0 > future_player_pos[1] > m:
        return False
    return True

# Player movement (self explanatory)
def player_movement(game_map: list, move: str, player_pos: list, n: int, m: int, player, apple):
    """
    player: class, which stands for player :)
    Двигаем игрока по полю. С встроенной проверкой на возможность хода.
    """
    possible = True
    is_apple = False
    
    # Some repetetive if statements, def will only make it harder
    if (move == 'w' or move == 'ц') and (0 <= player_pos[0] - 1 < n):
        game_map[player_pos[0]][player_pos[1]] = '*'
        player_pos[0] -= 1
        if game_map[player_pos[0]][player_pos[1]] == apple.appearance:
            is_apple = True
        game_map[player_pos[0]][player_pos[1]] = player.appearance
        
    elif (move == 's' or move == 'ы')  and (0 <= player_pos[0] + 1 < n):
        game_map[player_pos[0]][player_pos[1]] = '*'
        player_pos[0] += 1
        if game_map[player_pos[0]][player_pos[1]] == apple.appearance:
            is_apple = True
        game_map[player_pos[0]][player_pos[1]] = player.appearance
        
    elif (move == 'a' or move == 'ф') and (0 <= player_pos[1] - 1 < m):
        game_map[player_pos[0]][player_pos[1]] = '*'
        player_pos[1] -= 1
        if game_map[player_pos[0]][player_pos[1]] == apple.appearance:
            is_apple = True
        game_map[player_pos[0]][player_pos[1]] = player.appearance
        
    elif (move == 'd' or move == 'в') and (0 <= player_pos[1] + 1 < m):
        game_map[player_pos[0]][player_pos[1]] = '*'
        player_pos[1] += 1
        if game_map[player_pos[0]][player_pos[1]] == apple.appearance:
            is_apple = True
        game_map[player_pos[0]][player_pos[1]] = player.appearance
    
    # So it won't write 'impossible turn' when quitting a game
    elif move == 'q':
        pass
    
    # If all the if's not worked then the turn is impossible
    else:
        possible = False
    return player_pos, game_map, possible, is_apple
        
        
def clear_console():
       os.system('cls' if os.name == 'nt' else 'clear')
       
       
def main():
    """
    Часть комментариев будет на английском языке в связи с тем, что я страюсь прибить
    привычку писать больше комметов, а делать это как раз на английском. Это первый проект
    в который я решил попробовать имплементировать ООП так, что частично был использован ГПТ,
    чтобы научиться правильно работать с объектами, классами, функциями и прочим добром.
    
    А так это часть кода, где будет происходить вся движуха, связанная с игрой
    """

    # Making a game map n x m cells
    print("Введите n x m, через пробел (5 8): ", end='')
    n, m = map(int, input().split())
    playing_field = [['*' for _ in range(m)] for _ in range(n)]
    
    # Creating a real player
    smiley = Player(9786, n, m)
    
    # Creating an apple
    apples = Apple(63743, 0.1)
    
    # Placing a player on the random point of the map
    player_placement(playing_field, smiley)
    
    # Generating apples on the map randomly
    apple_generation(playing_field, n, m, apples, smiley)
    
    # Counting apples on the map
    apples_amount = sum([i.count(apples.appearance) for i in playing_field])
    
    print("Перемещение происходит на 'wasd' (Не забудьте сменить раскладку на английскую!)") 
    
    # Visualising the field for our game
    visualise(playing_field)
    
    """
    Я решил не делать отделтную функцию так, как это лишь усложнило бы процесс из-за
    большого количества используемых переменных.
    Тут я решил сделать while loop, который регулярно считывает ввод игрока без использования
    enter. И останавливается только при получении клавиши на выход из игры.
    Способ получения данных без enter подглядел в интернете, оказалось, что это
    осуществимо и без pygame... 
    Позже можно вставить конструкции ловящие ошибки, добавить больше видов яблок,
    сделать игру в отдельном окне и тд. Потенциал у проекта есть!
    """
    
    # Making a first move
    move = gh.getch().lower()
    while move != 'q':
        move = gh.getch().lower()
        # Making a move and collecting info about this move being possible and scoring
        smiley.pos, playing_field, is_possible, is_scored = player_movement(playing_field, move, smiley.pos, n, m, smiley, apples)
        
        # Adding a score if player gets an apple
        if is_scored: 
            smiley.score += 1
        
        # Cleaning terminal/console
        clear_console()
        
        # Visualisation of the game
        print("Score: ", smiley.score)
        visualise(playing_field)
        print("Что бы выйти нажмите 'q'")
        
        if not is_possible: print("Не возможный ход...")
        if smiley.score == apples_amount: print("Поздравляю, вы собрали все яблоки!!!")
                
main()
