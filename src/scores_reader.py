import argparse
import requests

class APIConfig:
    URL_TEST = "https://scores.frisbee.pl/test3/ext/watchlive.php/"
    URL_RONDO = "https://ultiscores.com/rondo/ext/watchlive.php/"
    HEADERS = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def post(self, data):
        response = requests.post(self.base_url, data=data, headers=APIConfig.HEADERS)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Failed to fetch data: {response.status_code} - {response.reason}")

class Command:
    def __init__(self, client):
        self.client = client

    def execute(self, data):
        raise NotImplementedError("Each command must implement the execute method.")


class CheckGameSchedule(Command):
    def execute(self, data):
        return self.client.post(data)


class CheckGameState(Command):
    def execute(self, data):
        return self.client.post(data)


class UpdateGame(Command):
    def execute(self, data):
        return self.client.post(data)


class GamePlayersTeamsInfo(Command):
    def execute(self, data):
        return self.client.post(data)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Ultimate Frisbee Game Information API Client")
    parser.add_argument("--url", choices=['test', 'rondo'], required=True, help="URL to use (test or rondo)")
    parser.add_argument("--game", type=int, help="Game ID to query")
    parser.add_argument("--date", help="Date for checking the schedule (format: YYYY-MM-DD)")
    parser.add_argument("--players", action="store_true", help="Include players info")
    parser.add_argument("--teams", action="store_true", help="Include teams info")
    parser.add_argument("--update", action="store_true", help="Include game updates")

    return parser.parse_args()

def main():
    args = parse_arguments()

    base_url = APIConfig.URL_TEST if args.url == 'test' else APIConfig.URL_RONDO
    client = APIClient(base_url)

    data = {}
    if args.game:
        data['game'] = args.game
    if args.date:
        data['schedule'] = ''
        data['date'] = args.date
    if args.players:
        data['players'] = 'true'
    if args.teams:
        data['teams'] = 'true'
    if args.update:
        data['update'] = 'true'

    command_map = {
        True: CheckGameSchedule(client),
        args.game and not any([args.players, args.teams, args.update]): CheckGameState(client),
        args.update: UpdateGame(client),
        any([args.players, args.teams]): GamePlayersTeamsInfo(client)
    }

    command = command_map[True]
    result = command.execute(data)
    print(result)

if __name__ == '__main__':
    main()