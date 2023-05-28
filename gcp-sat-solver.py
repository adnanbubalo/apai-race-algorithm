import sys
import random

def parse(benchmark_file):
    print(benchmark_file)
    clauses = []
    count = 0
    for line in open(benchmark_file):
        if line[0] == 'c':
            continue
        if line[0] == 'p':
            n_vars = int(line.split()[2])
            lit_clause = [[] for _ in range(n_vars * 2 + 1)]
            continue

        clause = []
        for literal in line[:-2].split():
            literal = int(literal)
            clause.append(literal)
            lit_clause[literal].append(count)
        clauses.append(clause)
        count += 1
    return clauses, n_vars, lit_clause

def get_random_interpretation(n_vars):
        return [i if random.random() < 0.5 else -i for i in range(n_vars + 1)]

def get_true_sat_lit(clauses, interpretation):
    true_sat_lit = [0 for _ in clauses]
    for index, clause in enumerate(clauses):
        for lit in clause:
            if interpretation[abs(lit)] == lit:
                true_sat_lit[index] += 1
    return true_sat_lit

def compute_broken_gs(clause, true_sat_lit, lit_clause):
    max_sat = -1
    best_literals = []
    for literal in clause:
        num_satisfied = sum([true_sat_lit[clause_index] for clause_index in lit_clause[literal]])

        if num_satisfied > max_sat:
            max_sat = num_satisfied
            best_literals = [literal]
        elif num_satisfied == max_sat:
            best_literals.append(literal)

    return random.choice(best_literals)

def update_tsl(literal_to_flip, true_sat_lit, lit_clause):
    for clause_index in lit_clause[literal_to_flip]:
        true_sat_lit[clause_index] += 1
    for clause_index in lit_clause[-literal_to_flip]:
        true_sat_lit[clause_index] -= 1

def run_sat(clauses, n_vars, lit_clause, max_flips_proportion = 4, max_tries = 100):
    max_flips = n_vars * max_flips_proportion
    max_score = len(clauses)
    best_interpretation = None
    
    for _ in range(max_tries):
        interpretation = get_random_interpretation(n_vars)
        true_sat_lit = get_true_sat_lit(clauses, interpretation) #value is true or false for each clause not the number of true literals
        score = sum(true_sat_lit)
        
        for _ in range(max_flips):
            unsatisfied_clauses_index = [index for index, true_lit in enumerate(true_sat_lit) if not true_lit]

            if not unsatisfied_clauses_index:
                return interpretation

            clause_index = random.choice(unsatisfied_clauses_index)
            unsatisfied_clause = clauses[clause_index]

            lit_to_flip = compute_broken_gs(unsatisfied_clause, true_sat_lit, lit_clause)

            update_tsl(lit_to_flip, true_sat_lit, lit_clause)
            interpretation[abs(lit_to_flip)] *= -1

            new_score = sum(true_sat_lit)

            if new_score == max_score:
                return interpretation

            if new_score > score:
                score = new_score
                if score == max_score:
                    return interpretation

        if best_interpretation is None or sum(get_true_sat_lit(clauses, best_interpretation)) < sum(true_sat_lit):
            best_interpretation = interpretation

    return best_interpretation

if __name__ == '__main__':
    clauses, n_vars, lit_clause = parse(sys.argv[1])

    solution = run_sat(clauses, n_vars, lit_clause)

    print ('s SATISFIABLE')
    print ('v ' + ' '.join(map(str, solution[1:])) + ' 0')