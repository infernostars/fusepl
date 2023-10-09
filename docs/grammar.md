| syntax     | lang                                     |
|------------|------------------------------------------|
| expression | term ((PLUS\|MINUS) term)*               |
| term       | factor ((MUL\|DIV) factor)*              |
| factor     | (PLUS\|MINUS) factor*<br/> power         |
| power      | atom (POW factor)*                       |
| atom       | INT\|FLOAT<br/> LPAREN expression RPAREN |
