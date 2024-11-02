import argparse
import requests
import os
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
            return response.text
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
class GameEvent:
    def __init__(self, event_time, team, event_type, assist=None, scorer=None, home_score=None, away_score=None):
        self.event_time = event_time
        self.team = team
        self.event_type = event_type
        self.assist = assist
        self.scorer = scorer
        self.home_score = home_score
        self.away_score = away_score

    def __str__(self):
        details = f"{self.event_time}s {self.team.upper()} {self.event_type}"
        if self.event_type == "S":
            details += f" (Assist: {self.assist}, Scorer: {self.scorer}, Scores: {self.home_score}-{self.away_score})"
        return details

class GameEventParser:
    @staticmethod
    def parse_event_data(response_text):
        try:
            event_data = json.loads(response_text)
        except json.JSONDecodeError:
            raise ValueError("Failed to decode JSON from response text.")

        # Basic game data
        game_details = {
            'game_time': event_data['ts']['time'] if 'ts' in event_data else None,
            'game_stopwatch_timestamp': event_data['ts']['ds'] if 'ts' in event_data else None,
            'game_stopped': event_data['ts']['stop'] if 'ts' in event_data else None,
            'home_score': event_data['h'],
            'away_score': event_data['a'],
            'players': {}
        }

        # Validate and handle player details
        if 'p' in event_data and event_data['p']:
            home_players = event_data['p'].get('h', {})
            away_players = event_data['p'].get('a', {})

            if home_players:
                game_details['players']['home'] = {
                    player_id: player_name for player_id, player_name in home_players.items()
                }
            if away_players:
                game_details['players']['away'] = {
                    player_id: player_name for player_id, player_name in away_players.items()
                }
        # Handling the presence of game events
        if 'e' in event_data:
            game_details['events'] = [
                {
                    'event_time': event['t'],
                    'team': event['e'],
                    'event_type': event['y'],
                    'assist': GameEventParser.get_player_name(game_details, event['e'], event.get('a')),
                    'scorer': GameEventParser.get_player_name(game_details, event['e'], event.get('s')),
                    'home_score_after': event.get('hs'),
                    'away_score_after': event.get('as')
                }
                for event in event_data.get('e', [])
            ]

        # Team names and abbreviations
        if 'hn' in event_data and 'an' in event_data:
            game_details['teams'] = {
                'home_name': event_data['hn'],
                'away_name': event_data['an']
            }
        if 'ha' in event_data and 'aa' in event_data:
            game_details['team_abbreviations'] = {
                'home_abbr': event_data['ha'],
                'away_abbr': event_data['aa']
            }

        return game_details

    @staticmethod
    def get_player_name(game_details, team, shirt_number):
        if shirt_number is None:
            return None
        team_key = 'home' if team == 'h' else 'away'
        players = game_details.get('players', {}).get(team_key, {})
        return players.get(str(shirt_number))


class Command:
    def __init__(self, client):
        self.client = client

    def execute(self, data):
        raise NotImplementedError("Each command must implement the execute method.")


class CheckGameSchedule(Command):
    def execute(self, data):
        games = self.client.post(data)
        games = GameParser.parse(games)
        return "\n".join(str(game) for game in games)

class CheckGameEvents(Command):
    def execute(self, data):
        game_details = self.client.post(data)
        event_details = GameEventParser.parse_event_data(game_details)

        # Handling team rosters
        home_players = event_details.get('players', {}).get('home', {})
        away_players = event_details.get('players', {}).get('away', {})

        self.write_team_roster('output/home_roster.txt', home_players)
        self.write_team_roster('output/away_roster.txt', away_players)

        # Handling team names
        abbreviations = event_details.get("team_abbreviations", {})
        home_abbr = abbreviations.get("home_abbr", "")
        away_abbr = abbreviations.get("away_abbr", "")
        self.write_to_file('output/home_name.txt', home_abbr)
        self.write_to_file('output/away_name.txt', away_abbr)

        # Handle scoring events
        scoring_events = [event for event in event_details.get('events', []) if event['event_type'] == 'S']
        latest_home_score, latest_away_score = "0", "0"
        latest_scorer, latest_assist = " ", " "
        if scoring_events:
            latest_event = max(scoring_events, key=lambda e: e['event_time'])
            # Ensuring to get the latest non-empty score & assist updates.
            scorer = latest_event['scorer']
            assist = latest_event['assist']
            if scorer:
                latest_scorer = scorer

            if assist:
                latest_assist = assist

            home_score = latest_event['home_score_after']
            away_score = latest_event['away_score_after']
            # Ensuring to get the latest non-empty score updates.
            if home_score:
                latest_home_score = home_score
            if away_score:
                latest_away_score = away_score

        self.write_to_file('output/home_score.txt', latest_home_score)
        self.write_to_file('output/away_score.txt', latest_away_score)
        self.write_to_file('output/scorer.txt', latest_scorer)
        self.write_to_file('output/assist.txt', latest_assist)

        return json.dumps(event_details, indent=4)

    def write_to_file(self, filepath, data):
        if data:
            self.ensure_directory(filepath)
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(data + '\n')

    def write_team_roster(self, filepath, players):
        self.ensure_directory(filepath)
        with open(filepath, 'w', encoding='utf-8') as file:
            for player_id, player_name in players.items():
                file.write(f"{player_id}: {player_name}\n")

    @staticmethod
    def ensure_directory(filepath):
        directory = os.path.dirname(filepath)
        if not os.path.exists(directory):
            os.makedirs(directory)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Ultimate Frisbee Game Information API Client")
    parser.add_argument("--url", choices=['test', 'rondo'], required=True, help="URL to use (test or rondo)")
    parser.add_argument("--game", type=int, help="Game ID to query")
    parser.add_argument("--date", help="Date for checking the schedule (format: YYYY-MM-DD)")

    return parser.parse_args()

def main():
    args = parse_arguments()

    base_url = APIConfig.URL_TEST if args.url == 'test' else APIConfig.URL_RONDO
    client = APIClient(base_url)

    data = {}
    if args.game:
        data['game'] = args.game
        data['update'] = 'true'
        data['players'] = 'true'
        data['teams'] = 'true'
        command = CheckGameEvents(client)
    if args.date:
        data['schedule'] = args.date
        data['date'] = args.date
        command = CheckGameSchedule(client)
    # if args.players or args.teams or args.update:
    #     data['info'] = 'detailed'

    result = command.execute(data)
    print(result)

if __name__ == '__main__':
    main()