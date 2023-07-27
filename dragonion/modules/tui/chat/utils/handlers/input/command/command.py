from .commands.join import join_command
from .commands.connect import connect_command
from .commands.disconnect import disconnect_command

from textual.widgets import Static


async def not_found_command(_: list):
    from dragonion.modules.tui import app

    app.query_one('MessagesContainer').write(
        "[red]Command not found[/], use /help to get list of available commands"
    )


async def handle_command(full_text: str):
    command, args = (full_text.partition(' ')[0], full_text.partition(' ')[2].split())

    try:
        result = await ({
            '/join': join_command,
            '/connect': connect_command,
            '/disconnect': disconnect_command
        }.get(command, not_found_command)(args))
    except Exception as e:
        result = f'{e.__class__}: {e}'

    if result is not None:
        from dragonion.modules.tui import app
        app.query_one('MessagesContainer').mount_scroll(Static(
            f"[red]Error[/] happened while executing {command}: "
            f"{result} \n"
        ))