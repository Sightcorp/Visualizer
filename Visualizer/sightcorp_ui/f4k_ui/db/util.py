import collections

def add_stacked_counts(toAdd, result):
    if not toAdd:
        return result
    elif not result:
        return toAdd
    filter_values = []
    for x in toAdd:
        filter_values.append(float(x[0]))
    for pair in result:
        if pair[0] in filter_values:
            for sublist in toAdd:
                if float(sublist[0]) == pair[0]:
                    pair[1] = pair[1] + sublist[1]
    else:
        pair[1] = pair[1]
    return result


def add_counts_multicol(a, b):
    if not a:
        return b
    elif not b:
        return a
    t = collections.deque()
    i = 0
    j = 0
    la = len(a)
    lb = len(b)
    while i < la or j < lb:
        if i >= la and j < lb:
            t.append(b[j])
            j += 1
        elif i < la and j >= lb:
            t.append(a[i])
            i += 1
        else:
            if a[i][0] < b[j][0]:
                t.append(a[i])
                i += 1
            elif a[i][0] == b[j][0]:
                sum_ab = [a[i][x] + b[j][x] for x in range(1, len(a[i]))]
                tmp = [a[i][0]]
                tmp.extend(sum_ab)
                t.append(tmp)
                i += 1
                j += 1
            else:
                t.append(b[j])
                j += 1
    return list(t)


def safe_division(a, b):
    if not b:
        return 0
    else:
        return round(a / b, 1)

def set_selected_value(counts, selected_values):
    # set to 1 if the key is a filter value
    return [[c[0], c[1], int(c[0] in selected_values)] for c in counts]