from django import forms
from django.db import models
from game.models import Game

class CharacterForm(forms.Form):
    character_name = forms.ChoiceField(choices=[('Colonel Mustard', 'Colonel Mustard'), ('Miss Scarlet', 'Miss Scarlet'), ('Professor Plum', 'Professor Plum'), ('Mr. Green', 'Mr. Green'), ('Mrs. White', 'Mrs. White'), ('Mrs. Peacock', 'Mrs. Peacock')])
