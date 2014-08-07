import qrcode

from cStringIO import StringIO

from django.http import Http404, HttpResponse
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

            return render(request, 'homepage.html', {
                'form': form,
                'hash': hash,
                'uuid': uuid,
            })
    else:
        form = ShortenUrlForm()

    return render(request, 'homepage.html', {
        'form': form,
    })


def qr(request, hash):
    """
    """
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.ERROR_CORRECT_H,
        box_size=8,
        border=4,
    )
    qr.add_data("http://wuss.eu/"+hash)
    qr.make(fit=True)
    #qr.make()

    img = qr.make_image()

    io = StringIO()
    img.save(io)

    return HttpResponse(io.getvalue(), content_type='image/png')


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
