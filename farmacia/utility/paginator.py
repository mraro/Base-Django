from django.core.paginator import Paginator


def make_paginations(request, obj, qty_pages):

    current_page = int(request.GET.get('page', 1))
    pagination = Paginator(obj, 9)
    medicines_page = pagination.get_page(current_page)
    len_pages = pagination.page_range

    middle_range = int(qty_pages / 2)
    start_range = current_page - middle_range
    stop_range = current_page + middle_range
    last_range = len(len_pages)

    start_range_offset = abs(start_range) if start_range < 0 else 0  # abs tira o sinal de negativo

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    if stop_range >= last_range:
        start_range = start_range - abs(last_range - stop_range)

    if last_range < current_page:
        current_page = last_range

    pagination = len_pages[start_range:stop_range]  # valorMenor:range:valorMaior
    return {
        'pagination': pagination,
        'middle_range': middle_range,
        'start_range': start_range,
        'stop_range': stop_range,
        'last_range': last_range,
        'first_page_out_of_range': current_page > middle_range,
        'last_page_out_of_range': current_page < last_range,
        'current_page': current_page,
        'medicines_page': medicines_page,
    }
