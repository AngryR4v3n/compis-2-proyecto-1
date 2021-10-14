grammar Decaf;

/*
 * Lexer Rules
 */
fragment ALPHA: [a-zA-Z_];

fragment DIGIT: [0-9];

fragment ALPHA_NUM: ALPHA | DIGIT;

fragment LETTER: [a-zA-Z];

ID: ALPHA ALPHA_NUM*;

NUM: DIGIT DIGIT*;

APOSTROPHE: '\'';

CHAR_LITERAL: APOSTROPHE (LETTER | [\\\t\n]) APOSTROPHE;


/*
 * Parser Rules
 */

program: 'class' 'Program' '{' (declaration)* '}' EOF;

declaration:
	structDeclaration
	| varDeclaration
	| methodDeclaration;

varDeclaration: 
	varType ID ';'
	| varType ID '[' NUM ']' ';';

structDeclaration: 'struct' ID '{' (varDeclaration)* '}' ';';

varType:
	'int' 
	| 'char' 
	| 'boolean'
	| 'struct' ID
	| structDeclaration
	| 'void';

methodDeclaration:
	methodType ID '(' 'void'? ')' block 
	| methodType ID '(' parameter ')' block 
	| methodType ID '(' parameter (',' parameter)+ ')' block ;
methodType: 'int' | 'char' | 'boolean' | 'void';

parameter: parameterType ID | parameterType ID '[' ']';

parameterType: 'int' | 'char' | 'boolean';

block: '{' (varDeclaration)* (statement)* '}';

statement:
	'if' '(' expression ')' block ('else' block)? #if
	| 'while' '(' expression ')' block #while
	| 'return' expression? ';' #returnSt
	| methodCall ';' #methodSt
	| block #blockSt
	| expression? ';' #expSt
	| location '=' expression #assignSt;
	


literal: 
	int_literal
	| char_literal
	| bool_literal;

int_literal: NUM;

char_literal: CHAR_LITERAL;

bool_literal: 'true' | 'false';

location: (ID | ID '[' expression ']') ('.' location)?;

methodCall:
	ID '()' 
	| ID '('expression')' 
	| ID '('expression (','expression)+ ')'; 

expression:
 	methodCall ';' #methodCallExp
	| location #locationExp
	| literal #literalExp
	| expression ('*' | '/' | '%') expression #otherIntOp
	| expression ('+' | '-') expression #sumOp
	| expression rel_op expression #relOp
	| expression eq_op expression #eqOp
	| expression cond_op expression #condOp
	| '-' expression #minusOp
	| '!' expression #notOp
	| '(' expression ')' #parensOp; 



arith_op: '*' | '/' | '%' | '+' | '-';

rel_op: '<' | '>' | '<=' | '>=';

eq_op: '==' | '!=';

cond_op: '&&' | '||';

WHITESPACE: [\t\r\n ] -> skip;