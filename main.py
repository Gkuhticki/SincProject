import datetime
import os
import shutil
import time
from datetime import datetime


log = []



# каталоги с root взял на всякий случай
# каталоги без root нужны для успешного создания каталогов в dst, и для сравнения итоговых данных
# в path_file_src по итогу хранятся все файлы по шаблону [[ФАЙЛ, ПУТЬ], [ФАЙЛ, ПУТЬ]]
only_all_catalogs_src = []
only_all_catalogs_src_without_root = []
path_file_src = []
path_time_file_src = []

only_all_catalogs_dst = []
only_all_catalogs_dst_without_root = []
path_file_dst = []
path_time_file_dst = []

def scraping_files_catalogs_of_src():
    tree_src = os.walk(src, topdown=True)
    len_src = len(src)
    for (root, dirs, files) in tree_src:
        inner_tempfiles = []
        inner_temp_path = []
        inner_tempdict_file_path = []

        only_all_catalogs_src.append(root)
        only_all_catalogs_src_without_root.append(root[len_src:])

        # записываем во временный словарь путь до файла без src, и отдельно записываем файлы в этой директории
        # это нужно для того что бы позже сформировать конечный список по шаблону [ПУТЬ, ФАЙЛ], [ПУТЬ, ФАЙЛ]
        inner_temp_path.append(root[len_src:])
        inner_tempfiles.extend(files)

        # цикл и строка после него  нужны для того что бы свормировать вложенный список,
        # где первым значением будет путь к файлу а вторым файл
        for i in inner_tempfiles:
            l = []
            count = len(inner_temp_path[0])
            # конструкция if else здесь необхадима для того на начальном этапе проставить все "/" в путях где это нужно,
            # иначе потом будут проблемы с экранированием

            if count == 0:
                l.append(inner_temp_path[0])
            else:
                l.append(inner_temp_path[0]+"/")
            l.append(str(i))
            inner_tempdict_file_path.append(l)
        path_file_src.extend(inner_tempdict_file_path)

    # Цикл ниже нужен для добавления времени изменения файла.
    # По итогу выполнения этого цикла должнен получиться список по шаблону [ПУТЬ, ДАТА/ВРЕМЯ ИЗМЕНЕНИЯ, ФАЙЛ], ...
    inner_tempdict_src = []
    for dirs in path_file_src:
        l = []
        path_file = str(src + dirs[0] + dirs[1])
        timechange = os.path.getmtime(path_file)
        l.append(dirs[0])
        l.append(str(timechange))
        l.append(dirs[1])
        inner_tempdict_src.append(l)
    path_time_file_src.extend(inner_tempdict_src)


def scraping_files_catalogs_of_dst():
    len_dst = len(dst)
    tree_dst = os.walk(dst, topdown=True)
    for (root, dirs, files) in tree_dst:
        inner_tempfiles = []
        inner_temp_path = []
        inner_tempdict_file_path = []

        only_all_catalogs_dst.append(root)
        only_all_catalogs_dst_without_root.append(root[len_dst:])

        # записываем во временный словарь путь до файла без dst, и отдельно записываем файлы в этой директории
        # это нужно для того что бы позже сформировать конечный список по шаблону [ПУТЬ, ФАЙЛ], [ПУТЬ, ФАЙЛ]
        inner_temp_path.append(root[len_dst:])
        inner_tempfiles.extend(files)

        # цикл и строка после него  нужны для того что бы свормировать вложенный список,
        # где первым значением будет путь к файлу а вторым файл
        for i in inner_tempfiles:
            l = []
            count = len(inner_temp_path[0])
            # конструкция if else здесь необхадима для того на начальном этапе проставить все "/" в путях где это нужно,
            # иначе потом будут проблемы с экранированием

            if count == 0:
                l.append(inner_temp_path[0])
            else:
                l.append(inner_temp_path[0]+"/")
            l.append(str(i))
            inner_tempdict_file_path.append(l)
        path_file_dst.extend(inner_tempdict_file_path)

    # Цикл ниже нужен для добавления времени изменения файла.
    # По итогу выполнения этого цикла должнен получиться список по шаблону [ПУТЬ, ДАТА/ВРЕМЯ ИЗМЕНЕНИЯ, ФАЙЛ], ...
    inner_tempdict_dst = []
    for dirs in path_file_dst:
        l = []
        path_file = str(dst + dirs[0] + dirs[1])
        timechange = os.path.getmtime(path_file)
        l.append(dirs[0])
        l.append(str(timechange))
        l.append(dirs[1])
        inner_tempdict_dst.append(l)
    path_time_file_dst.extend(inner_tempdict_dst)


def create_catalog_in_dst():
    for i in only_all_catalogs_src_without_root:
        try:
            current_datetime = str(datetime.now())
            os.makedirs(dst + i, mode=511)
            l = (current_datetime + ':  Создание каталога: ' + i)
            log.append(l)
            print(l)
        except:
            pass


# Формируем списки различий файлов и директорий для копирования и удаления лишних
time_file_only_in_src = []
time_file_only_in_dst = []
path_only_in_dst = []


