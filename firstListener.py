# Generated from first.g4 by ANTLR 4.6
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .firstParser import firstParser
else:
    from firstParser import firstParser

# This class defines a complete listener for a parse tree produced by firstParser.
class firstListener(ParseTreeListener):

    # Enter a parse tree produced by firstParser#tokens.
    def enterTokens(self, ctx:firstParser.TokensContext):
        pass

    # Exit a parse tree produced by firstParser#tokens.
    def exitTokens(self, ctx:firstParser.TokensContext):
        pass


    # Enter a parse tree produced by firstParser#program.
    def enterProgram(self, ctx:firstParser.ProgramContext):
        pass

    # Exit a parse tree produced by firstParser#program.
    def exitProgram(self, ctx:firstParser.ProgramContext):
        pass


    # Enter a parse tree produced by firstParser#id_.
    def enterId_(self, ctx:firstParser.Id_Context):
        pass

    # Exit a parse tree produced by firstParser#id_.
    def exitId_(self, ctx:firstParser.Id_Context):
        pass


    # Enter a parse tree produced by firstParser#pgm_body.
    def enterPgm_body(self, ctx:firstParser.Pgm_bodyContext):
        pass

    # Exit a parse tree produced by firstParser#pgm_body.
    def exitPgm_body(self, ctx:firstParser.Pgm_bodyContext):
        pass


    # Enter a parse tree produced by firstParser#decl.
    def enterDecl(self, ctx:firstParser.DeclContext):
        pass

    # Exit a parse tree produced by firstParser#decl.
    def exitDecl(self, ctx:firstParser.DeclContext):
        pass


    # Enter a parse tree produced by firstParser#string_decl.
    def enterString_decl(self, ctx:firstParser.String_declContext):
        pass

    # Exit a parse tree produced by firstParser#string_decl.
    def exitString_decl(self, ctx:firstParser.String_declContext):
        pass


    # Enter a parse tree produced by firstParser#str_.
    def enterStr_(self, ctx:firstParser.Str_Context):
        pass

    # Exit a parse tree produced by firstParser#str_.
    def exitStr_(self, ctx:firstParser.Str_Context):
        pass


    # Enter a parse tree produced by firstParser#var_decl.
    def enterVar_decl(self, ctx:firstParser.Var_declContext):
        pass

    # Exit a parse tree produced by firstParser#var_decl.
    def exitVar_decl(self, ctx:firstParser.Var_declContext):
        pass


    # Enter a parse tree produced by firstParser#var_type.
    def enterVar_type(self, ctx:firstParser.Var_typeContext):
        pass

    # Exit a parse tree produced by firstParser#var_type.
    def exitVar_type(self, ctx:firstParser.Var_typeContext):
        pass


    # Enter a parse tree produced by firstParser#any_type.
    def enterAny_type(self, ctx:firstParser.Any_typeContext):
        pass

    # Exit a parse tree produced by firstParser#any_type.
    def exitAny_type(self, ctx:firstParser.Any_typeContext):
        pass


    # Enter a parse tree produced by firstParser#id_list.
    def enterId_list(self, ctx:firstParser.Id_listContext):
        pass

    # Exit a parse tree produced by firstParser#id_list.
    def exitId_list(self, ctx:firstParser.Id_listContext):
        pass


    # Enter a parse tree produced by firstParser#id_tail.
    def enterId_tail(self, ctx:firstParser.Id_tailContext):
        pass

    # Exit a parse tree produced by firstParser#id_tail.
    def exitId_tail(self, ctx:firstParser.Id_tailContext):
        pass


    # Enter a parse tree produced by firstParser#param_decl_list.
    def enterParam_decl_list(self, ctx:firstParser.Param_decl_listContext):
        pass

    # Exit a parse tree produced by firstParser#param_decl_list.
    def exitParam_decl_list(self, ctx:firstParser.Param_decl_listContext):
        pass


    # Enter a parse tree produced by firstParser#param_decl.
    def enterParam_decl(self, ctx:firstParser.Param_declContext):
        pass

    # Exit a parse tree produced by firstParser#param_decl.
    def exitParam_decl(self, ctx:firstParser.Param_declContext):
        pass


    # Enter a parse tree produced by firstParser#param_decl_tail.
    def enterParam_decl_tail(self, ctx:firstParser.Param_decl_tailContext):
        pass

    # Exit a parse tree produced by firstParser#param_decl_tail.
    def exitParam_decl_tail(self, ctx:firstParser.Param_decl_tailContext):
        pass


    # Enter a parse tree produced by firstParser#func_declarations.
    def enterFunc_declarations(self, ctx:firstParser.Func_declarationsContext):
        pass

    # Exit a parse tree produced by firstParser#func_declarations.
    def exitFunc_declarations(self, ctx:firstParser.Func_declarationsContext):
        pass


    # Enter a parse tree produced by firstParser#func_decl.
    def enterFunc_decl(self, ctx:firstParser.Func_declContext):
        pass

    # Exit a parse tree produced by firstParser#func_decl.
    def exitFunc_decl(self, ctx:firstParser.Func_declContext):
        pass


    # Enter a parse tree produced by firstParser#func_body.
    def enterFunc_body(self, ctx:firstParser.Func_bodyContext):
        pass

    # Exit a parse tree produced by firstParser#func_body.
    def exitFunc_body(self, ctx:firstParser.Func_bodyContext):
        pass


    # Enter a parse tree produced by firstParser#stmt_list.
    def enterStmt_list(self, ctx:firstParser.Stmt_listContext):
        pass

    # Exit a parse tree produced by firstParser#stmt_list.
    def exitStmt_list(self, ctx:firstParser.Stmt_listContext):
        pass


    # Enter a parse tree produced by firstParser#stmt.
    def enterStmt(self, ctx:firstParser.StmtContext):
        pass

    # Exit a parse tree produced by firstParser#stmt.
    def exitStmt(self, ctx:firstParser.StmtContext):
        pass


    # Enter a parse tree produced by firstParser#base_stmt.
    def enterBase_stmt(self, ctx:firstParser.Base_stmtContext):
        pass

    # Exit a parse tree produced by firstParser#base_stmt.
    def exitBase_stmt(self, ctx:firstParser.Base_stmtContext):
        pass


    # Enter a parse tree produced by firstParser#assign_stmt.
    def enterAssign_stmt(self, ctx:firstParser.Assign_stmtContext):
        pass

    # Exit a parse tree produced by firstParser#assign_stmt.
    def exitAssign_stmt(self, ctx:firstParser.Assign_stmtContext):
        pass


    # Enter a parse tree produced by firstParser#assign_expr.
    def enterAssign_expr(self, ctx:firstParser.Assign_exprContext):
        pass

    # Exit a parse tree produced by firstParser#assign_expr.
    def exitAssign_expr(self, ctx:firstParser.Assign_exprContext):
        pass


    # Enter a parse tree produced by firstParser#read_stmt.
    def enterRead_stmt(self, ctx:firstParser.Read_stmtContext):
        pass

    # Exit a parse tree produced by firstParser#read_stmt.
    def exitRead_stmt(self, ctx:firstParser.Read_stmtContext):
        pass


    # Enter a parse tree produced by firstParser#write_stmt.
    def enterWrite_stmt(self, ctx:firstParser.Write_stmtContext):
        pass

    # Exit a parse tree produced by firstParser#write_stmt.
    def exitWrite_stmt(self, ctx:firstParser.Write_stmtContext):
        pass


    # Enter a parse tree produced by firstParser#return_stmt.
    def enterReturn_stmt(self, ctx:firstParser.Return_stmtContext):
        pass

    # Exit a parse tree produced by firstParser#return_stmt.
    def exitReturn_stmt(self, ctx:firstParser.Return_stmtContext):
        pass


    # Enter a parse tree produced by firstParser#expr.
    def enterExpr(self, ctx:firstParser.ExprContext):
        pass

    # Exit a parse tree produced by firstParser#expr.
    def exitExpr(self, ctx:firstParser.ExprContext):
        pass


    # Enter a parse tree produced by firstParser#expr_prefix.
    def enterExpr_prefix(self, ctx:firstParser.Expr_prefixContext):
        pass

    # Exit a parse tree produced by firstParser#expr_prefix.
    def exitExpr_prefix(self, ctx:firstParser.Expr_prefixContext):
        pass


    # Enter a parse tree produced by firstParser#factor.
    def enterFactor(self, ctx:firstParser.FactorContext):
        pass

    # Exit a parse tree produced by firstParser#factor.
    def exitFactor(self, ctx:firstParser.FactorContext):
        pass


    # Enter a parse tree produced by firstParser#factor_prefix.
    def enterFactor_prefix(self, ctx:firstParser.Factor_prefixContext):
        pass

    # Exit a parse tree produced by firstParser#factor_prefix.
    def exitFactor_prefix(self, ctx:firstParser.Factor_prefixContext):
        pass


    # Enter a parse tree produced by firstParser#postfix_expr.
    def enterPostfix_expr(self, ctx:firstParser.Postfix_exprContext):
        pass

    # Exit a parse tree produced by firstParser#postfix_expr.
    def exitPostfix_expr(self, ctx:firstParser.Postfix_exprContext):
        pass


    # Enter a parse tree produced by firstParser#call_expr.
    def enterCall_expr(self, ctx:firstParser.Call_exprContext):
        pass

    # Exit a parse tree produced by firstParser#call_expr.
    def exitCall_expr(self, ctx:firstParser.Call_exprContext):
        pass


    # Enter a parse tree produced by firstParser#expr_list.
    def enterExpr_list(self, ctx:firstParser.Expr_listContext):
        pass

    # Exit a parse tree produced by firstParser#expr_list.
    def exitExpr_list(self, ctx:firstParser.Expr_listContext):
        pass


    # Enter a parse tree produced by firstParser#expr_list_tail.
    def enterExpr_list_tail(self, ctx:firstParser.Expr_list_tailContext):
        pass

    # Exit a parse tree produced by firstParser#expr_list_tail.
    def exitExpr_list_tail(self, ctx:firstParser.Expr_list_tailContext):
        pass


    # Enter a parse tree produced by firstParser#primary.
    def enterPrimary(self, ctx:firstParser.PrimaryContext):
        pass

    # Exit a parse tree produced by firstParser#primary.
    def exitPrimary(self, ctx:firstParser.PrimaryContext):
        pass


    # Enter a parse tree produced by firstParser#addop.
    def enterAddop(self, ctx:firstParser.AddopContext):
        pass

    # Exit a parse tree produced by firstParser#addop.
    def exitAddop(self, ctx:firstParser.AddopContext):
        pass


    # Enter a parse tree produced by firstParser#mulop.
    def enterMulop(self, ctx:firstParser.MulopContext):
        pass

    # Exit a parse tree produced by firstParser#mulop.
    def exitMulop(self, ctx:firstParser.MulopContext):
        pass


    # Enter a parse tree produced by firstParser#if_stmt.
    def enterIf_stmt(self, ctx:firstParser.If_stmtContext):
        pass

    # Exit a parse tree produced by firstParser#if_stmt.
    def exitIf_stmt(self, ctx:firstParser.If_stmtContext):
        pass


    # Enter a parse tree produced by firstParser#else_part.
    def enterElse_part(self, ctx:firstParser.Else_partContext):
        pass

    # Exit a parse tree produced by firstParser#else_part.
    def exitElse_part(self, ctx:firstParser.Else_partContext):
        pass


    # Enter a parse tree produced by firstParser#cond.
    def enterCond(self, ctx:firstParser.CondContext):
        pass

    # Exit a parse tree produced by firstParser#cond.
    def exitCond(self, ctx:firstParser.CondContext):
        pass


    # Enter a parse tree produced by firstParser#compop.
    def enterCompop(self, ctx:firstParser.CompopContext):
        pass

    # Exit a parse tree produced by firstParser#compop.
    def exitCompop(self, ctx:firstParser.CompopContext):
        pass


    # Enter a parse tree produced by firstParser#while_stmt.
    def enterWhile_stmt(self, ctx:firstParser.While_stmtContext):
        pass

    # Exit a parse tree produced by firstParser#while_stmt.
    def exitWhile_stmt(self, ctx:firstParser.While_stmtContext):
        pass


