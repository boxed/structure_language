s = """
    foo
        bar
        baz
    foobar
        qwe
            asd
"""


class Fragment:
    def __init__(self, name=None, children=None):
        self.name = name
        self.children = children or []

    def __repr__(self):
        return f"F(name='{self.name}', children={self.children})"

    def __eq__(self, other):
        return self.name == other.name and self.children == other.children


F = Fragment


def parse_structure(structure):
    lines = structure.replace('    ', '\t').split('\n')
    last_indent = None
    stack = [F()]
    for line in lines:
        if not line.strip():
            continue

        indent = len(line) - len(line.lstrip('\t'))
        name = line.strip('\t ')

        if last_indent is None or indent == last_indent:
            pass
        elif indent == last_indent + 1:
            stack.append(stack[-1].children[-1])
        elif indent < last_indent:
            for _ in range(last_indent - indent):
                stack.pop()
        else:
            assert False, 'Indent can only increase by one level at a time'

        stack[-1].children.append(F(name=name))
        last_indent = indent

    return stack[0]


actual = parse_structure(s)

expected = F(
    children=[
        F(
            name='foo',
            children=[
                F(name='bar'),
                F(name='baz'),
            ],
        ),
        F(
            name='foobar',
            children=[
                F(
                    name='qwe',
                    children=[
                        F(name='asd'),
                    ],
                ),
            ],
        ),
    ],
)

assert actual == expected
