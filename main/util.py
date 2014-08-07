import qrcode
from cStringIO import StringIO

from django.core.cache import cache
from django.conf import settings


def qrimage(hash):
    """
    """
    key = "qr-image-{0}".format(hash)

    image = cache.get(key)

    if image:
        return image

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.ERROR_CORRECT_H,
        box_size=8,
        border=4,
    )

    qr.add_data("{0}/{1}".format(settings.SITE_URL, hash))
    qr.make(fit=True)

    img = qr.make_image()
    io = StringIO()
    img.save(io)

    cache.set(key, io.getvalue(), timeout=300)

    return io.getvalue()
