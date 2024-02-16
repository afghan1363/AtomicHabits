from habits_app.servises import TgBot
from celery import shared_task
from datetime import datetime, timedelta, timezone
from habits_app.models import Habit


@shared_task
def message_habit():
    bot = TgBot()
    now = datetime.now(tz=timezone.utc)
    habits = Habit.objects.filter(action_time__lte=now)
    if habits:
        for habit in habits:
            if habit.reward:
                text = (f'Не забудь {habit.place} в {habit.action_time.strftime("%H:%M")} '
                        f'выполнить {habit.action}, за это твоя награда {habit.reward}. '
                        f'На это у тебя {habit.execution_time} секунд')
            elif habit.associated_with:
                text = (f'Не забудь {habit.place} в {habit.action_time.strftime("%H:%M")} '
                        f'выполнить {habit.action}, на это у тебя {habit.execution_time} секунд.'
                        f' Потом сразу {habit.associated_with.place} сделай {habit.associated_with.action} '
                        f'На это у тебя {habit.associated_with.execution_time} секунд')
            else:
                text = (f'Не забудь {habit.place} в {habit.action_time.strftime("%H:%M")} '
                        f'выполнить {habit.action}. На это у тебя {habit.execution_time} секунд')

            try:
                bot.send_message(chat_id=habit.user.chat_id, text=text)
                habit.action_time += timedelta(days=int(habit.periodicity))
            except Exception as err:
                print(err)
            finally:
                habit.save()
