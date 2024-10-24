import argparse
import socket
import tqdm
import os
import time

def start_server(host, port,file_):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    print(f"Server {host}:{port} da ishlamoqda...")
    
    conn, addr = s.accept()
    print(f"Ulangan: {addr}")
    
    # Faylni qabul qilish jarayoni
    received_file_size = int(conn.recv(1024).decode())
    print(f"Qabul qilinadigan fayl hajmi: {received_file_size} bayt")
    
    progress = tqdm.tqdm(range(received_file_size), f"Qabul qilinmoqda", unit="B", unit_scale=True, unit_divisor=1024)
    
    with open(file_, 'wb') as f:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            f.write(data)
            progress.update(len(data))
        print("Fayl qabul qilindi")
        f.close()
    
    conn.close()
    s.close()




#============================================================================================================
#============================================================================================================
#============================================================================================================



def send_file(host, port, file_path):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    file_size = os.path.getsize(file_path)
    s.send(f"{file_size}".encode())

    progress = tqdm.tqdm(range(file_size),f"Jo'natilmoqda: {os.path.basename(file_path)}",unit = "B",unit_scale = True,unit_divisor = 1024)
    
    with open(file_path, 'rb') as f:

        while True:
            data = f.read(1024)
            if not data:
                break
            s.sendall(data)
            progress.update(len(data))
        print("Fayl jo'natildi")
        f.close()
    s.close()




#============================================================================================================
#============================================================================================================
#============================================================================================================




def main():
    
    parser = argparse.ArgumentParser(description='in and out data')
    parser.add_argument('--ip', type=str, help='IP manzilni kiriting')
    parser.add_argument('--f', type=str,required=False, help='fayl yo`lini ko`rsating')
    args = parser.parse_args()

    host = args.ip
    port = 12345

    if args.f == None:

        server_socket = socket.socket()  
        server_socket.bind((host, port))
        server_socket.listen(1) 
        conn,adress = server_socket.accept()
        file_name = ""
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            file_name = str(data)
            with open(data,'w') as f:
                pass
            f.close()
        conn.close()
        server_socket.close()
        start_server(host=host,port=port,file_=file_name)

    else:
    
        file_name = os.path.basename(args.f)
        client_socket = socket.socket()
        client_socket.connect((host, port))
        client_socket.send(file_name.encode())
        client_socket.close()
        time.sleep(1)
        send_file(host=host,port=port,file_path=args.f)

if __name__ == '__main__':
    main()
