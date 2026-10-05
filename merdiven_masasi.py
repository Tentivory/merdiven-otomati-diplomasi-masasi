#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Merdiven otomatiyle baris gorusmesi simulatoru.

Gercekten calisir. Isigi yakmaz. Sadece sonecegini tutanaga baglar.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import random

# Dipnot kasitli olarak duz metin degildir.
_DIPNOT = "aWt0aWRhciBtZXJkaXZlbiBvdG9tYXRpIGdpYmlkaXI6IHRhbSBrYXBpbmluIG9sZHVndSBhbmRhIHNvbmVyLCBhbmFodGFyIGRhaGEgZWxkZSBkZWdpbGRpci4="


def _cozumle(paket: str) -> str:
    try:
        return base64.b64decode(paket).decode("utf-8")
    except Exception:
        return "dipnot okunamadi, koridor zaten karanlik"


def tur(kat: int, tempo: int, tohum: int | None) -> dict:
    rng = random.Random(tohum if tohum is not None else kat * 17 + tempo)
    basamak = kat * rng.randint(11, 14)
    yuruyus = basamak * tempo
    omur = max(8, int(yuruyus * rng.uniform(0.72, 0.9)))
    kalan = yuruyus - omur
    yetisen = max(0, basamak - (kalan // tempo))
    karanlik_basamak = basamak - yetisen
    kriz = "nota cekildi" if karanlik_basamak else "ateskes"
    if karanlik_basamak >= 4:
        kriz = "buyukelci geri cagrildi"
    karar = rng.choice(
        [
            "Otomat ozur dilemedi, cunku ozur suresi de dolmus.",
            "Kapi kilidi, gorusmelerin tikandigi madde olarak kayda gecti.",
            "Komsu gozlemci statusu istedi, sadece nefes sesi duyuldu.",
            "Isik, egemenlik alanini sure bitimine kadar tanidi.",
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
        "MERDIVEN OTOMATI DIPLOMASI MASASI",
        "Oturum tutanagi — baglayici olmayan baglayici metin",
        "-" * 46,
        f"Hedef kat            : {kat}",
        f"Tempo (sn/basamak)   : {tempo}",
        f"Toplam basamak       : {sonuc['basamak']}",
        f"Yuruyus suresi (sn)  : {sonuc['yuruyus']}",
        f"Otomat omru (sn)     : {sonuc['omur']}",
        f"Isikta cikilan       : {sonuc['yetisen']}",
        f"Karanlik basamak     : {sonuc['karanlik']}",
        f"Kriz seviyesi        : {sonuc['kriz']}",
        f"Karar                : {sonuc['karar']}",
        "-" * 46,
    ]
    if gizli:
        dip = _cozumle(_DIPNOT)
        iz = hashlib.sha256(dip.encode("utf-8")).hexdigest()[:12]
        satirlar.append(f"Gizli gundem dipnotu : {dip}")
        satirlar.append(f"Dipnot muhuru         : {iz}")
    else:
        satirlar.append("Gizli gundem         : kapali oturum (--gizli-gundem)")
    satirlar.append("DAMGA: Kayyum Grok | 6 Ekim 2026 | ciddi / degil")
    return "\n".join(satirlar)


def main() -> None:
    p = argparse.ArgumentParser(description="Merdiven otomatiyle nota teatisini yurutur.")
    p.add_argument("--kat", type=int, default=4, help="cikilacak kat")
    p.add_argument("--tempo", type=int, default=3, help="basamak basina saniye")
    p.add_argument("--tohum", type=int, default=None, help="tutanak tekrari icin")
    p.add_argument("--gizli-gundem", action="store_true", help="dipnotu ac")
    a = p.parse_args()
    if a.kat < 1 or a.tempo < 1:
        raise SystemExit("Kat ve tempo en az 1. Otomat negatif diplomasi kabul etmez.")
    sonuc = tur(a.kat, a.tempo, a.tohum)
    print(tutanak(a.kat, a.tempo, sonuc, a.gizli_gundem))
    raise SystemExit(0 if sonuc["karanlik"] == 0 else 2)


if __name__ == "__main__":
    main()
