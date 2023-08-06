# coding: utf-8

import difflib
from collections import deque
from lib2to3.pytree import Leaf, Node
from typing import List, Optional

import click
from yapf.yapflib import pytree_utils


def walk(node):
    todo = deque([node])
    while todo:
        node = todo.popleft()
        for child in node.children:
            todo.append(child)
        yield node


def fix(string: str) -> str:
    rootnode = pytree_utils.ParseCodeToTree(string)
    for node in walk(rootnode):
        if (
            pytree_utils.NodeName(node) == "power"
            and pytree_utils.NodeName(node.children[0]) == "NAME"
            and node.children[0].value == "dict"
        ):
            trailer = node.children[1]
            if (
                pytree_utils.NodeName(trailer) != "trailer"
                or len(trailer.children) != 3
                or pytree_utils.NodeName(trailer.children[0]) != "LPAR"
                or pytree_utils.NodeName(trailer.children[(-1)]) != "RPAR"
            ):
                pass
            arglist = trailer.children[1]
            if pytree_utils.NodeName(arglist) == "arglist":
                flag = True
                for child in arglist.children:
                    if isinstance(child, Leaf):
                        if pytree_utils.NodeName(child) != "COMMA":
                            flag = False
                            break
                    elif isinstance(child, Node):
                        if (
                            pytree_utils.NodeName(child) != "argument"
                            or len(child.children) != 3
                            or pytree_utils.NodeName(child.children[1]) != "EQUAL"
                            or pytree_utils.NodeName(child.children[0]) != "NAME"
                        ):
                            flag = False
                            break
                    else:
                        flag = False
                        break
                if flag:
                    node.children.pop(0)
                    trailer.children[0] = Leaf(26, "{")
                    trailer.children[-1] = Leaf(27, "}")
                    for child in arglist.children:
                        if isinstance(child, Node):
                            child.children[0] = Leaf(
                                3, '"{0}"'.format(child.children[0].value)
                            )
                            child.children[1] = Leaf(11, ":")
            elif pytree_utils.NodeName(arglist) == "argument":
                if (
                    len(arglist.children) == 3
                    and pytree_utils.NodeName(arglist.children[1]) == "EQUAL"
                    and pytree_utils.NodeName(arglist.children[0]) == "NAME"
                ):
                    node.children.pop(0)
                    trailer.children[0] = Leaf(26, "{")
                    trailer.children[-1] = Leaf(27, "}")
                    arglist.children[0] = Leaf(
                        3, '"{0}"'.format(arglist.children[0].value)
                    )
                    arglist.children[1] = Leaf(11, ":")
    return str(rootnode)


def diff(s1: str, s2: str, fn: Optional[str]) -> str:
    return "".join(
        difflib.unified_diff(
            s1.splitlines(keepends=True), s2.splitlines(keepends=True), fn, fn,
        )
    )


@click.command()
@click.argument("filenames", nargs=-1, type=str)
@click.option(
    "--in-place",
    is_flag=True,
    help="make changes to files instead of printing outputs.",
)
def flaxer(filenames: List[str], in_place: bool):
    fixed = 0
    if filenames:
        for filename in filenames:
            string = open(filename).read()
            fixed_string = fix(string)
            if string != fixed_string:
                if in_place:
                    with open(filename, "w") as f:
                        f.write(fixed_string)
                else:
                    click.echo(diff(string, fixed_string, filename))
                fixed = 1
    else:
        string = ""
        while True:
            try:
                string += input() + "\n"
            except EOFError:
                break
        fixed_string = fix(string)
        click.echo(diff(string, fixed_string, None))
        if string != fixed_string:
            fixed = 1
    if fixed:
        raise click.exceptions.Exit(1)


def main():
    flaxer()


if __name__ == "__main__":
    main()
