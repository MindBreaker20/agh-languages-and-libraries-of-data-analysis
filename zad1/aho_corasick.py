'''
Author: Bartłomiej Jamiołkowski
Date: 28.10.2022
Topic: Aho-Corasick automaton
'''

# Budowanie automatu
def build(patterns):
    goto, fail_links, dictionary_links = {}, {}, {}
    tape = '#'.join(patterns)  # Taśma wzorów inspidowana tematyką maszyny Turinga
    parent, child = 0, 1  # Inicjalizacja pierwszego rodzica i potomka

    # Budowanie Goto - słownika słowników
    for i in range(len(tape)):
        if tape[i] != '#':
            if parent not in goto:
                goto[parent] = {tape[i]: child}  # Tworzenie zagnieżdżonego słownika przechowującego potomków rodzica
                parent = child
                child += 1
            else:
                if tape[i] in goto[parent]:
                    parent = goto[parent][tape[i]]  # Potomek staje się rodzicem dla swoich potomków
                else:
                    goto[parent][tape[i]] = child  # Aktualizacja słownika potomków danego rodzica
                    parent = child
                    child += 1
        else:
            parent = 0

    # Budowanie Failure links z użyciem algorytmu Breadth First Search
    visited_nodes, queue = [], []
    root_node = 0
    visited_nodes.append(root_node)
    queue.append(root_node)
    fail_links[0] = 0  # Przypisanie jokera do tej listy na potrzeby obliczeń

    while len(queue) > 0:
        node = queue[0]
        queue.pop(0)
        if node in goto.keys():
            for label, child in goto[node].items():
                if child not in visited_nodes:
                    queue.append(child)
                    visited_nodes.append(child)
                    if node == 0:  # Potomkowie korzenia mają fail linki do korzenia
                        fail_links[child] = 0
                    else:
                        parent_node = node  # Jedno cofnięcie się do rodzica
                        while True:  # Nieustanne poszukiwanie nowego fail linka
                            parent_node = fail_links[parent_node]  # Podążanie za fail linkiem
                            if parent_node == 0:
                                if label in goto[parent_node]:  # Jeśli z korzenia wychodzi etykieta
                                    fail_links[child] = goto[parent_node][label]
                                    break
                                else:  # Jesli z korzenia nie wychodzi etykieta
                                    fail_links[child] = 0
                                    break
                            else:
                                if parent_node in goto.keys():
                                    if label in goto[parent_node]:  # Fail link do potomka na wyższym szczeblu
                                        fail_links[child] = goto[parent_node][label]
                                        break

    # Budowanie Pattern nodes - słownik węzłów, gdzie kończą się podane wzorce
    pattern_nodes = {}
    global pattern_strings

    for pattern in pattern_strings:
        node = 0
        for i in range(len(pattern)):
            if pattern[i] in goto[node].keys():  # Jesli litera wzorca pokrywa się z etykietą wchodzącą węzła
                label = pattern[i]
                node = goto[node][label]
        pattern_nodes[node] = pattern_strings.index(pattern)  # Klucz to węzeł a wartość to indeks wzorca w liście

    # Budowanie Dictionary links
    for node, linked_node in fail_links.items():  # Przeszukiwanie fail linków
        for pattern_node in pattern_nodes.keys():  # Przeszukiwanie węzłów wzorca
            if linked_node == pattern_node:  # Jesli koniec fail linka jest węzłem wzorca to jest Dictionary link
                dictionary_links[node] = pattern_node

    return goto, fail_links, pattern_nodes, dictionary_links


# Szukanie wzorców w tekście
def search(goto, fail_links, pattern_nodes, dictionary_links, text):
    indexes = []
    node, counter = 0, 0
    text = text + "#"

    while text[counter] != '#':  # Obsługa goto, fail linków, dictionary links i etykiety z danej pozycji tekstu
        label = text[counter]

        if node in goto.keys():
            if label in goto[node].keys():
                node = goto[node][label]
            else:
                node = fail_links[node]
                continue
        else:
            node = fail_links[node]
            continue

        if node in pattern_nodes:  # Sprawdzenie czy sciezka w drzewie zawiera węzły wzorców
            idx = pattern_nodes[node]  # Wydobycie indeksu wzorca w liście wzorców
            pattern = pattern_strings[idx]  # wydobycie subtekstu z listy wzorców
            indexes.append(counter - len(pattern) + 1)  # Użycie dlugosci subtekstu do obliczenia indeksu

        if node in dictionary_links:  # Sprawdzenie czy sciezka w drzewie ma dictionary links (sub wzorce)
            idx1 = dictionary_links[node]  # Wydobycie numeru węzła sub wzorca
            idx2 = pattern_nodes[idx1]  # Wydobycie indeksu wzorca w liście wzorców
            pattern = pattern_strings[idx2]  # wydobycie subtekstu z listy wzorców
            indexes.append(counter - len(pattern) + 1)

        counter += 1

    indexes = list(set(indexes))  # Redukcja ewentualnych powtarzajacych sie indeksów
    return indexes


if __name__ == '__main__':
    while True:
        text_string = input("Enter your string: ")
        if text_string == "":
            break
        pattern_strings = []
        while True:
            your_pattern = input("Enter your pattern: ")
            if your_pattern == "":
                break
            else:
                pattern_strings.append(your_pattern)
        trie, f_links, p_nodes, d_links = build(pattern_strings)
        pattern_indexes = search(trie, f_links, p_nodes, d_links, text_string)
        print(pattern_indexes)
