import hashlib
import os
import struct
import math
import numpy as np
from math import pi

# -------------------- HELPER FONKSİYONLAR --------------------

def int_to_bits(n, bit_length=512):
    """Integer'ı 0/1 bit dizisine çevirir (MSB-first, sabit uzunluk)"""
    if n < 0:
        n = n & ((1 << bit_length) - 1)
    return bin(int(n))[2:].zfill(bit_length)

def baslangic_degeri_qthash_hybrid(blok_string: str, onceki_deger: int = 1, quant_bits: int = 256):
    """
    Hybrid versiyon: ROTL ve XOR karışımı ile örüntü kırıcı deterministik işlemler.
    - quant_bits: sin/cos quantization çözünürlüğü.
    """
    if len(blok_string) != 512:
        raise ValueError("Girdi bloğu 512 bit uzunluğunda olmalıdır.")
    if quant_bits < 8 or quant_bits > 4096:
        raise ValueError("quant_bits makul bir aralıkta olmalı (8..4096).")

    MAX_Q = (1 << quant_bits) - 1
    PRIME = (1 << 521) - 1  # modüler tamsayı işlemleri için
    baslangic_degeri = int(onceki_deger) % PRIME

    tabanlar = {'00': 23, '01': 29, '10': 31, '11': 37}
    gruplar = [blok_string[i:i+2] for i in range(0, 512, 2)]
    mask512 = (1 << 512) - 1

    onceki_en_cok = 0

    for i, grup in enumerate(gruplar):
        g = int(grup, 2)
        base = tabanlar[grup]
        pos = i + 1

        angle = ((g + 1) * (pos + 1)) * (pi / 180.0)
        phase = math.sin((baslangic_degeri % (1 << 30)) / float(1 << 30))
        sin_val = math.sin(angle + phase)
        cos_val = math.cos(angle - phase)

        q_sin = int(math.floor(((sin_val + 1.0) / 2.0) * MAX_Q))
        q_cos = int(math.floor(((cos_val + 1.0) / 2.0) * MAX_Q))
        q_sin = max(1, q_sin)
        q_cos = max(1, q_cos)

        exponent = (pos + (q_sin & ((1 << 30) - 1)))
        powmod = pow(base, exponent, PRIME)
        baslangic_degeri = (baslangic_degeri * powmod) % PRIME

        shift = ((i*2 - 1) + onceki_en_cok * base) % 511
        shift = max(1, shift)
        kaydirma = (q_cos << shift) & mask512
        baslangic_degeri = (baslangic_degeri ^ kaydirma) & mask512
        baslangic_degeri = ( (baslangic_degeri << shift) & mask512) | ((baslangic_degeri >> (512 - shift)) & mask512)

        bit_str = int_to_bits(baslangic_degeri, 512)
        invers = int(''.join('1' if b=='0' else '0' for b in bit_str), 2)
        invers_rotl = ( (invers << i) & mask512) | ((invers >> (512 - i)) & mask512)
        baslangic_degeri ^= invers_rotl

        onceki_en_cok = base

    son_deger = baslangic_degeri & mask512
    son_deger |= (1 << 511)
    return int(son_deger) if son_deger != 0 else 1

def generate_qt_hash_data(filename, target_bits=1000000, chunk_size=512):
    """Kendi algoritmanızla veri üretir."""
    with open(f"results/{filename}", "w") as f:
        total_bits_written = 0
        i = 0
        while total_bits_written < target_bits:
            blok = format(i, 'b').zfill(chunk_size)
            int_val = baslangic_degeri_qthash_hybrid(blok, onceki_deger=1, quant_bits=256)
            int_bits = int_to_bits(int_val, chunk_size)

            bits_to_write = min(chunk_size, target_bits - total_bits_written)
            f.write(int_bits[:bits_to_write])
            total_bits_written += bits_to_write
            i += 1
    print(f"{total_bits_written} bit içeren '{filename}' dosyası oluşturuldu.")

def generate_sha512_bit_stream(filename, target_bits=1000000):
    """SHA-512 ile veri üretir ve bitleri yazar."""
    chunk_size = 512 # SHA512 çıktısı 512 bit
    with open(f"results/{filename}", "w") as f:
        total_bits_written = 0
        i = 0
        while total_bits_written < target_bits:
            data = str(i).encode('utf-8')
            sha_hash = hashlib.sha512(data).hexdigest()
            bits = bin(int(sha_hash, 16))[2:].zfill(chunk_size)

            bits_to_write = min(chunk_size, target_bits - total_bits_written)
            f.write(bits[:bits_to_write])
            total_bits_written += bits_to_write
            i += 1
    print(f"{total_bits_written} bit içeren '{filename}' dosyası oluşturuldu.")

if __name__ == "__main__":
    os.makedirs("results", exist_ok=True)
    TARGET_BITS = 1000000

    # Kendi algoritmanız
    generate_qt_hash_data("qthash_test_data.txt", TARGET_BITS)

    # SHA-512
    generate_sha512_bit_stream("sha512_test_data.txt", TARGET_BITS)