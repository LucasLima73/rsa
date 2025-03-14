import ast
from socket import *
import random
from math import gcd

# Funções auxiliares para o RSA

def is_prime(n, k=10):
    """ Teste de primalidade usando Miller-Rabin. """
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
    """ Gera um número primo com o número de bits especificado. """
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

# Gera par de chaves do cliente
public_key_client, private_key_client = generate_keys()

# Conecta ao servidor
serverName = "10.1.70.25"
serverPort = 1300
clientSocket = socket(AF_INET, SOCK_STREAM)

print("🔹 Tentando conectar ao servidor...")
try:
    clientSocket.connect((serverName, serverPort))
    print("🔹 Conexão estabelecida com o servidor.")
except Exception as e:
    print(f"Erro ao conectar ao servidor: {e}")
    exit()

# Envia chave pública do cliente para o servidor
try:
    print("🔹 Enviando chave pública do cliente para o servidor...")
    clientSocket.send(f"{public_key_client[0]} {public_key_client[1]}".encode())
    print("🔹 Chave pública do cliente enviada.")
except Exception as e:
    print(f"Erro ao enviar chave pública do cliente: {e}")
    clientSocket.close()
    exit()

# Recebe chave pública do servidor
try:
    print("🔹 Aguardando chave pública do servidor...")
    server_key_data = clientSocket.recv(1024).decode()
    print(f"🔹 Chave pública do servidor recebida: {server_key_data}")
    n_server, e_server = map(int, server_key_data.split())
except Exception as e:
    print(f"Erro ao receber chave pública do servidor: {e}")
    clientSocket.close()
    exit()

while True:
    # Lê e criptografa mensagem
    sentence = input("🔹 Digite uma frase (ou 'sair' para encerrar): ")
    if sentence.lower() == 'sair':
        print("🔹 Conexão encerrada.")
        break
    
    encrypted_message = encrypt(sentence, e_server, n_server)

    # Envia mensagem criptografada
    try:
        print(f"🔹 Enviando mensagem criptografada: {encrypted_message}")
        clientSocket.send(str(encrypted_message).encode())
    except Exception as e:
        print(f"Erro ao enviar mensagem criptografada: {e}")
        break

    # Recebe mensagem criptografada do servidor
    try:
        print("🔹 Aguardando resposta do servidor...")
        encrypted_response = clientSocket.recv(65000).decode()
        print(f"🔹 Mensagem criptografada recebida do servidor: {encrypted_response}")
        
        # Verifica se a resposta não está vazia
        if not encrypted_response.strip():
            print("🔹 Resposta vazia recebida do servidor. Verifique o servidor.")
            break
        
        # Tenta avaliar a resposta de forma segura
        encrypted_response = ast.literal_eval(encrypted_response)
    except Exception as e:
        print(f"Erro ao processar resposta do servidor: {e}")
        break

    # Descriptografa resposta usando chave privada do cliente
    decrypted_response = decrypt(encrypted_response, private_key_client[1], private_key_client[0])

    print(f"🔹 Mensagem descriptografada: {decrypted_response}")

# Fecha conexão
clientSocket.close()
