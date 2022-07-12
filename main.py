from sly import Lexer
from sly import Parser


class BasicLexer(Lexer):
    tokens = {નામ, નંબર , શબ્દ}
    ignore = '\t '
    literals = {'=', '+', '-', '/',
                '*', '(', ')', ',', ';'}

    # Define tokens as regular expressions
    # (stored as raw strings)
     નામ= r'[ક-જ્ઞ][ક-જ્ઞ0-9_]*'
    શબ્દ= r'\".*?\"'

    # Number token
    @_(r'\d+')
    def NUMBER(self, t):
        # convert it into a python integer
        t.value = int(t.value)
        return t

    # Comment token
    @_(r'//.*')
    def COMMENT(self, t):
        pass

    # Newline token(used only for showing
    # errors in new line)
    @_(r'\n+')
    def newline(self, t):
        self.lineno = t.value.count('\n')

class BasicParser(Parser):
	#tokens are passed from lexer to parser
	tokens = BasicLexer.tokens

	precedence = (
		('left', '+', '-'),
		('left', '*', '/'),
		('right', 'UMINUS'),
	)

	def __init__(self):
		self.env = { }

	@_('')
	def statement(self, p):
		pass

	@_('var_assign')
	def statement(self, p):
		return p.var_assign

	@_('નામ "=" expr')
	def var_assign(self, p):
		return ('var_assign', p.નામ, p.expr)

	@_('નામ "=" STRING')
	def var_assign(self, p):
		return ('var_assign', p.નામ, p.STRING)

	@_('expr')
	def statement(self, p):
		return (p.expr)

	@_('expr "+" expr')
	def expr(self, p):
		return ('add', p.expr0, p.expr1)

	@_('expr "-" expr')
	def expr(self, p):
		return ('sub', p.expr0, p.expr1)

	@_('expr "*" expr')
	def expr(self, p):
		return ('mul', p.expr0, p.expr1)

	@_('expr "/" expr')
	def expr(self, p):
		return ('div', p.expr0, p.expr1)

	@_('"-" expr %prec UMINUS')
	def expr(self, p):
		return p.expr

	@_('નામ')
	def expr(self, p):
		return ('var', p.નામ)

	@_('નંબર')
	def expr(self, p):
		return ('num', p.નંબર)


class BasicExecute:
    def __init__(self, tree, env):
        self.env = env
        result = self.walkTree(tree)
        if result is not None and isinstance(result, int):
            print(result)
        if isinstance(result, str) and result[0] == '"':
            print(result)

    def walkTree(self, node):

        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node

        if node is None:
            return None

        if node[0] == 'program':
            if node[1] == None:
                self.walkTree(node[2])
            else:
                self.walkTree(node[1])
                self.walkTree(node[2])

        if node[0] == 'નં':
            return node[1]

        if node[0] == 'શબ્દ':
            return node[1]

        if node[0] == 'સરવાળો':
            return self.walkTree(node[1]) + self.walkTree(node[2])
        elif node[0] == 'બાદબાકી':
            return self.walkTree(node[1]) - self.walkTree(node[2])
        elif node[0] == 'ગુણાકાર':
            return self.walkTree(node[1]) * self.walkTree(node[2])
        elif node[0] == 'div':
            return self.walkTree(node[1]) / self.walkTree(node[2])

        if node[0] == 'var_assign':
            self.env[node[1]] = self.walkTree(node[2])
            return node[1]

        if node[0] == 'var':
            try:
                return self.env[node[1]]
            except LookupError:
                print("Undefined variable '" + node[1] + "' found!")
                return 0


if __name__ == '__main__':
    lexer = BasicLexer()
    parser = BasicParser()
    print('Tiger Language')
    env = {}

    while True:

        try:
            text = input('Tiger Language > ')

        except EOFError:
            break

        if text:
            tree = parser.parse(lexer.tokenize(text))
            BasicExecute(tree, env)

