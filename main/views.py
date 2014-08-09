from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect as _redirect

from .models import Link
from .util import qrimage
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

            return render(request, 'shortened.html', {
                'hash': hash,
                'uuid': uuid,
                'link': link,
            })
    else:
        form = ShortenUrlForm()

    return render(request, 'homepage.html', {
        'form': form,
    })


def qr(request, hash, save=False):
    """
    """
    l = Link()

    if not l.exists(hash):
        raise Http404

    response = qrimage(hash)
    response = HttpResponse(response, content_type="image/png")

    if not save:
        return response

    header = "attachment; filename='wuss_eu-{0}.png'"
    header = header.format(hash)

    response['Content-Disposition'] = header

    return response


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
    l = Link()

    if not l.exists(hash, uuid):
        raise Http404

    if request.method == 'POST':
        form = ShortenUrlForm(request.POST)
        if form.is_valid():
            link = form.cleaned_data['link']

            try:
                l = Link()
                l.modify(hash, uuid, link)
            except AuthFailure as e:
                raise Http404

            form = ShortenUrlForm()
            return render(request, 'modify.html', {
                'success': True,
                'form': form,
                'hash': hash,
                'uuid': uuid,
            })

    else:
        form = ShortenUrlForm()

    return render(request, 'modify.html', {
        'form': form,
        'hash': hash,
        'uuid': uuid,
    })
