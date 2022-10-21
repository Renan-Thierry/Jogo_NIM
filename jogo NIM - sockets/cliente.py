import socket
import pickle

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_servidor = '127.0.0.1'
porta_servidor = 5300 
dest = (ip_servidor, porta_servidor)
tcp.connect(dest) 

def imprimeParametros(n, m):
    print("\n=============================================================",end='\n')
    print("\n===== ♠  BEM-VINDO AO JOGO DO NIM! - CLIENT/JOGADOR 2 ♠ ===== ",end='\n')
    print("\n=============================================================",end='\n\n')
    print("A partida está configurada com os seguintes parâmetros:", end='\n\n')
    print(f"1- Número de peças: {n} peças\n")
    print(f"2- Peças por jogada: 1 a {m} peças\n")

def decisionOddOrEven():
    print("\n========== QUEM COMEÇA O JOGO? ==========  \n")
    print("Vamos decidir por impar ou par:\n")
    print("\t [0] - Ímpar\n")
    print("\t [1] - PAR\n\n")

    escolha = int(input("➔ Digite a opção [0 ou 1]: "))
    
    while (escolha != 0) & (escolha != 1):
        print("\n !!! A opção escolhida é inválida !!!\n")
        print("\t [0] - Ímpar\n")
        print("\t [1] - PAR\n")
        escolha = int(input("➔ Digite novamente [0 ou 1]: "))
    return escolha

def infoPlayerStartGame(player):
    print("\n\n========== START GAME ==========\n")

    if (player == 'player2'):
        print("O jogador 2 (client) ganhou o ímpar ou par e iniciará o jogo")
    else:
        print("O jogador 1 (server) ganhou o ímpar ou par e iniciará o jogo")


def usuario_escolhe_jogada():
      """
      - Solicita quantas peças o usuário irá tirar
      - Verifica a validade dos parâmetros
      - Retorna o valor de peças retiradas
      """
      numero = int(input('\n\n➔ Quantas peças você vai tirar? '))

      while numero > numPecas or numero > limitePecas or numero <= 0:
          print("\nOops! Jogada inválida! Tente de novo.")
          numero = int(input("\n➔ Quantas peças você vai tirar? "))

      return numero

def theEnd(ganhador):
      if (ganhador):
        print("\n\n================================\n")
        print("🏆🏆🏆 VOCÊ GANHOU!!🏆🏆🏆")
        print("\n================================\n")
      else:
        print("\n\n================================\n") 
        print("❌❌❌ VOCÊ PERDEU! ❌❌❌")
        print("\n================================\n")

# ==========================================================

numPecas, limitePecas = pickle.loads(tcp.recv(24))        # Parametros do jogo
imprimeParametros(numPecas, limitePecas)                  # Imprime parametros
odd_or_even = decisionOddOrEven()                         # Decisão de quem começa o jogo - Impar ou par
tcp.send(odd_or_even.to_bytes(16,'big'))                  # Envia um inteiro para indicar a escolha do impar ou par
resp1 = tcp.recv(1024)                                    # Recebendo a decisão de quem começa o jogo
initial_player = resp1.decode()
infoPlayerStartGame(initial_player)                       # Emite informação de quem começa o jogo
 
# =========================================================================

firstTime = None

if initial_player == 'player2':
    retirada = usuario_escolhe_jogada()
    print(f"\n\tVocê tirou {retirada} peça(s).")
    
    numPecas = numPecas - retirada
    print(f"\n\tAgora restam {numPecas} peças no tabuleiro.")
    tcp.send(numPecas.to_bytes(16, 'big'))
   
else:
    firstTime = True

while ((numPecas > 0) or firstTime):
    firstTime = False
    numPecas_server = int.from_bytes(tcp.recv(16), 'big')   
    jogada_anterior_restantes = numPecas - numPecas_server
    numPecas = numPecas_server

    if (numPecas == 0):
        theEnd(False)
        break
    
    print("\n================================\n")
    print(f"\n\tO player 1 tirou {jogada_anterior_restantes} peça(s).")
    print(f"\n\tAgora restam {numPecas} peças no tabuleiro.")
    
    if (numPecas == 0):
        theEnd(False)
        break
    
    retirada = usuario_escolhe_jogada()
    print(f"\n\tVocê tirou {retirada} peça(s).")
    
    numPecas = numPecas - retirada

    if (numPecas == 0):
        theEnd(True)
        break

    print(f"\n\tAgora restam {numPecas} peças no tabuleiro.")

    tcp.send(numPecas.to_bytes(16, 'big'))
    
# =========================================================================    

tcp.close()
input("aperte enter para encerrar")