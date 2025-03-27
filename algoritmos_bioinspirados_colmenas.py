
import numpy as np
import matplotlib.pyplot as plt

# ===================== Fitness Function (Regresión) =====================
def fitness(sol):
    ET, RH, HT, HH, WS = sol
    return 264.54 + (0.99 * ET) - (4.55 * RH) + (0.67 * HT) + (0.98 * HH) - (0.57 * WS)

# ===================== Genetic Algorithm =====================
def run_ga():
    from pygad import GA

    gene_space = [
        {'low': 18, 'high': 35},  # ET
        {'low': 50, 'high': 80},  # RH
        {'low': 25, 'high': 38},  # HT
        {'low': 50, 'high': 75},  # HH
        {'low': 0, 'high': 15},   # WS
    ]

    ga = GA(num_generations=200, num_parents_mating=10,
            fitness_func=lambda s, _: fitness(s),
            sol_per_pop=20, num_genes=5, gene_space=gene_space,
            parent_selection_type="rank",
            crossover_type="single_point",
            mutation_type="random",
            mutation_percent_genes=20)

    ga.run()
    return ga.best_solution()[0], ga.best_solution()[1]

# ===================== Ant Colony Optimization =====================
def run_aco(n_ants=20, iterations=100, alpha=1.0, beta=2.0, rho=0.5):
    ranges = [(18, 35), (50, 80), (25, 38), (50, 75), (0, 15)]
    num_params = len(ranges)
    pheromones = np.ones((num_params, 100))

    def discretize(val, p):
        low, high = ranges[p]
        return low + val * (high - low)

    best_score = -np.inf
    best_sol = None

    for _ in range(iterations):
        solutions = []
        scores = []
        for _ in range(n_ants):
            sol = []
            for p in range(num_params):
                idx = np.random.randint(0, 100)
                val = idx / 99.0
                sol.append(discretize(val, p))
            score = fitness(sol)
            solutions.append(sol)
            scores.append(score)

            if score > best_score:
                best_score = score
                best_sol = sol

        # Update pheromones
        pheromones *= (1 - rho)
        for i, sol in enumerate(solutions):
            for p in range(num_params):
                idx = int((sol[p] - ranges[p][0]) / (ranges[p][1] - ranges[p][0]) * 99)
                pheromones[p][idx] += scores[i] / max(scores)

    return best_sol, best_score

# ===================== Bee Colony Optimization =====================
def run_bco(num_bees=30, elite_bees=5, iterations=100):
    ranges = [(18, 35), (50, 80), (25, 38), (50, 75), (0, 15)]

    def random_solution():
        return [np.random.uniform(low, high) for (low, high) in ranges]

    def neighborhood(sol, radius=0.05):
        return [np.clip(sol[i] + np.random.uniform(-1, 1) * radius * (ranges[i][1] - ranges[i][0]), ranges[i][0], ranges[i][1])
                for i in range(len(sol))]

    population = [random_solution() for _ in range(num_bees)]
    best_score = -np.inf
    best_sol = None

    for _ in range(iterations):
        scores = [fitness(sol) for sol in population]
        elite_idx = np.argsort(scores)[-elite_bees:]
        new_population = []

        for i in elite_idx:
            elite_sol = population[i]
            new_population.append(elite_sol)
            for _ in range(int(num_bees / elite_bees) - 1):
                new_population.append(neighborhood(elite_sol))

        population = new_population[:num_bees]
        for sol in population:
            score = fitness(sol)
            if score > best_score:
                best_score = score
                best_sol = sol

    return best_sol, best_score

# ===================== Comparación =====================
if __name__ == "__main__":
    print("Ejecutando Algoritmo Genético...")
    ga_sol, ga_score = run_ga()
    print(f"GA -> Producción: {ga_score:.2f} kg")

    print("\n Ejecutando Algoritmo de Hormigas...")
    aco_sol, aco_score = run_aco()
    print(f"ACO -> Producción: {aco_score:.2f} kg")

    print("\nEjecutando Algoritmo de Abejas...")
    bco_sol, bco_score = run_bco()
    print(f"BCO -> Producción: {bco_score:.2f} kg")

    # Mostrar comparación
    labels = ['GA', 'ACO', 'BCO']
    values = [ga_score, aco_score, bco_score]
    plt.bar(labels, values)
    plt.ylabel("Producción de Miel (kg)")
    plt.title("Comparación de Algoritmos Bioinspirados")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
