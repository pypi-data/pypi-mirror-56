<div align="center">

# BattleBreakers.py
## Async library for interacting with Battle Breakers/Epic Games API.

</div>

## Installation

To install, simply type into command prompt:  
```py -3 -m pip install -U BattleBreakers```<br>

Or if you're on unix (linux/mac):<br>
```python3 -m pip install -U BattleBreakers```

## Example

```python
import BattleBreakers

client = BattleBreakers.client(
    email='',
    password=''
)

@client.event
def event_ready():
    print(f'Client ready as {client.display_name}.')
    print('Collecting daily reward.')
    await client.collect_daily_reward()

client.run()
```

## Documentation

To see the full documentation for this gem, please visit the [wiki](chrome://newtab Coming soon!)