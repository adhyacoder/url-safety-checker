from django.shortcuts import render
from .models import URLCheck
from urllib.parse import urlparse


# ----------------------------
# URL SAFETY CHECK FUNCTION
# ----------------------------

def check_url_safety(url):

    try:
        if not url.startswith("http"):
            url = "http://" + url

        domain = urlparse(url).netloc.replace("www.", "").lower()

    except:
        return "Unsafe URL", 100

    trusted_domains = [
        "google.com",
        "youtube.com",
        "github.com",
        "wikipedia.org",
        "microsoft.com"
    ]

    # SAFE DOMAIN CHECK
    if domain in trusted_domains:
        return "Safe URL", 0

    score = 50

    suspicious_words = [
        "login", "verify", "account", "bank",
        "password", "free", "win", "gift",
        "money", "reward", "update", "secure"
    ]

    url_lower = url.lower()

    for word in suspicious_words:
        if word in url_lower:
            score += 30

    if url.count(".") > 3:
        score += 25

    if url.count("-") > 4:
        score += 25

    if "@" in url:
        score += 40

    if len(url) > 80:
        score += 20

    if domain == "" or "." not in domain:
        return "Unsafe URL", 100

    if score > 100:
        score = 100

    if score >= 60:
        return "Unsafe URL", score
    else:
        return "Safe URL", score


# ----------------------------
# HOME PAGE
# ----------------------------

def home(request):
    result = ""
    score = 0
    url_input = ""

    if request.method == "POST":

        url_input = request.POST.get("url")

        result, score = check_url_safety(url_input)

        URLCheck.objects.create(
            url=url_input,
            result=result
        )

    return render(request, "home.html", {
        "result": result,
        "score": score,
        "url_input": url_input
    })


# ----------------------------
# HISTORY PAGE
# ----------------------------

def history(request):
    urls = URLCheck.objects.all().order_by('-checked_at')

    return render(request, "history.html", {
        "urls": urls
    })