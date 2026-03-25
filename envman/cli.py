"""
Command-line interface for EnvMan
"""
import click
import sys
from pathlib import Path
from .core import EnvManager
from . import __version__
from tabulate import tabulate


@click.group()
@click.version_option(version=__version__)
def cli():
    """EnvMan - Secure Environment Variable Manager
    
    Manage .env files across projects with encryption and team sharing.
    """
    pass


@cli.command()
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True,
              help='Master password for encryption')
def init(password):
    """Initialize EnvMan with master password"""
    try:
        manager = EnvManager()
        manager.init(password)
        click.echo(click.style("✓ EnvMan initialized!", fg='green'))
        click.echo("\nNext steps:")
        click.echo("  1. Add an environment: envman add production")
        click.echo("  2. Load variables: envman load production .env")
        click.echo("  3. Use environment: envman use production")
    except Exception as e:
        click.echo(click.style(f"✗ Error: {e}", fg='red'), err=True)
        sys.exit(1)


@cli.command()
@click.argument('name')
@click.option('--description', '-d', default='', help='Environment description')
def add(name, description):
    """Add a new environment"""
    try:
        manager = EnvManager()
        manager.add_environment(name, description)
        click.echo(click.style(f"✓ Environment '{name}' created!", fg='green'))
    except Exception as e:
        click.echo(click.style(f"✗ Error: {e}", fg='red'), err=True)
        sys.exit(1)


@cli.command()
def list():
    """List all environments"""
    try:
        manager = EnvManager()
        environments = manager.list_environments()
        
        if not environments:
            click.echo("No environments found. Create one with: envman add <name>")
            return
        
        table_data = [
            [env['name'], env['description'], env['created_at']]
            for env in environments
        ]
        
        click.echo(tabulate(
            table_data,
            headers=['Name', 'Description', 'Created'],
            tablefmt='simple'
        ))
    except Exception as e:
        click.echo(click.style(f"✗ Error: {e}", fg='red'), err=True)
        sys.exit(1)


@cli.command()
@click.argument('environment')
@click.argument('file', type=click.Path(exists=True))
def load(environment, file):
    """Load variables from .env file into environment"""
    try:
        manager = EnvManager()
        manager.load_from_file(environment, Path(file))
        click.echo(click.style(f"✓ Variables loaded into '{environment}'", fg='green'))
    except Exception as e:
        click.echo(click.style(f"✗ Error: {e}", fg='red'), err=True)
        sys.exit(1)


@cli.command()
@click.argument('environment')
def use(environment):
    """Switch to environment (creates .env in current directory)"""
    try:
        manager = EnvManager()
        manager.use_environment(environment)
        click.echo(click.style(f"✓ Now using '{environment}' environment", fg='green'))
        click.echo(f"  .env file created in {Path.cwd()}")
    except Exception as e:
        click.echo(click.style(f"✗ Error: {e}", fg='red'), err=True)
        sys.exit(1)


@cli.command()
@click.argument('environment')
@click.argument('key')
@click.option('--value', prompt=True, hide_input=True, help='Variable value')
def set(environment, key, value):
    """Set a variable in an environment"""
    try:
        manager = EnvManager()
        manager.set_variable(environment, key, value)
        click.echo(click.style(f"✓ Set {key} in '{environment}'", fg='green'))
    except Exception as e:
        click.echo(click.style(f"✗ Error: {e}", fg='red'), err=True)
        sys.exit(1)


@cli.command()
@click.argument('environment')
@click.option('--show-values/--hide-values', default=False, help='Show actual values')
def show(environment, show_values):
    """Show all variables in an environment"""
    try:
        manager = EnvManager()
        variables = manager.get_variables(environment)
        
        if not variables:
            click.echo(f"No variables in '{environment}'")
            return
        
        click.echo(f"\n{click.style(environment.upper(), fg='cyan', bold=True)} ({len(variables)} variables)\n")
        
        table_data = []
        for key, value in sorted(variables.items()):
            display_value = value if show_values else '•' * 8
            table_data.append([key, display_value])
        
        click.echo(tabulate(
            table_data,
            headers=['Key', 'Value'],
            tablefmt='simple'
        ))
    except Exception as e:
        click.echo(click.style(f"✗ Error: {e}", fg='red'), err=True)
        sys.exit(1)


@cli.command()
@click.argument('environment')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
def export(environment, output):
    """Export environment to .env file"""
    try:
        manager = EnvManager()
        output_path = Path(output) if output else Path(f"{environment}.env")
        manager.export_to_file(environment, output_path)
        click.echo(click.style(f"✓ Exported to {output_path}", fg='green'))
    except Exception as e:
        click.echo(click.style(f"✗ Error: {e}", fg='red'), err=True)
        sys.exit(1)


@cli.command()
@click.argument('environment')
def backup(environment):
    """Create a backup of an environment"""
    try:
        manager = EnvManager()
        backup_id = manager.backup_environment(environment)
        click.echo(click.style(f"✓ Backup created (ID: {backup_id})", fg='green'))
    except Exception as e:
        click.echo(click.style(f"✗ Error: {e}", fg='red'), err=True)
        sys.exit(1)


@cli.command()
@click.argument('env1')
@click.argument('env2')
def diff(env1, env2):
    """Compare two environments"""
    try:
        manager = EnvManager()
        differences = manager.diff_environments(env1, env2)
        
        click.echo(f"\n{click.style('Comparing:', fg='cyan', bold=True)} {env1} ↔ {env2}\n")
        
        if differences['only_in_first']:
            click.echo(click.style(f"Only in {env1}:", fg='yellow'))
            for key in sorted(differences['only_in_first'].keys()):
                click.echo(f"  - {key}")
            click.echo()
        
        if differences['only_in_second']:
            click.echo(click.style(f"Only in {env2}:", fg='yellow'))
            for key in sorted(differences['only_in_second'].keys()):
                click.echo(f"  + {key}")
            click.echo()
        
        if differences['different_values']:
            click.echo(click.style("Different values:", fg='red'))
            for key in sorted(differences['different_values'].keys()):
                click.echo(f"  ≠ {key}")
            click.echo()
        
        same_count = len(differences['same'])
        click.echo(click.style(f"✓ {same_count} variables are identical", fg='green'))
        
    except Exception as e:
        click.echo(click.style(f"✗ Error: {e}", fg='red'), err=True)
        sys.exit(1)


@cli.command()
@click.argument('environment')
@click.option('--output', '-o', required=True, type=click.Path(),
              help='Output file for sharing')
def share(environment, output):
    """Export environment for team sharing (encrypted)"""
    try:
        manager = EnvManager()
        output_path = Path(output)
        manager.export_for_sharing(environment, output_path)
        click.echo(click.style(f"✓ Environment ready to share: {output_path}", fg='green'))
        click.echo("\nTeam members can import with:")
        click.echo(f"  envman import {output_path}")
    except Exception as e:
        click.echo(click.style(f"✗ Error: {e}", fg='red'), err=True)
        sys.exit(1)


@cli.command(name='import')
@click.argument('file', type=click.Path(exists=True))
@click.option('--name', '-n', help='Custom environment name')
def import_env(file, name):
    """Import shared environment from file"""
    try:
        manager = EnvManager()
        manager.import_from_share(Path(file), name)
        click.echo(click.style("✓ Environment imported successfully!", fg='green'))
    except Exception as e:
        click.echo(click.style(f"✗ Error: {e}", fg='red'), err=True)
        sys.exit(1)


def main():
    """Main entry point"""
    cli()


if __name__ == '__main__':
    main()
