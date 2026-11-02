import os

import requests
from django.http import JsonResponse
from django.shortcuts import redirect, render
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = (os.getenv("BACKEND_URL") or "").rstrip("/")


def _get_recent_conversations():
    if not BACKEND_URL:
        return []

    try:
        response = requests.get(f"{BACKEND_URL}/api/v1/get-conservation", timeout=10)
        response.raise_for_status()
        data = response.json() if response.content else []

        if isinstance(data, dict):
            conversations = (
                data.get("conservation")
                or data.get("conversations")
                or data.get("data")
                or []
            )
        else:
            conversations = data

        return conversations if isinstance(conversations, list) else []
    except requests.exceptions.RequestException:
        return []


def home(request):
    recent_conversations = _get_recent_conversations()
    return render(
        request,
        "home.html",
        {
            "prompt": "",
            "response": "",
            "error": "",
            "recent_conversations": recent_conversations,
        },
    )


def create_conversation(request):
    prompt = request.POST.get("prompt", "").strip()

    if not prompt:
        return render(
            request,
            "home.html",
            {
                "prompt": "",
                "response": "",
                "error": "Prompt is required",
                "recent_conversations": _get_recent_conversations(),
            },
        )

    try:
        response = requests.post(
            f"{BACKEND_URL}/api/v1/create-conservation",
            json={"prompt": prompt},
            timeout=15,
        )
        response.raise_for_status()
        result = response.json()

        if isinstance(result, dict):
            assistant_message = (
                result.get("ai_response")
                or result.get("response")
                or result.get("message")
                or result.get("reply")
                or result.get("content")
                or str(result)
            )
        else:
            assistant_message = str(result)

        return render(request,"home.html",
            {
                "prompt": prompt,
                "response": assistant_message,
                "error": "",
                "recent_conversations": _get_recent_conversations(),
            },
            
        )
    except requests.exceptions.RequestException as exc:
        return render(
            request,
            "home.html",
            {
                "prompt": prompt,
                "response": "",
                "error": f"Backend call failed: {str(exc)}",
                "recent_conversations": _get_recent_conversations(),
            },
        )


def get_conservation(request):
    try:
        response = requests.get(f"{BACKEND_URL}/api/v1/get-conservation", timeout=10)
        response.raise_for_status()
        data = response.json() if response.content else []

        if isinstance(data, dict):
            conversations = (
                data.get("conservation")
                or data.get("conversations")
                or data.get("data")
                or []
            )
        else:
            conversations = data

        return JsonResponse({"conservation": conversations if isinstance(conversations, list) else []})
    
    except requests.exceptions.RequestException as exc:
        return JsonResponse({"error": f"Backend call failed: {str(exc)}"}, status=500)


def index(request):
    try:
        response = requests.get(BACKEND_URL, timeout=10)
        response.raise_for_status()
        return JsonResponse({"backend": response.json()})
    except requests.exceptions.RequestException as exc:
        return JsonResponse({"error": f"Backend call failed: {str(exc)}"}, status=500)


def delete_conversation(request, conversation_id):
    if request.method != "POST":
        return redirect("home")

    try:
        response = requests.delete(
            f"{BACKEND_URL}/api/v1/delete_agent_conversation/{conversation_id}",
            timeout=10,
        )
        response.raise_for_status()
        return redirect("home")
    except requests.exceptions.RequestException:
        return redirect("home")