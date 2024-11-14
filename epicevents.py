from auth import login, logout, status
import argparse


def main():
    parser = argparse.ArgumentParser(description="Epic Events CRM")
    subparsers = parser.add_subparsers(dest='command')

    # Command login
    subparsers.add_parser('login', help='Se connecter')

    # Command logout
    subparsers.add_parser('logout', help='Se déconnecter')

    # Command status
    subparsers.add_parser(
        'status', help='Afficher le statut de connexion')

    args = parser.parse_args()

    if args.command == 'login':
        login()
    elif args.command == 'logout':
        logout()
    elif args.command == 'status':
        status()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
