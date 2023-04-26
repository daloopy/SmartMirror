import requests
from datetime import datetime, timedelta
import pytz
from dateutil.parser import parse

# Set the API endpoint URL
def SportsInit():
    url = "https://api.sportradar.us/nba/trial/v7/en/games/2022/PST/schedule.json"
    api_key = "tm468wmru5u9yqswddjf9mtq"

    # Define the search range as starting 5 days before today and ending 7 days after today
    today = datetime.now(pytz.timezone("US/Eastern"))
    five_days_ago = today - timedelta(days=5)
    one_week_from_now = today + timedelta(days=5)

    # Set the API request parameters
    params = {
        "api_key": api_key,
        "status": "scheduled",
        "date": five_days_ago.strftime("%Y-%m-%d"),
        "end_date": one_week_from_now.strftime("%Y-%m-%d")
    }

    # Make the API request and get the response
    response = requests.get(url, params=params)
    return response

def GetGames(response):
    # Check if the request was successful
    if response.status_code == 200:
        # Get the games data from the response
        games_data = response.json()["games"]
        
        # Sort the games by scheduled time, with the most recent ones first
        sorted_games = sorted(games_data, key=lambda x: x["scheduled"], reverse=True)
        
        # Initialize lists to hold the past 5 games and the next 5 games
        past_games = []
        
        for game in sorted_games:
            game_datetime_str = game["scheduled"].replace("Z", "")
            game_datetime_utc = datetime.fromisoformat(game_datetime_str).replace(tzinfo=pytz.UTC)
            game_datetime_eastern = game_datetime_utc.astimezone(pytz.timezone("US/Eastern"))
            if game_datetime_eastern.date() < datetime.today().date():
                past_games.append(game)
        
        past_games.reverse()
        
        # Get the next 5 games
        next_games = []
        for game in sorted_games:
            game_datetime_str = game["scheduled"].replace("Z", "")
            game_datetime_utc = datetime.fromisoformat(game_datetime_str).replace(tzinfo=pytz.UTC)
            game_datetime_eastern = game_datetime_utc.astimezone(pytz.timezone("US/Eastern"))
            if game_datetime_eastern.date() >= datetime.today().date():
                next_games.append(game)

    return past_games, next_games

def Games_formatter(past_games, next_games):
    # Print the past games
    past_game_info = []
    #for game in past_games[-5:]:
    for index, game in enumerate(past_games[-5:]):
        home_team = game["home"]["name"]
        away_team = game["away"]["name"]
        temp = past_games[index]
        home_score = temp['home_points']
        away_score = temp['away_points']
        game_datetime_str = game["scheduled"].replace("Z", "")
        game_datetime_utc = datetime.fromisoformat(game_datetime_str).replace(tzinfo=pytz.UTC)
        game_datetime_eastern = game_datetime_utc.astimezone(pytz.timezone("US/Eastern"))
        game_date = game_datetime_eastern.strftime("%A, %B %d")
        game_time = game_datetime_eastern.strftime("%I:%M %p")
        past_info = [game_date, game_time, away_team, home_team, home_score,away_score ]
        past_game_info.append(past_info)
        #print(f"{game_date} - {game_time} - {away_team} @ {home_team}")
    
    # Print the next games
    #print("\nNext 5 games:")
    next_game_info = []
    for game in next_games[-5:]:
        home_team = game["home"]["name"]
        away_team = game["away"]["name"]
        game_datetime_str = game["scheduled"].replace("Z", "")
        game_datetime_utc = datetime.fromisoformat(game_datetime_str).replace(tzinfo=pytz.UTC)
        game_datetime_eastern = game_datetime_utc.astimezone(pytz.timezone("US/Eastern"))
        game_date = game_datetime_eastern.strftime("%A, %B %d")
        game_time = game_datetime_eastern.strftime("%I:%M %p")
        next_info = [game_date, game_time, away_team, home_team, "TBD", "TBD"]
        next_game_info.append(next_info)
        #print(f"{game_date} - {game_time} - {away_team} @ {home_team}")
    return past_game_info, next_game_info


def main():
    response = SportsInit()
    past_games, next_games = GetGames(response)
    past_game_info, next_game_info = Games_formatter(past_games, next_games)
    print("Past game")
    print(past_game_info)
    print(next_game_info)


if __name__ == "__main__":
    # call the main function
    main()  


