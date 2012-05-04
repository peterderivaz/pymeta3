========
PyMeta3
========

--------------------------------------------
A Pattern-Matching Language Based on Python
--------------------------------------------

Summary
=======

PyMeta is an implementation of OMeta, an object-oriented pattern-matching
language developed by Alessandro Warth.
PyMeta provides a compact syntax based on Parsing Expression Grammars (PEGs) 
for common lexing, parsing and tree-transforming activities in a way 
that's easy to reason about for Python programmers.

History
=======
The intriguing OMeta language was invented by Alessandro Warth.
(Website http://tinlizzie.org/ometa/)

This was ported to Python by Allen Short.  (Called PyMeta)

Some useful syntax updates were made by Waldemar Kornewald.  (Called PyMeta2)

This version contains some additional minor changes that I find useful:
1)	Instead of writing 
		token("(") 
    you can write
        #(         

2)	You can also add comments in Python style via
	    # This is a comment


How It Works
============

PyMeta compiles a grammar to a Python class, with the rules as methods. The
rules specify parsing expressions, which consume input and return values if
they succeed in matching.

The grammar can either match a string, or a nested set of lists containing strings.

Basic syntax
~~~~~~~~~~~~~~~~

``foo = ....``
   Define a rule named foo.
``expr1 expr2``
   Match expr1, and then match expr2 if it succeeds, returning the value of
   expr2. Like Python's ``and``.
``expr1 | expr2``
  Try to match expr1 --- if it fails, match expr2 instead. Like Python's
  ``or``.
``expr*``
  Match expr zero or more times, returning a list of matches.
``expr+``
  Match expr one or more times, returning a list of matches.
``expr?``
  Try to match expr. Returns None if it fails to match.
``~expr``
  Fail if the next item in the input matches expr.
``ruleName``
  Call the rule ``ruleName``.
``ruleName(pythonExpression)``
  Call the rule ``ruleName`` passing in the arguments in the Python expression.
``'x'``
  Match the literal character 'x'.
``expr:name``
  Bind the result of expr to the local variable ``name``.
``-> pythonExpression``
  Evaluate the given Python expression and return its result.
``~~expr``
  Lookahead and try to match expr, then rewind to the current position.
``#and`` 
  Match optional whitespace followed by the sequence of characters.
``[ expr ]``
  Matches a Python list that contains a pattern matching expr.
``?(pythonExpression)``
  Match only if the Python expression evaluates to true.
``!(pythonExpression)``
  Execute the Python expression if we reach this point.
``digit``
  Built in rule to match a digit
``letterOrDigit``
  Built in rule to match letters or digits
``anything``
  Built in rule to match any single character
``spaces``
  Built in rule to match any amount of whitespace
``apply(ruleExpr)``
  Calls the rule ruleExpr.  RuleExpr should be a Python expression that evaluates to a string naming the rule.   
  
Comments like Python comments are supported as well, starting with #
and extending to the end of the line.

Interface
=========

The starting point for defining a new grammar is
``pymeta.grammar.OMeta.makeGrammar``, which takes a grammar definition and a
dict of variable bindings for its embedded expressions and produces a Python
class. Grammars can be subclassed as usual, and makeGrammar can be called on
these classes to override rules and provide new ones. To invoke a grammar rule,
call ``grammarObject.apply()`` with its name.

Example Usage
=============

>>> from pymeta3.grammar import OMeta
>>> exampleGrammar = """
ones = '1' '1' -> 1
twos = '2' '2' -> 2
stuff = (ones | twos)+
"""
>>> Example = OMeta.makeGrammar(exampleGrammar, {})
>>> g = Example("11221111")
>>> result, error = g.apply("stuff")
>>> result
[1, 2, 1, 1]
