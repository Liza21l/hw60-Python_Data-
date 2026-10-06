import csv


# Зчитування графа з CSV-файлу
def read_graph(filename):
    graph = {}

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            vertex = row["vertex"]

            if row["neighbors"]:
                neighbors = row["neighbors"].split(",")
            else:
                neighbors = []

            graph[vertex] = neighbors

    return graph


# DFS
def dfs(graph, vertex, visited):
    visited.add(vertex)

    for neighbor in graph.get(vertex, []):
        if neighbor not in visited:
            dfs(graph, neighbor, visited)


# Пошук зв'язних компонент
def find_components(graph):
    visited = set()
    components = []

    for vertex in graph:
        if vertex not in visited:
            component = set()

            dfs(graph, vertex, component)

            visited.update(component)
            components.append(component)

    return components


# Перевірка зв'язності
def check_connectivity(graph):
    components = find_components(graph)

    if len(components) == 1:
        print("Граф зв'язний.")
    else:
        print("Граф не зв'язний.")
        print("Зв'язні компоненти:")

        for i, component in enumerate(components, 1):
            print(i, ":", component)


# Пошук циклу за допомогою DFS
def find_cycle(graph):
    visited = set()
    path = []

    def dfs_cycle(vertex):
        visited.add(vertex)
        path.append(vertex)

        for neighbor in graph.get(vertex, []):

            if neighbor in path:
                index = path.index(neighbor)
                return path[index:] + [neighbor]

            if neighbor not in visited:
                result = dfs_cycle(neighbor)

                if result is not None:
                    return result

        path.pop()
        return None

    for vertex in graph:
        if vertex not in visited:
            result = dfs_cycle(vertex)

            if result is not None:
                return result

    return None


# Алгоритм Тар'яна
def find_scc_tarjan(graph):
    index = 0

    indices = {}
    low = {}

    stack = []
    on_stack = set()

    components = []

    def dfs_tarjan(vertex):
        nonlocal index

        # Записуємо номер вершини
        indices[vertex] = index
        low[vertex] = index
        index += 1

        stack.append(vertex)
        on_stack.add(vertex)

        for neighbor in graph.get(vertex, []):

            # Якщо вершину ще не відвідували
            if neighbor not in indices:
                dfs_tarjan(neighbor)

                low[vertex] = min(
                    low[vertex],
                    low[neighbor]
                )

            # Якщо вершина вже знаходиться у стеку
            elif neighbor in on_stack:
                low[vertex] = min(
                    low[vertex],
                    indices[neighbor]
                )

        # Якщо vertex є коренем компоненти
        if low[vertex] == indices[vertex]:

            component = []

            while True:
                node = stack.pop()
                on_stack.remove(node)

                component.append(node)

                if node == vertex:
                    break

            components.append(component)

    # Запускаємо DFS для всіх вершин
    for vertex in graph:
        if vertex not in indices:
            dfs_tarjan(vertex)

    return components


# Головне меню
def main():

    graph = read_graph("graph.csv")

    print("Граф:")
    for vertex in graph:
        print(vertex, "->", graph[vertex])

    while True:

        print("\n--- МЕНЮ ---")
        print("1 - Перевірити зв'язність")
        print("2 - Знайти цикл")
        print("3 - Знайти компоненти сильної зв'язності")
        print("0 - Вихід")

        choice = input("Виберіть операцію: ")

        if choice == "1":

            check_connectivity(graph)

        elif choice == "2":

            cycle = find_cycle(graph)

            if cycle:
                print("Цикл знайдено:")
                print(" -> ".join(cycle))
            else:
                print("Циклів немає.")

        elif choice == "3":

            components = find_scc_tarjan(graph)

            print("Компоненти сильної зв'язності:")

            for i, component in enumerate(components, 1):
                print(i, ":", component)

        elif choice == "0":

            print("Програму завершено.")
            break

        else:

            print("Неправильний вибір.")


main()