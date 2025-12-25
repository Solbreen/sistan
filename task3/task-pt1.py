import json

def process_json_files(filenameA, filenameB) -> tuple:
    try:
        with open(filenameA, 'r', encoding='utf-8') as file:
            dataA = json.load(file)
        with open(filenameB, 'r', encoding='utf-8') as file:
            dataB = json.load(file)
        return dataA, dataB
    
    except Exception as e:
        print(f"Ошибка: {e}")
        return None, None      
    


def main(a: list, b: list):
    print(f"Исходные данные A: {a}")
    print(f"Исходные данные B: {b}")
    print("\n")

    order = []
    for item in a:
        if isinstance(item, list):
            order.extend(item)
        else:
            order.append(item)
    
    dictA = {x: 0 for x in order}
    dictB = {x: 0 for x in order}
    for i, val in enumerate(a):
        if isinstance(val, list):
            for j in val:
                dictA[j] = i
        else:
            dictA[val] = i
    for i, val in enumerate(b):
        if isinstance(val, list):
            for j in val:
                dictB[j] = i
        else:
            dictB[val] = i

    matrixAB = []
    for row in order:
        temprowAB = []
        for col in order:
            aij = 0 if dictA[col] < dictA[row] else 1
            bij = 0 if dictB[col] < dictB[row] else 1
            temprowAB.append(aij * bij)
        matrixAB.append(temprowAB)

    matrixABT = list(map(list, zip(*matrixAB)))

    finalMatrix = [[a or b for a, b in zip(row1, row2)] for row1, row2 in zip(matrixAB, matrixABT)]

    result = []
    for i, row in enumerate(finalMatrix):
        tempr = [order[i]]
        yes = []
        for j, val in enumerate(row):
            if val == 0:
                tempr.append(order[j])
        if len(tempr) > 1:
            if not any(any(item in sublist for item in tempr) for sublist in result):
                result.append(tempr)

    return json.dumps(result)

if __name__ == "__main__":
    '''
    Ведите в fullpathA и в fullpathB полные пути до ваших json файлов с ранжировкой.
    Если не заполнить, то можете ввести два списка с ранжировками в аргументы main().
    '''
    fullpathA = ""
    fullpathB = ""

    a, b = process_json_files(fullpathA, fullpathB)
    if a == None or b == None:
        a = ["T", ["K", "M"], "D", "Z"]
        b = [["T", "K"], "M", "Z", "D"]

    ah = [1, [2, 3], 4, [5, 6, 7], 8, 9, 10]
    bh = [3, [1, 4], 2, 6, [5, 7, 8], [9, 10]]

    result = main(a, b)
    print(f"Ядро противоречий для двух ранжировок: S(A, B) = {result}")