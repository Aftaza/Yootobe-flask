from datetime import datetime, timedelta

def format_views(angka):
    if angka >= 1000000:
        # Ubah ke format 1jt, 1jt = 1.000.000
        return f'{angka // 1000000}jt'
    else:
        # Format dengan koma sebagai pemisah ribuan
        return '{:,}'.format(angka).replace(',', '.')

def time_status(dt):
    sekarang = datetime.now()
    selisih = sekarang - dt

    if selisih.days >= 365:
        tahun = selisih.days // 365
        waktu = "tahun" if tahun == 1 else "tahun"
        return f"{tahun} {waktu} yang lalu"

    elif selisih.days >= 30:
        bulan = selisih.days // 30
        waktu = "bulan" if bulan == 1 else "bulan"
        return f"{bulan} {waktu} yang lalu"

    elif selisih.days >= 1:
        hari = selisih.days
        waktu = "hari" if hari == 1 else "hari"
        return f"{hari} {waktu} yang lalu"

    elif selisih.seconds >= 3600:
        jam = selisih.seconds // 3600
        waktu = "jam" if jam == 1 else "jam"
        return f"{jam} {waktu} yang lalu"

    elif selisih.seconds >= 60:
        menit = selisih.seconds // 60
        waktu = "menit" if menit == 1 else "menit"
        return f"{menit} {waktu} yang lalu"

    else:
        detik = selisih.seconds
        waktu = "detik" if detik == 1 else "detik"
        return f"{detik} {waktu} yang lalu"