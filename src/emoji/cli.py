import click
import emoji.api
from pathlib import Path
import toml


@click.command()
@click.option("--source-team", required=False)
@click.option("--target-team", required=False)
@click.option("--target-name", required=False)
@click.argument("name", required=True)
def migrate(source_team, name, target_team, target_name):
    config = toml.load(Path.home().joinpath(".slak/config.toml"))
    if source_team is None:
        source_team = config.get("defaults").get("source_team")
    if target_team is None:
        target_team = config.get("defaults").get("target_team")
    if target_name is None:
        target_name = name
    res = emoji.api.migrate_emoji(
        source_team=source_team,
        source_name=name,
        target_team=target_team,
        target_name=target_name
    )
    if res.get('ok'):
        print(f"'{target_name}' migrated to {target_team}")
    else:
        print(res)


@click.command()
@click.argument("team")
@click.argument("name")
def uri(team, name):
    uri = emoji.api.get_emoji_uri(team=team, emoji_name=name)
    print(uri)