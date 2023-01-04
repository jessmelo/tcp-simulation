# simulacao de servidor tcp usando udp
import socket
import random
import time

localIP = "127.0.0.1"  # ip local
localPort = 8000  # porta local
bufferSize = 1024  # tamanho do buffer

# Inicializa o servidor no ip e porta desejada
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.bind((localIP, localPort))

# Guarda mensagens recebidas
received_messages = {}

# Inicializa o tamanho da janela de congestionamento
cwnd = 1

# Define o slow start threshold inicial
ssthresh = 64

# Inicializa o tamanho máximo da janela de recebimento
MAX_WINDOW_SIZE = 10

# Inicializa a variável de tempo total e pacotes recebidos
total_time = 0
total_packets = 0

while True:
    # Define tempo de inicio antes de um acknowledgment
    start_time = time.time()

    # Espera por um acknowledgment
    msg, addr = servidor.recvfrom(bufferSize)

    # Simulando perda de pacote
    if random.random() < 0.1:
        print("Pacote perdido! :(")
        cwnd = cwnd - 1  # Decrementa janela de congestionamento
        continue

    # Decodando mensagem recebida
    msg = msg.decode()
    # Numero de sequencia da mensagem
    msg_seq_num = msg[:5]

    # Encerra servidor
    if msg[5:] == "Fim":
        end_time = time.time()  # Guarda o tempo final depois de um acknowledgment
        elapsed_time = end_time - start_time  # Calcula o tempo da transmissao
        total_time += elapsed_time  # Guarda tempo total de transmissao
        break

    # Verifica se é uma retransmissao
    if msg_seq_num in received_messages:
        # Se for uma retransmissao, enviar confirmacao
        ack_num = msg_seq_num
        print(ack_num)
        servidor.sendto(str(ack_num).encode(), addr)

        total_packets += 1
    else:
        # Se é uma nova mensagem, guarda no dicionário
        received_messages[msg_seq_num] = msg[5:]

        # Envia a confirmacao de recebimento da mensagem
        ack_num = msg_seq_num
        servidor.sendto(str(ack_num).encode(), addr)

        # Imprime a mensagem do cliente
        clientMsgSeqNum = "Mensagem do cliente: {}".format(msg[5:])
        clientMsg = "Número de sequência do pacote: {}".format(msg[:5])
        clientIP = "Endereço IP do cliente: {}".format(addr)

        total_packets += 1

        end_time = time.time()  # Guarda o tempo final depois de um acknowledgment
        elapsed_time = end_time - start_time  # Calcula o tempo da transmissao
        total_time += elapsed_time  # Guarda tempo total de transmissao

        print(clientMsgSeqNum)
        print(clientMsg)
        print(clientIP)


# Calcula o tempo médio de transmissão
avg_time = total_time / total_packets

# Resultados finais
print(f'Total de pacotes transmitidos: {total_packets}')
print(f'Tempo total de transmissão: {total_time} segundos')
print(f'Tempo médio de transmissão: {avg_time} segundos')
