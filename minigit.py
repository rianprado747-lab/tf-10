from collections import deque
class Minigit():
    __slots__ = ['_pais','_mensagem','_branch','_contador','_passos','_branch_atual']

    def __init__(self):
        self._pais = dict() # mapeia id do commit -> [lista_pais]
        self._mensagem = dict() # mapeia id do commit -> "mensagem do commit"
        self._branch = {'main': None}
        self._contador = 0
        self._passos = 0
        self._branch_atual = 'main'


    def commitar(self, mensagem):
        if not mensagem:
            raise ValueError('A mensagem não pode ser vazia')
        self._contador += 1
        id_commit = f'c{self._contador}'
        pai_atual = self._branch[self._branch_atual]

        if pai_atual is None:
            self._pais[id_commit] = []
        else:
            self._pais[id_commit] = [pai_atual]
        self._mensagem[id_commit] = mensagem
        self._branch[self._branch_atual] = id_commit
        self._passos = 2
        return id_commit


    def mensagem(self, commit):
        if commit not in self._mensagem:
            raise ValueError(f"O commit {commit} não existe.")
        self._passos = 1
        return self._mensagem[commit]

    def pais(self, commit):
        if commit not in self._pais:
            raise ValueError(f"O commit {commit} não existe.")
        self._passos = 1
        return tuple(self._pais[commit])

    @property
    def passos(self):
        return self._passos


    def criar_branch(self,nome):
        if nome in self._branch:
            raise ValueError(f'A branch {nome} já existe.')

        commit_atual = self._branch[self._branch_atual]

        if commit_atual is None:
            raise ValueError('Não é possivrel criar uma branch em um repósitorio sem commits.')

        self._branch[nome] = commit_atual

        self._passos = 1


    def trocar_branch(self,nome):
        if nome not in self._branch:
            raise ValueError(f'a branch {nome} não existe.')
        self._branch_atual = nome
        self._passos = 1


    def mesclar(self,nome):
        if nome not in self._branch:
            raise ValueError(f'a branch {nome} não existe.')
        if nome == self._branch_atual:
            raise ValueError(f'não é possivel mesclar a branch atual com ela mesma.')

        commit_atual = self._branch[self._branch_atual]
        commit_alvo = self._branch[nome]

        self._contador += 1
        id_commit = f"c{self._contador}"
        
        # a lista de pais tem DOIS elementos
        self._pais[id_commit] = [commit_atual, commit_alvo]
        
        self._mensagem[id_commit] = f"merge de {nome}"
        self._branch[self._branch_atual] = id_commit
        
        self._passos = 2
        return id_commit


    @property
    def branch_atual(self):
        self._passos = 1
        return self._branch_atual


    def log(self):
        commit_inicial = self._branch[self._branch_atual]
        if commit_inicial is None:
            self._passos = 0
            return()

        fila = deque([commit_inicial])
        anotados = set()
        resultado = []

        while fila:
            atual = fila.popleft()

            if atual not in anotados:
                anotados.add(atual)
                resultado.append(atual)

                for pai in self._pais[atual]:
                    fila.append(pai)

        self._passos = len(resultado)
        return tuple(resultado)

    def buscar(self, texto):
        passos_gastos = 0 
        for i in range (1, self._contador + 1):
            passos_gastos += 1
            id_commit = f'c{i}'

            if texto in self._mensagem[id_commit]:
                self._passos = passos_gastos
                return id_commit

        self._passos = passos_gastos
        return None


    def merges(self):
        passos = 0
        resultado = []

        for i in range(1, self._contador + 1):
            passos += 1
            id_commit = f'c{i}'

            if len(self._pais[id_commit]) > 1:
                resultado.append(id_commit)

        self._passos = passos 
        return tuple(resultado)
    

if __name__ == "__main__":
    # ==========================================
    # 1. ROTEIRO DE TESTES BÁSICO E TRATAMENTO DE ERROS
    # ==========================================
    def tentar(acao):
        try:
            acao()
        except ValueError as erro:
            print("erro:", erro)

    git = Minigit()
    git.commitar("primeiro commit")
    print(git.passos)
    git.commitar("segundo commit")
    git.criar_branch("feature")
    print(git.passos)
    git.commitar("terceiro commit")
    git.trocar_branch("feature")
    git.commitar("quarto commit")
    git.trocar_branch("main")
    git.mesclar("feature")
    
    print(git.pais("c5"))
    print(git.log(), git.passos)
    print(git.mensagem("c3"), git.passos)
    print(git.buscar("quarto"), git.passos)
    print(git.merges())
    
    git.trocar_branch("feature")
    print(git.log(), git.passos)
    git.trocar_branch("main")

    # Tentativas que devem falhar e imprimir o erro
    tentar(lambda: git.trocar_branch("inexistente"))
    tentar(lambda: git.criar_branch("main"))
    tentar(lambda: git.mesclar("main"))
    tentar(lambda: git.pais("c99"))

    print("\n" + "="*50 + "\n")

    # ==========================================
    # 2. MEDIÇÃO DE COMPLEXIDADE (LEITURA VS ESCRITA)
    # ==========================================
    def medir(quantidade):
        repo_teste = Minigit()
        for i in range(quantidade):
            repo_teste.commitar(f"commit {i}")
            
        passos_commitar = repo_teste.passos
        repo_teste.log()
        passos_log = repo_teste.passos
        
        return passos_commitar, passos_log

    print("commits   passos do commitar   passos do log")
    for qtd in [10, 100, 1000]:
        p_com, p_log = medir(qtd)
        # Formatação de string para alinhar a tabela corretamente
        print(f"{qtd:<10}{p_com:<21}{p_log}")
