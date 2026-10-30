# Avaliação de Desempenho e Complexidade - MiniGit

## Tabela de Medição (Leitura vs. Escrita)

| commits | passos do commitar | passos do log |
| :--- | :--- | :--- |
| 10 | 2 | 10 |
| 100 | 2 | 100 |
| 1000 | 2 | 1000 |

## Análise Teórica

**1. Por que o commitar gasta sempre 2 passos, e o log gasta mais conforme o histórico cresce?**
O `commitar` apenas adiciona chaves em dicionários e atualiza um ponteiro, operações de custo constante ($O(1)$) que independem do tamanho do sistema. Já o `log` varre a árvore para ler o histórico, exigindo um custo linear ($O(N)$) que aumenta proporcionalmente à quantidade de commits existentes.

**2. Por que mensagem(commit) gasta 1 passo e buscar(texto) pode gastar muitos? O que o dicionário ganha quando se procura pela chave, e o que ele não ajuda quando se procura pelo valor?**
Procurar pela chave no dicionário (como faz o método `mensagem`) utiliza tabelas *hash*, o que permite encontrar o dado quase instantaneamente ($O(1)$). No entanto, o dicionário não indexa os valores internamente; por isso, procurar um texto específico na mensagem (`buscar`) obriga o algoritmo a iterar por todos os itens um a um, gastando muitos passos.

**3. Por que o merge é um commit com dois pais, e por que isso faz do histórico um grafo, e não uma lista?**
O merge unifica duas linhas do tempo paralelas do repositório, por isso precisa referenciar o commit da branch atual e o da branch mesclada. Ao introduzir nós com múltiplos apontamentos (arestas) convergindo ou divergindo, a estrutura linear de uma lista é quebrada, formando um Grafo Direcionado Acíclico (DAG).

**4. Por que o método pais devolve uma tupla, e não a lista que está guardada dentro do dicionário?**
Devolver uma tupla aplica o princípio do "retorno defensivo" no encapsulamento da classe. Como as tuplas são imutáveis, garantimos que um código externo não consiga alterar a lista original (por exemplo, usando `.append()`) e destruir a integridade da nossa árvore de histórico.