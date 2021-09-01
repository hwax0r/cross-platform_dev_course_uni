"""
Created on Wed 1 Sep 11:05

@author: Sergeev David Evgenievich
Group: IVT-41-18
"""

import os
import shutil
import time


HASH_BASE: int = 28657
HASH_MOD: int = 100000

# path separator depends on OS
SEPARATOR: chr = os.sep


def timeit(f):
    def timed(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()
        print(f'func: {f.__name__} took: {te-ts:2.4f} sec')
        return result
    return timed


def hash_(to_be_processed: str, base: int, mod: int):
    hash_calc = 0
    for char in to_be_processed:
        symbol: int = ord(char)
        hash_calc = (hash_calc * base % mod + symbol) % mod
    return hash_calc


@timeit
def my_solution(target_directory: str):
    """
    Заданием предусмотрено разрешение коллизий названий файлов
    добавлением к началу названия файла соответствующую папку,
    в которой он находится, а также папки уровней выше вплоть
    до указанной пользователем директории.
    Коллизии - файлы с одинаковым названием

    Однако, есть ограничение на длину названия файла, это 260 символов.
    В таком случае предлагаю разрешать вложенность с помощью
    хэширования названия пути и добавления хэша в начало названия файла.
    Таким образом, в случае необходимости,пользователь сможет найти
    оригинальный путь файла в хэш-таблице или сгенерированном файле.
    """

    roots = dict()

    for current_path, folders, files in os.walk(target_directory):
        for file in files:
            # чистка от системных файлов
            file_name, file_extension = os.path.splitext(file)
            if file_name == '.DS_Store' or file_extension == '.DS_Store':
                continue

            local_path = current_path[:len(target_directory)]

            # перенос файла из директории файла в исходную
            # выполняется, если файл не в исходной директории
            if local_path != '':
                path_to_file: int = hash_(current_path[len(target_directory):], HASH_BASE, HASH_MOD)
                if path_to_file == 0:
                    continue
                if path_to_file not in roots.keys():
                    roots.update({path_to_file: current_path[len(target_directory):] + SEPARATOR})

                new_filename = f'{path_to_file}_{file}'
                shutil.move(f'{current_path}{SEPARATOR}{file}', f'{target_directory}{SEPARATOR}{new_filename}')

    # удаление папок в целевой директории
    target_directory_subfolders = [folder.path for folder in os.scandir(target_directory) if folder.is_dir()]
    for folder_path in target_directory_subfolders:
        shutil.rmtree(folder_path)

    # отчёт о ключах, кодирующих путь файлов
    roots_report = open(f'{target_directory}{SEPARATOR}work_report.txt', 'a')
    for key, value in sorted(roots.items()):
        print("{}: {}".format(key, value), file=roots_report)


@timeit
def recommended_solution(target_directory: str):
    for current_path, folders, files in os.walk(target_directory):
        for file in files:
            # чистка от системных файлов
            file_name, file_extension = os.path.splitext(file)
            if file_name == '.DS_Store' or file_extension == '.DS_Store':
                continue

            local_path = current_path[len(target_directory):]

            # перенос файла из директории файла в исходную
            # выполняется, если файл не в исходной директории
            if local_path != '':
                local_path = local_path.replace(SEPARATOR, '_')
                new_filename = f'{local_path}_{file}'
                shutil.move(f'{current_path}{SEPARATOR}{file}', f'{target_directory}{SEPARATOR}{new_filename}')

    # удаление папок в целевой директории
    target_directory_subfolders = [folder.path for folder in os.scandir(target_directory) if folder.is_dir()]
    for folder_path in target_directory_subfolders:
        shutil.rmtree(folder_path)


def main():
    target_dir: str = f'{os.getcwd()}{SEPARATOR}my_solution'
    my_solution(target_directory=target_dir)  # result in ./my_solution

    target_dir: str = f'{os.getcwd()}{SEPARATOR}recommended_solution'
    recommended_solution(target_directory=target_dir)  # result in ./recommended_solution


if __name__ == '__main__':
    main()
