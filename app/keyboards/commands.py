from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_commands(bot):
    commands = [
        BotCommand(command="start", description="Изменить свою группу"),
        BotCommand(command="schedule", description="Узнать свое рассписание"),
    ]

    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
