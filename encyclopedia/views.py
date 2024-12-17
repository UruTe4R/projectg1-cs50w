from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

from . import util

class CreateForm(forms.Form):
    title = forms.CharField(label="title")
    text = forms.CharField(label="text", widget=forms.Textarea(
        attrs={"placeholder": "Write Paragraph..."}
    ))

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
    print(request.method)
    if request.method == "POST":
        print("request>POST:", request.POST)
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            if title in util.list_entries():
                return render(request, "encyclopedia/add.html", {
                    "form": form,
                    "error": f"this title '{title}' already exists!"
                })
            util.save_entry(title, text)
            return HttpResponseRedirect(reverse("entry", args=[title]))
        else:
            # i send back the form again with errors
            return render(request, "encyclopedia/add.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/add.html", {
            "form": CreateForm()
        })
    

def not_found(request, not_found):
    return render(request, "encyclopedia/not_found.html", {
        "error_code": 404,
        "error": f"Page /{not_found} not found"
    })