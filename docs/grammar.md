KW = KEYWORD if something would end up being too long



| syntax     | lang                                                                           |
|------------|--------------------------------------------------------------------------------|
| block      | (block NEWLINE) expr                                                           |
| expression | KEYWORD:var IDENTIFIER EQ expr<br/>comp-expr (KEYWORD:(and/or/xor) comp-expr)* |
| comp-expr  | KEYWORD:not comp-expr<br/>arith-expr (EQ/LT/GT/LTE/GTE) arith-expr             |
| arith-expr | term ((PLUS/MINUS) term)                                                       |
| term       | factor ((MUL/DIV) factor)*                                                     |
| factor     | (PLUS/MINUS) factor*<br/> power                                                |
| power      | atom (POW factor)*                                                             |
| atom       | INT/FLOAT/IDENTIFIER<br/> LPAREN expression RPAREN<br/>if-expr                 |
| if-expr    | KW:if expr KW:then expr (KW:elif expr KW:then expr)* (KW:else expr)?           |                            