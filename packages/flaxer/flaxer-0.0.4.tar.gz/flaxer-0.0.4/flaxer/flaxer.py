# coding: utf-8

import ast
from collections import deque

import click

import astunparse


def walk(node):
    def m1(old_node, field):
        def _m1(new_node):
            setattr(old_node, field, new_node)

        return _m1

    def m2(old_node, field, idx):
        def _m2(new_node):
            getattr(old_node, field)[idx] = new_node

        return _m2

    todo = deque([(node, lambda *args: None)])
    while todo:
        node, modify_func = todo.popleft()
        for name in node._fields:
            try:
                field = getattr(node, name)
                if isinstance(field, ast.AST):
                    todo.append((field, m1(node, name)))
                elif isinstance(field, list):
                    for idx, item in enumerate(field):
                        if isinstance(item, ast.AST):
                            todo.append((item, m2(node, name, idx)))
            except AttributeError:
                pass
        yield node, modify_func


@click.command()
@click.option("-f", "--file", "file")
def main(file):
    if file:
        string = open(file).read()
    else:
        string = ""
        while True:
            try:
                string += input() + "\n"
            except EOFError:
                break
    rootnode = ast.parse(string)
    for node, modify in walk(rootnode):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if (
                node.func.id == "dict"
                and not any(isinstance(a, ast.Starred) for a in node.args)
                and not any(k.arg is None for k in node.keywords)
                and len(node.args) == 0
            ):
                modify(
                    ast.Dict(
                        keys=[ast.Constant(value=i.arg) for i in node.keywords],
                        values=[i.value for i in node.keywords],
                    )
                )
    print(astunparse.unparse(rootnode))


if __name__ == "__main__":
    main()
