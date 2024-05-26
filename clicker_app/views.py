# clicker_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, LoginForm
from .models import UserProfile
from django.utils import timezone
from django.core.cache import cache

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Проверка наличия профиля для пользователя
            if not UserProfile.objects.filter(user=user).exists():
                UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('click')
    else:
        form = SignUpForm()
    return render(request, 'clicker_app/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('click')
    else:
        form = LoginForm()
    return render(request, 'clicker_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def click(request):
    user_profile = UserProfile.objects.get(user=request.user)
    cache_key = f'score_{request.user.id}'
    score = cache.get(cache_key, user_profile.score)

    click_power = user_profile.upgrade_level * user_profile.character_bonus

    if 'click' in request.GET:
        score += click_power
        cache.set(cache_key, score)

    # Проверка и выполнение сбора очков ботом
    now = timezone.now()
    if user_profile.bot_level > 0 and (now - user_profile.last_bot_collect).seconds > 60:
        bot_points = user_profile.bot_level * 5 * user_profile.character_bonus
        score += bot_points
        user_profile.last_bot_collect = now
        cache.set(cache_key, score)
        user_profile.score = score
        user_profile.save()

    last_save = cache.get(f'last_save_{request.user.id}')
    if last_save is None or (now - last_save).seconds > 60:
        user_profile.score = score
        user_profile.save()
        cache.set(f'last_save_{request.user.id}', now)

    upgrade_cost = 100 * user_profile.upgrade_level
    bot_cost = 200 * (user_profile.bot_level + 1)
    character_cost = 500 * (user_profile.bot_level + 1)

    return render(request, 'clicker_app/click.html', {
        'score': score,
        'upgrade_level': user_profile.upgrade_level,
        'upgrade_cost': upgrade_cost,
        'bot_level': user_profile.bot_level,
        'bot_cost': bot_cost,
        'character_cost': character_cost,
        'character': user_profile.character
    })

@login_required
def upgrade(request):
    user_profile = UserProfile.objects.get(user=request.user)
    cache_key = f'score_{request.user.id}'
    score = cache.get(cache_key, user_profile.score)
    
    upgrade_cost = 100 * user_profile.upgrade_level

    if request.method == 'POST' and score >= upgrade_cost:
        user_profile.upgrade_level += 1
        score -= upgrade_cost
        cache.set(cache_key, score)
        user_profile.score = score
        user_profile.save()

    return redirect('click')

@login_required
def buy_bot(request):
    user_profile = UserProfile.objects.get(user=request.user)
    cache_key = f'score_{request.user.id}'
    score = cache.get(cache_key, user_profile.score)
    
    bot_cost = 200 * (user_profile.bot_level + 1)

    if request.method == 'POST' and score >= bot_cost:
        user_profile.bot_level += 1
        score -= bot_cost
        cache.set(cache_key, score)
        user_profile.score = score
        user_profile.save()

    return redirect('click')

@login_required
def buy_character(request):
    user_profile = UserProfile.objects.get(user=request.user)
    cache_key = f'score_{request.user.id}'
    score = cache.get(cache_key, user_profile.score)
    
    character_cost = 500 * (user_profile.bot_level + 1)
    new_character = request.POST.get('character')

    character_bonuses = {
        'hamster': 1,
        'dragon': 2,
        'phoenix': 3
    }

    if request.method == 'POST' and score >= character_cost:
        user_profile.character = new_character
        user_profile.character_bonus = character_bonuses.get(new_character, 1)
        score -= character_cost
        cache.set(cache_key, score)
        user_profile.score = score
        user_profile.save()

    return redirect('click')

@login_required
def leaderboard(request):
    users = UserProfile.objects.order_by('-score')[:10]
    return render(request, 'clicker_app/leaderboard.html', {'users': users})
