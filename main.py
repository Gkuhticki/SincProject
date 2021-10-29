import datetime
import os
import shutil
import time
from datetime import datetime


# Каталоги и деревья каталогов.
src = "/home/georg/my_projects/Test/src/"
dst = "/home/georg/my_projects/Test/dst/"

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
    for (root, dirs, files) in tree_src:
        inner_tempfiles = []
        inner_temp_path = []
        inner_tempdict_file_path = []

        only_all_catalogs_src.append(root)
        only_all_catalogs_src_without_root.append(root.strip(src))

        # записываем во временный словарь путь до файла без src, и отдельно записываем файлы в этой директории
        # это нужно для того что бы позже сформировать конечный список по шаблону [ПУТЬ, ФАЙЛ], [ПУТЬ, ФАЙЛ]
        inner_temp_path.append(root.strip(src))
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
    tree_dst = os.walk(dst, topdown=True)
    for (root, dirs, files) in tree_dst:
        inner_tempfiles = []
        inner_temp_path = []
        inner_tempdict_file_path = []

        only_all_catalogs_dst.append(root)
        only_all_catalogs_dst_without_root.append(root.strip(dst))

        # записываем во временный словарь путь до файла без dst, и отдельно записываем файлы в этой директории
        # это нужно для того что бы позже сформировать конечный список по шаблону [ПУТЬ, ФАЙЛ], [ПУТЬ, ФАЙЛ]
        inner_temp_path.append(root.strip(dst))
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
        print (dirs)
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

        # Отчищаем списки перед следующим циклом
        clear_all_list()
        i +=  1

        print("Цикл №", i)
        for i in log:
            print(i)


        time.sleep(600)
main_func()