def compare_changing():
    inner_time_file_only_in_src = [x for x in path_time_file_src if all(x[1:] != y[1:] for y in path_time_file_dst)]
    time_file_only_in_src.extend(inner_time_file_only_in_src)

    inner_time_file_only_in_dst = [x for x in path_time_file_dst if all(x[1:] != y[1:] for y in path_time_file_src)]
    time_file_only_in_dst.extend(inner_time_file_only_in_dst)

    inner_path_only_in_dst = [x for x in only_all_catalogs_dst_without_root if all(x[1:] != y[1:] for y in only_all_catalogs_src_without_root)]
    path_only_in_dst.extend(inner_path_only_in_dst)


def copy_files():
    for dirs in time_file_only_in_src:
        dir_filesrc = str(src + dirs[0] + dirs[2])
        pathdst = str(dst + dirs[0])
        try:
            shutil.copy2(dir_filesrc, pathdst)
            current_datetime = str(datetime.now())
            l = (current_datetime + ':  Копирование файла: ' + dir_filesrc)
            log.append(l)
            print(l)
        except:
            pass


def remove_file():
    for dirs in time_file_only_in_dst:
        pathfile  = str(dst + dirs[0] + dirs[2])
        try:
            os.remove(pathfile)
            current_datetime = str(datetime.now())
            l = (current_datetime + ':  Удаление файла: ' + pathfile)
            log.append(l)
            print(l)
        except:
            pass


def remove_catalogs():
    for dirs in path_only_in_dst:
        try:
            path = str(dst + dirs)
            os.rmdir(path)
            current_datetime = str(datetime.now())
            l = (current_datetime + ':  Удаление каталога: ' + path)
            log.append(l)
            print(l)
        except:
            pass


def clear_all_list():
    only_all_catalogs_src[:] = []
    only_all_catalogs_src_without_root[:] = []
    path_file_src[:] = []
    path_time_file_src[:] = []

    only_all_catalogs_dst[:] = []
    only_all_catalogs_dst_without_root[:] = []
    path_file_dst[:] = []
    path_time_file_dst[:] = []

    time_file_only_in_src[:] = []
    time_file_only_in_dst[:] = []

    path_only_in_dst[:] = []

    log[:] = []

def per_sinc():
    p = """
    Вас приветствует программа синхронизации каталогов,
    пожалуйста следуйте следующим инструкциям
    ______________________________________________________________
    Пожалуйста введите частоту синхронизации которая вас устроит.
    Если вы хотите синхронизировать каталог по минутам введите 'min',
    если хотите синхронизировать по часам введите 'hour'
    """
    print(p)
    global lot_time
    condition = False
    hour = "hour"
    minutes = "min"
    lot_time = int()
    while condition == False:
        print("Введите ваш выбор")
        i = (input())
        if i == minutes:
            print("Вы выбрали минуты отлично")
            print(
                "Теперь пожалуйста введите как часто вы хотите совершать синхронизацию введите кол-во минут (цифрами)")
            lot_min = int(input())
            print("Отлично синхронизация будет происходить каждые", lot_min, "минут")
            inner_lot = lot_min * 60
            lot_time = int(inner_lot)
            condition = True
        elif i == hour:
            print("Вы выбрали часы отлично")
            print(
                "Теперь пожалуйста введите как часто вы хотите совершать синхронизацию введите кол-во часов (цифрами)")
            lot_hour = int(input())
            print("Отлично синхронизация будет происходить каждые", lot_hour, "часов")
            inner_lot = lot_hour * 60 * 60
            lot_time = int(inner_lot)
            condition = True
        else:
            condition = False
            print("Это не верное значение введите предложанные данные")
            continue

def choice_catalogs():
    p1 = """
    Пожалуйста введите полный путь до корневого каталога откуда выгружать данные 
    по следующему шаблону: /home/folder/еще папка/конечный каталог/
    """
    p2 = """
        Пожалуйста введите полный путь до корневого каталога куда выгружать данные 
        по следующему шаблону: /home/folder/еще папка/конечный каталог/
        """
    p3 = """
            Пожалуйста введите полный путь до корневого каталога куда сохранять файл логов 
            по следующему шаблону: /home/folder/еще папка/конечный каталог/
            """
    print(p1)
    path_src = input()
    print(p2)
    path_dst = input()
    print(p3)
    path_log_int = input()
    global src
    global dst
    global path_log
    src = path_src
    dst = path_dst
    path_log = path_log_int


def logging():
    log_p_f = path_log + 'logFile.txt'
    f = open( log_p_f, 'a' )
    for item in log: f.write("%s\n" % item)
    f.close()


def main_func():
    i = 0
    while True :
        # Для начала получаем данные фалов и каталогов src и dst
        scraping_files_catalogs_of_src()
        scraping_files_catalogs_of_dst()

        # Далее пытаемся создать необходимые каталоги в dst если они еще не созданы и
        # формируем списки различий директорий для копирования и удаления файлов
        create_catalog_in_dst()
        compare_changing()

        # Удаляем и копируем файлы и директории
        remove_file()
        remove_catalogs()
        copy_files()

        logging()
        # Отчищаем списки перед следующим циклом
        clear_all_list()
        i += 1

        print("Цикл №", i)



        time.sleep(lot_time)


per_sinc()
choice_catalogs()
main_func()
