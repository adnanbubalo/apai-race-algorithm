# Graph coloring problem solver 
Local search algorithm made to solve the graph coloring problem (GCP)\
Made for the subject Advanced Programming in Artificial Intelligence\
The algorithm takes longer to solve more complicated graphs
# Generating a random graph 
```
python rnd-graph-gen.py <num-nodes> <edge-prob> <num-colors> [<random-seed>] > graph_name.cnf
```
# Running the algorithm
```
python gcp-sat-solver.py <input-graph-file>
```
# Running the algorithm with time labels (works only in Linux)
```
python race-incomplete.py <benchmark-folder> gcp-sat-solver.py
```
