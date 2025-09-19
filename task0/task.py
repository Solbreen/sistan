import csv
from io import StringIO

def matrixPrint(matrix):
    for row in matrix:
        print(row)

def main(csv_bytes):
    # Декодируем байтовую строку в обычную строку
    csv_string = csv_bytes.decode('utf-8')
    
    # Заменяем escaped \n на настоящие переносы строк
    csv_string = csv_string.replace('\\n', '\n')
    
    # Читаем CSV из строки
    reader = csv.reader(StringIO(csv_string.strip()))
    
    edges = []
    vertices = set()
    
    # Обрабатываем каждую строку данных
    for row in reader:
        if len(row) < 2:
            continue
        # Извлекаем номера вершин из первого и второго столбцов
        u = int(row[0].strip())
        v = int(row[1].strip())
        edges.append((u, v))
        vertices.update([u, v])
    
    # Сортируем вершины для consistent порядка
    vertices = sorted(vertices)
    n = len(vertices)
    
    # Создаём mapping из вершины в индекс
    vertex_to_index = {vertex: idx for idx, vertex in enumerate(vertices)}
    
    # Инициализируем матрицу смежности нулями
    adjacency_matrix = [[0] * n for _ in range(n)]
    
    # Заполняем матрицу смежности
    for u, v in edges:
        i = vertex_to_index[u]
        j = vertex_to_index[v]
        adjacency_matrix[i][j] = 1
        adjacency_matrix[j][i] = 1  # Граф неориентированный
    
    return adjacency_matrix

if __name__ == "__main__":
    # Пример вызова с байтовой строкой
    import sys
    
    if len(sys.argv) > 1:
        # Получаем CSV данные из аргумента командной строки как байтовую строку
        csv_data = sys.argv[1].encode('utf-8')
        result = main(csv_data)
        matrixPrint(result)
