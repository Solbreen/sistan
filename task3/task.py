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


def task(a: list, b: list):

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

    core = []
    matrixC = matrixAB
    for i, row in enumerate(finalMatrix):
        tempr = [order[i]]
        for j, val in enumerate(row):
            if val == 0:
                tempr.append(order[j])
                matrixC[i][j] = 1
        if len(tempr) > 1:
            if not any(any(item in sublist for item in tempr) for sublist in core):
                core.append(tempr)

    matrixCT = list(map(list, zip(*matrixC)))

    matrixE = matrixC
    for i, row in enumerate(matrixC):
        for j, _ in enumerate(row):
            matrixE[i][j] = matrixC[i][j] * matrixCT[i][j]

    matrixES = matrixE
    n = len(order)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                matrixES[i][j] = matrixES[i][j] or (matrixES[i][k] and matrixES[k][j])

    visited = [False] * n
    components = []
    for i in range(n):
        if not visited[i]:
            component = [order[i]]
            visited[i] = True
            for j in range(i + 1, n):
                if not visited[j]:
                    if matrixES[i][j] == 1 and matrixES[j][i] == 1:
                        component.append(order[j])
                        visited[j] = True
            
            components.append(component)

    n_clusters = len(components)
    representatives = [cluster[0] for cluster in components]
    
    pos_in_B = {}
    for obj in order:
        pos_in_B[obj] = dictB[obj]
    cluster_indices = list(range(n_clusters))
    cluster_indices.sort(key=lambda idx: pos_in_B[representatives[idx]])
    
    final_ranking = []
    for cluster_idx in cluster_indices:
        cluster = components[cluster_idx]
        if len(cluster) == 1:
            final_ranking.append(cluster[0])
        else:
            final_ranking.append(sorted(cluster))

    return json.dumps(final_ranking, ensure_ascii=False)



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

    result = task(ah, bh)
    print(f"Согласованная кластерная ранжировка: f(A, B) = {result}")
    result = main(ah, bh)
    print(f"Ядро противоречий для двух ранжировок: S(A, B) = {result}")