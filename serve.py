import argparse
from Server.Server import Server

def main():
    parser = argparse.ArgumentParser(description='Starts the chat server')
    
    parser.add_argument('--host', type=str, help='The host IP, default is 0.0.0.0')
    parser.add_argument('--port', type=int, help='The port for the server to run on, default is 9999')
    args = parser.parse_args()


    server = Server(args.host if args.host else '0.0.0.0', args.port if args.port else 9999)
    server.start()


if __name__ == '__main__':
    main()
