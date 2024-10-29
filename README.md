# TelegramMuzikBot

# Telegram Music Bot

Bu proje, Telegram botu olarak çalışan bir müzik indirme aracıdır. Kullanıcılar, bot ile istedikleri şarkının adını yazarak şarkının ses dosyasını indirip alabilirler. Bot, **yt-dlp** kütüphanesini kullanarak YouTube'dan ses dosyalarını indirmektedir.

## Özellikler

- Şarkı adı girerek arama yapma.
- En iyi ses kalitesi ile MP3 formatında indirme.
- Geçersiz dosya adlarını temizleme.
- İndirme klasörünü otomatik olarak yönetme.

## Gerekli Kütüphaneler

Bu projeyi çalıştırmak için aşağıdaki kütüphanelerin yüklü olması gerekmektedir:

- `pyTelegramBotAPI`
- `yt-dlp`

Bu kütüphaneleri yüklemek için şu komutları kullanabilirsiniz:

```bash
pip install pyTelegramBotAPI yt-dlp
```

## Kurulum

1. `TOKEN` değişkenine Telegram botunuzun API anahtarını girin.
2. `downloads` adlı bir indirme klasörü oluşturulur. Proje dizininde bu klasör bulunmalıdır.
3. Botu çalıştırmak için terminal veya komut istemcisine şu komutu girin:

```bash
python your_script_name.py
```

## Kullanım

1. Telegram'da botunuzu bulun ve başlatın.
2. Dinlemek istediğiniz şarkının adını gönderin.
3. Bot, şarkıyı bulacak ve MP3 formatında ses dosyasını size gönderecektir.

## Hata Ayıklama

Bot çalışırken bir hata ile karşılaşırsanız, hata mesajları konsolda görüntülenecektir. Genel hata durumları için özel mesajlar gönderilmektedir.

## Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.

## Geliştirici

- [Adil Oğuz]
