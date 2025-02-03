import random
import os
import json


def clear_screen():
    # 운영체제에 따라 명령어가 다름
    if os.name == 'nt':  # Windows일 경우
        os.system('cls')
    else:  # Linux, macOS일 경우
        os.system('clear')


def print_banner():
    banner = """
                =========================================================
                 __  __    _    ____ _____    ____    _    __  __ _____
                |  \/  |  / \  / ___| ____|  / ___|  / \  |  \/  | ____|
                | |\/| | / _ \| |  _|  _|   | |  _  / _ \ | |\/| |  _|
                | |  | |/ ___ \ |_| | |___  | |_| |/ ___ \| |  | | |___
                |_|  |_/_/   \_\____|_____|  \____/_/   \_\_|  |_|_____|

                =========================================================
                """
    print(banner)

# 게임의 메인 메뉴 및 실행 함수
def play_game():
    global maze, size
    print_banner()
    while True:
        print("◆────────────────────────────────◆")
        print("│      🎮  미로 게임 메뉴 🎮        │")
        print("◆────────────────────────────────◆")
        print("│ 1. 🏁 미로게임 시작               │")
        print("│ 2. 💾 미로게임 불러오기            │")
        print("│ 3. 🏆 랭킹 보기                  │")
        print("│ 4. ❌ 게임 종료                  │")
        print("◆────────────────────────────────◆")
        select_menu = input('원하는 메뉴를 선택해주세요: ')

        if select_menu == '1':  # 새로운 게임 시작
            while True:
                user_name = input('닉네임을 입력해주세요: ').lower()
                if user_name.isalpha():
                    user = User(user_name)
                    break
                else:
                    print('닉네임은 문자로만 만들어주세요')

            while True:
                print("◆────────────────────────────────◆")
                print("│              난이도             │")
                print("◆────────────────────────────────◆")
                print("│ 1. 초보 (5x5)                   │")
                print("│ 2. 중수 (10 x 10)               │")
                print("│ 3. 고수 (15 x 15)               │")
                print("◆────────────────────────────────◆")
                select_level = input('레벨을 선택해 주세요: ')
                if select_level.isdigit():
                    if select_level == '1':
                        size = 5
                    elif select_level == '2':
                        size = 10
                    elif select_level == '3':
                        size = 15
                    else:
                        print('정확한 레벨을 선택해 주세요')
                        continue
                    maze = make_maze(size)
                    break
                else:
                    print('숫자를 입력해 주세요')
                user.set_level(select_level)

        elif select_menu == '2':  # 저장된 게임 불러오기
            user_name = input('닉네임을 입력해주세요: ').lower()
            loaded_data = load_game(user_name)
            if not loaded_data:
                continue
            user, maze = loaded_data

        elif select_menu == '3':  # 랭킹 보기
            print_ranking('ranking.json')
            continue

        elif select_menu == '4':  # 게임 종료
            print('게임을 종료 합니다')
            break

        else:
            print('잘못된 입력입니다. 다시 입력해주세요')
            continue

        play_maze(maze, user)


def ranking(user):
    save_ranking('ranking.json', user.name, user.score)
    print_ranking('ranking.json')


def save_ranking(filename, user_name, score):
    try:
        with open(filename, 'r') as f:
            rankings = json.load(f)
    except FileNotFoundError:
        rankings = []

    rankings.append({'name': user_name, 'score': score})

    with open(filename, 'w') as f:
        json.dump(rankings, f, indent=4)


def load_ranking(filename):
    try:
        with open(filename, 'r') as f:
            rankings = json.load(f)
        return sorted(rankings, key=lambda x: x['score'], reverse=False)
    except FileNotFoundError:
        return []


def print_ranking(filename):
    rankings = load_ranking(filename)
    if not rankings:
        print("◆────────────────────────────────◆")
        print("│              랭킹               │")
        print("◆────────────────────────────────◆")
        print("|         랭킹이 비어있습니다         2|")
        print("◆────────────────────────────────◆")
        return
    print("◆────────────────────────────────◆")
    print("│              랭킹               │")
    print("◆────────────────────────────────◆")
    for rank, user in enumerate(rankings, 1):
        print(f"│  {rank}. {user['name']} - {user['score']}점                │")
    print("◆────────────────────────────────◆")


