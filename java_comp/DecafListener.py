# Generated from Decaf.g4 by ANTLR 4.9
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .DecafParser import DecafParser
else:
    from DecafParser import DecafParser

# This class defines a complete listener for a parse tree produced by DecafParser.
class DecafListener(ParseTreeListener):

    # Enter a parse tree produced by DecafParser#program.
    def enterProgram(self, ctx:DecafParser.ProgramContext):
        pass

    # Exit a parse tree produced by DecafParser#program.
    def exitProgram(self, ctx:DecafParser.ProgramContext):
        pass


    # Enter a parse tree produced by DecafParser#declaration.
    def enterDeclaration(self, ctx:DecafParser.DeclarationContext):
        pass

    # Exit a parse tree produced by DecafParser#declaration.
    def exitDeclaration(self, ctx:DecafParser.DeclarationContext):
        pass


    # Enter a parse tree produced by DecafParser#varDeclaration.
    def enterVarDeclaration(self, ctx:DecafParser.VarDeclarationContext):
        pass

    # Exit a parse tree produced by DecafParser#varDeclaration.
    def exitVarDeclaration(self, ctx:DecafParser.VarDeclarationContext):
        pass


    # Enter a parse tree produced by DecafParser#structDeclaration.
    def enterStructDeclaration(self, ctx:DecafParser.StructDeclarationContext):
        pass

    # Exit a parse tree produced by DecafParser#structDeclaration.
    def exitStructDeclaration(self, ctx:DecafParser.StructDeclarationContext):
        pass


    # Enter a parse tree produced by DecafParser#varType.
    def enterVarType(self, ctx:DecafParser.VarTypeContext):
        pass

    # Exit a parse tree produced by DecafParser#varType.
    def exitVarType(self, ctx:DecafParser.VarTypeContext):
        pass


    # Enter a parse tree produced by DecafParser#methodDeclaration.
    def enterMethodDeclaration(self, ctx:DecafParser.MethodDeclarationContext):
        pass

    # Exit a parse tree produced by DecafParser#methodDeclaration.
    def exitMethodDeclaration(self, ctx:DecafParser.MethodDeclarationContext):
        pass


    # Enter a parse tree produced by DecafParser#methodType.
    def enterMethodType(self, ctx:DecafParser.MethodTypeContext):
        pass

    # Exit a parse tree produced by DecafParser#methodType.
    def exitMethodType(self, ctx:DecafParser.MethodTypeContext):
        pass


    # Enter a parse tree produced by DecafParser#parameter.
    def enterParameter(self, ctx:DecafParser.ParameterContext):
        pass

    # Exit a parse tree produced by DecafParser#parameter.
    def exitParameter(self, ctx:DecafParser.ParameterContext):
        pass


    # Enter a parse tree produced by DecafParser#parameterType.
    def enterParameterType(self, ctx:DecafParser.ParameterTypeContext):
        pass

    # Exit a parse tree produced by DecafParser#parameterType.
    def exitParameterType(self, ctx:DecafParser.ParameterTypeContext):
        pass


    # Enter a parse tree produced by DecafParser#block.
    def enterBlock(self, ctx:DecafParser.BlockContext):
        pass

    # Exit a parse tree produced by DecafParser#block.
    def exitBlock(self, ctx:DecafParser.BlockContext):
        pass


    # Enter a parse tree produced by DecafParser#if.
    def enterIf(self, ctx:DecafParser.IfContext):
        pass

    # Exit a parse tree produced by DecafParser#if.
    def exitIf(self, ctx:DecafParser.IfContext):
        pass


    # Enter a parse tree produced by DecafParser#while.
    def enterWhile(self, ctx:DecafParser.WhileContext):
        pass

    # Exit a parse tree produced by DecafParser#while.
    def exitWhile(self, ctx:DecafParser.WhileContext):
        pass


    # Enter a parse tree produced by DecafParser#returnSt.
    def enterReturnSt(self, ctx:DecafParser.ReturnStContext):
        pass

    # Exit a parse tree produced by DecafParser#returnSt.
    def exitReturnSt(self, ctx:DecafParser.ReturnStContext):
        pass


    # Enter a parse tree produced by DecafParser#methodSt.
    def enterMethodSt(self, ctx:DecafParser.MethodStContext):
        pass

    # Exit a parse tree produced by DecafParser#methodSt.
    def exitMethodSt(self, ctx:DecafParser.MethodStContext):
        pass


    # Enter a parse tree produced by DecafParser#blockSt.
    def enterBlockSt(self, ctx:DecafParser.BlockStContext):
        pass

    # Exit a parse tree produced by DecafParser#blockSt.
    def exitBlockSt(self, ctx:DecafParser.BlockStContext):
        pass


    # Enter a parse tree produced by DecafParser#expSt.
    def enterExpSt(self, ctx:DecafParser.ExpStContext):
        pass

    # Exit a parse tree produced by DecafParser#expSt.
    def exitExpSt(self, ctx:DecafParser.ExpStContext):
        pass


    # Enter a parse tree produced by DecafParser#assignSt.
    def enterAssignSt(self, ctx:DecafParser.AssignStContext):
        pass

    # Exit a parse tree produced by DecafParser#assignSt.
    def exitAssignSt(self, ctx:DecafParser.AssignStContext):
        pass


    # Enter a parse tree produced by DecafParser#literal.
    def enterLiteral(self, ctx:DecafParser.LiteralContext):
        pass

    # Exit a parse tree produced by DecafParser#literal.
    def exitLiteral(self, ctx:DecafParser.LiteralContext):
        pass


    # Enter a parse tree produced by DecafParser#int_literal.
    def enterInt_literal(self, ctx:DecafParser.Int_literalContext):
        pass

    # Exit a parse tree produced by DecafParser#int_literal.
    def exitInt_literal(self, ctx:DecafParser.Int_literalContext):
        pass


    # Enter a parse tree produced by DecafParser#char_literal.
    def enterChar_literal(self, ctx:DecafParser.Char_literalContext):
        pass

    # Exit a parse tree produced by DecafParser#char_literal.
    def exitChar_literal(self, ctx:DecafParser.Char_literalContext):
        pass


    # Enter a parse tree produced by DecafParser#bool_literal.
    def enterBool_literal(self, ctx:DecafParser.Bool_literalContext):
        pass

    # Exit a parse tree produced by DecafParser#bool_literal.
    def exitBool_literal(self, ctx:DecafParser.Bool_literalContext):
        pass


    # Enter a parse tree produced by DecafParser#location.
    def enterLocation(self, ctx:DecafParser.LocationContext):
        pass

    # Exit a parse tree produced by DecafParser#location.
    def exitLocation(self, ctx:DecafParser.LocationContext):
        pass


    # Enter a parse tree produced by DecafParser#methodCall.
    def enterMethodCall(self, ctx:DecafParser.MethodCallContext):
        pass

    # Exit a parse tree produced by DecafParser#methodCall.
    def exitMethodCall(self, ctx:DecafParser.MethodCallContext):
        pass


    # Enter a parse tree produced by DecafParser#parensOp.
    def enterParensOp(self, ctx:DecafParser.ParensOpContext):
        pass

    # Exit a parse tree produced by DecafParser#parensOp.
    def exitParensOp(self, ctx:DecafParser.ParensOpContext):
        pass


    # Enter a parse tree produced by DecafParser#literalExp.
    def enterLiteralExp(self, ctx:DecafParser.LiteralExpContext):
        pass

    # Exit a parse tree produced by DecafParser#literalExp.
    def exitLiteralExp(self, ctx:DecafParser.LiteralExpContext):
        pass


    # Enter a parse tree produced by DecafParser#eqOp.
    def enterEqOp(self, ctx:DecafParser.EqOpContext):
        pass

    # Exit a parse tree produced by DecafParser#eqOp.
    def exitEqOp(self, ctx:DecafParser.EqOpContext):
        pass


    # Enter a parse tree produced by DecafParser#locationExp.
    def enterLocationExp(self, ctx:DecafParser.LocationExpContext):
        pass

    # Exit a parse tree produced by DecafParser#locationExp.
    def exitLocationExp(self, ctx:DecafParser.LocationExpContext):
        pass


    # Enter a parse tree produced by DecafParser#notOp.
    def enterNotOp(self, ctx:DecafParser.NotOpContext):
        pass

    # Exit a parse tree produced by DecafParser#notOp.
    def exitNotOp(self, ctx:DecafParser.NotOpContext):
        pass


    # Enter a parse tree produced by DecafParser#sumOp.
    def enterSumOp(self, ctx:DecafParser.SumOpContext):
        pass

    # Exit a parse tree produced by DecafParser#sumOp.
    def exitSumOp(self, ctx:DecafParser.SumOpContext):
        pass


    # Enter a parse tree produced by DecafParser#minusOp.
    def enterMinusOp(self, ctx:DecafParser.MinusOpContext):
        pass

    # Exit a parse tree produced by DecafParser#minusOp.
    def exitMinusOp(self, ctx:DecafParser.MinusOpContext):
        pass


    # Enter a parse tree produced by DecafParser#methodCallExp.
    def enterMethodCallExp(self, ctx:DecafParser.MethodCallExpContext):
        pass

    # Exit a parse tree produced by DecafParser#methodCallExp.
    def exitMethodCallExp(self, ctx:DecafParser.MethodCallExpContext):
        pass


    # Enter a parse tree produced by DecafParser#otherIntOp.
    def enterOtherIntOp(self, ctx:DecafParser.OtherIntOpContext):
        pass

    # Exit a parse tree produced by DecafParser#otherIntOp.
    def exitOtherIntOp(self, ctx:DecafParser.OtherIntOpContext):
        pass


    # Enter a parse tree produced by DecafParser#relOp.
    def enterRelOp(self, ctx:DecafParser.RelOpContext):
        pass

    # Exit a parse tree produced by DecafParser#relOp.
    def exitRelOp(self, ctx:DecafParser.RelOpContext):
        pass


    # Enter a parse tree produced by DecafParser#condOp.
    def enterCondOp(self, ctx:DecafParser.CondOpContext):
        pass

    # Exit a parse tree produced by DecafParser#condOp.
    def exitCondOp(self, ctx:DecafParser.CondOpContext):
        pass


    # Enter a parse tree produced by DecafParser#arith_op.
    def enterArith_op(self, ctx:DecafParser.Arith_opContext):
        pass

    # Exit a parse tree produced by DecafParser#arith_op.
    def exitArith_op(self, ctx:DecafParser.Arith_opContext):
        pass


    # Enter a parse tree produced by DecafParser#rel_op.
    def enterRel_op(self, ctx:DecafParser.Rel_opContext):
        pass

    # Exit a parse tree produced by DecafParser#rel_op.
    def exitRel_op(self, ctx:DecafParser.Rel_opContext):
        pass


    # Enter a parse tree produced by DecafParser#eq_op.
    def enterEq_op(self, ctx:DecafParser.Eq_opContext):
        pass

    # Exit a parse tree produced by DecafParser#eq_op.
    def exitEq_op(self, ctx:DecafParser.Eq_opContext):
        pass


    # Enter a parse tree produced by DecafParser#cond_op.
    def enterCond_op(self, ctx:DecafParser.Cond_opContext):
        pass

    # Exit a parse tree produced by DecafParser#cond_op.
    def exitCond_op(self, ctx:DecafParser.Cond_opContext):
        pass



del DecafParser