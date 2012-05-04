from .runtime import OMetaBase, _MaybeParseError, ParseError, EOFError

class BootBaseTraits(object):
    def parseGrammar(self, name, builder, *args):
        """
        Entry point for converting a grammar to code (of some variety).

        @param name: The name for this grammar.

        @param builder: A class that implements the grammar-building interface
        (interface to be explicitly defined later)
        """
        self.builder = builder(name, self, *args)
        res, err = self.apply("grammar")
        try:
            x = self.input.head()
        except EOFError:
            pass
        else:
            raise ParseError("Grammar parse failed.\n%s" % self.currentError.formatError(''.join(self.input.data)))
        return res

    def applicationArgs(self):
        """
        Collect rule arguments, a list of Python expressions separated by
        spaces.
        """
        args = []
        while True:
            try:
                (arg, endchar), err = self.pythonExpr(" )")
                if not arg:
                    break
                args.append(self.builder.expr(arg))
                if endchar == ')':
                    break
            except _MaybeParseError:
                break
        if args:
            return args
        else:
            x = str(''.join(self.input.data[max(0, self.input.position-1):]))
            raise _MaybeParseError(self.input.position, None, "Grammar parse failed.\nLeftover bits:\n%s" % x)

    def ruleValueExpr(self):
        """
        Find and generate code for a Python expression terminated by a close
        paren/brace or end of line.
        """
        (expr, endchar), err = self.pythonExpr(endChars="\r\n)]")
        if endchar:
            self.input = self.input.prev()
        return self.builder.expr(expr)

    def semanticActionExpr(self):
        """
        Find and generate code for a Python expression terminated by a
        close-paren, whose return value is ignored.
        """
        return self.builder.action(self.pythonExpr(')')[0][0])

    def semanticPredicateExpr(self):
        """
        Find and generate code for a Python expression terminated by a
        close-paren, whose return value determines the success of the pattern
        it's in.
        """
        expr = self.builder.expr(self.pythonExpr(')')[0][0])
        return self.builder.pred(expr)

class BootBase(BootBaseTraits, OMetaBase):
    pass
