# git bot — AI çalışma kuralları

Kişisel kod kasası ve sürekli git senkronizasyonu için otomasyon çalışma alanı.
Arka planda `auto_sync.py` izleyicisi her iş birimini yedekler ve senkronlar.

> ### Tek dosya kuralı
> Bu depoda AI talimatları **yalnızca bu dosyada** tutulur. `CLAUDE.md` tek
> satırlık `@AGENTS.md` importudur. Araç adıyla ikinci bir kural dosyası
> (`GEMINI.md`, `.cursorrules`, `.clinerules`, `copilot-instructions.md`)
> **açılmaz** — aynı metnin kopyaları birbirinden ayrışıyor.
> (04.09.2026: bu dosya ile `GEMINI.md` gerçekten ayrışmıştı, birleştirildi.)

## 0. Önce ortak bağlamı oku

Umut birden çok AI aracı kullanıyor (Claude Code, Antigravity/Gemini, Cline).
Ortak bağlam tek yerde:

```
/Users/umut/ai-context/
├── README.md        ← önce burayı oku
├── 00-umut.md       ← kullanıcı profili ve çalışma tarzı
├── 01-projeler.md   ← proje indeksi
├── kurallar/        ← UYULMASI ZORUNLU kurallar
├── projeler/        ← proje başına tam bağlam
└── bilgi-bankasi/   ← derin teknik notlar
```

Öğrendiğin kalıcı her bilgiyi oraya **geri yaz** —
bkz. `/Users/umut/ai-context/kurallar/baglami-md-ye-yaz.md`.

## 1. 🔴 Gizlilik sınırı (KATI KURAL)

- **Şirket / iş kodu:** Hiçbir şirket, iş, tescilli, müşteri veya işveren
  kodunu/verisini **asla** otomatik commit'leme, push'lama veya senkronlama.
- **Katı izolasyon:** Otomatik commit ve otomatik push **yalnızca** açıkça
  kişisel olan kasalara/projelere uygulanır (ör. `daily-code-vault`).
- Bir şeyin kişisel mi iş mi olduğundan emin değilsen **Umut'a sor**, otomatiğe bırakma.

## 2. Kişisel projelerde otonom çalışma

- Manuel onay için **durma**; kaliteli kodu yaz, testleri çalıştır, değişikliği
  kendin sonuçlandır.
- Kod yazıldığında / özellik tamamlandığında **sık sık** commit ve push et
  (`origin main`).
- Commit mesajları **Conventional Commit** biçiminde: `feat:`, `fix:`,
  `refactor:`, `docs:`, `style:`, `test:`, `chore:`.
- Arka plandaki otomatik senkron izleyicisi sürekli çalışır; her iş birimi
  gerçek zamanlı yedeklenir.

## 3. Kalite standartları & Günlük Otomatik Bakım

- Geçici/çöp kod yazma.
- **Otomatik günlük push:** Sıfırdan yapay/sentetik algoritma modülü üretmek
  yerine; mevcut kod yapısını bozmadan basit temizlik, boşluk (whitespace)
  düzeltmeleri, EOF satır sonu düzeni ve kod hijyeni gibi güvenli bakım işlerini
  yap (`style:` / `chore:`).
- **Kod geliştirilmeyen günler:** Dosyalara zoraki değişiklik eklemek yerine
  boş commit (`git commit --allow-empty`) atarak yeşil kutucukları ve senkronizasyonu
  koru; kod dosyalarına gereksiz dokunma.
- Temiz ve modüler mimari, tam tip belirtimleri (type hints), docstring'ler ve
  kapsamlı birim testleri. Her temizlikten sonra testlerin hatasız geçtiğini doğrula.

## 4. Günlük

Bu depoda çalışma günlüğü `JOURNAL.md` dosyasındadır.
(Diğer kişisel projelerde bu dosyanın adı `WORKLOG.md` — isim birliği ileride
yapılabilir, şimdilik her depo kendi mevcut adını korur.)
