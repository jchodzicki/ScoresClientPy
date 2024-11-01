import argparse
import requests
import json

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
            return GameParser.parse(response.text)
        else:
            raise Exception(f"Failed to fetch data: {response.status_code} - {response.reason}")

class Game:
    def __init__(self, game_id, date, time, home_team, home_abbr, home_score, away_team, away_abbr, away_score, is_finished, division):
        self.game_id = game_id
        self.date = date
        self.time = time
        self.home_team = home_team
        self.home_abbr = home_abbr
        self.home_score = home_score
        self.away_team = away_team
        self.away_abbr = away_abbr
        self.away_score = away_score
        self.is_finished = is_finished
        self.division = division

    def __str__(self):
        return (
            f"Game ID: {self.game_id}\n"
            f"Date: {self.date} Start Time: {self.time}\n"
            f"Home Team: {self.home_team} ({self.home_abbr}) - {self.home_score}\n"
            f"Away Team: {self.away_team} ({self.away_abbr}) - {self.away_score}\n"
            f"Division: {self.division}\n"
            f"Game Finished: {'Yes' if self.is_finished else 'No'}\n"
        )

class GameParser:
    @staticmethod
    def parse(response_text):
        if not response_text.strip():
            return []

        try:
            games_data = json.loads(response_text)
        except json.JSONDecodeError:
            raise ValueError("Failed to decode JSON from response text.") from None

        if not isinstance(games_data, list):
            raise ValueError("JSON content is not formatted as a list of games.")

        games = []
        for game in games_data:
            try:
                parsed_game = Game(
                    game_id=game['i'],
                    date=game['d'],
                    time=game['t'],
                    home_team=game['hn'],
                    home_abbr=game['ha'],
                    home_score=game.get('h', 'TBD'),
                    away_team=game['an'],
                    away_abbr=game['aa'],
                    away_score=game.get('a', 'TBD'),
                    is_finished=game['e'],
                    division=game['dv']
                )
                games.append(parsed_game)
            except KeyError as e:
                print(f"Warning: Skipping a game due to missing required attribute: {e}")
            except Exception as e:
                print(f"Warning: An error occurred while processing a game: {e}")

        return games

class Command:
    def __init__(self, client):
        self.client = client

    def execute(self, data):
        raise NotImplementedError("Each command must implement the execute method.")


class CheckGameSchedule(Command):
    def execute(self, data):
        games = self.client.post(data)
        return "\n".join(str(game) for game in games)


class CheckGameState(Command):
    def execute(self, data):
        games = self.client.post(data)
        return "\n".join(str(game) for game in games)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Ultimate Frisbee Game Information API Client")
    parser.add_argument("--url", choices=['test', 'rondo'], required=True, help="URL to use (test or rondo)")
    parser.add_argument("--game", type=int, help="Game ID to query")
    parser.add_argument("--date", help="Date for checking the schedule (format: YYYY-MM-DD)")
    parser.add_argument("--players", action="store_true", help="Include players info (boolean: true|false)")
    parser.add_argument("--teams", action="store_true", help="Include teams info (boolean: true|false)")
    parser.add_argument("--update", action="store_true", help="Include game updates (boolean: true|false)")

    return parser.parse_args()

def main():
    args = parse_arguments()

    base_url = APIConfig.URL_TEST if args.url == 'test' else APIConfig.URL_RONDO
    client = APIClient(base_url)

    data = {}
    if args.game:
        data['game'] = args.game
    if args.date:
        data['schedule'] = args.date
        data['date'] = args.date
    if args.players or args.teams or args.update:
        data['info'] = 'detailed'

    command_map = {
        args.date: CheckGameSchedule(client),
        args.game: CheckGameState(client)
    }
    command = command_map.get(True) or command_map.get(args.game)
    result = command.execute(data)
    print(result)

if __name__ == '__main__':
    main()