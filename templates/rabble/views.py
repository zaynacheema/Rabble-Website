from django.shortcuts import render
from .models import SubRabble


def index(request):
    subrabbles = SubRabble.objects.filter(community_id=1)
    print("🧠 Found subRabbles:", subrabbles.count())
    return render(request, "rabble/index.html", {"subrabbles": subrabbles})

def profile(request):
    return render(request, "rabble/profile.html")

