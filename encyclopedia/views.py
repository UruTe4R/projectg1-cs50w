from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
import random
import markdown2

from . import util

class AddForm(forms.Form):
    title = forms.CharField(label="title")
    text = forms.CharField(label="text", widget=forms.Textarea(
        attrs={"placeholder": "Write Paragraph..."}
    ))

class EditForm(forms.Form):
    text = forms.CharField(label="edit text", widget=forms.Textarea(
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
    # pattern = r"^#.+\n(?P<text>.+)"
    # print("title", title)
    # print("entry", entry)
    # match = re.search(pattern, entry, re.DOTALL)
    # if not match:
    #     return HttpResponseRedirect(reverse("not_found", args=[404]))
    # content = match.group("text")
    
    if not entry:
        return HttpResponseRedirect(reverse("not_found", args=[404]))
    return render(request, "encyclopedia/entry.html", {
        "entry": markdown2.markdown(entry),
        "title": title
    })
    

def add_page(request):
    print(request.method)
    if request.method == "POST":
        print("request>POST:", request.POST)
        form = AddForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            if title in util.list_entries():
                return render(request, "encyclopedia/add.html", {
                    "form": form,
                    "error": f"this title '{title}' already exists!"
                })
            print("title:", title, "text:", text)
            util.save_entry(title, text)
            return HttpResponseRedirect(reverse("entry", args=[title]))
        else:
            # i send back the form again with errors
            return render(request, "encyclopedia/add.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/add.html", {
            "form": AddForm()
        })
    

def edit(request, heading):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            util.save_entry(heading, text)
            return HttpResponseRedirect(reverse("entry", args=[heading]))
        else:
            return render(request, "encyclopedia/edit.html", {
                "form": form
            })
    else:
        entry = util.get_entry(heading)
        if not entry:
            print("entry not found")
            return HttpResponseRedirect(reverse("not_found", args=[404]))
        print(entry)
        # pattern = r"^#.+\n(?P<text>.+)"
        # entry = util.get_entry(heading)
        # match = re.search(pattern, entry, re.DOTALL)
        # if not match:
        #     print("match not found")
        #     return HttpResponseRedirect(reverse("not_found", args=[404]))
        # content = match.group("text")
        form = EditForm(initial={"text": entry})
        return render(request, "encyclopedia/edit.html", {
            "heading": heading,
            "form": form
        })
    
def random_f(request):
    list = util.list_entries()
    result = random.choice(list)
    return HttpResponseRedirect(reverse("entry", args=[result]))

def not_found(request, not_found):
    return render(request, "encyclopedia/not_found.html", {
        "error_code": 404,
        "error": f"Page /{not_found} not found"
    })