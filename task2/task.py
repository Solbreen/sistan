from typing import List, Tuple
import math

def task(s: str, e: str) -> Tuple[float, float]:
    s = s.replace('\\n', '\n')
    edges = []
    for line in s.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(',')
        if len(parts) != 2:
            continue
        u, v = parts[0].strip(), parts[1].strip()
        if u and v:
            edges.append((u, v))
    
    nodes = set()
    for u, v in edges:
        nodes.add(u)
        nodes.add(v)
    if e not in nodes:
        nodes.add(e)

    sorted_nodes = sorted(nodes, key=lambda x: int(x))
    n = len(sorted_nodes)
    node_to_index = {node: idx for idx, node in enumerate(sorted_nodes)}
    
    r1 = [[False] * n for _ in range(n)]
    r2 = [[False] * n for _ in range(n)]
    r3 = [[False] * n for _ in range(n)]
    r4 = [[False] * n for _ in range(n)]
    r5 = [[False] * n for _ in range(n)]
    
    children_map = {}
    for u, v in edges:
        i, j = node_to_index[u], node_to_index[v]
        r1[i][j] = True
        r2[j][i] = True
        if u not in children_map:
            children_map[u] = []
        children_map[u].append(v)
    
    def dfs(start: int, visited: List[bool], adj_matrix: List[List[bool]]):
        stack = [start]
        while stack:
            node = stack.pop()
            for neighbor in range(n):
                if adj_matrix[node][neighbor] and not visited[neighbor]:
                    visited[neighbor] = True
                    stack.append(neighbor)
    
    reachable = [[False] * n for _ in range(n)]
    for i in range(n):
        visited = [False] * n
        dfs(i, visited, r1)
        reachable[i] = visited[:]
    
    for i in range(n):
        for j in range(n):
            if i != j:
                if reachable[i][j] and not r1[i][j]:
                    r3[i][j] = True
                if reachable[j][i] and not r2[i][j]:
                    r4[i][j] = True
    
    for parent, children in children_map.items():
        if len(children) > 1:
            child_indices = [node_to_index[child] for child in children]
            for i in range(len(child_indices)):
                for j in range(i + 1, len(child_indices)):
                    idx1, idx2 = child_indices[i], child_indices[j]
                    r5[idx1][idx2] = True
                    r5[idx2][idx1] = True
    
    relation_matrices = [r1, r2, r3, r4, r5]
    k = len(relation_matrices)
    
    l_matrix = []
    
    for j in range(n):
        l_row = []
        for relation_matrix in relation_matrices:
            l_ij = sum(1 for i in range(n) if relation_matrix[j][i])
            l_row.append(l_ij)
        l_matrix.append(l_row)
    
    max_connections = n - 1
    total_entropy = 0.0
    
    for j in range(n):
        for i in range(k):
            l_ij = l_matrix[j][i]
            if l_ij > 0:
                P = l_ij / max_connections
                H = -P * math.log2(P)
                total_entropy += H
    
    H_MR = total_entropy
    c = 1 / (math.e * math.log(2))
    H_ref = c * n * k
    h_MR = H_MR / H_ref
    H_MR_rounded = round(H_MR, 1)
    h_MR_rounded = round(h_MR, 1)
    
    return (H_MR_rounded, h_MR_rounded)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        csv_data = sys.argv[1]
        result = task(csv_data, "1")
        print(f"Энтропия структуры: {result[0]}")
        print(f"Нормированная сложность: {result[1]}")