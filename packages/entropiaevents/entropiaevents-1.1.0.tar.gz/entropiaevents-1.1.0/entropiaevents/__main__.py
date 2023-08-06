from entropiaevents import WikiEvents

### Logging ###
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    level=getattr(logging, 'INFO')
)

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    events = WikiEvents()
    for event in events.events:
        logger.info(event)
