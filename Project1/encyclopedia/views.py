from django.shortcuts import render,redirect
from . import util
from django.http import HttpResponseRedirect
from markdown2 import Markdown
from django.urls import reverse
from django import forms
from random import choice

class CreateForm(forms.Form):
    """ a new form to create a new encyclopedia in the website"""
    title = forms.CharField(widget=forms.TextInput(attrs={
      "placeholder": "title"}))
    text = forms.CharField(widget=forms.Textarea(attrs={
      "placeholder": "page Content with Github Markdown"}))

class EditForm(forms.Form):
    """ Form to edit an existing encyclopedia entry """
    text = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Page Content with GitHub Markdown"}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request,entry):
    encyclopedia = util.get_entry(entry)
    
    if encyclopedia!=None:
        encyclopedia= Markdown().convert(encyclopedia)
        return render(request,"encyclopedia/entry.html",{
            "entry":entry,
            "content": encyclopedia
        })
    else:

        return render(request,"encyclopedia/entry.html",{
            "entry":entry,
            "content":encyclopedia       
        })
        
        
def search(request):
    if request.method == "POST":
        searchFor = request.POST.get("q")
        similar=util.similar_titles(searchFor)
        if isinstance(similar, list):
            return render(request, "encyclopedia/index.html", {
                "entries":similar 
            })
        else:
            return HttpResponseRedirect(reverse('entry', kwargs={'entry': similar}))            
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.similar_titles("")
        })
    
def error(request):
    return render(request,"encyclopedia/error.html")
    
def create(request):
    if request.method =="GET":
        return render(request,"encyclopedia/create.html", {
            "create_form": CreateForm()
        })
    elif request.method == "POST":
        title=request.POST.get("title")
        if isinstance(util.similar_titles(title),str):
            return error(request)
        else:
            content=request.POST.get("text")
            util.save_entry(title,content)
            return HttpResponseRedirect(reverse('entry', kwargs={'entry': title}))            


def randomm(request):
    entries = util.list_entries()
    title = choice(entries)
    return HttpResponseRedirect(reverse('entry', kwargs={'entry': title}))            


def edit(request, entry):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["text"]
            util.save_entry(entry, content)
            return HttpResponseRedirect(reverse("entry", kwargs={"entry": entry}))
    else:
        content = util.get_entry(entry)
        if content==None:
            return error(request)
        form = EditForm(initial={"text": content})
    
    return render(request, "encyclopedia/edit.html", {
        "form": form,
        "entry": entry
    })