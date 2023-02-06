# import ctypes
# import os
# import platform
# import subprocess
# import sys
# import win32api
#
# def get_free_space_mb(dirname):
#     """Return folder/drive free space (in megabytes)."""
#     if platform.system() == 'Windows':
#         free_bytes = ctypes.c_ulonglong(0)
#         ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dirname), None, None, ctypes.pointer(free_bytes))
#         return free_bytes.value
#     else:
#         st = os.statvfs(dirname)
#         return st.f_bavail * st.f_frsize / 1024 / 1024
#
#
# def make_space_used(directory):
#     """
#     Esta função analisa o espaço usado na pasta passada como parâmetro.
#     :param directory: O diretório que deve ser analisado
#     :return: O espaço usado na pasta, em bytes
#     """
#     # Aqui, usamos o comando 'dir' para obter o tamanho da pasta
#     dir_command = 'dir ' + directory + ' /A-D /-C /S'
#     dir_output = subprocess.check_output(dir_command, shell=True)
#
#     # Separando os resultados para obter o espaço usado
#     dir_output = dir_output.decode().split()
#
#     # Obtendo o índice da palavra "bytes" para achar o tamanho
#     byte_index = dir_output.index('bytes') - 1
#
#     # Retornando o espaço usado
#     return int(dir_output[byte_index])
#
# letras = os.scandir('H:')
# print(make_space_used('/'))
# for x in letras:
#     print("H:/"+ x.name)
#     free_space = get_free_space_mb("H:/"+ x.name)
#     print('in GB {:.2f}'.format(free_space / 1073741824))
#
# # print('in MB {:.2f}'.format(free_space / 1048576))
# # print(f'in TB {free_space}')
#
# #
# # import pywhatkit as whats
# #
# # number = '+5511945950834'
# # whats.sendwhatmsg(
# #     number,
# #     'OSSO',11,20
# # )
#
#
#
