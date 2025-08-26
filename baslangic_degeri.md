**wave\_seed\_generator.py Fonksiyonunun Matematiksel Açıklaması**

**1) Girdi**

* 512‑bitlik blok:
  `B = b1 b2 ... b512,  bi ∈ {0,1}`

  Bu blok 2‑bit gruplara ayrılır:
  `Gi = (b2i-1, b2i),  i = 1,...,256`

* Başlangıç değeri:
  `S0 = 1`

* Kuantizasyon çözünürlüğü:
  `q = quant_bits` (varsayılan: 256)

---

**2) Grup taban seçimi**
Her 2‑bitlik grup için taban şu şekilde tanımlanır:

```
taban(Gi) =
    3   eğer Gi = 00
    5   eğer Gi = 01
    7   eğer Gi = 10
    11  eğer Gi = 11
```

---

**3) Trigonometrik açı hesaplama**
Öncelikle:
`θi = (g+1)(i+1) * π/180`

Burada `g = int(Gi)`.

Ek faz kayması:
`φ = sin((Si-1 mod 2^30) / 2^30)`

Trigonometrik değerler:

```
sin_val = sin(θi + φ)
cos_val = cos(θi - φ)
```

---

**4) Quantization (diskretleştirme)**
**Bu adım chatGPT tarafından önerilmiştir**
`[-1,1]` aralığını `[0, 2^q - 1]` aralığına yayar:

```
q_sin = floor(((sin_val + 1) / 2) * (2^q - 1))
q_cos = floor(((cos_val + 1) / 2) * (2^q - 1))
```

Eğer sonuç sıfır çıkarsa en az `1` yapılır.

---

**5) Modüler üs alma**
Üs değeri:
`ei = (i+1) + (q_sin mod 2^30)`

Sonuç:
`pi = taban(Gi)^ei mod P`

Burada `P = 2^521 - 1` (Mersenne asalı).

---

**6) Karıştırma adımları**
Öncelikle:
`Si = (Si-1 * pi) mod P`

Ardından cos’a bağlı kaydırma:

```
Δi = (q_cos << (i mod 512)) & (2^512 - 1)
Si = (Si XOR Δi) & (2^512 - 1)
```

Son adımda bit döndürme:
`Si = ROTL(Si, i mod 512, 512)`

---

**7) Çıkış**
Sonuç:
`Sfinal = S256 & (2^512 - 1)`

Ve **MSB = 1** olacak şekilde ayarlanır.

---

**Özet**
Fonksiyon her 512‑bitlik blok için:
`Sfinal = F(B, S0)`

Burada `F`, şu işlemlerden oluşan bir **karma fonksiyondur**:

* Modüler üs alma (kriptografik karıştırma)
* Sin/Cos tabanlı quantization (kaotik analog etki)
* XOR ve bit rotasyonu (dağılım genişletme)

Sonuç: deterministik, fakat oldukça **kaotik görünümlü 512‑bit sayı**.
