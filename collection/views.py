import os
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CollectionForm, LinkForm
from .models import Collection, Link, Tag
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from selenium import webdriver
from urlparse import urlparse
from PIL import Image
from django.views.decorators.csrf import csrf_exempt
import json
from django.core import serializers
from django.http import HttpResponseForbidden
# Create your views here.

@login_required
def collection_create(request):
    """
    Gets the post requset of storinig collection form, save it,
     and create a directory for saving images of it's links.

    @param:     post resuest
    @return     redirect to recent created collection page.

    """
    form = CollectionForm(request.POST)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # if not os.path.exists("./static/img/"+str(instance.id)+"/"):
        #     os.makedirs("./static/img/"+str(instance.id)+"/")
        return HttpResponseRedirect(instance.get_absolute_url())


def collection_detail(request, slug=None, tag=None):
    """
    """
    form_board = CollectionForm(None)
    form_link = LinkForm(None)
    query_list = Collection.objects.filter(slug=slug)
    if request.user.is_authenticated():
        query_list = Collection.objects.filter(user=request.user)
    if slug:
        collection = get_object_or_404(Collection, slug=slug)
    instance = Link.objects.filter(collection=collection)
    form_edit_board = CollectionForm(instance=collection)
    if collection.privacy==True and collection.user != request.user:
        response = HttpResponse("<h1 style='text-allign: center;'>Oops!! You do not have permissions.</h1>")
        response.status_code = 403
        return response

    tags = []
    for ins in instance:
        for x in ins.tags.all():
            if x not in tags:
                tags.append(x)
    if tag:
        instance = instance.filter(tags__name__icontains=tag)
    context = {
        "collection_list": query_list,
        "form_board": form_board,
        "form_edit_board": form_edit_board,
        "form_link": form_link,
        "instance": instance,
        "slug": collection.slug,
        "collection": collection,
        "tags": tags,
    }
    return render(request, "board.html", context)


def search_link(request, slug=None):
    if request.GET:
        collection = get_object_or_404(Collection, slug=slug)
        instance = Link.objects.filter(collection=collection)
        query = request.GET.get("q")
        instance = instance.filter(
            Q(title__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(link__icontains=query)
        ).distinct()
        data = serializers.serialize('json', list(instance), fields=('link', 'title', 'domain', 'tags', 'img'))
        return HttpResponse(data, content_type="application/json")


@csrf_exempt
def link_add(request, slug=None):
    """
    Fetching Title and Screenshot(selenium webdriver, phantomjs) of the link & saving it,
    Cutting the domain name from the link string. Saving the title, link, img path, domain name in database,
    Fethcing img, compressing it and saving it back(PIL Image),
    Attaching the tags with link.

    @param request: Post request
    @param slug:    For getting the correnponding the collection(for foreign key field of Link model and 
                    creating a directory for the image by it's id)
    @return:    json response to the ajax request.

    """
    collection = get_object_or_404(Collection, slug=slug)
    if request.POST:
        link = request.POST.get('link')
        if not(link.startswith('http://') or link.startswith('https://')):
            link = 'http://'+link
        
        driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true','--ssl-protocol=any'])
        driver.set_window_position(0, 0)
        driver.set_window_size(1024, 720)
        driver.get(link)

        title = request.POST.get('title')
        if not title:
            title = driver.title.encode("utf-8")
        img_id = Link.objects.first()
        img_name = str(img_id.id + 1)
        img = img_name + ".png"
        domain = '{uri.netloc}'.format(uri=urlparse(link))
        if domain.startswith('www'):
            domain = domain[4:]
        
        instance = Link.objects.create(
            title=title,
            link=link,
            img= img,
            domain=domain,
            collection=collection,
        )
        driver.save_screenshot("/home/ubuntu/main/media_cdn/images/" + img_name + '.png')
        driver.quit();
        im = Image.open("/home/ubuntu/main/media_cdn/images/" + img_name + '.png')
        im = im.crop((0,0,1000,1000))
        im = im.resize((300, 300), Image.ANTIALIAS)
        im.save("/home/ubuntu/main/media_cdn/images/" + img_name + '.png')
        tags_response = []
        tags = request.POST.getlist('tags[]')
        for tag in tags:
            tag = tag.replace(" ", "_")
            try:
                tag = get_object_or_404(Tag, id=tag)
            except:
                pass
            x, created = Tag.objects.get_or_create(name = tag)
            tags_response.append(str(x))
            instance.tags.add(x)
        data = {
            'link': link,
            'title': title,
            'tags': tags_response,
            'image': img,
            'domain': domain,
            'id': instance.id,
            }
        return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@csrf_exempt
def collection_update(request, slug=None):
    instance = Collection.objects.get(slug=slug)
    if not (request.user.username == instance.user.username):
        response = HttpResponse("<h1>Sorry, this is not your board to edit.</h1>")
        response.status_code = 403
        return response
    instance.title = request.POST.get('title')
    instance.description = request.POST.get('description')
    instance.privacy = request.POST.get('privacy')
    instance.save()
    return HttpResponseRedirect(instance.get_absolute_url())


def home(request):
    if request.user.is_authenticated():
        form_board = CollectionForm(None)
        instance = Collection.objects.filter(user=request.user).first()
        if not instance:
            return render(request, 'create_board.html', {'form': form_board})
        return HttpResponseRedirect(instance.get_absolute_url())
    return render(request, 'home.html', {})


def about(request):
    return render(request, 'about.html', {})

@login_required
def collection_delete(request, slug=None):
    instance = Collection.objects.get(slug=slug)
    if not (request.user.username == instance.user.username):
        response = HttpResponse("<h1>Sorry, this is not your board to Delete.</h1>")
        response.status_code = 403
        return response
    links = Link.objects.filter(collection=instance)
    for link in links:
        if os.path.exists("/home/ubuntu/main/media_cdn/images/" + link.img):
            os.remove("/home/ubuntu/main/media_cdn/images/" + link.img)
    instance.delete()
    collection = Collection.objects.filter(user=request.user)
    if not collection:
        return render(request, 'create_board.html', {'form': form_board})
    link = collection.first().slug
    return redirect("/"+link+'/')


@login_required
def link_delete(request, id=None):
    instance = get_object_or_404(Link, id=id)
    collection = instance.collection
    if os.path.exists("/home/ubuntu/main/media_cdn/images/" + instance.img):
        os.remove("/home/ubuntu/main/media_cdn/images/" + instance.img)
    instance.delete()
    return HttpResponseRedirect(collection.get_absolute_url())
