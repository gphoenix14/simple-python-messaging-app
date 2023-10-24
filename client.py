import socket
import threading

class Client:
    def __init__(self, nickname, group, pin, host='0.0.0.0', port=55555):
        print("""
   _
 ('v')
//-\\
(\_=_/)
 ^^ ^^

Innovery Academy 2023 by Giuseppe Longobardi
        """)

        self.nickname = nickname
        self.group = group
        self.pin = pin
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.broadcast_mode = True

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('utf-8'))
                elif message == 'GROUP':
                    self.client.send(self.group.encode('utf-8'))
                elif message == 'NEW_PIN' or message == 'PIN':
                    self.client.send(self.pin.encode('utf-8'))
                elif message == 'WRONG_PIN':
                    print("PIN errato!")
                    self.client.close()
                    break
                else:
                    print(message)
            except:
                print("Errore")
                self.client.close()
                break

    def write(self):
        print("Scrivi '/send private' per inviare messaggi solo al tuo gruppo")
        print("Scrivi '/send broadcast' per inviare messaggi a tutti i gruppi")
        while True:
            message = input("")
            if message == '/send private':
                self.broadcast_mode = False
                print("Hai scelto di inviare messaggi solo al tuo gruppo")
            elif message == '/send broadcast':
                self.broadcast_mode = True
                print("Hai scelto di inviare messaggi a tutti i gruppi")
            else:
                if self.broadcast_mode:
                    message = f'BROADCAST:{self.nickname}: {message}'
                else:
                    message = f'PRIVATE:{self.nickname}: {message}'
                self.client.send(message.encode('utf-8'))

if __name__ == "__main__":
    host = input("Inserisci l'indirizzo IP del server: ")
    port = int(input("Inserisci la porta del server: "))
    nickname = input("Scegli un nickname: ")
    group = input("Scegli un gruppo di appartenenza: ")
    pin = input("Inserisci il PIN del gruppo: ")
    client = Client(nickname, group, pin, host, port)
    receive_thread = threading.Thread(target=client.receive)
    receive_thread.start()
    write_thread = threading.Thread(target=client.write)
    write_thread.start()
