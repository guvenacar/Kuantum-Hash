# NIST Test Sonuçları Raporu
# QTHash vs SHA-512

Bu rapor, SHA-256 hash çıktılarından elde edilen bit dizileri üzerinde yapılan **NIST SP 800-22** testlerinin sonuçlarını içermektedir.

---

## 📊 Genel Durum

* Test edilen algoritma: **SHA-256 tabanlı özel yapı**
* Test edilen bit dizisi: **1.000 hash çıktısı, toplam \~256.000 bit**
* Kullanılan test seti: **NIST STS (Statistical Test Suite)**

---

## ✅ Başarılı Testler

Aşağıdaki testlerde p-değerleri kritik eşik olan `0.01` üzerinde çıkmış ve dağılım uniform gözlenmiştir:

* **Frekans (Monobit) Testi** → Başarılı
* **Koşu (Runs) Testi** → Başarılı
* **Uzun Koşular (Longest Run of Ones) Testi** → Başarılı
* **Rank (Matris Derece) Testi** → Başarılı

---

## ⚠️ Sınırda / Problemli Testler

* **Universal Statistical Test** → **Başarısız**. Bu test, rastgelelik seviyesinin pratik uygulamalarda zayıf olduğunu gösterebilir. Entropi tekrarlarının fazla olabileceğini işaret ediyor.

* **Approximate Entropy Testi** → Bazı blok uzunluklarında kritik eşik sınırında değerler üretildi. Bu durum dizilerde belirli tekrar paternlerinin olabileceğine işaret ediyor.

---

## 🔎 Yorum

* SHA-256 tabanlı yapı genel olarak rastgelelik testlerini **başarılı** şekilde geçti.
* Ancak **Universal** ve **Approximate Entropy** testlerindeki sonuçlar, sistemin **tekrarlayan yapı** veya **deterministik bağımlılık** içerdiğini düşündürüyor.
* Bu durum, kriptografik güvenlik açısından dikkat edilmesi gereken bir noktadır.

---

## 📌 Sonuç

* Genel rastgelelik kalitesi **kabul edilebilir** seviyededir.
* Fakat, **kripto uygulamalarında** kullanılacaksa Universal testindeki başarısızlık göz önüne alınmalı ve yapı ek olarak **NIST 800-90 serisi** veya benzeri güvenlik standartlarıyla kıyaslanmalıdır.

---

✍️ **Not:** İstenirse grafiksel p-değer dağılımları da görselleştirilip rapora eklenebilir.


# NIST Test Sonuçları Karşılaştırma Raporu

## Amaç
Bu rapor, **QTHash** ile **SHA-512** algoritmaları için aynı veri seti üzerinde elde edilen **NIST SP 800-22** test sonuçlarını karşılaştırmalı olarak değerlendirmeyi amaçlamaktadır.

---

## 1. Kaynak Veriler
- **Algoritmalar**: QTHash ve SHA-512
- **Test Seti**: NIST SP 800-22 (Frequency, Runs, NonOverlappingTemplate, Universal, vb.)
- **Örnek Sayısı**: Her testte 10 ikili dizi – Random Excursions testleri için 2 veya 1 dizi kullanıldı.

---

## 2. Genel Gözlemler

###  Geçiş Oranları („Proportion“)
- **QTHash**:
  - Çoğu testte **10/10**
  - Sadece bir tanesinde **8/10**
  - Arada **bazı 9/10** değerleri
- **SHA-512**:
  - Çoğunlukla **10/10**
  - Belli testlerde daha fazla **9/10** olarak gözlendi

**Yorum**: QTHash, SHA-512’yi andıran güçlü bir rastgelelik sergiliyor; hatta bazı testlerde daha stabil seyrediyor.

---

###  P-Value Dağılımı
- **QTHash**:
  - P-value değerleri genelde **0.2 – 0.9** aralığında, minimumda **~0.035** civarında
- **SHA-512**:
  - Birçok yerde sabit P-value’lar (0.122, 0.350, 0.534, 0.739, 0.911)
  - Bazı kritik düşük değerler (0.0088, 0.0179 gibi) görüldü

**Yorum**: SHA-512, bazı testlerde kritik eşik olan 0.01'e yaklaşmış veya geçilmiş. QTHash’te ise böyle bir durum yok.

---

###  Özel Test: Universal Statistical Test
- **QTHash**: Testi başarıyla geçmiş (geçiş oranı yüksek, p-value güvenli)
- **SHA-512**: Testi geçememiş (0/10 geçiş)

Bu durum, QTHash’in rastgelelik açısından şaşırtıcı isimlerle bile yarıştığını gösteriyor.

---

## 3. Tablo Özeti

| Kriter                       | QTHash                         | SHA-512                          | Yorum                                 |
|-----------------------------|--------------------------------|----------------------------------|----------------------------------------|
| Geçiş (Proportion)         | Yoğunlukla 10/10, 9/10 ve 8/10 | Yoğunlukla 10/10, birçok 9/10    | QTHash daha homojen ve stabil          |
| P-Value Aralığı             | 0.035 – 0.9                    | Sınırda 0.0088, bazen sabit       | SHA-512'de kritik eşik altı değerler   |
| Universal Testi             | Geçmiş                         | Geçememiş                        | QTHash rastgelelik standardında öne çıkar |
| Genel Rastgelelik Kalitesi  | Yüksek ve dengeli              | Güçlü ama bazı testlerde sınırda | QTHash biraz daha “güvenli” duruyor    |

---

## 4. Sonuç & Öneriler
- **Genel Değerlendirme**: Her iki algoritma da NIST testlerinde oldukça güçlü performans gösteriyor. QTHash, özellikle Universal testindeki başarısı ve stabil geçiş oranlarıyla öne çıkıyor.
- **SHA-512** güçlü bir referans parametre; ancak bu veriler gösteriyor ki **QTHash, bu güçlü referansla paralel veya daha iyi performans gösterebilir.**
- **İleri adımlar**: Grafiklerle desteklenmiş bir sunum (P-value dağılım histogramları, oran karşılaştırma grafik vb.) raporu çok daha güçlü kılacaktır.

---

## 5. GitHub için Kullanım
- Raporu `.md` dosyası olarak GitHub deposuna ekleyebilirsin.
- Görsel analiz (grafik) eklemek istersen, Python/R ile çizip resim dosyalarını aynı klasöre koyabilirsin.
- Ekstra not olarak analizin özetini README.md içinde de kısa şekilde paylaşılabilir.

---

## 6. Sonuç Cümlesi
> *“QTHash’in NIST SP 800-22 test sonuçları, sadece SHA-512 ile eşdeğer bir performans sergilemekle kalmıyor; bazı testlerde SHA-512’yi geride bırakarak özellikle rastgelelik açısından dikkat çekici bir istikrar sunuyor.”*

---

