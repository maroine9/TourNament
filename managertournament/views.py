from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Tournament ,TournamentForm ,Participant ,Team, Player, Match
from django.http import HttpResponseBadRequest

def tournament_list(request):
    tournaments = Tournament.objects.all()
    return render(request, 'tournament_list.html', {'tournaments': tournaments})

def tournament_detail(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    matches = Match.objects.filter(tournament=tournament)
    teams = Team.objects.filter(tournament=tournament).values_list('id', 'name')  # Récupérer les noms des équipes
    all_teams = Team.objects.all()  # Obtenez toutes les équipes pour le sélecteur de création de match

    return render(request, 'tournament_detail.html', {'tournament': tournament, 'teams': teams, 'all_teams': all_teams})


def team_list(request):
    teams = Team.objects.all()
    return render(request, 'team_list.html', {'teams': teams})

def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    return render(request, 'team_detail.html', {'team': team})

def player_list(request):
    players = Player.objects.all()
    return render(request, 'player_list.html', {'players': players})

def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk)
    return render(request, 'player_detail.html', {'player': player})

def match_list(request):
    matches = Match.objects.all()
    return render(request, 'match_list.html', {'matches': matches})

def match_detail(request, pk):
    match = get_object_or_404(Match, pk=pk)
    return render(request, 'match_detail.html', {'match': match})


def registration_form(request):
    if request.method == 'POST':
        tournament_name = request.POST['tournament_name']
        participant_name = request.POST['participant_name']
        # Créer un nouveau tournoi
        tournament = Tournament.objects.create(name=tournament_name)
        # Créer un nouveau participant lié au tournoi
        participant = Participant.objects.create(tournament=tournament, name=participant_name)
        return redirect('registration_success')
    return render(request, 'registration_form.html')

def result_form(request):
    # Implémentez la logique pour le formulaire de saisie des résultats ici
    return render(request, 'result_form.html')

def leaderboard(request):
    # Implémentez la logique pour afficher le classement des équipes ici
    teams = Team.objects.all().order_by('-score')
    return render(request, 'leaderboard.html', {'teams': teams})

def tournament_create(request):
    if request.method == 'POST':
        tournament_form = TournamentForm(request.POST)
        if tournament_form.is_valid():
            # Création d'un tournoi à partir des données du formulaire
            tournament = tournament_form.save()

            # Récupération des noms des équipes à partir des données POST
            team1_name = request.POST.get('team1')
            team2_name = request.POST.get('team2')

            # Création des objets d'équipe associés au tournoi
            team1 = Team.objects.create(name=team1_name, tournament=tournament)
            team2 = Team.objects.create(name=team2_name, tournament=tournament)

            return redirect('managertournament:tournament_detail', pk=tournament.pk)
    else:
        tournament_form = TournamentForm()
    return render(request, 'tournament_create.html', {'tournament_form': tournament_form})

def create_match(request, tournament_id):
    if request.method == 'POST':
        print(request.POST)  # Affiche les données du formulaire dans la console
        team1_id = request.POST.get('team1')
        team2_id = request.POST.get('team2')
        date = request.POST.get('date')
        time = request.POST.get('time')

        if not all([team1_id, team2_id, date, time]):
            return HttpResponseBadRequest("Tous les champs sont requis pour créer un match.")

        tournament = get_object_or_404(Tournament, pk=tournament_id)

        team1 = get_object_or_404(Team, pk=team1_id, tournament=tournament)
        team2 = get_object_or_404(Team, pk=team2_id, tournament=tournament)

        match = Match.objects.create(tournament=tournament, team1=team1, team2=team2, date=date, time=time)

        return redirect('managertournament:tournament_detail', pk=tournament_id)

    else:
        return HttpResponseBadRequest("Requête invalide")


def update_match(request, match_id):
    if request.method == 'POST':
        match = get_object_or_404(Match, pk=match_id)
        
        # Récupérer les données du formulaire
        score_team1 = request.POST.get('score_team1')
        score_team2 = request.POST.get('score_team2')
        status = request.POST.get('status')
        date = request.POST.get('date')
        # Mettre à jour les champs du match
        match.score_team1 = score_team1
        match.score_team2 = score_team2
        match.status = status
        match.date = date
        match.save()
        
        return redirect('managertournament:tournament_detail', pk=match.tournament.pk)
    else:
        return HttpResponseBadRequest("Invalid request")



class TournamentListView(ListView):
    model = Tournament
    template_name = 'tournament_list.html'
    context_object_name = 'tournaments'

class TournamentDetailView(DetailView):
    model = Tournament
    template_name = 'tournament_detail.html'
    context_object_name = 'tournament'

class TeamListView(ListView):
    model = Team
    template_name = 'team_list.html'
    context_object_name = 'teams'

class TeamDetailView(DetailView):
    model = Team
    template_name = 'team_detail.html'
    context_object_name = 'team'

class PlayerListView(ListView):
    model = Player
    template_name = 'player_list.html'
    context_object_name = 'players'

class PlayerDetailView(DetailView):
    model = Player
    template_name = 'player_detail.html'
    context_object_name = 'player'

class MatchListView(ListView):
    model = Match
    template_name = 'match_list.html'
    context_object_name = 'matches'

class MatchDetailView(DetailView):
    model = Match
    template_name = 'match_detail.html'
    context_object_name = 'match'
