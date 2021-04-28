import itertools
import logging
import os
import string
import subprocess
from pathlib import Path
from time import sleep
from typing import Generator

import click
import feedparser
import requests
from requests import Request, Session

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
    subprocess.call(
        [
            "scp",
            "-o",
            "UserKnownHostsFile=/dev/null",
            "-o",
            "StrictHostKeyChecking=no",
            local_path,
            f"{remote_host}:{remote_pathname}",
        ]
    )
    pass


def handle_link(link):
    filename = "-".join(link.rsplit("/")[-2:])
    if not has_file(filename):
        local_path = LOCAL_DATA_DIR / filename
        download_file(link, local_path)
        upload_file(local_path, REMOTE_HOST, REMOTE_WATCH_PATH / filename)
        logging.info("Sync ", REMOTE_WATCH_PATH / filename)


def full_scan_iterator():
    searches = itertools.product(string.ascii_lowercase, string.ascii_lowercase)
    for search in searches:
        needle = "".join(search)
        yield feed_request({"title": needle})


@click.command()
@click.option("--full_scan", default=False, type=bool)
def execute(full_scan=False):
    s = requests.Session()
    if full_scan:
        searches = full_scan_iterator()
    else:
        searches = [feed_request()]

    for search in searches:
        resp = s.send(search)
        for link in response_to_links(resp.content):
            handle_link(link)


if __name__ == "__main__":
    execute()
