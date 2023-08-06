# coding: utf-8

from collections import deque
from lib2to3.pytree import Leaf, Node

import click
from yapf.yapflib import pytree_utils


def walk(node):
    todo = deque([node])
    while todo:
        node = todo.popleft()
        for child in node.children:
            todo.append(child)
        yield node


def fix(string):
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


@click.command()
@click.argument("filenames", nargs=-1, type=str)
@click.option(
    "--in-place",
    is_flag=True,
    help="make changes to files instead of printing outputs.",
)
def flaxer(filenames, in_place):
    if filenames:
        for filename in filenames:
            string = open(filename).read()
            string = fix(string)
            if in_place:
                with open(filename, "w") as f:
                    f.write(string)
            else:
                print(string)
    else:
        string = ""
        while True:
            try:
                string += input() + "\n"
            except EOFError:
                break
        string = fix(string)
        print(string)


def main():
    flaxer()


if __name__ == "__main__":
    main()
