import os
import daemon
import time
import requests
import logging
from dotenv import load_dotenv
import typer


app = typer.Typer()
logging.basicConfig(level=logging.INFO)


def check_api():
    while True:
        response = requests.get(
            os.environ.get('API_URL', 'http://localhost:12345')
        )
        if response.ok:
            logging.info('Response text: {}'.format(response.text))
        else:
            logging.error('Response text: {}'.format(response.text))
        time.sleep(5)


@app.command()
def stop():
    # implement me!
    pass


@app.command()
def start():
    logger = logging.getLogger()
    handler = logging.FileHandler('application-check.log', 'w', 'utf-8')
    # logger.addHandler(handler)
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    context = daemon.DaemonContext(
        files_preserve=[handler.stream, ],
    )
    with context:
        check_api()


if __name__ == "__main__":
    app()
    load_dotenv()
