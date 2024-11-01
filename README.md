# Ultimate Frisbee Game Information API Client

### Common Requirements

Ensure you have Python and requests library installed:

```shell
pip install requests
```

### Usage

The CLI is going to have the following interface.

```shell
usage: python scores_reader.py [-h] [--game]

source

Pure Python command-line Scores reader.

optional arguments:
-h, --help     show this help message and exit
--game         Print game results as JSON in stdout
```

### Contact
For any additional questions or requests, please reach out via your preferred method of communication.

### API documentation

This API provides access to game schedules, current game states, game updates, and game details including player and team information.
## Base URL for Test

https://scores.frisbee.pl/test3/ext/watchlive.php/

## Base URL for Rondo

https://ultiscores.com/rondo/ext/watchlive.php/
(Note: The slash at the end of each URL is mandatory)

## Common Header

All requests to the API should be made with the POST method and include the following header:

```html
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
```
## Endpoints

1. Get List of Games Scheduled for a Selected Date

```html
POST /watchlive.php

Parameters
schedule: (empty value)
date: specific date in YYYY-MM-DD format (e.g., "2024-10-28")
Sample Response
json
```

```html
[
{
"i": 1026,
"hn": "Impala",
"an": "Jenot",
"ha": "IMP",
"aa": "JNT",
"f": "1",
"d": "28.10.2024",
"t": "14:00",
"h": null,
"a": null,
"e": false,
"dv": "mixed"
},
...
]
```

2. Get Current State of a Specific Game

```html
POST /watchlive.php

Parameters
game: game ID (e.g., 1042)
Sample Response
json

```

```html
{
"ts": {
"time": "1591",
"ds": "17301220648",
"stop": true
},
"h": 1,
"a": 1
}
```

3. Get Updates for a Specific Game

```html
POST /watchlive.php

Parameters
game: game ID (e.g., 1042)
update: true
Sample Response
json
```

```html
{
"ts": {"time":"1591", "ds":"17301220648", "stop":true},
"h": 1,
"a": 1,
"o": "h",
"e": [
{"t": 0, "e": "h", "y": "O"},
{"t": 47, "e": "h", "y": "T"},
...
]
}
```

4. Get Players and Teams Information for a Game

```html
POST /watchlive.php

Parameters
game: game ID (e.g., 1042)
players: true
teams: true
Sample Response
json
```

```html
{
"ts":{"time":"1591", "ds":"17301220648", "stop":true},
"h":1,
"a":1,
"p": {
"h": {"30":"Kajetan Mazurek", "13":"Ernest Kubiak", ...},
"a": {"54":"Alek B\u0142aszczyk", "94":"Jaros\u0142aw Michalak", ...}
},
"hn": "Guziec",
"an": "Cziru",
...
}
```

## Quick Note:

Please remember that different URLs might have different access or further specific parameters for your requests. Always check if you're using the correct endpoint.