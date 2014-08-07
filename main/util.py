import qrcode
from cStringIO import StringIO

from django.core.cache import cache


def qrimage(data):
    """
    """
    response = cache.get(data)

    if response:
        return response

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.ERROR_CORRECT_H,
        box_size=8,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    #qr.make()

    img = qr.make_image()
    io = StringIO()
    img.save(io)
    response = io.getvalue()

    cache.set(data, response, timeout=300)

    return response
