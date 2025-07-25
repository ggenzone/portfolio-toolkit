import click


def not_implemented(command_name):
    """Standard message for not implemented commands"""
    click.echo(f"⚠️  Command '{command_name}' is not implemented yet")
    click.echo("   This functionality is under development")


def load_json_file(filepath):
    """Load and validate JSON file"""
    import json

    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        click.echo(f"Error: File '{filepath}' not found")
        raise click.Abort()
    except json.JSONDecodeError:
        click.echo(f"Error: Invalid JSON in file '{filepath}'")
        raise click.Abort()
