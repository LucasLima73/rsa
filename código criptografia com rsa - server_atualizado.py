from socket import *
import random
from math import gcd

# Funções auxiliares para o RSA (mesmas do client)

def is_prime(n, k=10):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    def check(a):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return True
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                return True
        return False

    for _ in range(k):
        a = random.randint(2, n - 2)
        if not check(a):
            return False
    return True

def generate_prime(bits):
    while True:
        num = random.getrandbits(bits)
        if is_prime(num):
            return num

def generate_keys():
    p = generate_prime(16)
    q = generate_prime(16)
    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(2, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)

    d = pow(e, -1, phi)

    return (n, e), (n, d)

def encrypt(message, e, n):
    return [pow(ord(char), e, n) for char in message]

def decrypt(cipher, d, n):
    return ''.join([chr(pow(char, d, n)) for char in cipher])

# Gera par de chaves do servidor
public_key_server, private_key_server = generate_keys()

# Configura servidor
serverPort = 1300
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(5)

print("🔹 TCP Server Iniciado...\n")

while True:  # Loop para continuar aceitando novas conexões
    # Aceita conexão do cliente
    connectionSocket, addr = serverSocket.accept()

    print(f"🔹 Conexão estabelecida com: {addr}")

    # Recebe chave pública do cliente
    client_key_data = connectionSocket.recv(1024).decode()
    n_client, e_client = map(int, client_key_data.split())

    # Envia chave pública do servidor para o cliente
    connectionSocket.send(f"{public_key_server[0]} {public_key_server[1]}".encode())

    while True:  # Loop interno para receber e responder múltiplas mensagens
        try:
            # Recebe mensagem criptografada do cliente
            encrypted_message = eval(connectionSocket.recv(65000).decode())
            
            # Se o cliente desconectar (conexão fechada), sai do loop
            if not encrypted_message:
                print("🔹 Cliente desconectado")
                break

            # Descriptografa mensagem com chave privada do servidor
            decrypted_message = decrypt(encrypted_message, private_key_server[1], private_key_server[0])

            print(f"🔹 Mensagem criptografada recebida do cliente: {encrypted_message}")
            print(f"🔹 Mensagem descriptografada do cliente: {decrypted_message}")

            # Transforma em maiúsculas
            capitalized_message = decrypted_message.upper()

            # Recriptografa com chave pública do cliente
            encrypted_response = encrypt(capitalized_message, e_client, n_client)

            # Envia mensagem criptografada de volta para o cliente
            connectionSocket.send(str(encrypted_response).encode())

            print(f"🔹 Mensagem transformada em maiúsculas: {capitalized_message}")
            print(f"🔹 Mensagem criptografada enviada ao cliente: {encrypted_response}")

        except Exception as e:
            print(f"🔹 Erro ao receber ou processar mensagem: {e}")
            break

    # Fecha a conexão após o cliente desconectar ou erro
    connectionSocket.close()
    print(f"🔹 Conexão com {addr} fechada.\n")
