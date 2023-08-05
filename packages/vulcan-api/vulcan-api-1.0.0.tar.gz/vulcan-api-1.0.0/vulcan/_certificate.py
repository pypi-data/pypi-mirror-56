# -*- coding: utf-8 -*-

import platform

import requests
from related import immutable, StringField

from ._utils import uuid, now, get_base_url, log, APP_VERSION, APP_NAME


@immutable
class Certificate:
    pfx = StringField(key="CertyfikatPfx")
    key = StringField(key="CertyfikatKlucz")
    key_formatter = StringField(key="CertyfikatKluczSformatowanyTekst")
    base_url = StringField(key="AdresBazowyRestApi")

    @classmethod
    def get(cls, token, symbol, pin):
        token = str(token).upper()
        symbol = str(symbol).lower()
        pin = str(pin)

        data = {
            "PIN": pin,
            "TokenKey": token,
            "AppVersion": APP_VERSION,
            "DeviceId": uuid(),
            "DeviceName": "Vulcan API",
            "DeviceNameUser": "",
            "DeviceDescription": "",
            "DeviceSystemType": "Python",
            "DeviceSystemVersion": platform.python_version(),
            "RemoteMobileTimeKey": now() + 1,
            "TimeKey": now(),
            "RequestId": uuid(),
            "RemoteMobileAppVersion": APP_VERSION,
            "RemoteMobileAppName": APP_NAME,
        }

        headers = {
            "RequestMobileType": "RegisterDevice",
            "User-Agent": "MobileUserAgent",
        }

        base_url = get_base_url(token)
        url = "{}/{}/mobile-api/Uczen.v3.UczenStart/Certyfikat".format(base_url, symbol)

        log.info("Registering...")

        r = requests.post(url, json=data, headers=headers)
        j = r.json()
        log.debug(j)

        cert = j["TokenCert"]
        log.info("Registered successfully!")

        return cert
