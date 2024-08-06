import random

class Ambiente:
    def __init__(self):
        self.grid = [[0 for _ in range(5)] for _ in range(5)]
        self.objetivo = self.gerar_objetivo()
        self.gerar_obstaculos(3)

    def gerar_objetivo(self):
        while True:
            x = random.randint(0, 4)
            y = random.randint(0, 4)
            if (x, y) != (0, 0) and self.grid[x][y] == 0:  # O objetivo não deve estar na célula do agente e não deve ser um obstáculo
                return (x, y)

    def gerar_obstaculos(self, num_obstaculos):
        posicoes_disponiveis = [(x, y) for x in range(5) for y in range(5)]
        posicoes_disponiveis.remove((0, 0))  # Remover a posição inicial do agente
        posicoes_disponiveis.remove(self.objetivo)  # Remover a posição do objetivo

        for _ in range(num_obstaculos):
            if not posicoes_disponiveis:
                break
            posicao = random.choice(posicoes_disponiveis)
            posicoes_disponiveis.remove(posicao)
            self.grid[posicao[0]][posicao[1]] = 1  # 1 representa um obstáculo

    def mostrar_ambiente(self):
        for i, linha in enumerate(self.grid):
            linha_display = ''
            for j, celula in enumerate(linha):
                if (i, j) == self.objetivo:
                    linha_display += '* '  # Representa o objetivo
                elif celula == 1:
                    linha_display += '1 '  # Representa um obstáculo
                else:
                    linha_display += '0 '
            print(linha_display)
        print(f"Objetivo está na posição: {self.objetivo}")

class Agente:
    def __init__(self, ambiente):
        self.ambiente = ambiente
        self.posicao = [0, 0]  # Começa sempre na posição [0, 0]
        self.modelo_interno = [['None' for _ in range(5)] for _ in range(5)]  # Inicialmente, o modelo é todo '.' (vazio)
        self.atualizar_modelo()  # Atualiza o modelo com a posição inicial

    def atualizar_modelo(self):
        x, y = self.posicao
        if (x, y) == self.ambiente.objetivo:
            self.modelo_interno[x][y] = '*'  # Marca a célula do objetivo com '*'
        else:
            self.modelo_interno[x][y] = self.ambiente.grid[x][y]

    def mover(self, direcao):
        if direcao == 'cima' and self.posicao[0] > 0:
            self.posicao[0] -= 1
        elif direcao == 'baixo' and self.posicao[0] < 4:
            self.posicao[0] += 1
        elif direcao == 'esquerda' and self.posicao[1] > 0:
            self.posicao[1] -= 1
        elif direcao == 'direita' and self.posicao[1] < 4:
            self.posicao[1] += 1
        self.atualizar_modelo()

    def escolher_acao(self):
        objetivo = self.ambiente.objetivo
        x, y = self.posicao

        # Verifica as direções possíveis e calcula distâncias
        direcoes = []
        if x > 0:  # Cima
            direcao = 'cima'
            direcoes.append(direcao)
        if x < 4:  # Baixo
            direcao = 'baixo'
            direcoes.append(direcao)
        if y > 0:  # Esquerda
            direcao = 'esquerda'
            direcoes.append(direcao)
        if y < 4:  # Direita
            direcao = 'direita'
            direcoes.append(direcao)

        # Escolhe a melhor direção com base na distância até o objetivo
        melhor_direcao = None
        menor_distancia = float('inf')
        for direcao in direcoes:
            novo_x, novo_y = self.calcular_nova_posicao(direcao)
            if (0 <= novo_x < 5) and (0 <= novo_y < 5) and self.ambiente.grid[novo_x][novo_y] != 1:
                distancia = abs(novo_x - objetivo[0]) + abs(novo_y - objetivo[1])
                if distancia < menor_distancia:
                    menor_distancia = distancia
                    melhor_direcao = direcao

        if melhor_direcao:
            self.mover(melhor_direcao)

    def calcular_nova_posicao(self, direcao):
        x, y = self.posicao
        if direcao == 'cima':
            return (x - 1, y)
        elif direcao == 'baixo':
            return (x + 1, y)
        elif direcao == 'esquerda':
            return (x, y - 1)
        elif direcao == 'direita':
            return (x, y + 1)
        return (x, y)

    def agir(self):
        objetivo = self.ambiente.objetivo
        x, y = self.posicao

        if (x, y) == objetivo:
            self.modelo_interno[x][y] = '*'  # Marca a célula do objetivo com '*'
            print(f"Objetivo alcançado na posição {self.posicao}")
            return

        self.escolher_acao()

def main():
    ambiente = Ambiente()
    agente = Agente(ambiente)

    print("Estado inicial do ambiente:")
    ambiente.mostrar_ambiente()

    passos = 0
    while agente.posicao != list(ambiente.objetivo) and passos < 25:
        agente.agir()
        print("\nEstado do ambiente após a ação do agente:")
        ambiente.mostrar_ambiente()
        print("\nModelo interno do agente:")
        for linha in agente.modelo_interno:
            print(' '.join(str(celula) for celula in linha))
        passos += 1

    if agente.posicao == list(ambiente.objetivo):
        print("Objetivo alcançado!")
    else:
        print("Número máximo de passos alcançado. Objetivo não encontrado.")

if __name__ == "__main__":
    main()
