# -*- coding: utf-8 -*-

__all__ = ['ast', 'iter_child_nodes']

try:
    import ast
    iter_child_nodes = ast.iter_child_nodes
except ImportError:   # Python 2.5
    import _ast as ast

    def _ast_compat(node):
        if isinstance(node, ast.ClassDef):
            node.decorator_list = []
        elif isinstance(node, ast.FunctionDef):
            node.decorator_list = node.decorators
        return node

    def iter_child_nodes(node, astcls=ast.AST, ast_compat=_ast_compat):
        """
        Yield all direct child nodes of *node*, that is, all fields that
        are nodes and all items of fields that are lists of nodes.
        """
        if not node._fields:
            return
        for name in node._fields:
            field = getattr(node, name, None)
            if isinstance(field, astcls):
                yield _ast_compat(field)
            elif isinstance(field, list):
                for item in field:
                    if isinstance(item, astcls):
                        yield _ast_compat(item)
