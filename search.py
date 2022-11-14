import concurrent.futures
import os
import time

disked = os.popen('wmic logicaldisk get name').read().split()
disked = disked[1:]

search_menleev = []

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[31m'
    UNDERLINE = '\033[4m'

def menu():
    os.system('cls')
    #выбирите что хотите искать папку или файл через case
    print(f' 1 - Поиск {bcolors.WARNING}папки{bcolors.ENDC}')
    print(f' 2 - Поиск {bcolors.WARNING}файла{bcolors.ENDC}\n')
    choice = input('Выберите действие: ')
    if choice == '1':
        os.system('cls')
        game = input('Введите название папки или папок\nЗаменив пробел на _ если искомая папка состоит из двух и более слов: ')
        searching = 'папки'
        start(game, searching)
    elif choice == '2':
        os.system('cls')
        game = input('Введите название файла или файлов c расширением или без\nЗамените пробел на _ если искомый файл состоит из двух и более слов: ')
        searching = 'файлы'
        if len(game.split()) == 1:
            start(game, searching)
        elif len(game.split()) > 1:
            for i in game.split():
                start(i, searching)
    else:
        os.system('cls')
        print(f'{bcolors.RED}Неверный ввод{bcolors.ENDC}')
        time.sleep(1)
        menu()
    os.system('cls')
    print(bcolors.RED + 'Поиск завершен! Если файлы найдены, то они будут записаны в файлы с именами файлов, которые вы искали.' + bcolors.ENDC)
    for i in range(5, 0, -1):
        print(i, end='\r')
        time.sleep(1)
    menu()

def start(game, searching):
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(disked)) as executor:
        for mountpoint in disked:
            executor.submit(search, mountpoint, game, searching)
    create_file(game)
    return

def search(mountpoint, game, searching):
    print('[●] Поиск',  bcolors.WARNING + game + bcolors.ENDC, 'на диске', bcolors.OKBLUE + mountpoint + bcolors.ENDC)
    disk = mountpoint + '\\'
    for root, dirs, files in os.walk(disk):
        if searching == 'папки':
            for folder in dirs:
                if folder.startswith(game):
                    search_menleev.append(os.path.join(root,folder))
                    print('[●] Папка', bcolors.WARNING + game + bcolors.ENDC, 'найдена:', bcolors.OKBLUE + root + '\\' + folder + bcolors.ENDC)
                elif game.replace('_', ' ') in folder:
                    search_menleev.append(os.path.join(root,folder))
                    print('[●] Папка', bcolors.WARNING + game + bcolors.ENDC, 'найдена:', bcolors.OKBLUE + root + '\\' + folder + bcolors.ENDC)
        if searching == 'файлы':
            for file in files:
                if file.startswith(game):
                    search_menleev.append(os.path.join(root,file))
                    print('[●] Файл', bcolors.WARNING + game + bcolors.ENDC, 'найден:', bcolors.OKBLUE + root + '\\' + file + bcolors.ENDC)
                elif game.replace('_', ' ') in file:
                    search_menleev.append(os.path.join(root,file))
                    print('[●] Папка', bcolors.WARNING + game + bcolors.ENDC, 'найден:', bcolors.OKBLUE + root + '\\' + file + bcolors.ENDC)
    return

def create_file(game):
    with open(game + '.txt', 'a') as f:
        for i in search_menleev:
            f.write(i + '\n')
    search_menleev.clear()
    return

if __name__ == '__main__':
    menu()