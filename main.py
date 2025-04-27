import random

# --- Modelagem dos Objetos do Jogo ---

class Bola:
    def __init__(self, x, y, velocidade_x=0, velocidade_y=0):
        self.x = x
        self.y = y
        self.velocidade_x = velocidade_x
        self.velocidade_y = velocidade_y

    def mover(self):
        self.x += self.velocidade_x
        self.y += self.velocidade_y

    def movendo_direcao_gol(self):
        return self.velocidade_x < 0

class Goleiro:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def mover_para(self, bola):
        # Movimento básico: tentar alinhar a posição Y com a bola
        if self.y < bola.y:
            self.y += 1
        elif self.y > bola.y:
            self.y -= 1

    def tentar_defesa(self, bola):
        return abs(self.x - bola.x) <= 1 and abs(self.y - bola.y) <= 1

# --- Simulação ---

def simular_jogo():
    goleiro = Goleiro(1, 3)
    bola = Bola(10, random.randint(0,6), velocidade_x=-1)

    defesas = 0
    gols_sofridos = 0

    for tempo in range(15):
        print(f"\nTempo {tempo+1}")
        bola.mover()
        goleiro.mover_para(bola)

        print(f"Posição da Bola: ({bola.x:.1f}, {bola.y:.1f})")
        print(f"Posição do Goleiro: ({goleiro.x}, {goleiro.y})")

        if bola.x <= 1:  # Bola chegou na área do gol
            if goleiro.tentar_defesa(bola):
                print("\033[92mDEFESA!\033[0m")
                defesas += 1
            else:
                print("\033[91mGOL SOFRIDO!\033[0m")
                gols_sofridos += 1
            break  # Fim do episódio

    print(f"\nResultado Final: Defesas = {defesas}, Gols Sofridos = {gols_sofridos}")

if __name__ == "__main__":
    simular_jogo()
