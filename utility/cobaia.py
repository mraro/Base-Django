# import ctypes
# import os
# import platform
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
# free_space = get_free_space_mb("H:/")
# print('in MB {:.2f}'.format(free_space / 1048576))
# print('in GB {:.2f}'.format(free_space / 1073741824 ))
# print(f'in TB {free_space}')
# letras = os.scandir('/')
# print(dir(letras))
# for x in letras:
#     print(x)
#
# import pywhatkit as whats
#
# number = '+5511945950834'
# whats.sendwhatmsg(
#     number,
#     'OSSO',11,20
# )


if __name__ == '__main__':
    x = int(2)
    y = int(2)
    z = int(2)
    n = int(3)
    lista = [x, y, z]
    [xx , yy , zz] = 0 , 0, 0
    # result = []
    # [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [0, 1, 2], [0, 2, 1], [0, 2, 2], [1, 0, 0], [1, 0, 2], [1, 1, 1],
    # [1, 1, 2], [1, 2, 0], [1, 2, 1], [1, 2, 2], [2, 0, 1], [2, 0, 2], [2, 1, 0], [2, 1, 1], [2, 1, 2], [2, 2, 0],
    # [2, 2, 1], [2, 2, 2]]

    # for xx in range(x + 1):
    #     result.append([0, 0, xx])

    result = [[xx, yy, zz] for xx in range(x+1) for yy in range(y+1) for zz in range(z+1) if sum([xx, yy, zz]) != n]

    print(result)
