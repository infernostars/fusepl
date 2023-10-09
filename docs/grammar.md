| syntax     | lang                                                              |
|------------|-------------------------------------------------------------------|
| expression | term ((PLUS\|MINUS) term)*                                        |
| term       | factor ((MUL\|DIV) factor)*                                       |
| factor     | INT\|FLOAT<br/>(PLUS\|MINUS) factor<br/> LPAREN expression RPAREN |
