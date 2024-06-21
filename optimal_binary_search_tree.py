class OptimalBST:
    def __init__(self, p, q, words):
        self.n = len(p)
        self.e = [[0] * (self.n + 1) for _ in range(self.n + 1)]
        self.w = [[0] * (self.n + 1) for _ in range(self.n + 1)]
        self.root = [[0] * (self.n + 1) for _ in range(self.n + 1)]
        self.p = p
        self.q = q
        self.optional_bst_create()
        self.words = words

    def optional_bst_create(self):
        for i in range(1, self.n + 2):
            self.e[i - 1][i - 1] = self.q[i - 1]
            self.w[i - 1][i - 1] = self.q[i - 1]
        for l in range(1, self.n + 1):
            for i in range(1, self.n - l + 2):
                j = i + l - 1
                self.e[i - 1][j] = float('inf')
                self.w[i - 1][j] = self.w[i - 1][j - 1] + self.p[j - 1] + self.q[j]
                for r in range(i, j + 1):
                    t = self.e[i - 1][r - 1] + self.e[r][j] + self.w[i - 1][j]
                    if t < self.e[i - 1][j]:
                        self.e[i - 1][j] = t
                        self.root[i - 1][j] = r


    def treeCost(self):
        return self.e[0][self.n]


    def pocet_porovnani(self, word, i=0, j=None, parent=None, path=None):
        if j is None:
            j = self.n
        if parent is None:
            parent = 0
        if path is None:
            path = []
        root = self.root[i][j]
        if root == 0:
            print(f"Slovo '{word}' nebolo najdene.")
            return 0

        path.append(self.words[root - 1])

        if self.words[root - 1] == word:
            if path:
                print("Cesta :", "---".join(path))
            return 1

        if word < self.words[root - 1]:
            if root - 1 >= i:
                comparisons = self.pocet_porovnani(word, i, root - 1, root, path)
            else:
                comparisons = 0
        else:
            if root <= j:
                comparisons = self.pocet_porovnani(word, root, j, root, path)
            else:
                comparisons = 0

        return 1 + comparisons

def read_dictionary_file(filename):
    words = []
    all_frequencies = []
    with open(filename, 'r') as file:
        for line in file:
            frequency, word = line.split()
            frequency = int(frequency)
            words.append(word)
            all_frequencies.append(frequency)

    sorted_indices = sorted(range(len(words)), key=lambda i: words[i])
    words = [words[i] for i in sorted_indices]
    all_frequencies = [all_frequencies[i] for i in sorted_indices]

    return words, all_frequencies


def probability_key(all_frequencies, indices_greater_than_50000, total_frequency):
    ratios = []
    for idx in indices_greater_than_50000:
        ratio = all_frequencies[idx] / total_frequency
        ratios.append(ratio)
    return ratios


def key_dict(indices_greater_than_50000, words):
    ratios = []
    for idx in indices_greater_than_50000:
        ratio = words[idx]
        ratios.append(ratio)
    return ratios

def probability_dummy(all_frequencies, indices_greater_than_50000, total_frequency):
    probabilities = []
    num_indices = len(indices_greater_than_50000)

    if indices_greater_than_50000[0] == 0:
        probabilities.append(0.0)
    else:
        freq_sum = sum(all_frequencies[:indices_greater_than_50000[0]])
        probability = freq_sum / total_frequency
        probabilities.append(probability)

    for i in range(num_indices - 1):
        left_index = indices_greater_than_50000[i]
        right_index = indices_greater_than_50000[i + 1]
        freq_sum = sum(all_frequencies[left_index + 1:right_index])
        probability = freq_sum / total_frequency
        probabilities.append(probability)

    if num_indices > 0:
        last_index = indices_greater_than_50000[-1]
        last_freq = sum(all_frequencies[last_index + 1:])
        last_probability = last_freq / total_frequency
        probabilities.append(last_probability)

    return probabilities


if __name__ == "__main__":
    dictionary_file = "dictionary.txt"
    words, all_frequencies = read_dictionary_file(dictionary_file)
    total_frequency = sum(all_frequencies)
    indices_greater_than_50000 = []
    for idx, freq in enumerate(all_frequencies):
        if freq > 50000:
            indices_greater_than_50000.append(idx)

    probapility_p = probability_key(all_frequencies, indices_greater_than_50000, total_frequency)
    print("Pravdepodobnost p:")
    print(probapility_p)
    total_prob_p = sum(probapility_p)

    probapility_q = probability_dummy(all_frequencies, indices_greater_than_50000, total_frequency)
    print("Pravdepodobnost q:")
    print(probapility_q)
    total_prob_q = sum(probapility_q)

    keys = key_dict(indices_greater_than_50000, words)
    print("Kluce")
    print(keys)

    bst = OptimalBST(probapility_p, probapility_q,keys)
    cost = bst.treeCost()
    print("Cost pre optimal BST: {:.2f}".format(cost))

    slovo = 'so'
    comparisons = bst.pocet_porovnani(slovo)
    print(f"Pocet porovnani pre slovo '{slovo}': {comparisons}")