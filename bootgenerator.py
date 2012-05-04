# Generates a boot grammar and stores it in boot_generated.py. If everything looks OK you can
# replace your boot.py with the generated module.
if __name__ == '__main__':
    import os, sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from pymeta import builder, grammar
    fp = open(os.path.join(os.path.dirname(__file__), 'boot_generated.py'), 'wb')
    ometa_grammar = grammar.OMetaGrammar(grammar.ometaGrammar)
    tree = ometa_grammar.parseGrammar('BootOMetaGrammar', builder.TreeBuilder)
    fp.write(builder.writeBoot(tree))
