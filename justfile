# regular run of numio
run:
    python3 ./src/main.py -nio /home/oosting/IO-partdiff/numio-posix advanced empty

alloc:
    salloc -p west -N 1
 
# balanced run of numio
run-balanced:
    mpirun -N 1 python3 ./src/main.py -nio /home/oosting/IO-partdiff/numio-posix advanced balanced

# generate requirements
update-requirements:
    pip3 freeze > requirements.txt