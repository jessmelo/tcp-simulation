# simulacao de cliente tcp usando udp
import socket
import time

# Inicializa o cliente
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

seq_num = 0  # Inicializa o numero de sequencia da mensagem
server_address = ("127.0.0.1", 8000)  # IP do servidor
bufferSize = 1024  # Tamanho do buffer

while True:
    # Recebe o input do usuário
    message = input("Mensagem para o servidor: ")

    # Incrementa o numero de sequencia da mensagem
    seq_num += 1

    # Adiciona o numero de sequencia na mensagem a ser enviada
    data = str(seq_num).zfill(5) + message

    # Envia a mensagem para o servidor
    cliente.sendto(data.encode(), server_address)

    # Espera a confirmacao de recebimento do servidor
    cliente.settimeout(1.0)
    try:
        ack, _ = cliente.recvfrom(1024)
        ack = ack.decode()
        ack_num = int(ack)

        # Se o servidor confirmar o recebimento da mensagem enviada, imprime que foi recebida
        if ack_num == seq_num:
            print("Mensagem recebida pelo servidor! Número de sequência do pacote: {}".format(ack))
    except socket.timeout:
        # Se ocorrer timeout, reenvia mensagem
        print("Timeout, retransmitindo mensagem")
        cliente.sendto(data.encode(), server_address)
