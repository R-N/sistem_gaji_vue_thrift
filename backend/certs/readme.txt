Use mkcert to generate server certs:
- https://github.com/FiloSottile/mkcert

Do not use generate_server on generator.py

A. Server
1. mkcert -install
2. Browse to the installed directory (you can check with "mkcert -CAROOT"), take rootCA.pem
3. Copy it to ./backend/certs, and rename it to rootCA.crt
4. mkcert localhost 127.0.0.1 <computer static ip> <computer name>
5. Rename the outputs to server.crt and server.key
6. Make sure they are in ./backend/certs
7. python certs/generator.py

B. Client
1. Install rootCA.crt as root trusted certs 