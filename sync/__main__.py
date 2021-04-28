from typing import Generator
import os
import logging
import subprocess
from time import sleep
from pathlib import Path

import feedparser
import click
import requests
from requests import Session, Request

from config import (
    HTTP_AUTH,
    LOCAL_DATA_DIR,
    REMOTE_HOST,
    REMOTE_WATCH_PATH,
    SEARCH_BASE_URL,
)


def feed_request(params={}) -> requests.PreparedRequest:
    search_params = {"free": "yes", **params}
    search_query = ",".join(["%s:%s" % (k, v) for k, v in search_params.items()])
    url = SEARCH_BASE_URL + search_query
    req = Request("GET", url, auth=HTTP_AUTH)
    return req.prepare()


def response_to_links(resp: bytes) -> Generator[str, None, None]:
    tree = feedparser.parse(resp)
    for entry in tree.entries:
        yield entry.link


def has_file(filename):
    return (LOCAL_DATA_DIR / filename).is_file()


def download_file(url, to_filename: Path):
    resp = requests.get(url, auth=HTTP_AUTH)
    with to_filename.open("wb") as f:
        f.write(resp.content)


def upload_file(local_path, remote_host, remote_pathname):
    subprocess.call(["scp", local_path, f"{remote_host}:{remote_pathname}"])
    pass


@click.command()
@click.argument("sleep_interval", default=-1, type=int)
def execute(sleep_interval):
    while 1:
        s = requests.Session()
        resp = s.send(feed_request())
        content = resp.content
        for link in response_to_links(content):
            filename = "-".join(link.rsplit("/")[-2:])
            if not has_file(filename):
                local_path = LOCAL_DATA_DIR / filename
                download_file(link, local_path)
                upload_file(local_path, REMOTE_HOST, REMOTE_WATCH_PATH / filename)
                logging.info("Sync ", REMOTE_WATCH_PATH / filename)
        if sleep_interval > -1:
            logging.info(f"Sleep for {sleep_interval}s")
            sleep(sleep_interval)
        else:
            break


if __name__ == "__main__":
    execute()
