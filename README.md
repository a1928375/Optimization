# Optimization

(1) Optimization Phase

(2) Recursive optimization:  A fuller answer would replace return tree with return (etype, a, op, b) at the end. The question only asked you to handle a+(5*0), but we would really like to be more general as well.

(3) Bending Numbers:  In class we discussed a number of arithmetic optimizations for JavaScript. In our approach to optimization, a sub-tree of the abstract syntax is replaced with a new abstract syntax tree. In addition to using arithmetic identities, such as X*0 == 0 for all X, we can also perform arithmetic operations on constants. For example, if a JavaScript loop or recursive procedure containts 1+2+3, we can just evaluate it to 6 once and then not perform the two additions again. This technique is called "constant folding". Write a procedure optimize(exp) that takes a JavaScript expression AST node and returns a new, simplified JavaScript expression AST. You must handle:

       X * 1 == 1 * X == X     for all X
       X * 0 == 0 * X == 0     for all X
       X + 0 == 0 + X == X     for all X
       X - X == 0              for all X

and constant folding for +, - and * (e.g., replace 1+2 with 3) 

To do constant folding, given a parse tree for X+Y we want to try to add the values for the parse trees of X and Y. If X and Y are both numbers, that will work. But if X or Y is an identifier, for example, that will not work, because the types will not match. 

(4) The living optimization:  In addition to optimizing expressions, it is also possible to optimize statements. There are many ways to do so, and we will explore one in this problem. Consider this JavaScript fragment: 

       function myfun(a,b,c,d) {
               a = 1;
               b = 2;
               c = 3;
               d = 4; 
               a = 5;
               d = c + b;
               return (a + d);
               } 

Many of the assignment statements end up computing values that are never used. The output of the function only really depends on the final values of a and d. This function, with two of the lines removed, computes the same answer: 

       function myfun(a,b,c,d) {
               # a = 1;
               b = 2;
               c = 3;
               # d = 4; 
               a = 5;
               d = c + b;
               return (a + d);
               } 

Those lines can be safely removed because they do not compute a value that is used later. We say that a variable is LIVE if the value it holds may be needed in the future. More formally, a variable is LIVE if its value may be read before the next time it is overwritten. Whether or not a variable is LIVE depends on where you are looking in the program, so most formally we say a variable is live at some point P if it may be read before being overwritten after P. We can compute the set of live variables by looking at the statements in the function in reverse order. 

              return (a + d);

Since the output of the function depends on (a + d), a and d are both live right before this statement. Now we consider one more statement: 

               d = c + b;
               return (a + d);
 
"a" and "d" were live going in to the return statement. What is live before "d = c + b"? Well, since "d" is overwritten, we have to remove it from the set. But since "c" and "b" are written, we have to add them to the set. So the set of live variables before that assignment statement is "a", "b", "c". In fact, we could annotate the whole program: 

       function myfun(a,b,c,d) {
               a = 1;
               # LIVE: nothing 
               b = 2;
               # LIVE: b 
               c = 3;
               # LIVE: c, b
               d = 4; 
               # LIVE: c, b 
               a = 5;
               # LIVE: a, c, b 
               d = c + b;
               # LIVE: a, d
               return (a + d);
              } 

Once we know which variables are LIVE, we can now remove assignments to variables that will never be read later. Such assignments are called DEAD code. Formally, given an assignment statement "X = ...", if "X" is notlive after that statement, the whole statement can be removed. 

Note that remove some dead code may make it possible to remove more later. For example, in this fragment:

               a = 1;
               b = a + 1;
               c = 2;
               return c; 

We can initially find the following LIVE variables: 

               a = 1;
               # LIVE: a
               b = a + 1;
               # LIVE: nothing
               c = 2;
               # LIVE: c
               return c; 

But if we remove the "b = a + 1" assignment and repeat the process, we will be able to remove the "a = 1" code as well. In this assignment, you will write an optimizer that removes dead code. For simplicity, we will only consider sequences of assignment statements (once we can optimize those, we could weave together a bigger optimizer that handles both branches of if statements, and so on, but we'll just do simple lists of assignments for now). 

We will encode JavaScript fragments as lists of tuples. For example,

               a = 1;
               b = a + 1;
               c = 2;

Will be encoded as:

       fragment2 = [ ("a", ["1"] ) ,           # a = 1
                     ("b", ["a", "1"] ),       # b = a operation 1
                     ("c", ["2"] ), ]          # c = 2 

That is, each assignment "LHS = RHS op RHS op RHS ..." will just be encoded as (LHS, [RHS, RHS, RHS]). A block is then a list of such assignments. 

Write a procedure removedead(fragment,returned). "fragment" is encoded as above. "returned" is a list of variables returned at the end of the fragment (and thus LIVE at the end of it). 

       Hint 1: One way to reverse a list is [::-1] 
       >>> [1,2,3][::-1]
       [3, 2, 1]

       Hint 2: One "functional programming" way to make a new list that is just like L but with all copies of X removed is:
       [ e for e in L if e != X ] 

       Hint 3: Remember that if anything changes, you should call yourself recursively because you may find even more dead code.
       
(5) Do Not Repeat Repeated Work:  In class we studied many approaches to optimizing away redundant computation. For example, "X * 0" can be replaced with "0", because we know in advance that the result will always be 0. However, even if we do not know the answer in advance, we can sometimes save work. Consider this program fragment:

       x = a + b + c;
       y = 2;
       z = a + b + c; 

Even though we do not know what "a + b + c" will be, there is no reason for us to compute it twice! We can replace the program with: 

       x = a + b + c;
       y = 2;
       z = x;          # works since "x = a + b + c;" above and neither a nor b nor c has been changed since

... and always compute the same answer. This family of optimizations is sometimes called "common expression elimination" -- the subexpression "a+b+c" was common to two places in the code, so we eliminated it in one. In this problem we will only consider a special case of this optimization. If we see the assignment statement:

       var1 = right_hand_side ;  

Then all subsequent assignment statements:

       var2 = right_hand_side ;

can be replaced with "var2 = var1 ;" provided that the "right_hand_side"s match exactly and provided that none of the variables involved in "right_hand_Side" have changed. For example, this program cannot be optimized in this way:  

       x = a + b + c;
       b = 2;
       z = a + b + c; 

Even though the right-hand-sides are exact matches, the value of b has changed in the interim so, to be safe, we have to recompute "a + b + c" and cannot replace "z = a + b + c" with "z = x". For this problem we will use the abstract syntax tree format from our JavaScript interpreter. Your procedure will be given a list of statements and should return an optimized list of statements (using the optimization
above). However, you will *only* be given statement of the form:

       ("assign", variable_name, rhs_expression) 

No other types of statements (e.g., "if-then" statements) will be passed to your procedure. Similarly, the rhs_expression will *only* contain expressions of these three (nested) form:

       ("binop", exp, operator, exp)
       ("number", number)
       ("identifier", variable_name) 

No other types of expressions (e.g., function calls) will appear. Write a procedure "optimize()" that takes a list of statements (again,
only assignment statements) as input and returns a new list of optimized statements that compute the same value but avoid recomputing
whole right-hand-side expressions. (If there are multiple equivalent optimizations, return whichever you like.) Hint: x = y + z makes anything involving y and z un-available, and then makes y + z available (and stored in variable x). 
