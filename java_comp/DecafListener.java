// Generated from Decaf.g4 by ANTLR 4.9
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link DecafParser}.
 */
public interface DecafListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link DecafParser#program}.
	 * @param ctx the parse tree
	 */
	void enterProgram(DecafParser.ProgramContext ctx);
	/**
	 * Exit a parse tree produced by {@link DecafParser#program}.
	 * @param ctx the parse tree
	 */
	void exitProgram(DecafParser.ProgramContext ctx);
	/**
	 * Enter a parse tree produced by {@link DecafParser#declaration}.
	 * @param ctx the parse tree
	 */
	void enterDeclaration(DecafParser.DeclarationContext ctx);
	/**
	 * Exit a parse tree produced by {@link DecafParser#declaration}.
	 * @param ctx the parse tree
	 */
	void exitDeclaration(DecafParser.DeclarationContext ctx);
	/**
	 * Enter a parse tree produced by the {@code normalVar}
	 * labeled alternative in {@link DecafParser#varDeclaration}.
	 * @param ctx the parse tree
	 */
	void enterNormalVar(DecafParser.NormalVarContext ctx);
	/**
	 * Exit a parse tree produced by the {@code normalVar}
	 * labeled alternative in {@link DecafParser#varDeclaration}.
	 * @param ctx the parse tree
	 */
	void exitNormalVar(DecafParser.NormalVarContext ctx);
	/**
	 * Enter a parse tree produced by the {@code arrVar}
	 * labeled alternative in {@link DecafParser#varDeclaration}.
	 * @param ctx the parse tree
	 */
	void enterArrVar(DecafParser.ArrVarContext ctx);
	/**
	 * Exit a parse tree produced by the {@code arrVar}
	 * labeled alternative in {@link DecafParser#varDeclaration}.
	 * @param ctx the parse tree
	 */
	void exitArrVar(DecafParser.ArrVarContext ctx);
	/**
	 * Enter a parse tree produced by {@link DecafParser#structDeclaration}.
	 * @param ctx the parse tree
	 */
	void enterStructDeclaration(DecafParser.StructDeclarationContext ctx);
	/**
	 * Exit a parse tree produced by {@link DecafParser#structDeclaration}.
	 * @param ctx the parse tree
	 */
	void exitStructDeclaration(DecafParser.StructDeclarationContext ctx);
	/**
	 * Enter a parse tree produced by the {@code intType}
	 * labeled alternative in {@link DecafParser#varType}.
	 * @param ctx the parse tree
	 */
	void enterIntType(DecafParser.IntTypeContext ctx);
	/**
	 * Exit a parse tree produced by the {@code intType}
	 * labeled alternative in {@link DecafParser#varType}.
	 * @param ctx the parse tree
	 */
	void exitIntType(DecafParser.IntTypeContext ctx);
	/**
	 * Enter a parse tree produced by the {@code charType}
	 * labeled alternative in {@link DecafParser#varType}.
	 * @param ctx the parse tree
	 */
	void enterCharType(DecafParser.CharTypeContext ctx);
	/**
	 * Exit a parse tree produced by the {@code charType}
	 * labeled alternative in {@link DecafParser#varType}.
	 * @param ctx the parse tree
	 */
	void exitCharType(DecafParser.CharTypeContext ctx);
	/**
	 * Enter a parse tree produced by the {@code boolType}
	 * labeled alternative in {@link DecafParser#varType}.
	 * @param ctx the parse tree
	 */
	void enterBoolType(DecafParser.BoolTypeContext ctx);
	/**
	 * Exit a parse tree produced by the {@code boolType}
	 * labeled alternative in {@link DecafParser#varType}.
	 * @param ctx the parse tree
	 */
	void exitBoolType(DecafParser.BoolTypeContext ctx);
	/**
	 * Enter a parse tree produced by the {@code structType}
	 * labeled alternative in {@link DecafParser#varType}.
	 * @param ctx the parse tree
	 */
	void enterStructType(DecafParser.StructTypeContext ctx);
	/**
	 * Exit a parse tree produced by the {@code structType}
	 * labeled alternative in {@link DecafParser#varType}.
	 * @param ctx the parse tree
	 */
	void exitStructType(DecafParser.StructTypeContext ctx);
	/**
	 * Enter a parse tree produced by the {@code structDec}
	 * labeled alternative in {@link DecafParser#varType}.
	 * @param ctx the parse tree
	 */
	void enterStructDec(DecafParser.StructDecContext ctx);
	/**
	 * Exit a parse tree produced by the {@code structDec}
	 * labeled alternative in {@link DecafParser#varType}.
	 * @param ctx the parse tree
	 */
	void exitStructDec(DecafParser.StructDecContext ctx);
	/**
	 * Enter a parse tree produced by the {@code void}
	 * labeled alternative in {@link DecafParser#varType}.
	 * @param ctx the parse tree
	 */
	void enterVoid(DecafParser.VoidContext ctx);
	/**
	 * Exit a parse tree produced by the {@code void}
	 * labeled alternative in {@link DecafParser#varType}.
	 * @param ctx the parse tree
	 */
	void exitVoid(DecafParser.VoidContext ctx);
	/**
	 * Enter a parse tree produced by {@link DecafParser#methodDeclaration}.
	 * @param ctx the parse tree
	 */
	void enterMethodDeclaration(DecafParser.MethodDeclarationContext ctx);
	/**
	 * Exit a parse tree produced by {@link DecafParser#methodDeclaration}.
	 * @param ctx the parse tree
	 */
	void exitMethodDeclaration(DecafParser.MethodDeclarationContext ctx);
	/**
	 * Enter a parse tree produced by {@link DecafParser#methodType}.
	 * @param ctx the parse tree
	 */
	void enterMethodType(DecafParser.MethodTypeContext ctx);
	/**
	 * Exit a parse tree produced by {@link DecafParser#methodType}.
	 * @param ctx the parse tree
	 */
	void exitMethodType(DecafParser.MethodTypeContext ctx);
	/**
	 * Enter a parse tree produced by {@link DecafParser#parameter}.
	 * @param ctx the parse tree
	 */
	void enterParameter(DecafParser.ParameterContext ctx);
	/**
	 * Exit a parse tree produced by {@link DecafParser#parameter}.
	 * @param ctx the parse tree
	 */
	void exitParameter(DecafParser.ParameterContext ctx);
	/**
	 * Enter a parse tree produced by {@link DecafParser#parameterType}.
	 * @param ctx the parse tree
	 */
	void enterParameterType(DecafParser.ParameterTypeContext ctx);
	/**
	 * Exit a parse tree produced by {@link DecafParser#parameterType}.
	 * @param ctx the parse tree
	 */
	void exitParameterType(DecafParser.ParameterTypeContext ctx);
	/**
	 * Enter a parse tree produced by {@link DecafParser#block}.
	 * @param ctx the parse tree
	 */
	void enterBlock(DecafParser.BlockContext ctx);
	/**
	 * Exit a parse tree produced by {@link DecafParser#block}.
	 * @param ctx the parse tree
	 */
	void exitBlock(DecafParser.BlockContext ctx);
	/**
	 * Enter a parse tree produced by the {@code if}
	 * labeled alternative in {@link DecafParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterIf(DecafParser.IfContext ctx);
	/**
	 * Exit a parse tree produced by the {@code if}
	 * labeled alternative in {@link DecafParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitIf(DecafParser.IfContext ctx);
	/**
	 * Enter a parse tree produced by the {@code while}
	 * labeled alternative in {@link DecafParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterWhile(DecafParser.WhileContext ctx);
	/**
	 * Exit a parse tree produced by the {@code while}
	 * labeled alternative in {@link DecafParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitWhile(DecafParser.WhileContext ctx);
	/**
	 * Enter a parse tree produced by the {@code returnSt}
	 * labeled alternative in {@link DecafParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterReturnSt(DecafParser.ReturnStContext ctx);
	/**
	 * Exit a parse tree produced by the {@code returnSt}
	 * labeled alternative in {@link DecafParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitReturnSt(DecafParser.ReturnStContext ctx);
	/**
	 * Enter a parse tree produced by the {@code methodSt}
	 * labeled alternative in {@link DecafParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterMethodSt(DecafParser.MethodStContext ctx);
	/**
	 * Exit a parse tree produced by the {@code methodSt}
	 * labeled alternative in {@link DecafParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitMethodSt(DecafParser.MethodStContext ctx);
	/**
	 * Enter a parse tree produced by the {@code blockSt}
	 * labeled alternative in {@link DecafParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterBlockSt(DecafParser.BlockStContext ctx);
	/**
	 * Exit a parse tree produced by the {@code blockSt}
	 * labeled alternative in {@link DecafParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitBlockSt(DecafParser.BlockStContext ctx);
	/**
	 * Enter a parse tree produced by the {@code expSt}
	 * labeled alternative in {@link DecafParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterExpSt(DecafParser.ExpStContext ctx);
	/**
	 * Exit a parse tree produced by the {@code expSt}
	 * labeled alternative in {@link DecafParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitExpSt(DecafParser.ExpStContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assignSt}
	 * labeled alternative in {@link DecafParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterAssignSt(DecafParser.AssignStContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assignSt}
	 * labeled alternative in {@link DecafParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitAssignSt(DecafParser.AssignStContext ctx);
	/**
	 * Enter a parse tree produced by {@link DecafParser#literal}.
	 * @param ctx the parse tree
	 */
	void enterLiteral(DecafParser.LiteralContext ctx);
	/**
	 * Exit a parse tree produced by {@link DecafParser#literal}.
	 * @param ctx the parse tree
	 */
	void exitLiteral(DecafParser.LiteralContext ctx);
	/**
	 * Enter a parse tree produced by {@link DecafParser#int_literal}.
	 * @param ctx the parse tree
	 */
	void enterInt_literal(DecafParser.Int_literalContext ctx);
	/**
	 * Exit a parse tree produced by {@link DecafParser#int_literal}.
	 * @param ctx the parse tree
	 */
	void exitInt_literal(DecafParser.Int_literalContext ctx);
	/**
	 * Enter a parse tree produced by {@link DecafParser#char_literal}.
	 * @param ctx the parse tree
	 */
	void enterChar_literal(DecafParser.Char_literalContext ctx);
	/**
	 * Exit a parse tree produced by {@link DecafParser#char_literal}.
	 * @param ctx the parse tree
	 */
	void exitChar_literal(DecafParser.Char_literalContext ctx);
	/**
	 * Enter a parse tree produced by {@link DecafParser#bool_literal}.
	 * @param ctx the parse tree
	 */
	void enterBool_literal(DecafParser.Bool_literalContext ctx);
	/**
	 * Exit a parse tree produced by {@link DecafParser#bool_literal}.
	 * @param ctx the parse tree
	 */
	void exitBool_literal(DecafParser.Bool_literalContext ctx);
	/**
	 * Enter a parse tree produced by {@link DecafParser#location}.
	 * @param ctx the parse tree
	 */
	void enterLocation(DecafParser.LocationContext ctx);
	/**
	 * Exit a parse tree produced by {@link DecafParser#location}.
	 * @param ctx the parse tree
	 */
	void exitLocation(DecafParser.LocationContext ctx);
	/**
	 * Enter a parse tree produced by {@link DecafParser#methodCall}.
	 * @param ctx the parse tree
	 */
	void enterMethodCall(DecafParser.MethodCallContext ctx);
	/**
	 * Exit a parse tree produced by {@link DecafParser#methodCall}.
	 * @param ctx the parse tree
	 */
	void exitMethodCall(DecafParser.MethodCallContext ctx);
	/**
	 * Enter a parse tree produced by the {@code parensOp}
	 * labeled alternative in {@link DecafParser#expression}.
	 * @param ctx the parse tree
	 */
	void enterParensOp(DecafParser.ParensOpContext ctx);
	/**
	 * Exit a parse tree produced by the {@code parensOp}
	 * labeled alternative in {@link DecafParser#expression}.
	 * @param ctx the parse tree
	 */
	void exitParensOp(DecafParser.ParensOpContext ctx);
	/**
	 * Enter a parse tree produced by the {@code literalExp}
	 * labeled alternative in {@link DecafParser#expression}.
	 * @param ctx the parse tree
	 */
	void enterLiteralExp(DecafParser.LiteralExpContext ctx);
	/**
	 * Exit a parse tree produced by the {@code literalExp}
	 * labeled alternative in {@link DecafParser#expression}.
	 * @param ctx the parse tree
	 */
	void exitLiteralExp(DecafParser.LiteralExpContext ctx);
	/**
	 * Enter a parse tree produced by the {@code eqOp}
	 * labeled alternative in {@link DecafParser#expression}.
	 * @param ctx the parse tree
	 */
	void enterEqOp(DecafParser.EqOpContext ctx);
	/**
	 * Exit a parse tree produced by the {@code eqOp}
	 * labeled alternative in {@link DecafParser#expression}.
	 * @param ctx the parse tree
	 */
	void exitEqOp(DecafParser.EqOpContext ctx);
	/**
	 * Enter a parse tree produced by the {@code locationExp}
	 * labeled alternative in {@link DecafParser#expression}.
	 * @param ctx the parse tree
	 */
	void enterLocationExp(DecafParser.LocationExpContext ctx);
	/**
	 * Exit a parse tree produced by the {@code locationExp}
	 * labeled alternative in {@link DecafParser#expression}.
	 * @param ctx the parse tree
	 */
	void exitLocationExp(DecafParser.LocationExpContext ctx);
	/**
	 * Enter a parse tree produced by the {@code notOp}
	 * labeled alternative in {@link DecafParser#expression}.
	 * @param ctx the parse tree
	 */
	void enterNotOp(DecafParser.NotOpContext ctx);
	/**
	 * Exit a parse tree produced by the {@code notOp}
	 * labeled alternative in {@link DecafParser#expression}.
	 * @param ctx the parse tree
	 */
	void exitNotOp(DecafParser.NotOpContext ctx);
	/**
	 * Enter a parse tree produced by the {@code sumOp}
	 * labeled alternative in {@link DecafParser#expression}.
	 * @param ctx the parse tree
	 */
	void enterSumOp(DecafParser.SumOpContext ctx);
	/**
	 * Exit a parse tree produced by the {@code sumOp}
	 * labeled alternative in {@link DecafParser#expression}.
	 * @param ctx the parse tree
	 */
	void exitSumOp(DecafParser.SumOpContext ctx);
	/**
	 * Enter a parse tree produced by the {@code minusOp}
	 * labeled alternative in {@link DecafParser#expression}.
	 * @param ctx the parse tree
	 */
	void enterMinusOp(DecafParser.MinusOpContext ctx);
	/**
	 * Exit a parse tree produced by the {@code minusOp}
	 * labeled alternative in {@link DecafParser#expression}.
	 * @param ctx the parse tree
	 */
	void exitMinusOp(DecafParser.MinusOpContext ctx);
	/**
	 * Enter a parse tree produced by the {@code methodCallExp}
	 * labeled alternative in {@link DecafParser#expression}.
	 * @param ctx the parse tree
	 */
	void enterMethodCallExp(DecafParser.MethodCallExpContext ctx);
	/**
	 * Exit a parse tree produced by the {@code methodCallExp}
	 * labeled alternative in {@link DecafParser#expression}.
	 * @param ctx the parse tree
	 */
	void exitMethodCallExp(DecafParser.MethodCallExpContext ctx);
	/**
	 * Enter a parse tree produced by the {@code otherIntOp}
	 * labeled alternative in {@link DecafParser#expression}.
	 * @param ctx the parse tree
	 */
	void enterOtherIntOp(DecafParser.OtherIntOpContext ctx);
	/**
	 * Exit a parse tree produced by the {@code otherIntOp}
	 * labeled alternative in {@link DecafParser#expression}.
	 * @param ctx the parse tree
	 */
	void exitOtherIntOp(DecafParser.OtherIntOpContext ctx);
	/**
	 * Enter a parse tree produced by the {@code relOp}
	 * labeled alternative in {@link DecafParser#expression}.
	 * @param ctx the parse tree
	 */
	void enterRelOp(DecafParser.RelOpContext ctx);
	/**
	 * Exit a parse tree produced by the {@code relOp}
	 * labeled alternative in {@link DecafParser#expression}.
	 * @param ctx the parse tree
	 */
	void exitRelOp(DecafParser.RelOpContext ctx);
	/**
	 * Enter a parse tree produced by the {@code condOp}
	 * labeled alternative in {@link DecafParser#expression}.
	 * @param ctx the parse tree
	 */
	void enterCondOp(DecafParser.CondOpContext ctx);
	/**
	 * Exit a parse tree produced by the {@code condOp}
	 * labeled alternative in {@link DecafParser#expression}.
	 * @param ctx the parse tree
	 */
	void exitCondOp(DecafParser.CondOpContext ctx);
	/**
	 * Enter a parse tree produced by {@link DecafParser#arith_op}.
	 * @param ctx the parse tree
	 */
	void enterArith_op(DecafParser.Arith_opContext ctx);
	/**
	 * Exit a parse tree produced by {@link DecafParser#arith_op}.
	 * @param ctx the parse tree
	 */
	void exitArith_op(DecafParser.Arith_opContext ctx);
	/**
	 * Enter a parse tree produced by {@link DecafParser#rel_op}.
	 * @param ctx the parse tree
	 */
	void enterRel_op(DecafParser.Rel_opContext ctx);
	/**
	 * Exit a parse tree produced by {@link DecafParser#rel_op}.
	 * @param ctx the parse tree
	 */
	void exitRel_op(DecafParser.Rel_opContext ctx);
	/**
	 * Enter a parse tree produced by {@link DecafParser#eq_op}.
	 * @param ctx the parse tree
	 */
	void enterEq_op(DecafParser.Eq_opContext ctx);
	/**
	 * Exit a parse tree produced by {@link DecafParser#eq_op}.
	 * @param ctx the parse tree
	 */
	void exitEq_op(DecafParser.Eq_opContext ctx);
	/**
	 * Enter a parse tree produced by {@link DecafParser#cond_op}.
	 * @param ctx the parse tree
	 */
	void enterCond_op(DecafParser.Cond_opContext ctx);
	/**
	 * Exit a parse tree produced by {@link DecafParser#cond_op}.
	 * @param ctx the parse tree
	 */
	void exitCond_op(DecafParser.Cond_opContext ctx);
}