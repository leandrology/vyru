from django.shortcuts import render, redirect
from django.contrib import messages
import subprocess
import os

# Get the current directory of admin.py
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go two folders up
three_folders_up = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))

# Create your views here.

def train(request):
    if request.method == 'POST':
        # Execute the script to restart the Rasa server
        action = request.POST.get('action')
        if action == 'train':
            subprocess.run(["rasa", "train"], cwd=three_folders_up+"/", shell=False)
            # subprocess.run(["rasa", "train"], cwd="C:\\Users\\Philip\\Documents\\ServingIntel\\AI-BI", shell=True)
            # subprocess.run(["echo","1969Firebird!", "|","sudo", "-S","systemctl", "restart", "rasa.service"], cwd="/home/lancewbell/AI-BI/")
            # subprocess.run(["echo","1969Firebird!", "|","sudo", "-S","systemctl", "restart", "rasa-actions.service"], cwd="/home/lancewbell/AI-BI/")
    return redirect(request.META.get('HTTP_REFERER',''))

