# Beatmap Parser
- Python package for parsing hit objects from .osu files
- Developed for the osu! MLpp project

## Basic Usage
```
from beatmap_parser.beatmap import parse_hit_objects

path = 'path/to/1234567.osu'

with open(path, encoding='latin-1') as file:
  hit_objects = parse_hit_objects(file)
```
Note: latin-1 encoding avoids some errors
 
