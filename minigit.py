class Minigit():
    __slots__ = ['_pais','_mensagem','_branch','_contador','_passos','_branch_atual']

    def __init__(self):
        self._pais = dict() # mapeia id do commit -> [lista_pais]
        self._mensagem = dict() # mapeia id do commit -> "mensagem do commit"
        self._branch = {'main': None}
        self._contador = 0
        self._passos = 1
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
        self._passos = 1
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
        
        self._mensagens[id_commit] = f"merge de {nome}"
        self._branches[self._branch_atual] = id_commit
        
        self._passos = 1
        return id_commit


    @property
    def branch_atual(self):
        self._passos = 1
        return self._branch_atual
    
r = Minigit()
r.passos = 1
