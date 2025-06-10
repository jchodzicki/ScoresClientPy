# Ultimate Frisbee Game Information API Client

### Common Requirements

Ensure you have Python and required libraries installed:

```shell
pip install -r requirements.txt
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

## Info Table
| Env name | URL param  | URL to scores                                                     |
|----------|------------|-------------------------------------------------------------------|
| test3    | test       | [link](https://scores.frisbee.pl/test3/ext/watchlive.php/)        |
| winterunleashed       | wu         | [link](https://ultiscores.com/winterunleashed/ext/watchlive.php/) |
| pomeranian     | pomeranian | [link](https://ultiscores.com/pomeranian/ext/watchlive.php/)      |

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

## Unit test coverage:

To execute unit tests run the following command in a project directory:
```shell
pytest
```


## How to run it on Windows or MacOs
1. Download and install Docker Desktop https://www.docker.com/products/docker-desktop/
2. Start Docker Desktop and make sure it works (`docker --version` in the terminal). If you want to run the terminal then
MacOs: Run `Terminal` from Applications 
Windows: Press `Windows + r`. In the Run box, type `cmd`, then click OK
3. In the terminal navigate to the folder in which this README.md file is located using the `cd` command in terminal, e.g. `cd ~/ScoresClientPy`
4. Run the next command to start docker
```shell
docker build -t scores .
```
Something like this should appear:
```
[+] Building 5.0s (11/11) FINISHED                                                                                                                                                     docker:desktop-linux
 => [internal] load build definition from Dockerfile                                                                                                                                                   0.0s
 => => transferring dockerfile: 385B                                                                                                                                                                   0.0s
 => [internal] load metadata for docker.io/library/python:3.9-slim                                                                                                                                     0.5s
 => [internal] load .dockerignore                                                                                                                                                                      0.0s
 => => transferring context: 2B                                                                                                                                                                        0.0s
 => [1/6] FROM docker.io/library/python:3.9-slim@sha256:f9364cd6e0c146966f8f23fc4fd85d53f2e604bdde74e3c06565194dc4a02f85                                                                               0.0s
 => => resolve docker.io/library/python:3.9-slim@sha256:f9364cd6e0c146966f8f23fc4fd85d53f2e604bdde74e3c06565194dc4a02f85                                                                               0.0s
 => [internal] load build context                                                                                                                                                                      0.0s
 => => transferring context: 7.71kB                                                                                                                                                                    0.0s
 => CACHED [2/6] WORKDIR /app                                                                                                                                                                          0.0s
 => [3/6] COPY requirements.txt .                                                                                                                                                                      0.0s
 => [4/6] RUN pip install --no-cache-dir -r requirements.txt                                                                                                                                           3.5s
 => [5/6] COPY . .                                                                                                                                                                                     0.0s 
 => [6/6] WORKDIR /app/src                                                                                                                                                                             0.0s 
 => exporting to image                                                                                                                                                                                 0.8s 
 => => exporting layers                                                                                                                                                                                0.5s 
 => => exporting manifest sha256:49d65889e5ef998d55505e92cd85685b8cef1a936cdf614e0041ac3d7f273589                                                                                                      0.0s 
 => => exporting config sha256:07386f00a9bc071837f53e1e88d30acb4a24cffd6998fcace97350edd5e1ee96                                                                                                        0.0s 
 => => exporting attestation manifest sha256:8b035c3343c76f07cc5f6383ebf500bb1c66eb7476aef4ec0f3ad6204a0f35a1                                                                                          0.0s
 => => exporting manifest list sha256:8f7737d3472fda36222d6fb1f2ed9fb2c02b8bcb4f9d59e9f8921e834f8892d1                                                                                                 0.0s
 => => naming to docker.io/library/scores:latest                                                                                                                                                       0.0s
 => => unpacking to docker.io/library/scores:latest                                                                                                                                                    0.2s

View build details: docker-desktop://dashboard/build/desktop-linux/desktop-linux/2lwao18ngeh8khlh8meq54ats

What's next:
    View a summary of image vulnerabilities and recommendations → docker scout quickview
```


5. Execute the following command in terminal to enter bash script in docker container.
```shell
docker run -it -v $(pwd)/forstream:/app/src/output scores /bin/sh
```
Expected result is:
```
# 
```
6. We can now run a test to see if the script works. Use the next command in terminal

```shell
python scores_reader.py --url test --date 2023-06-23
```
Information about the games for specified date should appear. For example:
```
Game ID: 1036
Date: 23.06.2023 Start Time: 16:00
Home Team: Alpaka (ALP) - None
Away Team: Edredon (EDR) - None
Division: mixed
Game Finished: No

Game ID: 1045
Date: 23.06.2023 Start Time: 16:00
Home Team: Cziru (CZR) - 7
Away Team: Flaming (FLM) - 4
Division: mixed
Game Finished: Yes

Game ID: 1050
Date: 23.06.2023 Start Time: 16:00
Home Team: Jenot (JNT) - None
Away Team: Hihara (HHR) - None
Division: mixed
Game Finished: No

# 
```

7. A `forstream` folder will be created in the source directory where this README.md file is. 
Now we can run the command to track specific game by Id. For example:
```shell
python scores_reader.py --url test --game 1060 --start
```
Then files will start appearing as described in this README, which should be plugged into OBS.
8. To abort the script use `ctrl+c` in the terminal.