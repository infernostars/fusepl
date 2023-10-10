| syntax       | lang                                                                                |
|--------------|-------------------------------------------------------------------------------------|
| expression   | KEYWORD:VAR IDENTIFIER EQ expr<br/>comp-expr ((KEYWORD:AND\|KEYWORD:OR) comp-expr)* |
| comp-expr    | NOT comp-expr<br/>arith-expr (EQ\|LT\|GT\|LTE\|GTE) arith-expr                      |
| arith-expr   | term ((PLUS\|MINUS) term)                                                           |
| term         | factor ((MUL\|DIV) factor)*                                                         |
| factor       | (PLUS\|MINUS) factor*<br/> power                                                    |
| power        | atom (POW factor)*                                                                  |
| atom         | INT\|FLOAT\|IDENTIFIER<br/> LPAREN expression RPAREN                                |