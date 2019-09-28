# Optimization

(1) Optimization Phase

(2) Fix It Up:  A fuller answer would replace return tree with return (etype, a, op, b) at the end. The question only asked you to handle a+(5*0), but we would really like to be more general as well.

(3) Bending Numbers:  In class we discussed a number of arithmetic optimizations for JavaScript. In our approach to optimization, a sub-tree of the abstract syntax is replaced with a new abstract syntax tree. In addition to using arithmetic identities, such as X*0 == 0 for all X, we can also perform arithmetic operations on constants. For example, if a JavaScript loop or recursive procedure containts 1+2+3, we can just evaluate it to 6 once and then not perform the two additions again. This technique is called "constant folding". Write a procedure optimize(exp) that takes a JavaScript expression AST node and returns a new, simplified JavaScript expression AST. You must handle:

       X * 1 == 1 * X == X     for all X
       X * 0 == 0 * X == 0     for all X
       X + 0 == 0 + X == X     for all X
       X - X == 0              for all X

and constant folding for +, - and * (e.g., replace 1+2 with 3) 

To do constant folding, given a parse tree for X+Y we want to try to add the values for the parse trees of X and Y. If X and Y are both numbers, that will work. But if X or Y is an identifier, for example, that will not work, because the types will not match. 
