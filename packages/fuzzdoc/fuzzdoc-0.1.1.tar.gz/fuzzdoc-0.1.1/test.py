def listImportablesFromAST(ast_):
    from ast import (Assign, ClassDef, FunctionDef, Import, ImportFrom, Name,
                     For, Tuple, Try, With)

    if isinstance(ast_, (ClassDef, FunctionDef)):
        return [ast_.name]
    elif isinstance(ast_, (Import, ImportFrom)):
        return [name.asname if name.asname else name.name for name in ast_.names]

    ret = []

    if isinstance(ast_, Assign):
        for target in ast_.targets:
            if isinstance(target, Tuple):
                ret.extend([elt.id for elt in target.elts])
            elif isinstance(target, Name):
                ret.append(target.id)
        return ret

    # These two attributes cover everything of interest from If, Module,
    # and While. They also cover parts of For, Try, and With.
    if hasattr(ast_, 'body') and isinstance(ast_.body, list):
        for innerAST in ast_.body:
            ret.extend(listImportablesFromAST(innerAST))
    if hasattr(ast_, 'orelse'):
        for innerAST in ast_.orelse:
            ret.extend(listImportablesFromAST(innerAST))

    if isinstance(ast_, For):
        target = ast_.target
        if isinstance(target, Tuple):
            ret.extend([elt.id for elt in target.elts])
        else:
            ret.append(target.id)
    elif isinstance(ast_, Try):
        for innerAST in ast_.handlers:
            ret.extend(listImportablesFromAST(innerAST))
    elif isinstance(ast_, With):
        if ast_.optional_vars:
            ret.append(ast_.optional_vars.id)
    return ret

def listImportablesFromSource(source, filename = '<Unknown>'):
    from ast import parse
    return listImportablesFromAST(parse(source, filename))

def listImportablesFromSourceFile(filename):
    with open(filename) as f:
        source = f.read()
    return listImportablesFromSource(source, filename)

print(listImportablesFromSourceFile('fuzzdoc'))
