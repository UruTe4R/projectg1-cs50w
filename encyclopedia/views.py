from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

from . import util


def index(request):
    print("BRO", request.method)
    print("a", request.POST)
    print("b", type(request.POST))
    entries = util.list_entries()
    if request.method == "POST":
        results = []
        for entry in sorted(entries):
            if request.POST.get('q').lower() == entry.lower():
                return HttpResponseRedirect(reverse("entry", args=[entry]))
            elif request.POST.get('q').lower() in entry.lower():
                results.append(entry)
                return render(request, "encyclopedia/index.html", {
                    "entries": results,
                    "result": True
                })
        return render(request, "encyclopedia/index.html", {
            "entries": results,
            "result": True
        })
    else:    
        return render(request, "encyclopedia/index.html", {
            "entries": entries
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
    

def not_found(request):
    return render(request, "encyclopedia/not_found.html", {
        "error_code": 404,
        "error": "Page not found"
    })