def play_maze(maze, user):
    clear_screen()
    print_maze(maze, user)
    directions = {'1', '2', '3', '4', 's'}
    


    print('\n*********************************')
    print('미로를 탐험합니다. 목적지 "G"로 이동하세요!')
    print('*********************************\n')


    while True:
        print("◆────────────────────────────────◆")
        print("│              이동방향             │")
        print("◆────────────────────────────────◆")
        print("│ 1. 동쪽                         │")
        print("│ 2. 남쪽                         │")
        print("│ 3. 서쪽                         │")
        print("│ 4. 북쪽                         │")
        print("│ s. 저장후 종료                    │")
        print("◆────────────────────────────────◆")

        user_input = input("무엇을 입력하시겠어요?: ")

        if user_input not in directions:
            print('잘못된 입력입니다. 다시 입력해주세요')
            continue

        if user_input.lower() == 's':
            save_game(maze, user)
            print('저장이 완료되었습니다.')
            break
        else:
            clear_screen()
            move_maze(maze, int(user_input) - 1, user)
            print_maze(maze, user)
            if check_goal(maze, user):
                print(f'축하합니다 {user.name}! 도착했습니다. 총 이동 횟수: {user.score}')
                ranking(user)
                break

def save_game(maze, user):
    filename = f'{user.name}_save.json'
    game_data = {
        'user': user.to_dict(),
        'maze': maze
    }
    with open(filename, 'w') as file:
        json.dump(game_data, file, indent=4)


def load_game(user_name):
    filename = f'{user_name}_save.json'
    if not os.path.exists(filename):
        print('저장된 게임을 찾을 수 없습니다.')
        return None

    with open(filename, 'r') as file:
        game_data = json.load(file)
        user_data = game_data['user']
        maze = game_data['maze']
        user = User(user_data['name'], user_data['x'], user_data['y'], user_data['score'])
        return user, maze


def print_maze(maze, user):
    for y, row in enumerate(maze):
        line = ""
        for x, cell in enumerate(row):
            if y == user.y_position and x == user.x_position:
                line += "[S]"  # 유저 위치는 대괄호로 표시
            elif cell == '1':
                line += "[█]"  # 벽은 대괄호로 감싸 표시
            elif cell == '0':
                line += "[ ]"  # 빈 칸은 빈 대괄호로 표시
            elif cell == 'G':
                line += "[G]"  # 목표는 대괄호로 표시
        print(line)


def move_maze(maze, direction, user):
    dir = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    nx = user.x_position + dir[direction][0]
    ny = user.y_position + dir[direction][1]

    if is_valid_room(maze, nx, ny):
        user.move(nx, ny)
    else:
        print('잘못된 이동입니다 다시 선택해 주세요')
        return


def check_goal(maze, user):
    if maze[user.x_position][user.y_position] == 'G':
        return True
    else:
        return False


def is_valid_room(maze, nx, ny):
    size = len(maze) // 2 + 1
    if 0 < nx <= size * 2 + 1 and 0 < ny < size * 2 + 1 and maze[ny][nx] != '1':
        return True
    return False


class Room:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.visit = 0
        self.prev = None
        self.dir = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
        random.shuffle(self.dir)

    def get_cur_pos(self):
        return self.x, self.y

    def get_next_pos(self):
        return self.dir.pop()


def make_maze(size):
    rooms = [[Room(x, y) for x in range(size)] for y in range(size)]
    maze = [['1' for _ in range(size * 2 + 1)] for _ in range(size * 2 + 1)]

    visited = []

    def make(cur_room):
        cx, cy = cur_room.get_cur_pos()
        visited.append((cx, cy))
        maze[cy * 2 + 1][cx * 2 + 1] = '0'
        while cur_room.dir:
            nx, ny = cur_room.get_next_pos()
            if 0 <= nx < size and 0 <= ny < size:
                if (nx, ny) not in visited:
                    maze[cy + ny + 1][cx + nx + 1] = '0'
                    make(rooms[ny][nx])
    make(rooms[0][0])
    maze[size * 2 - 1][size * 2 - 1] = 'G'
    return maze


class User:
    def __init__(self, name, x=1, y=1, score=0):
        self.name, self.x_position, self.y_position, self.score = name, x, y, score
        self.level = 0

    def move(self, x, y):
        self.x_position = x
        self.y_position = y
        self.score += 1

    def set_level(self, level):
        self.level = level

    def to_dict(self):
        return {
            'name': self.name,
            'level': self.level,
            'score': self.score,
            'x': self.x_position,
            'y': self.y_position
        }


if __name__ == '__main__':
    play_game()