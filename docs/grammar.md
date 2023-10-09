| syntax     | lang                                                          |
|------------|---------------------------------------------------------------|
| expression | term ((PLUS\|MINUS) term)*<br/>KEYWORD:VAR IDENTIFIER EQ expr |
| term       | factor ((MUL\|DIV) factor)*                                   |
| factor     | (PLUS\|MINUS) factor*<br/> power                              |
| power      | atom (POW factor)*                                            |
| atom       | INT\|FLOAT\|IDENTIFIER<br/> LPAREN expression RPAREN          |
