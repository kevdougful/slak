from dotenv import load_dotenv, dotenv_values
import os
from pathlib import Path
import requests


def _get_token(team):
    # TODO: Use click's context passing to move this out of the business logic
    #       and into the CLI layer.
    load_dotenv(dotenv_path=Path.home().joinpath(".slak/.env"))
    token = os.getenv(team.upper() + "_TOKEN")
    if token is None:
        raise ValueError(f"cannot find token for '{team}'")
    return token


def get_emoji_uri(team, emoji_name):
    token = _get_token(team)
    res = requests.get(f'https://{team}.slack.com/api/emoji.list?token={token}')
    emoji_list = res.json().get('emoji')
    uri = emoji_list.get(emoji_name)
    if uri is None:
        raise ValueError(f"no '{emoji_name}' found in {team}")
    if uri.startswith('alias:'):
        return emoji_list.get(uri[6:])
    else:
        return uri


def _download_emoji(team, emoji_name):
    uri = get_emoji_uri(team, emoji_name)
    res = requests.get(uri)
    return res.content


def _add_emoji(team, emoji_name, image):
    token = _get_token(team)
    req = requests.Request(
        method='POST',
        url=f'https://{team}.slack.com/api/emoji.add?token={token}',
        files={'image': image},
        data={'mode': 'data', 'name': emoji_name},
    ).prepare()
    return requests.Session().send(req)


def migrate_emoji(source_team, source_name, target_team, target_name):
    image = _download_emoji(source_team, source_name)
    res = _add_emoji(target_team, target_name, image).json()
    return res

