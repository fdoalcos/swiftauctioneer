import secrets
from django import forms
from markdown2 import Markdown
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from . import util

class CreateForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control border col-md-11'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control border col-md-11'}))

class EditPage(forms.Form):
    Edit = forms.CharField(label="Description", widget=forms.Textarea( attrs={'class': 'form-control border col-md-11'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "home": True
    })

def entry(request, entry):
    markdowner = Markdown()
    entries = util.get_entry(entry)

    if entries is None:
        return render(request, "encyclopedia/sorry.html", {
            "title": entry
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(entries),
            "title": entry
        })


def search(request):
    value = request.GET.get('q', '')
    if util.get_entry(value) is not None:
        '''
        The "entry" after the "reverse" word is the function above and the
        "entry" after kwargs is its parameter from the entry function which
        takes and entry parameter
        ex. def entry(request, entry):
                //code
        '''
        return HttpResponseRedirect(reverse("entry", kwargs={'entry': value }))

    else:
        '''
        "listofentries is a list for us to append the "util.list_entries()"
        if the "entry" in for loops is a part of "util.list_entries"
        ex. for entry in util.list_entries:
                it means that if you put an input like "ytho" then
                it has words in the python then we should append that
                entry
        '''
        listofentries= []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                listofentries.append(entry)

    return render(request, "encyclopedia/index.html", {
        "entries": listofentries,
        "search": True,
        "value": value

    })

def createnewpage(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            if util.get_entry(title) is None:
                util.save_entry(title, description)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))
            else:
                messages.error(request, "title already existed, please try another name")
        else:
            return render(request, "encyclopedia/create.html", {
                'form': form
            })

    return render(request, "encyclopedia/create.html", {
        'form': CreateForm()
    })



def edit(request, title):

    Edited = EditPage(initial={"Edit": util.get_entry(title)})

    if request.method == "POST":
        form = EditPage(request.POST)

        if form.is_valid():
            newcontent = form.cleaned_data["Edit"]
            util.save_entry(title, newcontent)
            return HttpResponseRedirect(reverse('entry', args=[title]))

        else:
            return render(request, "encyclopedia/sorry.html", {
                'title': title
            })

    return render(request, "encyclopedia/edit.html", {
        'form': Edited,
        'title': title
    })

def random(request):
    random = util.list_entries()
    randomized = secrets.choice(random)
    return HttpResponseRedirect(reverse("entry", kwargs={'entry': randomized}))





