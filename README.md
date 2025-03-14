# Sistema de Comunicação Seguro com RSA

Este projeto implementa um sistema de comunicação seguro entre um **servidor** e um **cliente** utilizando o algoritmo RSA (Rivest-Shamir-Adleman) para criptografia e descriptografia de mensagens. O servidor e o cliente se comunicam através de uma rede TCP, realizando troca de mensagens criptografadas.

### Tecnologias Utilizadas

- **Python 3**: Linguagem de programação utilizada para implementação.
- **Socket Programming**: Para a comunicação entre o servidor e o cliente.
- **Criptografia RSA**: Para garantir a segurança da comunicação, utilizando chaves públicas e privadas.

---

## Estrutura do Código

### 1. **Servidor (Server)**

O servidor é responsável por gerar seu par de chaves públicas e privadas, receber as chaves públicas do cliente, realizar a troca de mensagens criptografadas e enviar as respostas. Ele utiliza o algoritmo RSA para criptografar e descriptografar as mensagens.

#### Funções principais do servidor:

- **`is_prime(n, k=10)`**: Verifica se um número `n` é primo utilizando o teste de primalidade Miller-Rabin.
  
- **`generate_prime(bits)`**: Gera um número primo aleatório com o número de bits especificado.
  
- **`generate_keys()`**: Gera o par de chaves pública e privada do servidor.

- **`encrypt(message, e, n)`**: Criptografa a mensagem `message` usando a chave pública `(e, n)`.

- **`decrypt(cipher, d, n)`**: Descriptografa a mensagem criptografada `cipher` usando a chave privada `(d, n)`.

#### Funcionamento do Servidor:

1. O servidor gera um par de chaves RSA (pública e privada).
2. Inicia o socket TCP, aguardando conexões de clientes na porta 1300.
3. Quando uma conexão é estabelecida, o servidor recebe a chave pública do cliente e envia a sua chave pública de volta.
4. O servidor então recebe mensagens criptografadas do cliente, as descriptografa usando sua chave privada, transforma a mensagem em maiúsculas e reenvia a resposta criptografada ao cliente.

### 2. **Cliente (Client)**

O cliente gera seu par de chaves RSA (pública e privada), conecta-se ao servidor e troca mensagens criptografadas com o servidor. O cliente envia uma mensagem criptografada, recebe a resposta criptografada e a descriptografa.

#### Funções principais do cliente:

- **`is_prime(n, k=10)`**: Função auxiliar que realiza o teste de primalidade Miller-Rabin, similar à função do servidor.
  
- **`generate_prime(bits)`**: Função para gerar um número primo aleatório com o número de bits especificado.
  
- **`generate_keys()`**: Gera o par de chaves pública e privada do cliente.

- **`encrypt(message, e, n)`**: Criptografa a mensagem utilizando a chave pública `(e, n)` do servidor.

- **`decrypt(cipher, d, n)`**: Descriptografa a mensagem usando a chave privada `(d, n)` do cliente.

#### Funcionamento do Cliente:

1. O cliente gera um par de chaves RSA.
2. Conecta-se ao servidor na porta 1300.
3. Envia sua chave pública ao servidor.
4. Recebe a chave pública do servidor.
5. O cliente então criptografa uma mensagem, a envia ao servidor e aguarda a resposta.
6. A resposta do servidor, que está criptografada, é recebida e descriptografada utilizando a chave privada do cliente.

---

## Como Executar

### 1. **Servidor:**

1. Salve o código do servidor em um arquivo, por exemplo `server.py`.
2. Abra um terminal e execute o servidor com o comando:

   ```bash
   python server.py
