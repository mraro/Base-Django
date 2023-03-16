import socket
import pysrt
import subprocess

# Defina as configurações do servidor
HOST = 'localhost'  # Endereço IP do servidor
PORT = 9999  # Porta do servidor
BUFFER_SIZE = 1024  # Tamanho do buffer

# Defina as configurações do sinal de vídeo SDI
SDI_DEVICE = '/dev/video0'  # Dispositivo de entrada do sinal SDI
SDI_CODEC = 'dnxhd'  # Codec a ser usado para codificar o sinal SDI
SDI_BITRATE = '36M'  # Taxa de bits do sinal SDI

# Crie o socket do servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f'Servidor iniciado em {HOST}:{PORT}')

    # Aceite conexões de clientes
    conn, addr = s.accept()
    with conn:
        print(f'Conexão estabelecida de {addr}')

        # Inicie o loop para receber e enviar dados
        while True:
            data = conn.recv(BUFFER_SIZE)  # Receba dados do cliente
            if not data:
                break
            print(f'Dados recebidos do cliente: {data.decode()}')

            # Decodifique os dados SRT
            subs = pysrt.from_string(data.decode())

            # Extraia a legenda e a mídia
            subtitle = subs[0].text if len(subs) > 0 else ''
            media = subs[1].text if len(subs) > 1 else ''

            # Adicione o código aqui para processar a legenda e a mídia, por exemplo:
            # - Carregue a mídia de um arquivo ou URL
            # - Adicione a legenda à mídia
            # - Codifique a mídia usando um codec de vídeo adequado
            # - Transmita a mídia usando o sinal de vídeo SDI

            # Codifique a mídia usando o codec DNxHD
            ffmpeg_cmd = [
                'ffmpeg',
                '-i', media,
                '-c:v', SDI_CODEC,
                '-b:v', SDI_BITRATE,
                '-f', 'sdi',
                SDI_DEVICE
            ]
            subprocess.run(ffmpeg_cmd, check=True)

            # Encode os dados SRT
            encoded_data = subs.to_srt().encode()

            # Envie os dados de volta para o cliente
            conn.sendall(encoded_data)

print('Conexão encerrada')