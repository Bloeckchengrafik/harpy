#!/usr/bin/env just --justfile

all: test1 test2 test3

test1:
    python3 -m harpy -i test_data/1.py -o .harpy/a.out -r

test2:
    python3 -m harpy -i test_data/2.py -o .harpy/a.out -r

test3:
    python3 -m harpy -i test_data/3.py -o .harpy/a.out -r

test4:
    python3 -m harpy -i test_data/4.py -o .harpy/a.out -r

test5:
    python3 -m harpy -i test_data/5.py -o .harpy/a.out -r
