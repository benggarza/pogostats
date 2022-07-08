def sorting(request_args, table, columns):
    order = []
    i = 0
    while True:
        col_index = request_args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request_args.get(f'columns[{col_index}][data]')
        if col_name not in columns:
            col_name = 'name'
        descending = request_args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(table, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    return order