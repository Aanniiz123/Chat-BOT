import os

import requests
from django.http import JsonResponse
from django.shortcuts import render
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")


def home(request):
    return render(request, "home.html", {"prompt": "", "response": "", "error": ""})


def create_conversation(request):
    prompt = request.POST.get("prompt", "").strip()

    if not prompt:
        return render(
            request,
            "home.html",
            {"prompt": "", "response": "", "error": "Prompt is required"},
        )

    try:
        response = requests.post(
            f"{BACKEND_URL}api/v1/create-conservation",
            json={"prompt": prompt},
            timeout=15,
        )
        response.raise_for_status()
        result = response.json()

        if isinstance(result, dict):
            assistant_message = (
                result.get("response")
                or result.get("message")
                or result.get("reply")
                or result.get("content")
                or str(result)
            )
        else:
            assistant_message = str(result)

        return render(request, "home.html", {
            "prompt": prompt,
            "response": assistant_message,
            "error": "",
        })
    except requests.exceptions.RequestException as exc:
        return render(request, "home.html", {
            "prompt": prompt,
            "response": "",
            "error": f"Backend call failed: {str(exc)}",
        })


def get_conservation(request):
    pass


def index(request):
    try:
        response = requests.get(BACKEND_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        return JsonResponse({"backend": data})
    except requests.exceptions.RequestException as exc:
        return JsonResponse({"error": f"Backend call failed: {str(exc)}"}, status=500)
