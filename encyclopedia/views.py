from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)
    print(f"entry: {type(entry)}")
    if not entry:
        return HttpResponseRedirect(reverse("not_found"))
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": entry
    })
    

def add_page(request):
    if request.method == "POST":
        ...
    else:
        return render(request, "encyclopedia/add.html")

def search_page(request):
    ...

def not_found(request):
    return render(request, "encyclopedia/not_found.html", {
        "error_code": 404,
        "error": "Page not found"
    })