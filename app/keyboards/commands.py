from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot):
    commands = [
        BotCommand(command="start", description="Изменить свою группу"),
        BotCommand(command="schedule", description="Узнать свое расписание"),
        BotCommand(command="newsletter_no", description="Отписаться от рассылку расписания"),
        BotCommand(command="newsletter_yes", description="Подписаться на рассылку расписания"),
    ]

    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
