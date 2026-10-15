import time
from exnovaapi.stable_api import Exnova

# === CONFIGURAÇÃO EXNOVA 
EMAIL = ""
SENHA = ""
CONTA = "DEMO"
# === SUA GESTÃO - VERSÃO ÚNICA ===
G1 = 6.00
G2 = 18.00
G3 = 89.64
G4 = 132.91  # REC

VALOR_ENTRADA = G1
STOP_WIN = 50.00
STOP_LOSS = 30.00

API = None
lucro_total = 0

def conectar():
    global API
    API = Exnova(EMAIL, SENHA)
    check, reason = API.connect()
    if check:
        API.change_balance(CONTA)
        print(f"Conectado! Saldo {CONTA}: {API.get_balance()}")
        return True
    print(f"Erro conexao: {reason}")
    return False

def operar(par="EURUSD-OTC", direcao="call", valor=G1):
    global lucro_total
    API.buy(valor, par, direcao, 1)
    id = API.get_order_id()
    print(f"Entrada {direcao} {par} R$ {valor}")
    resultado = API.check_win_v4(id)
    if resultado == "win":
        lucro_total += valor * 0.8
        print(f"WIN! Lucro: {lucro_total}")
        return True
    else:
        lucro_total -= valor
        print(f"LOSS! Lucro: {lucro_total}")
        return False

def banca_gestao():
    global VALOR_ENTRADA
    # Tenta G1
    if not operar(valor=G1):
        # G2
        if not operar(valor=G2):
            # G3 x3 = LUCRO - 3 tentativas no G3
            win_g3 = False
            for i in range(3):
                if operar(valor=G3):
                    win_g3 = True
                    break
            if not win_g3:
                # G4 RECUPERAÇÃO
                operar(valor=G4)
    
while True:
    if not conectar():
        time.sleep(5)
        continue
    
    # SEU SINAL AQUI - exemplo MHI
    # Troca por sua estratégia
    banca_gestao()
    
    if lucro_total >= STOP_WIN or lucro_total <= -STOP_LOSS:
        print("Meta batida! Parando.")
        break
    time.sleep(60)
