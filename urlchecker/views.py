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
        return "Unsafe URL", 100, "The URL format appears to be invalid or suspicious."

    trusted_domains = [
        "google.com",
        "youtube.com",
        "github.com",
        "wikipedia.org",
        "microsoft.com"
    ]

    if domain in trusted_domains:
        return (
            "Safe URL",
            0,
            "This URL belongs to a trusted and widely recognized domain that is commonly used by millions of users worldwide."
        )

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
        return (
            "Unsafe URL",
            100,
            "The URL structure is invalid and may not point to a legitimate website."
        )

    if score > 100:
        score = 100

    if score >= 60:
        return (
            "Unsafe URL",
            score,
            "This URL contains suspicious keywords and patterns that are commonly used in phishing or scam websites. Users should verify the website before entering any personal or financial information."
        )
    else:
        return (
            "Safe URL",
            score,
            "This URL does not contain suspicious patterns and appears to follow a normal website structure. No immediate security concerns were detected."
        )

# ----------------------------
# CATEGORY DETECTION
# ----------------------------

def get_category(domain):

    if "google" in domain:
        return "Search & Information Service"

    elif "youtube" in domain:
        return "Video Streaming Platform"

    elif "github" in domain:
        return "Software Development Platform"

    elif "wikipedia" in domain:
        return "Online Knowledge Resource"

    elif "microsoft" in domain:
        return "Technology Company"

    elif "facebook" in domain:
        return "Social Media Platform"

    elif "instagram" in domain:
        return "Social Media Platform"

    elif "amazon" in domain:
        return "E-Commerce Website"

    else:
        return "Independent Website"

# ----------------------------
# HTTPS STATUS
# ----------------------------

def get_https_status(url):

    if url.startswith("https://"):
        return "Secure Connection (HTTPS Enabled)"

    return "Not Secure (HTTP Only)"

# ----------------------------
# HOME PAGE
# ----------------------------

def home(request):

    result = ""
    score = 0
    reason = ""
    category = ""
    https_status = ""
    recommendation = ""
    url_input = ""

    if request.method == "POST":

        url_input = request.POST.get("url")

        result, score, reason = check_url_safety(url_input)

        try:
            test_url = url_input

            if not test_url.startswith("http"):
                test_url = "http://" + test_url

            domain = urlparse(test_url).netloc.replace("www.", "").lower()

            category = get_category(domain)

        except:
            category = "Independent Website"

        https_status = get_https_status(url_input)

        if result == "Unsafe URL":
            recommendation = """
⚠️ Do not enter passwords or banking details.
⚠️ Verify the website before proceeding.
⚠️ Avoid downloading files from this URL.
"""
        else:
            recommendation = """
✅ No major risks detected.
✅ Always verify website authenticity before sharing sensitive information.
"""

        URLCheck.objects.create(
            url=url_input,
            result=result
        )

    return render(request, "home.html", {
        "result": result,
        "score": score,
        "reason": reason,
        "category": category,
        "https_status": https_status,
        "recommendation": recommendation,
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