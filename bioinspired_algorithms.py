
import numpy as np  # Import required libraries
import matplotlib.pyplot as plt  # Import required libraries

# ===================== Fitness Function (Regression) =====================
def fitness(sol):  # Define fitness function for the optimization (regression model)
    ET, RH, HT, HH, WS = sol
    return 264.54 + (0.99 * ET) - (4.55 * RH) + (0.67 * HT) + (0.98 * HH) - (0.57 * WS)

# ===================== Genetic Algorithm =====================
def run_ga():  # Function to run Genetic Algorithm (GA)
    from pygad import GA

    # Define the gene space for each variable
    gene_space = [  # Define the ranges for each gene (parameter)
        {'low': 18, 'high': 35},  # ET
        {'low': 50, 'high': 80},  # RH
        {'low': 25, 'high': 38},  # HT
        {'low': 50, 'high': 75},  # HH
        {'low': 0, 'high': 15},   # WS
    ]

    # Initialize the Genetic Algorithm
    ga = GA(num_generations=200, num_parents_mating=10,  # Initialize Genetic Algorithm with parameters
            fitness_func=lambda s, _: fitness(s),
            sol_per_pop=20, num_genes=5, gene_space=gene_space,
            parent_selection_type="rank",
            crossover_type="single_point",
            mutation_type="random",
            mutation_percent_genes=20)

    ga.run()  # Run the Genetic Algorithm process
    return ga.best_solution()[0], ga.best_solution()[1]  # Return the best solution and its fitness score from GA

# ===================== Ant Colony Optimization =====================
def run_aco(n_ants=20, iterations=100, alpha=1.0, beta=2.0, rho=0.5):  # Function to run Ant Colony Optimization (ACO)
    # Define parameter ranges
    ranges = [(18, 35), (50, 80), (25, 38), (50, 75), (0, 15)]  # Define parameter ranges for optimization
    num_params = len(ranges)
    pheromones = np.ones((num_params, 100))  # Initialize pheromone levels  # Initialize pheromone matrix for ACO

    def discretize(val, p):  # Function to map discrete pheromone value to actual parameter range
        low, high = ranges[p]
        return low + val * (high - low)

    best_score = -np.inf
    best_sol = None

    for _ in range(iterations):  # Iterate through ACO optimization steps
        solutions = []  # Initialize list to store solutions
        scores = []  # Calculate fitness scores for bee population
        for _ in range(n_ants):
            sol = []  # Generate a new solution
            for p in range(num_params):
                idx = np.random.randint(0, 100)
                val = idx / 99.0
                sol.append(discretize(val, p))
            score = fitness(sol)  # Evaluate fitness of the generated solution
            solutions.append(sol)
            scores.append(score)

            if score > best_score:
                best_score = score
                best_sol = sol

        # Update pheromone trails
        pheromones *= (1 - rho)  # Evaporate pheromones
        for i, sol in enumerate(solutions):
            for p in range(num_params):
                idx = int((sol[p] - ranges[p][0]) / (ranges[p][1] - ranges[p][0]) * 99)
                pheromones[p][idx] += scores[i] / max(scores)  # Update pheromone based on solution quality

    return best_sol, best_score

# ===================== Bee Colony Optimization =====================
def run_bco(num_bees=30, elite_bees=5, iterations=100):  # Function to run Bee Colony Optimization (BCO)
    # Define parameter ranges
    ranges = [(18, 35), (50, 80), (25, 38), (50, 75), (0, 15)]  # Define parameter ranges for optimization

    def random_solution():  # Function to generate a random solution (BCO)
        return [np.random.uniform(low, high) for (low, high) in ranges]

    def neighborhood(sol, radius=0.05):  # Function to generate a neighboring solution around elite bees (BCO)
        return [np.clip(sol[i] + np.random.uniform(-1, 1) * radius * (ranges[i][1] - ranges[i][0]), ranges[i][0], ranges[i][1])
                for i in range(len(sol))]

    population = [random_solution() for _ in range(num_bees)]  # Initialize bee population
    best_score = -np.inf
    best_sol = None

    for _ in range(iterations):  # Iterate through ACO optimization steps
        scores = [fitness(sol) for sol in population]  # Calculate fitness scores for bee population
        elite_idx = np.argsort(scores)[-elite_bees:]  # Select elite bees based on scores
        new_population = []  # Generate new population based on elite solutions

        for i in elite_idx:
            elite_sol = population[i]
            new_population.append(elite_sol)
            for _ in range(int(num_bees / elite_bees) - 1):
                new_population.append(neighborhood(elite_sol))

        population = new_population[:num_bees]  # Initialize bee population
        for sol in population:  # Update best solution found
            score = fitness(sol)  # Evaluate fitness of the generated solution
            if score > best_score:
                best_score = score
                best_sol = sol

    return best_sol, best_score

# ===================== Comparison =====================
if __name__ == "__main__":  # Main execution block to compare algorithms
    print("Running Genetic Algorithm...")  # Print message: Running GA
    ga_sol, ga_score = run_ga()
    print(f"GA -> Production: {ga_score:.2f} kg")

    print("\nRunning Ant Colony Optimization Algorithm...")  # Print message: Running ACO
    aco_sol, aco_score = run_aco()
    print(f"ACO -> Production: {aco_score:.2f} kg")

    print("\nRunning Bee Colony Optimization Algorithm...")  # Print message: Running BCO
    bco_sol, bco_score = run_bco()
    print(f"BCO -> Production: {bco_score:.2f} kg")

    # Display comparison
    labels = ['GA', 'ACO', 'BCO']  # Labels for the bar chart comparison
    values = [ga_score, aco_score, bco_score]  # Values (fitness scores) for each algorithm
    plt.bar(labels, values)  # Plot bar chart to compare algorithms
    plt.ylabel("Honey Production (kg)")  # Label for y-axis
    plt.title("Comparison of Bio-inspired Algorithms")  # Title of the plot
    plt.grid(True)  # Add grid to the plot
    plt.tight_layout()  # Adjust layout to prevent overlap
    plt.show()  # Show the final plot
