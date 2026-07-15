import ast

class StaticAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.mcc = 1
        self.nbd = 0
        self.current_depth = 0
        self.nom = 0
        self.rfc = 0
        self.imports = set()
        self.variables = set()
        self.attributes = set()

    def visit_FunctionDef(self, node):
        self.nom += 1
        self.generic_visit(node)

    def visit_If(self, node):
        self._complexity(node)

    def visit_For(self, node):
        self._complexity(node)

    def visit_While(self, node):
        self._complexity(node)

    def _complexity(self, node):
        self.mcc += 1
        self.current_depth += 1
        self.nbd = max(self.nbd, self.current_depth)
        self.generic_visit(node)
        self.current_depth -= 1

    def visit_Call(self, node):
        self.rfc += 1
        self.generic_visit(node)

    def visit_Import(self, node):
        for n in node.names:
            self.imports.add(n.name)

    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.add(node.module)

    def visit_Name(self, node):
        self.variables.add(node.id)

    def visit_Attribute(self, node):
        self.attributes.add(node.attr)
        self.generic_visit(node)

def extract_metrics_from_code(code):
    tree = ast.parse(code)
    analyzer = StaticAnalyzer()
    analyzer.visit(tree)

    loc = len(code.strip().split("\n"))

    return {
        "LOC": loc,
        "MCC": analyzer.mcc,
        "NBD": analyzer.nbd,
        "NOM": analyzer.nom,
        "RFC": analyzer.rfc,
        "CBO": len(analyzer.imports),
        "WMC": analyzer.mcc + analyzer.nom,
        "LCOM": max(0.1, 1 - (len(analyzer.variables) / max(1, analyzer.nom * 5))),
        "ATFD": len(analyzer.attributes)
    }