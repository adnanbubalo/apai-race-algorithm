import sys
import random

def parse(file):
    print(file)
    clauses = []
    for line in open(file):
        if line[0] == 'c':
            continue
        if line[0] == 'p':
            n_vars = int(line.split()[2])
            continue

        clause = []
        for literal in line[:-2].split():
            literal = int(literal)
            clause.append(literal)
        clauses.append(clause)
    return clauses, n_vars

def count_unsatisfied(clauses, interpretation):
    unsatisfied = 0
    for clause in clauses:
        clause_value = False
        for lit in clause:
            clause_value = clause_value or interpretation[abs(lit)] == lit 
            if clause_value:
                break
        if not clause_value:
            unsatisfied += 1
    return unsatisfied

def count_satisfied(clauses, interpretation):
    count = 0
    for clause in clauses:
        for lit in clause:
            if lit == interpretation[abs(lit)]:
                count += 1
                break
    return count

def run_sat(clauses, num_vars, p = 0.5):
    interpretation = [random.choice([i, -i]) for i in range(num_vars + 1)]
    unsatisfied = count_unsatisfied(clauses, interpretation)

    while 1:
        if unsatisfied == 0:
            return interpretation

        best_var, best_satisfied = None, 0
        for var in range(1, num_vars + 1):
            interpretation[var] = interpretation[var] * -1
            satisfied = count_satisfied(clauses, interpretation)
            if satisfied > best_satisfied:
                best_var, best_satisfied = var, satisfied
            interpretation[var] = interpretation[var] * -1

        interpretation[best_var] = interpretation[best_var] * -1
        unsatisfied = count_unsatisfied(clauses, interpretation)

        if random.random() < p:
            var = random.randint(0, num_vars - 1)
            interpretation[var] = interpretation[var] * -1
            unsatisfied = count_unsatisfied(clauses, interpretation)


if __name__ == '__main__':
    clauses, n_vars = parse(sys.argv[1])

    solution = run_sat(clauses, n_vars)

    print ('s SATISFIABLE')
    print ('v ' + ' '.join(map(str, solution[1:])) + ' 0')