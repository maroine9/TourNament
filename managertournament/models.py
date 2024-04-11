

from django.db import models
from django import forms
from django.utils import timezone


class Tournament(models.Model):
    SPORT_TYPES = (
        ('football', 'Football'),
        ('basketball', 'Basketball'),
        ('tennis', 'Tennis'),
    )
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    sport_type = models.CharField(max_length=100, choices=SPORT_TYPES)
    teams = models.ManyToManyField('Team', related_name='tournaments', blank=True)
    app_label = 'managertournament'
    # Ajoutez d'autres champs selon vos besoins

class TournamentForm(forms.ModelForm):
    team1 = forms.CharField(max_length=100, label='Équipe 1')
    team2 = forms.CharField(max_length=100, label='Équipe 2')

    class Meta:
        model = Tournament
        fields = ['name', 'start_date', 'end_date', 'sport_type', 'team1', 'team2']


class Team(models.Model):
    name = models.CharField(max_length=100)
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "teams"
    app_label = 'managertournament'
    # Ajoutez d'autres champs selon vos besoins

class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    app_label = 'managertournament'
    # Ajoutez d'autres champs selon vos besoins

class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    date = models.DateField(default=None, null=True)
    team1 = models.ForeignKey(Team, related_name='team1_matches', on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name='team2_matches', on_delete=models.CASCADE)
    time = models.TimeField()
    def __str__(self):
        return f"{self.team1.name} vs {self.team2.name}"
    # Ajoutez les champs score_team1 et score_team2 au modèle Match
    score_team1 = models.IntegerField(default=0)
    score_team2 = models.IntegerField(default=0)

    def determine_winner(self):
        if self.score_team1 > self.score_team2:
            return self.team1
        elif self.score_team1 < self.score_team2:
            return self.team2
        else:
            return None
    app_label = 'managertournament'
    # Ajoutez d'autres champs selon vos besoins

class MatchResultForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['score_team1', 'score_team2']
    
        
class Participant(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    app_label = 'managertournament'
    # Ajoutez d'autres champs selon vos besoins


        