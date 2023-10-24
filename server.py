import socket
import threading

class Server:
    def __init__(self, host='0.0.0.0', port=55555):
        print("""
   _
 ('v')
//-\\
(\_=_/)
 ^^ ^^

Innovery Academy 2023 by Giuseppe Longobardi
        """)

        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.clients = []
        self.nicknames = []
        self.groups = []
        self.group_pins = {}

    def broadcast(self, message, group, all_groups):
        for client, g in zip(self.clients, self.groups):
            if all_groups or g == group:
                client.send(message)

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                group = self.groups[self.clients.index(client)]
                all_groups = message.startswith("BROADCAST:")
                private = False
                if all_groups:
                    message = message[len("BROADCAST:"):]
                else:
                    private = message.startswith("PRIVATE:")
                    if private:
                        message = message[len("PRIVATE:"):]
                message_to_send = f'[{group}]' + ('(private)' if private else '') + message
                self.broadcast(message_to_send.encode('utf-8'), group, all_groups)
                print(message_to_send)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                group = self.groups[index]
                self.nicknames.remove(nickname)
                self.groups.remove(group)
                self.broadcast(f'[{group}]{nickname} ha lasciato la chat!'.encode('utf-8'), group, False)
                print(f"[{group}]{nickname} ha lasciato la chat!")
                break

    def receive(self):
        while True:
            client, address = self.server.accept()
            print(f'Connesso con {str(address)}')

            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            self.nicknames.append(nickname)

            client.send('GROUP'.encode('utf-8'))
            group = client.recv(1024).decode('utf-8')

            if group in self.group_pins:
                client.send('PIN'.encode('utf-8'))
                pin = client.recv(1024).decode('utf-8')
                if self.group_pins[group] != pin:
                    client.send('WRONG_PIN'.encode('utf-8'))
                    client.close()
                    continue
            else:
                client.send('NEW_PIN'.encode('utf-8'))
                pin = client.recv(1024).decode('utf-8')
                self.group_pins[group] = pin

            self.groups.append(group)
            self.clients.append(client)

            print(f'Nickname del client è {nickname}!')
            print(f'{nickname} si è unito al gruppo {group}!')
            self.broadcast(f'[{group}]{nickname} si è unito alla chat!'.encode('utf-8'), group, False)
            client.send('Connesso al server!'.encode('utf-8'))

            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

if __name__ == "__main__":
    port = int(input("Scegli una porta: "))
    server = Server(port=port)
    server.receive()
