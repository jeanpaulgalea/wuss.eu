from django.http import Http404
from django.shortcuts import render, redirect as _redirect

from .models import Link
from .forms import ShortenUrlForm
from .exceptions import NotFound, AuthFailure


def shorten(request):
    """
    """
    if request.method == 'POST':
        form = ShortenUrlForm(request.POST)
        if form.is_valid():
            link = form.cleaned_data['link']

            l = Link()
            hash, uuid = l.shorten(link)

            return render(request, 'success.html', {
                'link': link,
                'hash': hash,
                'uuid': uuid
            })
    else:
        form = ShortenUrlForm()

    return render(request, 'homepage.html', {
        'form': form,
    })


def redirect(request, hash):
    """
    """
    try:
        l = Link()
        url = l.resolve(hash)
    except NotFound as e:
        raise Http404

    return _redirect(url, permanent=False)


def modify(request, hash, uuid):
    """
    """
    if request.method == 'POST':
        form = ShortenUrlForm(request.POST)
        if form.is_valid():
            link = form.cleaned_data['link']

            try:
                l = Link()
                l.modify(hash, uuid, link)
            except AuthFailure as e:
                raise Http404

            return render(request, 'success.html', {
                'link': link,
                'hash': hash,
                'uuid': uuid,
            })

    else:
        form = ShortenUrlForm()

    return render(request, 'modify.html', {
        'hash': hash,
        'uuid': uuid,
        'form': form,
    })
