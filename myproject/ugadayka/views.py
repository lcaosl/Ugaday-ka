from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
import random


@login_required
def index(request):
    # Инициализация или получение игровых данных из сессии
    game_data = request.session.get('game_data', {})

    if not game_data:
        reset_game_session(request)
        game_data = request.session['game_data']

    current_time = timezone.now()
    next_attempt_time = timezone.datetime.fromisoformat(game_data['next_attempt_time'])

    # Обработка сброса игры
    if 'reset' in request.GET and current_time >= next_attempt_time:
        reset_game_session(request)
        return redirect('index')

    # Обработка попытки угадать
    if request.method == 'POST' and not game_data['attempt_used'] and current_time >= next_attempt_time:
        try:
            user_number = int(request.POST.get('number', 0))
            game_data['user_number'] = user_number
            game_data['attempt_used'] = True
            game_data['guessed'] = (user_number == game_data['secret_number'])

            if game_data['guessed']:
                game_data['current_win'] = min(50, 5 + game_data.get('win_streak', 0) * 5)
                game_data['total_coins'] = game_data.get('total_coins', 0) + game_data['current_win']
                game_data['win_streak'] = game_data.get('win_streak', 0) + 1
            else:
                game_data['win_streak'] = 0

            game_data['next_attempt_time'] = (current_time + timedelta(minutes=1)).isoformat()
            request.session['game_data'] = game_data
            request.session.modified = True
            return redirect('index')

        except ValueError:
            pass

    # Вычисление оставшегося времени
    remaining_seconds = max(0, int((next_attempt_time - current_time).total_seconds()))

    return render(request, 'ugadayka/index.html', {
        'game_data': game_data,
        'next_attempt_available': current_time >= next_attempt_time,
        'remaining_seconds': remaining_seconds
    })


def reset_game_session(request):
    request.session['game_data'] = {
        'secret_number': random.randint(1, 100),
        'attempt_used': False,
        'guessed': False,
        'user_number': None,
        'next_attempt_time': timezone.now().isoformat(),
        'win_streak': 0,
        'current_win': 0,
        'total_coins': request.session.get('game_data', {}).get('total_coins', 0),
    }
    request.session.modified = True