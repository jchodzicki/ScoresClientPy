# Ultimate Frisbee Game Information API Client

### Common Requirements

Ensure you have Python and requests library installed:

```shell
pip install requests
```

### Usage

The CLI is going to have the following interface.

```shell
usage:  scores_reader.py [-h] --url {test,rondo} [--game GAME] [--date DATE] [--start]

arguments:

-h, --help          show this help message and exit
  --url {test,rondo}  URL to use (test or rondo)
  --game GAME         Game ID to query
  --date DATE         Date for checking the schedule (format: YYYY-MM-DD)
  --start             Start processing game events every 30 seconds
```

### Contact
For any additional questions or requests, please reach out via email: atarasenko.engineering@gmail.com.

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

## 1. Get List of Games Scheduled for a Selected Date

```html
POST /watchlive.php

Parameters
schedule: (empty value)
date: specific date in YYYY-MM-DD format (e.g., "2024-10-28")
```

Sample Response
```json
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
  }
]
```

```html

i - game id
hn - home team name
an - away team name
ha - home team abbreviation
aa - away team abbreviation
f - field (it will be always field 1)
d - date
t - game start time
h - current home score
a - current away score
e - true if game is finished
dv - division (always "mixed")

```

## 2. Get Current State of a Specific Game

```html
POST /watchlive.php

Parameters
game: game ID (e.g., 1042)
```

Sample Response
```json
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

```html
ts - stop watch data
time - game time in seconds (it goes from zero up)
ds - timestamp in deciseconds when time was calculated (if your timestamp is higher, you can add the difference to game time)
stop - true if game time is not running (it should be only true before and after the game - for this test game is stopped)
h,a - current home/away score
```

## 3. Get Updates for a Specific Game

```html
POST /watchlive.php

Parameters
game: game ID (e.g., 1042)
update: true
```

Sample Response
```json
{
  "ts": {
    "time": "1591",
    "ds": "17301220648",
    "stop": true
  },
  "h": 1,
  "a": 1,
  "o": "h",
  "e": [
    {
      "t": 0,
      "e": "h",
      "y": "O"
    },
    {
      "t": 47,
      "e": "h",
      "y": "T"
    }
  ]
}
```

```html
o - "h" or "a", indicates which team is in possesion; "e" if game has ended
e - list of game events
t - event game time in seconds
e - team the event concerns
y - type of event
O - starting in offence
T - turnover
S - score
a - assist (shirt number, "XX" for callahan)
s - score (shirt number)
hs - home score after this point
as - away score after this point
TO - timeout
E - game end
```

## 4. Get Players and Teams Information for a Game

```html
POST /watchlive.php

Parameters
game: game ID (e.g., 1042)
players: true
teams: true
```

Sample Response
```json
{
  "ts": {
    "time": "1591",
    "ds": "17301220648",
    "stop": true
  },
  "h": 1,
  "a": 1,
  "p": {
    "h": {
      "30": "Kajetan Mazurek",
      "13": "Ernest Kubiak"
    },
    "a": {
      "54": "Alek Błaszczyk",
      "94": "Jarosław Michalak"
    }
  },
  "hn": "Guziec",
  "an": "Cziru"
}
```

## Quick Note:

Please remember that different URLs might have different access or further specific parameters for your requests. Always check if you're using the correct endpoint.