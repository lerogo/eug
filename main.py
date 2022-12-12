#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

from src import CodeGen


def main(args):
    if len(args) == 1:
        source = args[0]
        gen = CodeGen(source)
    elif len(args) == 2:
        source = args[0]
        output = args[1]
        gen = CodeGen(source, output)
    else:
        print(">> Please input the source file .")
        exit()
    gen.generate()


if __name__ == '__main__':
    print(f"easy to use, easy to get.")
    print(f"This is a new programming language that makes web crawlers easy to use and easy to get the data you want.")
    main(sys.argv[1:])
