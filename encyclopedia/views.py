from django.shortcuts import render, redirect
from django.contrib import messages
import markdown2 as md
from . import util
from django import forms
import re, random as rand

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def search(request, search):
    if search in util.list_entries():
        html = md.markdown(util.get_entry(search))
        return render(request, "encyclopedia/search.html", {
            "search": search, "html": html
        })
    else:
        return render(request, "encyclopedia/error.html")

def random(request):
    randomPage = rand.choice(util.list_entries())
    if randomPage in util.list_entries():
        html = md.markdown(util.get_entry(randomPage))
        return render(request, "encyclopedia/search.html", {
            "random": randomPage, "html": html
        })
    else:
        return render(request, "encyclopedia/error.html")

def find(request):
    if request.method == "GET":
        query = request.GET.get('q')
        for queryMatch in util.list_entries():
            if query.casefold() == queryMatch.casefold():
                html = md.markdown(util.get_entry(query))
                return render(request, "encyclopedia/search.html", {
                    "queryMatch": queryMatch, "html": html
                })
        regex = re.compile(query.casefold())
        matchList = []
        for a in util.list_entries():
            if regex.match(a.casefold()):
                matchList.append(a)
        if not matchList:
            matchList = util.list_entries()
        return render(request, "encyclopedia/list.html", {
            "match": matchList
        })

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Markdown Content", widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))

def newpage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title in util.list_entries():
                messages.error(request, f"'{title}' page title already exists!!\nPlease type another title.")
                return render(request, "encyclopedia/newpage.html", {
                    "form": form
                })
            else:
                util.save_entry(title, content)
                return redirect(f"/wiki/{title}")
        else:
            return render(request, "encyclopedia/newpage.html", {
                "form": form
            })
    # elif request.method == "GET":
    #     # editTitle = request.GET.get("search")
    #     # editContent = util.get_entry(editTitle)
    #     NewPageForm(request.GET)
    # """
    # Here working on edit page section
    # else:
    #     form = NewPageForm(util.get_entry(title, content))
    # """
    return render(request, "encyclopedia/newpage.html", {
        "form": NewPageForm()
    })

# def edit(request):
#     return render(request, "encyclopedia/newpage.html")