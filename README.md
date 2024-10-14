# Asp2pddl
## ASP
```
conda create -n ASP python=3.10
conda activate ASP
conda install -c potassco clingo
```

## PDDL
```
./sgplan522/sgplan522 -o domain.pddl -f problem.pddl -out plan
```

## Asp2pddl
```
python asp2pddl.py 
```