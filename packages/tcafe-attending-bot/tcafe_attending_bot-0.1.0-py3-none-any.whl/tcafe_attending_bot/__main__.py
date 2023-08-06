#!/usr/bin/env python
# coding: UTF-8

import asyncio
import json
from pathlib import Path
from typing import Generator, List, Tuple

import aiohttp
from bs4 import BeautifulSoup
from xdg import BaseDirectory

_BASE_URL = 'http://tcafe2a.com'
_APP_NAME = 'tcafe'
_ID_KEY = 'id'
_PW_KEY = 'password'


async def attend(identifier: str, password: str) -> None:
    async with aiohttp.ClientSession() as session:
        data = dict(mb_id=identifier, mb_password=password)

        # login
        async with session.post(_BASE_URL + '/bbs/login_check.php', data=data):
            pass

        # get hidden values
        async with session.get(_BASE_URL + '/attendance/selfattend2.php') as res:
            attend_page = BeautifulSoup(await res.text(), features='html.parser')
            # language=JQuery-CSS
            hidden_values: List[BeautifulSoup] = attend_page.select('form[name=frm1] input[type=hidden]')

            data = {v.attrs['name']: v.attrs['value'] for v in hidden_values}

        # attend
        async with session.post(_BASE_URL + '/attendance/selfattend2_p.php', data=data):
            pass


def _get_accounts() -> Generator[Tuple[str, str], None, None]:
    for directory in BaseDirectory.xdg_data_dirs:
        config_path = Path(directory) / _APP_NAME / 'accounts.json'

        if not config_path.is_file():
            continue

        try:
            with config_path.open() as fp:
                config = json.load(fp)
        except IOError:
            continue

        if not isinstance(config, list):
            continue

        for account in config:
            if not isinstance(account, dict) or \
                    not isinstance(account.get(_ID_KEY), str) or not isinstance(account.get(_PW_KEY), str):
                continue

            yield account[_ID_KEY], account[_PW_KEY]

    yield from ()


async def main() -> None:
    accounts = tuple(_get_accounts())

    if len(accounts) != 0:
        await asyncio.wait(tuple(attend(_id, _pw) for _id, _pw in _get_accounts()))


def console_entry() -> None:
    asyncio.run(main())


if __name__ == '__main__':
    asyncio.run(main())
