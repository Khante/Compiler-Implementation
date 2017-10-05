grammar first;
tokens: .* EOF;
program: 'PROGRAM' id_ 'BEGIN' pgm_body 'END';
id_: IDENTIFIER;
pgm_body: decl func_declarations;
decl: string_decl decl
    | var_decl decl
	|
	;
string_decl: 'STRING' id_ ':=' str_ ';';
str_: STRINGLITERAL;

var_decl: var_type id_list ';';
var_type: 'FLOAT'
		| 'INT'
//		| 'STRING' //wut~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ this line was added
		;
any_type: var_type
		| 'VOID'
		;
//wut id_list: '['id_ (',' id_tail)* ']';  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
id_list: id_  id_tail;
id_tail: ',' id_ id_tail 
	|
	;//wut~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

param_decl_list: param_decl  param_decl_tail 
               |
			   ;
param_decl: var_type id_;
param_decl_tail: ',' param_decl param_decl_tail
               |
			   ;
func_declarations: func_decl func_declarations
				|
				;
func_decl: 'FUNCTION' any_type id_ '(' param_decl_list ')' 'BEGIN' func_body 'END';
func_body: decl stmt_list;

stmt_list:stmt stmt_list
		 |
		 ;
stmt: base_stmt 
	| if_stmt 
	| while_stmt
	;
base_stmt:assign_stmt 
		 | read_stmt 
		 | write_stmt 
		 | return_stmt
		 ;
	   
assign_stmt: assign_expr ';';
assign_expr: id_ ':=' expr;
read_stmt: 'READ' '(' id_list ')' ';';
write_stmt: 'WRITE' '('id_list')' ';';
return_stmt: 'RETURN' expr ';';

expr: expr_prefix factor;
expr_prefix:expr_prefix factor addop
           |
		   ; 
factor: factor_prefix postfix_expr;
factor_prefix: factor_prefix postfix_expr mulop
			| 
			; 
postfix_expr: primary 
			| call_expr
			;
call_expr:id_ '(' expr_list ')';
expr_list:  expr expr_list_tail  
         |
		 ;
expr_list_tail: ',' expr expr_list_tail 
              |
			  ;

primary: '(' expr ')'
	   | id_ 
	   | INTLITERAL
	   | FLOATLITERAL
	   ;
addop: '+'
     | '-'
	 ;
mulop: '*'
     | '/'
	 ;

if_stmt: 'IF' '(' cond ')' decl stmt_list else_part 'ENDIF';
else_part: 'ELSE' decl stmt_list
         |
		 ;
cond: expr compop expr;
compop: '<' | '>' | '=' | '!=' | '<=' | '>=' ;
while_stmt: 'WHILE' '(' cond ')' decl stmt_list 'ENDWHILE';

KEYWORD: ('PROGRAM' | 'BEGIN' | 'END' | 'FUNCTION' | 'READ' | 'WRITE' | 'IF' | 'ELSE' | 'ENDIF' | 'WHILE' | 'ENDWHILE' | 'CONTINUE ' | 'BREAK' | 'RETURN' | 'INT' | 'VOID' | 'STRING' | 'FLOAT');
OPERATOR: (':=' | '+' | '-' | '*' | '/' | '(' | ')' | ';' | ','  );
INTLITERAL: ('0'..'9')+;
IDENTIFIER : ([A-Z]|[a-z]|'0'..'9')+;
FLOATLITERAL:([0-9]*[.])?[0-9]+ ;
STRINGLITERAL: '"'('\\"' | ~('\n'|'\r'))*?'"';
COMMENT: '--' ~('\r' | '\n')* ->skip;
WHITESPACE: [ \r\n\t]+ ->skip ;