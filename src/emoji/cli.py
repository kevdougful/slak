import click
import emoji.api


@click.command()
@click.option("--source-team", required=True)
@click.option("--source-name", required=True)
@click.option("--target-team", required=True)
@click.option("--target-name", required=False)
def migrate(source_team, source_name, target_team, target_name=None):
    res = emoji.api.migrate_emoji(
        source_team=source_team,
        source_name=source_name,
        target_team=target_team,
        target_name=target_name
    )
    if res.get('ok'):
        print(f"'{source_name}' migrated to {target_team}")
    else:
        print(res)
