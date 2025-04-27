import random

# classes do jogo

class Bola:
    def __init__(self, x, y, velocidade_x=0):
        self.x = x
        self.y = y
        self.velocidade_x = velocidade_x

    def mover(self):
        self.x += self.velocidade_x

class GoleiroAprendiz:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.q_table = {}
        self.acoes = ['subir', 'descer', 'ficar']

    def estado(self, bola):
        return self.y - bola.y

    def escolher_acao(self, estado, exploracao=0.2):
        if random.random() < exploracao or estado not in self.q_table:
            return random.choice(self.acoes)
        return max(self.q_table[estado], key=self.q_table[estado].get)

    def agir(self, acao):
        if acao == 'subir':
            self.y += 1
        elif acao == 'descer':
            self.y -= 1

    def tentar_defesa(self, bola):
        return abs(self.x - bola.x) <= 1 and abs(self.y - bola.y) <= 1

    def atualizar_q_table(self, estado, acao, recompensa, novo_estado, alpha=0.1, gamma=0.9):
        if estado not in self.q_table:
            self.q_table[estado] = {a: 0 for a in self.acoes}
        if novo_estado not in self.q_table:
            self.q_table[novo_estado] = {a: 0 for a in self.acoes}
        futuro = max(self.q_table[novo_estado].values())
        self.q_table[estado][acao] += alpha * (recompensa + gamma * futuro - self.q_table[estado][acao])

# simulacao

def simular_jogo(epocas=300):
    defesas = 0
    gols_sofridos = 0

    goleiro = GoleiroAprendiz(1, 3)

    for epoca in range(1, epocas + 1):
        bola = Bola(10, random.randint(0,6), velocidade_x=-1)

        for tempo in range(20):
            estado = goleiro.estado(bola)
            acao = goleiro.escolher_acao(estado)
            goleiro.agir(acao)
            bola.mover()
            novo_estado = goleiro.estado(bola)

            if bola.x <= 1:
                if goleiro.tentar_defesa(bola):
                    recompensa = 1
                    defesas += 1
                else:
                    recompensa = -1
                    gols_sofridos += 1

                goleiro.atualizar_q_table(estado, acao, recompensa, novo_estado)
                break
            else:
                goleiro.atualizar_q_table(estado, acao, -0.01, novo_estado)

        # a cada 50 partidas, imprime o desempenho atual
        if epoca % 50 == 0:
            taxa_sucesso = (defesas / epoca) * 100
            print(f"Após {epoca} partidas: Defesas = {defesas}, Gols sofridos = {gols_sofridos}, Sucesso = {taxa_sucesso:.2f}%")

    print(f"\nResultados Finais após {epocas} jogos:")
    print(f"Defesas: {defesas}")
    print(f"Gols sofridos: {gols_sofridos}")
    print(f"Taxa de sucesso final: {(defesas / epocas) * 100:.2f}%")

if __name__ == "__main__":
    try:
        epocas = int(input("Digite o número de partidas para treinar o goleiro: "))
        simular_jogo(epocas)
    except ValueError:
        print("Por favor, digite um número inteiro válido.")