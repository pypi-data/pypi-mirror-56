# entropiaevents

## Installation

```
pip install entropiaevents
```

## Usage
### Standalone

```
python -m entropiaevents
```

### As module

```
from entropiaevents import WikiEvents
entropia = WikiEvents()
```

## Documentation
### WikiEvents()
#### Methods
##### .to_json_file( filename )

Write the list of all events as JSON string to _filename_.

#### Attributes
##### .events

List of all events.
