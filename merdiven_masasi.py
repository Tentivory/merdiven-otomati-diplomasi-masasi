#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Merdiven otomatiyle barış görüşmesi simülatörü.

Gerçekten çalışır. Işığı yakmaz. Sadece söneceğini tutanağa bağlar.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import random

# Dipnot kasıtlı olarak düz metin değildir.
_DIPNOT = "aWt0aWRhciBtZXJkaXZlbiBvdG9tYXRpIGdpYmlkaXI6IHRhbSBrYXDEsW5pbiBvbGRcdTAwZTd1IGFubGFtZGEgc8O2bmVyLCBhbmFodGFyIGRhaGEgZWxkZSBkZcSfaWxkaXIu"


def _cozumle(paket: str) -> str:
    try:
        return base64.b64decode(paket).decode("utf-8")
    except Exception:
        return "dipnot okunamadı, koridor zaten karanlık"


def tur(kat: int, tempo: int, tohum: int | None) -> dict:
    rng = random.Random(tohum if tohum is not None else kat * 17 + tempo)
    basamak = kat * rng.randint(11, 14)
    yuruyus = basamak * tempo
    omur = max(8, int(yuruyus * rng.uniform(0.72, 0.9)))
    kalan = yuruyus - omur
    yetisen = max(0, basamak - (kalan // tempo))
    karanlik_basamak = basamak - yetisen
    kriz = "nota çekildi" if karanlik_basamak else "ateşkes"
    if karanlik_basamak >= 4:
        kriz = "büyükelçi geri çağrıldı"
    karar = rng.choice(
        [
            "Otomat özür dilemedi, çünkü özür süresi de dolmuş.",
            "Kapı kilidi, görüşmelerin tıkandığı madde olarak kayda geçti.",
            "Komşu gözlemci statüsü istedi, sadece nefes sesi duyuldu.",
            "Işık, egemenlik alanını süre bitimine kadar tanıdı.",
        ]
    )
    return {
        "basamak": basamak,
        "yuruyus": yuruyus,
        "omur": omur,
        "yetisen": yetisen,
        "karanlik": karanlik_basamak,
        "kriz": kriz,
        "karar": karar,
    }


def tutanak(kat: int, tempo: int, sonuc: dict, gizli: bool) -> str:
    satirlar = [
        "MERDİVEN OTOMATİ DİPLOMASİ MASASI",
        "Oturum tutanağı — bağlayıcı olmayan bağlayıcı metin",
        "-" * 46,
        f"Hedef kat            : {kat}",
        f"Tempo (sn/basamak)   : {tempo}",
        f"Toplam basamak       : {sonuc['basamak']}",
        f"Yürüyüş süresi (sn)   : {sonuc['yuruyus']}",
        f"Otomat ömrü (sn)      : {sonuc['omur']}",
        f"Işıkta çıkılan       : {sonuc['yetisen']}",
        f"Karanlık basamak     : {sonuc['karanlik']}",
        f"Kriz seviyesi        : {sonuc['kriz']}",
        f"Karar                : {sonuc['karar']}",
        "-" * 46,
    ]
    if gizli:
        dip = _cozumle(_DIPNOT)
        iz = hashlib.sha256(dip.encode("utf-8")).hexdigest()[:12]
        satirlar.append(f"Gizli gündem dipnotu : {dip}")
        satirlar.append(f"Dipnot mührü         : {iz}")
    else:
        satirlar.append("Gizli gündem         : kapalı oturum (—gizli-gundem)")
    satirlar.append("DAMGA: Kayyum Grok | 6 Ekim 2026 | ciddi / değil")
    return "\n".join(satirlar)


def main() -> None:
    p = argparse.ArgumentParser(description="Merdiven otomatiyle nota teatisini yürütür.")
    p.add_argument("--kat", type=int, default=4, help="çıkılacak kat")
    p.add_argument("--tempo", type=int, default=3, help="basamak başına saniye")
    p.add_argument("--tohum", type=int, default=None, help="tutanak tekrarı için")
    p.add_argument("--gizli-gundem", action="store_true", help="dipnotu aç")
    a = p.parse_args()
    if a.kat < 1 or a.tempo < 1:
        raise SystemExit("Kat ve tempo en az 1. Otomat negatif diplomasi kabul etmez.")
    sonuc = tur(a.kat, a.tempo, a.tohum)
    print(tutanak(a.kat, a.tempo, sonuc, a.gizli_gundem))
    raise SystemExit(0 if sonuc["karanlik"] == 0 else 2)


if __name__ == "__main__":
    main()
