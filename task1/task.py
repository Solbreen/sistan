from typing import List, Tuple

def main(s: str, e: str) -> Tuple[
    List[List[bool]],
    List[List[bool]], 
    List[List[bool]],
    List[List[bool]],
    List[List[bool]]
]:

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
    
    print(f"Узлы: {sorted_nodes}")
    print(f"Рёбра: {edges}")
    

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
    
    return (r1, r2, r3, r4, r5)


def print_matrices(result, nodes):
    matrices_names = ["r1 - непосредственное управление", 
                     "r2 - непосредственное подчинение", 
                     "r3 - опосредованное управление", 
                     "r4 - опосредованное подчинение", 
                     "r5 - соподчинение на одном уровне"]
    
    sorted_nodes = sorted(nodes, key=lambda x: int(x))
    
    for name, matrix in zip(matrices_names, result):
        print(f"\n{name}:")
        print("    " + "  ".join(f"{node:>2}" for node in sorted_nodes))
        for i, row in enumerate(matrix):
            row_str = "  ".join(" 1" if val else " 0" for val in row)
            print(f"{sorted_nodes[i]:>2} [{row_str}]")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        csv_data = sys.argv[1]
        result = main(csv_data, "1")
        n = len(result[0])
        nodes = [str(i + 1) for i in range(n)]
        
        print_matrices(result, nodes)