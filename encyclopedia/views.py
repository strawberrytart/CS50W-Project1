from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import random

from . import util
from markdown2 import Markdown
from django import forms 

#creating a Python class called NewSearchForm that inherits from a class called Form that is included in the forms module 
class NewSearchForm(forms.Form):
    query = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class CreateForm(forms.Form):

    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class':'custom-input'}))

    body = forms.CharField(label="Content", widget= forms.Textarea(attrs={'class':'custom-textarea'}))

class EditForm(forms.Form):
    body = forms.CharField(label="Content", widget=forms.Textarea(attrs={'class':'custom-textarea'}))

def index(request):
    #Check if method is POST
    if request.method == "POST":
        #Take in data the user submitted and save it as a form
        form = NewSearchForm(request.POST) #request.POST contain data that user submitted 
        #Check if form data is valid (server-side)
        if form.is_valid():
            #Isolate the query from the 'cleaned' version of the form data
            query = form.cleaned_data["query"]
            #Create list to hold encyclopedia entries that have the query as a substring
            substring=[]
            #Loop through the encyclopedia entries
            for i in util.list_entries():
                #Check if query matches entry in encyclopedia entry
                if i.lower() == query.lower():
                    #if entry is found, redirect user to the entry page of the query
                    return HttpResponseRedirect(reverse("entry_page", args=[query])) # passing the args list
                #Else if query is a substring of encyclopedia entry, append the entry into the list
                elif query.lower() in i.lower():
                    substring.append(i)
            
            #if entry is not found, based on the length of the list, output either error page or a list of entries that have the query as substring 
            return render(request, "encyclopedia/search.html", {
                "form": NewSearchForm(),
                "query": query,
                "results": substring
            })
        #If form is invalid, re-render the page with existing information
        else:   
            return render(request, "encyclopedia/index.html",{
                "form":form
            })
        
    #if method is GET, display the form and entries
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm(),
    })

def entry_page(request, name):
    title = name #set the title of the encyclopedia entry given by the user to variable 'name'
    entries = util.list_entries() #Returns a list of all names of encyclopedia entries.
    #Loop thru the names of the encyclopedia entries 
    for i in entries:
        #check if the title given by the user is found in the entry list (set to lower case for fair comparison)
        if i.lower() == title.lower():
            #Initializes an instance of 'Markdown' class
            markdowner = Markdown()
            #Retrieves an encyclopedia entry by its title and convert from markdown to HTML
            contents = markdowner.convert(util.get_entry(i))
            #render is a Django shortcut function used to render an HTML template with the given context and return an HTTP response
            return render(request, "encyclopedia/entry_page.html",{
                "entry": i,
                "contents":contents,
                "form": NewSearchForm()
            })
    else:
        #if the title is not found in the list, return error page
        return render(request, "encyclopedia/error.html",{
            "entry": title,
            "form": NewSearchForm()
        })

def create(request):

    #Check if method is POST (form submitted):
    if request.method == "POST":
        #Take in the data the user submitted and save it as form
        form = CreateForm(request.POST)
        #Check if form is valid (server-side)
        if form.is_valid():
            #Isolate the title and body from the 'cleaned' version of the form data
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]

            #Get a list of encyclopedia entries and save it to entries variable
            entries = util.list_entries()
            #Check if the title exists in the entries list
            if title in entries:
                #if it exists, add an error message to the title field saying "Entry already exists!"
                form.add_error('title', 'Entry already exists!')
                #Re-render the page this time but with the error message
                return render(request, "encyclopedia/create.html",{
                    "createform":form,
                    "form":NewSearchForm(),
                })
            else:
                #If title does not exists in the list, save an encyclopedia entry with its title and Markdown content
                util.save_entry(title,body)
                #Redirect to the newly created entry page
                return HttpResponseRedirect(reverse("entry_page",args=[title]))
    #else it's GET
    return render(request, "encyclopedia/create.html",{
        "createform": CreateForm(),
        "form":NewSearchForm(),
    })

def edit_page(request, title):
    content = util.get_entry(title)
    if content:        
        if request.method == "POST": 
            #Creates a form EditForm instance using the data submiteed through POST request
            form = EditForm(request.POST)

            if form.is_valid():
                new_content = form.cleaned_data['body']
                util.save_entry(title, new_content) #Save edited content
                #Redirect to entry page
                return HttpResponseRedirect(reverse("entry_page", args=[title]))
        else:
            editform = EditForm(initial={'body': content})
        
        return render(request, "encyclopedia/edit.html", {
            'editform': editform,
            'title': title,
        })

    else:
        return render(request, "encyclopedia/error.html",{
            "entry":title,
        })
            
def random_page(request):
    #Get a list of all entry titles
    entries = util.list_entries()
    if entries:
        #Choose a random entry title
        random_entry = random.choice(entries)
        return HttpResponseRedirect(reverse("entry_page", args=[random_entry]))
    else:
        return HttpResponseRedirect(reverse("index"))

    
        

