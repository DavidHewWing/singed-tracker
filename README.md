# Singed Tracker
A discord bot, that allows for stat tracking among friends and gamers in a server for League of Legends

## Commands

### Version 1 

- !list - list all users in the server
- !add - add user to the tracking stats
- !leaders - list top 10 users in the discord
- !stat [user] - find stats for specific user

## Development

### Running in Development
```
python3 -m venv packages
source packages/bin/activate
export PYTHONPATH="${PYTHONPATH}:/path/to/project" (use `pwd` for MacOS to find the file path)
pip3 install -r requirements.txt
```

### 

### Adding Packages
```
pip freeze > requirements.txt
```