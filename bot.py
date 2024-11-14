from telethon import TelegramClient, events
import random
import re
import sqlite3
from telethon import Button
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from requests.adapters import HTTPAdapter
from mezhepler import get_mezhepler_info 
from ö_söz import get_random_quote
import httpx
import http.client
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerChat
import json
from hijri_converter import Gregorian, Hijri
import asyncio
import os
from telethon.tl.types import ChannelParticipantsAdmins  # Adminleri almak için gerekli import
from datetime import datetime


# API ID ve API Hash bilgilerini buraya ekle
api_id = '28319460'  # Kendi API ID'nizi buraya yazın
api_hash = '2b96c98ca24a841eaf687db2cb8082c5'  # Kendi API Hash'inizi buraya yazın
bot_token = '7763011142:AAFlwQNLG7M01pbcQd2qE9kCb57ho5Ett_A'

# Telegram istemcisi oluştur
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)


@client.on(events.NewMessage)
async def my_event_handler(event):
    username = event.sender.username or event.sender.id

    # Kullanıcıyı sözlükte kontrol et
    if username not in user_data:
        user_data[username] = {'message_count': 0}

    user_data[username]['message_count'] += 1
    message_text = event.message.message

    # Komutları kontrol et
    if message_text.startswith('/startt'):
        await event.respond(f'Esteuzubillah Selamın Aleyküm, {username}! ')
    elif message_text.startswith('/count'):
        await event.respond(f'{username} {user_data[username]["message_count"]} mesaj gönderdin.')
    if message_text.startswith('dedikodu'):
        await event.respond('Esteuzubillah dedikodu haramdır..!')
    if message_text.startswith('Müslümanmısın'):
        await event.respond('Elhamdülillah Çok şükür, Müslümanım.')
    if message_text.startswith('besmele'):
        await event.respond('**BİSMİLLAHİRRAHMANİRRAHİM**.')
    if message_text.startswith('Ne zamandan beri müslümansın'):
        await event.respond('Kalu beladan beri.')
    if message_text.startswith('Rabbin kimdir'):
        await event.respond('Rabbim Allahu Tealadır (c.c)')
    if message_text.startswith('Seni kim yarattı'):
        await event.respond('Beni Alemlerin Rabbi Olan Allah yarattı.')
    if message_text.startswith('esmaül hüsna'):
        await event.respond('Esmaül Hüsna İçin /99 komutunu kullanınız..')
    if message_text.startswith('/developer'):
        await event.respond('__Bu botu kodlayan ve geliştiren değerli sahibim:__ @SakirBey 💻') 
    if message_text.startswith('/ekip'):
        await event.respond('**Emeği Geçenler...**\n\n@SakirBey 💎\n\n@Murrroooooooo 👑\n\n@Unknow41E ⚡️\n\n__Hepinize Canı Gönülden Teşekkürler...__')
    if message_text.startswith('Abdestin farzı kaç'):
        await event.respond('Kuranda abdestin dört farzı belirtilmiştir. Bunlar:\n\n1.**Yüzün Yıkanması**: “Yüzlerinizi yıkayın.” (Maide Suresi, 5:6)\n\n2.**Ellerin Dirseklerle Birlikte Yıkanması:** “Ellerinizi dirseklerinize kadar yıkayın.” (Maide Suresi, 5:6)\n\n3.**Başın 4/1 Mesh Edilmesi:** “Başlarınızı mesh edin.” (Maide Suresi, 5:6)\n\n4.**Ayakların Aşık Kemiklerine Kadar Mesh Edilmesi:** “Ayaklarınızı topuklarınıza kadar mesh edin.” (Maide Suresi, 5:6)\n\nBu dört unsur abdestin farzlarıdır ve abdestin geçerli olması için bu adımların yerine getirilmesi gereklidir.')

@client.on(events.NewMessage(pattern='/mezhep (.+)'))
async def mezhep_handler(event):
    mezhep = event.pattern_match.group(1).strip()  # Kullanıcının gönderdiği mezhep ismini al
    info = get_mezhepler_info(mezhep)
    await event.respond(info)

@client.on(events.NewMessage(pattern="/tarih"))
async def tarih(event):
    # Güncel Miladi tarih
    miladi_tarih = datetime.now()
    miladi_str = miladi_tarih.strftime("%Y-%m-%d")  # Yıl-Ay-Gün formatında
    
    # Hicri tarihe çevirme
    hicri_tarih = Gregorian(miladi_tarih.year, miladi_tarih.month, miladi_tarih.day).to_hijri()
    hicri_str = f"{hicri_tarih.year}-{hicri_tarih.month}-{hicri_tarih.day}"
    
    # Yanıt mesajı
    tarih_mesaji = (
        f"**📅 Güncel Tarihler**\n\n"
        f"**Miladi Tarih:** {miladi_str}\n"
        f"**Hicri Tarih:** {hicri_str}"
    )
    
    await event.reply(tarih_mesaji)

@client.on(events.NewMessage(pattern='/ösöz'))
async def handler(event):
    random_quote = get_random_quote()  # ö_söz.py dosyasındaki fonksiyondan rastgele sözü al
    await event.respond(random_quote)  # Kullanıcıya rastgele sözü gönder


# 1. Rastgele Hadis veya Ayet Gönderimi
hadisler = [
    "Bir kimse ilim öğrenmek için bir yola girerse, Allah ona cennetin yolunu kolaylaştırır. **(Müslim)**",
    "Kolaylaştırınız, zorlaştırmayınız; müjdeleyiniz, nefret ettirmeyiniz. **(Buhari)**",
    "Ameller niyetlere göredir. **(Buhari ve Müslim)**",
    "Müslüman, elinden ve dilinden başkalarının emin olduğu kimsedir. **(Buhari, İman 4; Müslim, İman 14.)**",
    "Güzel söz sadakadır. **(Buhari, Edeb 34; Müslim, Zekât 56.)**",
    "Sözünde duran, emanete riayet eden mümin tam mümindir. **(Tirmizî, Birr 9.)**",
    "Temizlik imandandır. **(Müslim, Taharet 1.)**",
    "İnsanlara merhamet etmeyene, Allah da merhamet etmez. **(Buhari, Tevhid 2; Müslim, Fedâil 66.)**",
    "Hediyeleşin ki birbirinize sevginiz artsın. **(Muvatta, Hüsnü’l-Hulk 16.)**",
    "Kim susarsa, kurtulur. **(Tirmizî, Zühd 11.)**",
    "Sadaka malı eksiltmez. **(Müslim, Birr 69.)**",
    "Birbirinize buğz etmeyin, birbirinize sırt çevirmeyin, birbirinize haset etmeyin; ey Allah'ın kulları kardeş olun. **(Müslim, Birr 23; Buhari, Edeb 57.)**",
    "**Ebu Hureyre (r.a)'dan, Resulullah (s.a.v)'in şöyle buyurduğu rivayet edilmiştir:**\n__Sizden birinizin ailesinin yanına dönmesine namazdan başka bir mani yok iken, namaz vaktini kılmak için kendisini bekletmesi, onu namazda yapar__ **(Buhari ve Müslim)**",
    "**Ebu Hureyre (r.a)'dan, Resulullah (s.a.v)'in şöyle buyurduğu rivayet edilmiştir:**\n__Kulun Rabbine en yakın olduğu hal secde halidir. O halde secdede iken çok dua yapınız.__ **(Müslim)**",
    "**Ebu Hureyre (r.a)'dan, Resulullah (s.a.v)'in şöyle buyurduğu rivayet edilmiştir:**\n__Allah'a ve ahiret gününe iman eden kimse, ya hayır söylesin, ya da sussun.__ **(Buhari ve Müslim)**",
]

sünnetler = [
    "Affetmek🌹",
    "Çalışmak🌹",
    "Süt içmek🌹",
    "Saç örmek🌹",
    "Etli yemek🌹",
    "Koşmamak🌹",
    "Saç uzatmak🌹",
    "Koku sürmek🌹",
    "Sohbet etmek🌹",
    "Kabak yemek🌹",
    "Teravi kılmak🌹",
    "Selâm vermek🌹",
    "Yardımlaşmak🌹",
    "3 kez sarılmak🌹",
    "Sahur yapmak🌹",
    "Düzenli olmak🌹",
    "İlim öğrenmek🌹",
    "Sessiz ağlamak🌹",
    "Sadaka vermek🌹",
    "Ezanı dinlemek🌹",
    "İki öğün yemek🌹",
    "Teşekkür etmek🌹",
    "Temiz giyinmek🌹",
    "Birbirini sevmek🌹",
    "Pazarlık yapmak🌹",
    "Hal hatır sormak🌹",
    "Tebessüm etmek🌹",
    "Misafir ağırlamak🌹",
    "Kıyafeti katlamak🌹",
    "Birbirini uyarmak🌹",
    "Artık bırakmamak🌹",
    "Kaşları düzeltmek🌹",
    "İğne iplik taşımak🌹",
    "Eşikte oturmamak🌹",
    "Ölümü hatırlamak🌹",
    "Misafiri uğurlamak🌹",
    "Sevdiğini söylemek🌹",
    "Heybetli görünmek🌹",
    "Yumurtayı yıkamak🌹",
    "Yastıksız yatmamak🌹",
    "Birbirine sabretmek🌹",
    "Doymadan kalkmak🌹",
    "Yerde yemek yemek🌹",
    "Gül suyu kullanmak🌹",
    "Davete icabet etmek🌹",
    "Yemeği yavaş yemek🌹",
    "Sebze ve eti yıkamak🌹",
    "Öğle uykusu uyumak🌹",
    "Ekmeği elle koparmak🌹",
    "Yeri gelince konuşmak🌹",
    "Vakıa sûresini okumak🌹",
    "Misafire ilgi göstermek🌹",
    "Hasta iken hamdetmek🌹",
    "İlk verilen sözü tutmak🌹",
    "Yemeğe tuzla başlamak🌹",
    "Beyaz ve yeşil giyinmek🌹",
    "Yavaş ve tane konuşmak🌹",
    "Suyu üç yudumda içmek🌹",
    "Yoldaki engeli kaldırmak🌹",
    "Yemekte güzel konuşmak🌹",
    "Kahvaltıda 7 zeytin yemek🌹",
    "Aynaya bakınca dua etmek🌹",
    "Misafiri tekrar davet etmek🌹",
    "Sabah uyanınca el yıkamak🌹",
    "Birbirinin kusurunu örtmek🌹",
    "Elleri ve yüzü kurulamamak🌹",
    "Akşam bulaşık bırakmamak🌹",
    "Yemekten sonra tatlı yemek🌹",
    "Yemeklerin ağzını kapatmak🌹",
    "Su içerken kıbleye yönelmek🌹",
    "Kapı açıldığında yan durmak🌹",
    "Her işe besmele ile başlamak🌹",
    "Çatlak bardaktan su içmemek🌹",
    "Yemeğe besmele ile başlamak🌹\n\n**BİSMİLLAHİRRAHMANİRRAHİM**\n\n**Rahman ve Rahim Olan Allahın Adıyla**",
    "Arkadaş ziyaretinde bulunmak🌹",
    "Seccadeyi sünnet üzere katlamak🌹",
    "Abdest alırken yüzüğü çevirmek🌹",
    "Cuma günü gusül abdesti almak🌹",
    "Bir şey yerken 3 parmakla yemek🌹",
    "İsraf etmemek ışıkları söndürmek🌹",
]

esmalar = [
    "**Allah(C.C.):**\n\n__Eşi benzeri olmayan, bütün noksan sıfatlardan münezzeh tek ilah, Her biri sonsuz bir hazine olan bütün isimlerini kuşatan özel ismi. İsimlerin sultanı.__",
    "**Er-Rahmân:** \n\n__Dünyada bütün mahlükata merhamet eden, şefkat gösteren, ihsan eden.__",
    "**Er-Rahîm:** \n\n__Ahirette, sadece müminlere acıyan, merhamet eden.__",
    "**El-Melik:**\n\n__Mülkün, kâinatın sahibi, mülk ve saltanatı devamlı olan.__",
    "**El-Kuddûs:**\n\n__Her noksanlıktan uzak ve her türlü takdîse lâyık olan.__",
    "**Es-Selâm:**\n\n__Her türlü tehlikelerden selamete çıkaran. Cennetteki bahtiyar kullarına selâm eden.__",
    "**El-Mü’min:**\n\n__Güven veren, emin kılan, koruyan, iman nurunu veren.__",
    "**El-Müheymin:**\n\n__Her şeyi görüp gözeten, her varlığın yaptıklarından haberdar olan.__",
    "**El-Azîz:**\n\n__İzzet sahibi, her şeye galip olan, karşı gelinemeyen.__",
    "**El-Cebbâr:**\n\n__Azamet ve kudret sahibi. Dilediğini yapan ve yaptıran. Hükmüne karşı gelinemeyen.__",
    "**El-Mütekebbir:**\n\n__Büyüklükte eşi, benzeri yok.__",
    "**El-Hâlık:**\n\n__Yaratan, yoktan var eden. Varlıkların geçireceği halleri takdir eden.__",
    "**El-Bâri:**\n\n__Her şeyi kusursuz ve mütenasip yaratan.__",
    "**El-Musavvir:**\n\n__Varlıklara şekil veren ve onları birbirinden farklı özellikte yaratan.__",
    "**El-Gaffâr:**\n\n__Günahları örten ve çok mağfiret eden. Dilediğini günah işlemekten koruyan.__",
    "**El-Kahhâr:**\n\n__Her istediğini yapacak güçte olan, galip ve hâkim.__",
    "**El-Vehhâb:**\n\n__Karşılıksız nimetler veren, çok fazla ihsan eden.__",
    "**Er-Razzâk:**\n\n__Her varlığın rızkını veren ve ihtiyacını karşılayan.__",
    "**El-Fettâh:**\n\n__Her türlü sıkıntıları gideren.__",
    "**El-Alîm:**\n\n__Gizli açık, geçmiş, gelecek, her şeyi, ezeli ve ebedi ilmi ile en mükemmel bilen.__",
    "**El-Kâbıd:**\n\n__Dilediğinin rızkını daraltan, ruhları alan.__",
    "**El-Bâsıt:**\n\n__Dilediğinin rızkını genişleten, ruhları veren.__",
    "**El-Hâfıd:**\n\n__Kâfir ve facirleri alçaltan.__",
    "**Er-Râfi:**\n\n__Şeref verip yükselten.__",
    "**El-Mu’ız:**\n\n__Dilediğini aziz eden.__",
    "**El-Müzil:**\n\n__Dilediğini zillete düşüren, hor ve hakir eden.__",
    "**Es-Semi:**\n\n__Her şeyi en iyi işiten, duaları kabul eden.__",
    "**El-Basîr:**\n\n__Gizli açık, her şeyi en iyi gören.__",
    "**El-Hakem:**\n\n__Mutlak hakim, hakkı bâtıldan ayıran. Hikmet sahibi.__",
    "**El-Adl:**\n\n__Mutlak adil, yerli yerinde yapan.__",
    "**El-Latîf:**\n\n__Her şeye vakıf, lütuf ve ihsan sahibi olan.__",
    "**El-Habîr:**\n\n__Her şeyden haberdar. Her şeyin gizli taraflarından haberi olan.__",
    "**El-Halîm:**\n\n__Cezada, acele etmeyen, yumuşak davranan, hilm sahibi.__",
    "**El-Azîm:**\n\n__Büyüklükte benzeri yok. Pek yüce.__",
    "**El-Gafûr:**\n\n__Affı, mağfireti bol.__",
    "**Eş-Şekûr:**\n\n__Az amele, çok sevap veren.__",
    "**El-Aliyy:**\n\n__Yüceler yücesi, çok yüce.__",
    "**El-Kebîr:**\n\n__Büyüklükte benzeri yok, pek büyük.__",
    "**El-Hafîz:**\n\n__Her şeyi koruyucu olan.__",
    "**El-Mukît:**\n\n__Rızıkları yaratan.__",
    "**El-Hasîb:**\n\n__Kulların hesabını en iyi gören.__",
    "**El-Celîl:**\n\n__Celal ve azamet sahibi olan.__",
    "**El-Kerîm:**\n\n__Keremi, lütuf ve ihsânı bol, karşılıksız veren, çok ikram eden.__",
    "**Er-Rakîb:**\n\n__Her varlığı, her işi her an gözeten. Bütün işleri murakabesi altında bulunduran.__",
    "**El-Mucîb:**\n\n__Duaları, istekleri kabul eden.__",
    "**El-Vâsi:**\n\n__Rahmet ve kudret sahibi, ilmi ile her şeyi ihata eden.__",
    "**El-Hakîm:**\n\n__Her işi hikmetli, her şeyi hikmetle yaratan.__",
    "**El-Vedûd:**\n\n__İyiliği seven, iyilik edene ihsan eden. Sevgiye layık olan.__",
    "**El-Mecîd:**\n\n__Nimeti, ihsanı sonsuz, şerefi çok üstün, her türlü övgüye layık bulunan.__",
    "**El-Bâis:**\n\n__Mahşerde ölüleri dirilten, Peygamber gönderen.__",
    "**Eş-Şehîd:**\n\n__Zamansız, mekansız hiçbir yerde olmayarak her zaman her yerde hazır ve nazır olan.__",
    "**El-Hak:**\n\n__Varlığı hiç değişmeden duran. Var olan, hakkı ortaya çıkaran.__",
    "**El-Vekîl:**\n\n__Kulların işlerini bitiren. Kendisine tevekkül edenlerin işlerini en iyi neticeye ulaştıran.__",
    "**El-Kaviyy:**\n\n__Kudreti en üstün ve hiç azalmaz.__",
    "**El-Metîn:**\n\n__Kuvvet ve kudret menbaı, pek güçlü.__",
    "**El-Veliyy:**\n\n__Müslümanların dostu, onları sevip yardım eden.__",
    "**El-Hamîd:**\n\n__Her türlü hamd ve senaya layık olan.__",
    "**El-Muhsî:**\n\n__Yarattığı ve yaratacağı bütün varlıkların sayısını bilen.__",
    "**El-Mübdi:**\n\n__Maddesiz, örneksiz yaratan.__",
    "**El-Muîd:**\n\n__Yarattıklarını yok edip, sonra tekrar diriltecek olan.__",
    "**El-Muhyî:**\n\n__İhya eden, yarattıklarına can veren.__",
    "**El-Mümît:**\n\n__Her canlıya ölümü tattıran.__",
    "**El-Hayy:**\n\n__Ezeli ve ebedi bir hayat ile diri olan.__",
    "**El-Kayyûm:**\n\n__Mahlukları varlıkta durduran, zatı ile kaim olan.__",
    "**El-Vâcid:**\n\n__Kendisinden hiçbir şey gizli kalmayan, hiçbir şeye muhtaç olmayan.__",
    "**El-Mâcid:**\n\n__Kadri ve şânı büyük, keremi, ihsanı bol olan.__",
    "**El-Vâhid:**\n\n__Zat, sıfat ve fiillerinde benzeri ve ortağı olmayan, tek olan.__",
    "**Es-Samed:**\n\n__Hiçbir şeye ihtiyacı olmayan, herkesin muhtaç olduğu merci.__",
    "**El-Kâdir:**\n\n__Dilediğini dilediği gibi yaratmaya muktedir olan.__",
    "**El-Muktedir:**\n\n__Dilediği gibi tasarruf eden, her şeyi kolayca yaratan kudret sahibi.__",
    "**El-Mukaddim:**\n\n__Dilediğini yükselten, öne geçiren, öne alan.__",
    "**El-Muahhir:**\n\n__Dilediğini alçaltan, sona, geriye bırakan.__",
    "**El-Evvel:**\n\n__Ezeli olan, varlığının başlangıcı olmayan.__",
    "**El-Âhir:**\n\n__Ebedi olan, varlığının sonu olmayan.__",
    "**Ez-Zâhir:**\n\n__Yarattıkları ile varlığı açık, aşikâr olan, kesin delillerle bilinen.__",
    "**El-Bâtın:**\n\n__Aklın tasavvurundan gizli olan.__",
    "**El-Vâlî:**\n\n__Bütün kâinatı idare eden, onların işlerini yoluna koyan.__",
    "**El-Müteâlî:**\n\n__Son derece yüce olan.__",
    "**El-Berr:**\n\n__İyilik ve ihsanı bol olan.__",
    "**Et-Tevvâb:**\n\n__Tevbeleri kabul edip, günahları bağışlayan.__",
    "**El-Müntekım:**\n\n__Asilerin, zalimlerin cezasını veren.__",
    "**El-Afüvv:**\n\n__Affı çok olan, günahları mağfiret eden.__",
    "**Er-Raûf:**\n\n__Çok merhametli, pek şefkatli.__",
    "**Mâlik-ül Mülk:**\n\n__Mülkün, her varlığın sahibi.__",
    "**Zül-Celâli vel İkrâm:**\n\n__Celal, azamet, şeref, kemal ve ikram sahibi.__",
    "**El-Muksit:**\n\n__Mazlumların hakkını alan, adaletle hükmeden, her işi birbirine uygun yapan.__",
    "**El-Câmi:**\n\n__İki zıttı bir arada bulunduran. Kıyamette her mahlûkatı bir araya toplayan.__",
    "**El-Ganiyy:**\n\n__İhtiyaçsız, muhtaç olmayan, her şey Ona muhtaç olan.__",
    "**El-Mugnî:**\n\n__Müstağni kılan. İhtiyaç gideren, zengin eden.__",
    "**El-Mâni:**\n\n__Dilemediği şeye mani olan, engelleyen.__",
    "**Ed-Dârr:**\n\n__Elem, zarar verenleri yaratan.__",
    "**En-Nâfi:**\n\n__Fayda veren şeyleri yaratan.__",
    "**En-Nûr:**\n\n__Âlemleri nurlandıran, dilediğine nur veren.__",
    "**El-Hâdî:**\n\n__Hidayet veren.__",
    "**El-Bedî:**\n\n__Misalsiz, örneksiz harikalar yaratan. (Eşi ve benzeri olmayan).__",
    "**El-Bâkî:**\n\n__Varlığının sonu olmayan, ebedi olan.__",
    "**El-Vâris:**\n\n__Her şeyin asıl sahibi olan.__",
    "**Er-Reşîd:**\n\n__İrşada muhtaç olmayan, doğru yolu gösteren.__",
    "**Es-Sabûr:**\n\n__Ceza vermede, acele etmeyen.__",
]

ayetler = [
    "Şüphesiz namaz, müminlere belirli vakitlerde farz kılınmıştır. (Nisa, 103)",
    "Allah sabredenlerle beraberdir. (Bakara, 153)",
    "Zor da olsa sabredin; şüphesiz Allah'ın yardımı yakındır. (Bakara, 214)",
    "Senden önce gönderdiğimiz bütün peygamberler de şüphesiz yemek yerler, sokaklarda gezinirlerdi. Sabreder misiniz diye sizi birbirinizle deneriz. Ve Rabbın Basir olandır.  (Furkan, 20)",
]

quranInfo = {
    'surah': {
        1: ["Al-Fatihah", 7],
        2: ["Al-Baqarah", 286],
        3: ["Al-Imran", 200],
        4: ["An-Nisa", 176],
        5: ["Al-Maidah", 120],
        6: ["Al-An'am", 165],
        7: ["Al-A'raf", 206],
        8: ["Al-Anfal", 75],
        9: ["At-Tawbah", 129],
        10: ["Yunus", 109],
        11: ["Hud", 123],
        12: ["Yusuf", 111],
        13: ["Ar-Ra'd", 43],
        14: ["Ibrahim", 52],
        15: ["Al-Hijr", 99],
        16: ["An-Nahl", 128],
        17: ["Al-Isra", 111],
        18: ["Al-Kahf", 110],
        19: ["Maryam", 98],
        20: ["Ta-Ha", 135],
        21: ["Al-Anbiya", 112],
        22: ["Al-Hajj", 78],
        23: ["Al-Mu'minun", 118],
        24: ["An-Nur", 64],
        25: ["Al-Furqan", 77],
        26: ["Ash-Shu'ara", 227],
        27: ["An-Naml", 93],
        28: ["Al-Qasas", 88],
        29: ["Al-Ankabut", 69],
        30: ["Ar-Rum", 60],
        31: ["Luqman", 34],
        32: ["As-Sajda", 30],
        33: ["Al-Ahzab", 73],
        34: ["Saba", 54],
        35: ["Fatir", 45],
        36: ["Ya-Sin", 83],
        37: ["As-Saffat", 182],
        38: ["Sad", 88],
        39: ["Az-Zumar", 75],
        40: ["Ghafir", 85],
        41: ["Fussilat", 54],
        42: ["Ash-Shura", 53],
        43: ["Az-Zukhruf", 89],
        44: ["Ad-Dukhan", 59],
        45: ["Al-Jathiya", 37],
        46: ["Al-Ahqaf", 35],
        47: ["Muhammad", 38],
        48: ["Al-Fath", 29],
        49: ["Al-Hujurat", 18],
        50: ["Qaf", 45],
        51: ["Adh-Dhariyat", 60],
        52: ["At-Tur", 49],
        53: ["An-Najm", 62],
        54: ["Al-Qamar", 55],
        55: ["Ar-Rahman", 78],
        56: ["Al-Waqi'a", 96],
        57: ["Al-Hadid", 29],
        58: ["Al-Mujadila", 22],
        59: ["Al-Hashr", 24],
        60: ["Al-Mumtahina", 13],
        61: ["As-Saff", 14],
        62: ["Al-Jumu'a", 11],
        63: ["Al-Munafiqun", 11],
        64: ["At-Taghabun", 18],
        65: ["At-Talaq", 12],
        66: ["At-Tahrim", 12],
        67: ["Al-Mulk", 30],
        68: ["Al-Qalam", 52],
        69: ["Al-Haqqah", 52],
        70: ["Al-Ma'arij", 44],
        71: ["Nuh", 28],
        72: ["Al-Jinn", 28],
        73: ["Al-Muzzammil", 20],
        74: ["Al-Muddathir", 56],
        75: ["Al-Qiyama", 40],
        76: ["Al-Insan", 31],
        77: ["Al-Mursalat", 50],
        78: ["An-Naba", 40],
        79: ["An-Nazi'at", 46],
        80: ["Abasa", 42],
        81: ["At-Takwir", 29],
        82: ["Al-Infitar", 19],
        83: ["Al-Mutaffifin", 36],
        84: ["Al-Inshiqaq", 25],
        85: ["Al-Buruj", 22],
        86: ["At-Tariq", 17],
        87: ["Al-A'la", 19],
        88: ["Al-Ghashiyah", 26],
        89: ["Al-Fajr", 30],
        90: ["Al-Balad", 20],
        91: ["Ash-Shams", 15],
        92: ["Al-Lail", 21],
        93: ["Ad-Duha", 11],
        94: ["Ash-Sharh", 8],
        95: ["At-Tin", 8],
        96: ["Al-Alaq", 19],
        97: ["Al-Qadr", 5],
        98: ["Al-Bayyina", 8],
        99: ["Az-Zalzala", 8],
        100: ["Al-Adiyat", 11],
        101: ["Al-Qari'a", 11],
        102: ["At-Takathur", 8],
        103: ["Al-Asr", 3],
        104: ["Al-Humaza", 9],
        105: ["Al-Fil", 5],
        106: ["Quraish", 4],
        107: ["Al-Ma'un", 7],
        108: ["Al-Kawthar", 3],
        109: ["Al-Kafirun", 6],
        110: ["An-Nasr", 3],
        111: ["Al-Masad", 5],
        112: ["Al-Ikhlas", 4],
        113: ["Al-Falaq", 5],
        114: ["An-Nas", 6]
    }
}


def get_random_hadis():
    return random.choice(hadisler)

def get_random_ayet():
    return random.choice(ayetler)

def get_random_sunnet():
    return random.choice(sünnetler)

def get_random_99():
    return random.choice(esmalar)

# 3. Dualar
dualar = {
    "sabah duası": "Allahumme bika esbahna ve bika emseyna...",
    "yolculuk duası": "Subhanellezi sehhara lena haza...",
    "yatarken okunan dua": "Bismike Allahumme emutu ve ahya..."
}

def get_dua(dua_name):
    return dualar.get(dua_name, "Bu dua bulunamadı.")

# 6. Zekat Hesaplama Aracı
def calculate_zekat(wealth, debts):
    net_wealth = wealth - debts
    zekat = net_wealth * 0.025 if net_wealth > 0 else 0
    return zekat

# 7. Soru-Cevap Modülü
faq = {
    "namaz nasıl kılınır": "Namaz, niyetle başlar ve kıyam, rükû, secde gibi bölümlerle devam eder.",
    "oruç kimlere farzdır": "Oruç, ergenlik çağına gelmiş, akıl sağlığı yerinde, müslüman kişilere farzdır.",
    "ameli mezhep imamları": "İmamı Azam Ebu Hanife, İmamı Şafii, İmamı Malik, Ahmed İbni Hanbel",
    "itikadi mezhep imamları": "İmamı Maturidi ve İmamı Eş’ari",
    "mezhep İmamlarının isimleri": "Numan bin Sabit, Muhammed İdris eş-Şafiî, Ahmed ibn-i Hanbel, Enes bin Malik",
    "mezhep ne demektir": "İslam âlimlerinin Kur’an ve sünnet çerçevesinde, birbirleri arasındaki yorum farklılıklarından meydana gelen görüşleridir.",
    "icma nedir kaç çeşittir": "Peygamberimizden sonra ortaya çıkan fıkhi bir meselede, âlimlerin görüş birliği yapmalarıdır. Ör: mut’a nikâhının haramlığı icmadır.\n\nA:Sarih İcma(Âlimlerin hepsinin katıldığı) B:Sükutî icma(bir âlim icma yapar diğerleri farklı bir görüş belirtmeksizin susarlar)",
}

def get_faq(question):
    return faq.get(question.lower(), "Bu sorunun cevabı bulunamadı.")

# 8. İlmihal Bilgileri
ilmihal = {
    "oruç": "Oruç, İslam'ın beş şartından biridir. Ramazan ayında tutulur.",
    "zekat": "Zekat, fakirlere verilmesi gereken mali bir ibadettir.",
    "imanın esasları": "İmanın 6 temel şartı vardır:\n\n**Allah'a İman**: Allah’ın varlığına ve birliğine inanmak.\n\n**Meleklere iman:** Meleklerin Allah’ın emirlerini yerine getiren nurani varlıklar olduğuna inanmak.\n\n**Kitaplara iman:** Allah’ın insanlara rehberlik etmek için kutsal kitaplar gönderdiğine inanmak (Tevrat, Zebur, İncil, Kur'an).\n\n**Peygamberlere iman:** Allah’ın insanlara yol göstermek için peygamberler gönderdiğine inanmak\n\n**Ahiret gününe iman:** Ölümden sonra dirilişe ve ahirette hesap verileceğine inanmak\n\n**Kader ve kazaya iman:** Her şeyin Allah’ın ilmi ve takdiri ile gerçekleştiğine inanmak.",
    "ibadetler": "İslam'da ibadetler, kulun Allah’a olan bağlılığını ve şükran duygusunu ifade etme şeklidir. Beş temel ibadet vardır:\n\n**Namaz:** Günde beş vakit kılınan farz ibadet. Namaz, temizliğe ve vakitlere göre yapılır.\n\n**Oruç:** Ramazan ayında, tan yerinin ağarmasından güneş batıncaya kadar yeme-içmeden uzak durmaktır.\n\n**Zekat:** Maddi durumu iyi olanların ihtiyaç sahiplerine mallarının kırkta birini vermesi.\n\n**Hac:** Maddi ve fiziksel durumu uygun olan Müslümanların ömürde bir kez Kâbe’ye gitmeleri.\n\n**Kelime-i Şehadet:** İslam’ın temel inanç sözüdür ve “Eşhedü en lâ ilâhe illallah ve eşhedü enne Muhammeden abdühû ve rasûlüh” şeklindedir.",
    "temizlik": "İslam’da temizlik, ibadetin ön şartıdır. Hem maddi hem de manevi temizlik önemlidir:\n\n**Abdest:** Namaz kılmadan önce alınan ve bazı beden uzuvlarının yıkanması ile yapılan temizlik.\n\n**Gusül:** Tüm vücudun yıkanmasıdır, cünüplük hali gibi durumlarda farzdır.\n\n**Teyemmüm:** Su bulunmadığında veya su kullanılamadığında yapılan abdest türüdür.",
    "ahlak": "Ahlak, İslam’ın en temel konularından biridir. Güzel ahlak, doğruluk, dürüstlük, yardımseverlik, sabır, tevazu gibi değerleri içerir. Ahlaklı bir Müslüman; yalan söylemez, emanete hıyanet etmez, kötü davranışlardan uzak durur.",
    "helal ve haram": "İslam’da helal olan (izin verilen) ve haram olan (yasaklanan) davranışlar ve yiyecek-içecekler vardır:\n\n**Helal:** Allah’ın izin verdiği şeylerdir.\n\n**Haram:** İçki, domuz eti, hırsızlık gibi yasaklanan şeylerdir.",
    "nikah ve evlilik": "Evlilik, İslam'da teşvik edilen bir ibadettir. İki kişinin dinî ve yasal kurallara göre evlenmesi gerekir. Nikahın geçerli olması için belirli şartlar (şahitler, mehir vb.) bulunur.",
    "ahiret inancı": "İslam, ölümden sonra bir hayatın varlığını kabul eder. Ölen kişi kabir hayatını yaşar ve kıyametten sonra tekrar diriltilerek hesap verir. İyilik yapanlar cennete, kötülük yapanlar ise cehenneme gidecektir.",
    "muamelat": "İslam, ticaret ve toplumsal ilişkilerde adaletli, dürüst ve helal kazanç elde etmeyi emreder. Faiz gibi bazı kazanç yolları haram kılınmıştır."
}

def get_ilmihal(info):
    return ilmihal.get(info, "Bu konu hakkında bilgi bulunamadı.")

# Bot Komutları
@client.on(events.NewMessage(pattern='/hadis'))
async def hadis_handler(event):
    await event.respond(get_random_hadis())

@client.on(events.NewMessage)
async def slm_komutu(event):
    # Gelen mesajın içeriğini küçük harfe çeviriyoruz
    mesaj = event.message.message.lower()
    
    # Mesaj 'selamın aleyküm' içeriyorsa yanıtla
    if mesaj == 'slm':
        await event.reply("**Aleyküm Selam ve Rahmetullah ve bereketuhu hoş geldin**")

@client.on(events.NewMessage)
async def selam_komutu(event):
    # Gelen mesajın içeriğini küçük harfe çeviriyoruz
    mesaj = event.message.message.lower()
    
    # Mesaj 'selamın aleyküm' içeriyorsa yanıtla
    if mesaj == 'selamın aleyküm':
        await event.reply("**Aleyküm Selam ve Rahmetullah ve bereketuhu hoş geldin**")

@client.on(events.NewMessage(pattern=r'/sures'))
async def list_all_suras(event):
    all_suras = "**Kur'an Sureleri:**\n\n"
    for surah_num, (surah_name, ayah_count) in quranInfo['surah'].items():
        all_suras += f"{surah_num}. {surah_name} - Ayet Sayısı: {ayah_count}\n"
    
    await event.reply(all_suras)

@client.on(events.NewMessage(pattern='/99'))
async def esma_handler(event):
    await event.respond(get_random_99())

@client.on(events.NewMessage(pattern='/sunnet'))
async def sunnet_handler(event):
    await event.respond(get_random_sunnet())

@client.on(events.NewMessage(pattern='/ayet'))
async def ayet_handler(event):
    await event.respond(get_random_ayet())


anlik_calisan = []

log_grub = -1002469640841

tekli_calisan = []

ozel_list = [5710250764]
anlik_calisan = []
grup_sayi = []
etiketuye = []
rxyzdev_tagTot = {}
rxyzdev_initT = {}

OWNER_ID = 5710250764
BOT_ID = 7763011142
@client.on(events.ChatAction)
async def hg(event):
    # Öncelikle `action_message` ve `action` nesnesinin varlığını kontrol ediyoruz
    if event.action_message and hasattr(event.action_message.action, 'users'):
        # from_id'yi kullanıcı nesnesine dönüştürüyoruz
        from_user = await event.client.get_entity(event.action_message.from_id)

        for new_user in event.action_message.action.users:
            if str(new_user) == str(BOT_ID):
                await event.reply(
                    f"Hey Selamın Aleyküm {from_user.first_name}, beni {event.chat.title} grubuna eklediğin için teşekkürler⚡️\n\nİslami Bilgilerimi Sizinle Paylaşmak İçin Hizmetinizdeyim İnşeAllah. Komutlar için /help yazmanız yeterlidir✨"
                )

            elif str(new_user) == str(OWNER_ID):
                await event.reply("İşte bu gelen benim sahibim.")
            elif str(new_user) == "5710250764":
                await event.reply("İşte bu gelen benim geliştiricim.")


@client.on(events.NewMessage(pattern="/help"))
async def help(event):
    # Sadece komutu çalıştıran kullanıcı bilgisi
    usr = await event.get_sender()
    ad = f"[{usr.first_name}](tg://user?id={usr.id})"
    
    # Günlük grubuna sadece bir kere mesaj gönderme
    await client.send_message(log_grub, f"ℹ️ {ad} Kişisi Botu Başlattı.")
    
    # Kullanıcıya yanıt gönderme
    helptext = ("**⚙️Yardım Menüsü**\n\nTüm Komutlar İçin /komut Yeterli Olacaktır..")

    # Komut çalıştıran kullanıcıya yanıt gönderme
    await event.reply(
        helptext,
        buttons=[
            [Button.url('Beni Gruba Ekle ➕', f"https://t.me/sakirviphapy_bot?startgroup=a")],
            [Button.url('Support🛠', f"https://t.me/SakirBey2")],
            [Button.url('Sahibim🔖', f"https://t.me/SakirBey")],
            [Button.url('Developer🧑‍🔧', 'https://t.me/SakirBey2')],
            [Button.url('Github Code', 'https://nolur.com')],
        ],
        link_preview=False
    )

@client.on(events.NewMessage(pattern="/start"))
async def help(event):
    # Sadece komutu çalıştıran kullanıcı bilgisi
    usr = await event.get_sender()
    ad = f"[{usr.first_name}](tg://user?id={usr.id})"
    
    # Günlük grubuna sadece bir kere mesaj gönderme
    await client.send_message(log_grub, f"ℹ️ {ad} Kişisi Botu Başlattı.")
    
    # Kullanıcıya yanıt gönderme
    helptext = ("**⚙️Yardım Menüsü**\n\nTüm Komutlar İçin /komut Yeterli Olacaktır..")

    # Komut çalıştıran kullanıcıya yanıt gönderme
    await event.reply(
        helptext,
        buttons=[
            [Button.url('Beni Gruba Ekle ➕', f"https://t.me/sakirviphapy_bot?startgroup=a")],
            [Button.url('Support🛠', f"https://t.me/SakirBey2")],
            [Button.url('Sahibim🔖', f"https://t.me/SakirBey")],
            [Button.url('Developer🧑‍🔧', 'https://t.me/SakirBey2')],
            [Button.url('Github Code', 'https://nolur.com')],
        ],
        link_preview=False
    )


# Veritabanı bağlantısı
conn = sqlite3.connect('tespih.db')
cursor = conn.cursor()

# Kullanıcılar için bir tablo oluşturma (Eğer yoksa)
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    first_name TEXT,
    tespih_count INTEGER DEFAULT 0
)
''')
conn.commit()

# Tespih komutu işleyici
@client.on(events.NewMessage(pattern="/tespih"))
async def tespih_handler(event):
    # Kullanıcı bilgilerini al
    user_id = event.sender_id
    first_name = (await event.get_sender()).first_name

    # Veritabanında kullanıcı var mı kontrol et
    cursor.execute("SELECT tespih_count FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    
    if result:
        # Kullanıcı zaten varsa tespih sayısını artır
        tespih_count = result[0] + 1
        cursor.execute("UPDATE users SET tespih_count = ? WHERE user_id = ?", (tespih_count, user_id))
    else:
        # Kullanıcı yoksa yeni kullanıcı olarak ekle
        tespih_count = 1
        cursor.execute("INSERT INTO users (user_id, first_name, tespih_count) VALUES (?, ?, ?)", 
                       (user_id, first_name, tespih_count))
    
    # Değişiklikleri kaydet
    conn.commit()
    
    # Kullanıcıya yanıt gönder
    await event.respond(f"📿 {first_name}, **toplam** {tespih_count} **tespih çektiniz.📿**")

# Tespih sayısını sıfırlama komutu
@client.on(events.NewMessage(pattern="/sifirla"))
async def reset_tespih(event):
    # Sadece sudo kullanıcıları komutu çalıştırabilir
    if event.sender_id in sudo_users:
        # Tüm kullanıcıların tespih sayısını sıfırlama
        cursor.execute("UPDATE users SET tespih_count = 0")
        conn.commit()
        
        await event.respond("✅ Tüm kullanıcıların tespih sayısı sıfırlandı.")
    else:
        await event.respond("⛔ Bu komutu yalnızca sudo kullanıcıları kullanabilir.")


@client.on(events.ChatAction)
async def welcome_user(event):
    # Yeni bir kullanıcı katıldıysa
    if event.user_joined or event.user_added:
        # Kullanıcının adını ve kimliğini al
        user = await event.get_user()
        user_id = user.id
        user_name = user.first_name

        # Hoş geldin mesajını kullanıcıyı etiketleyerek gönder
        welcome_message = f"**Selamın Aleyküm** [{user_name}](tg://user?id={user_id})! **Grubumuza hoş geldin** 😊"
        
        # Mesajı Markdown formatında gönderin
        await event.reply(welcome_message, parse_mode='md')

@client.on(events.NewMessage(pattern='/dua (?P<dua_name>[\w\s]+)'))
async def dua_handler(event):
    dua_name = event.pattern_match.group('dua_name')
    await event.respond(get_dua(dua_name))


# Küfürlü kelimelerin listesi
profane_words = ['amk', 'aq', 'sg']  # Burada küfürlü kelimeleri girin

@client.on(events.NewMessage())
async def filter_profane_words(event):
    message = event.message.text.lower()  # Mesajı küçük harfe dönüştür
    user_id = event.sender_id  # Mesajı gönderen kullanıcının ID'si
    chat = await event.get_chat()  # Mesajın gönderildiği grup

    # Grup yöneticilerini almak için get_participants fonksiyonunu kullan
    participants = await client.get_participants(chat, filter=ChannelParticipantsAdmins)  # Adminleri al
    admins = [admin.id for admin in participants]  # Admin'lerin id'lerini al

    # Eğer kullanıcı bir yönetici değilse, küfürlü kelimeleri kontrol et
    if user_id not in admins:
        for word in profane_words:
            if word in message:
                # Mesajı sil
                await event.delete()
                
                # Kullanıcıyı etiketleyerek uyarı gönder
                await event.reply(f"@{event.sender.username or event.sender.first_name}, lütfen küfürlü dil kullanmayın!")
                break  # Bir kelimeyle eşleştiğinde döngüyü sonlandır

API_URL = "https://api.aladhan.com/v1/timingsByCity"

@client.on(events.NewMessage(pattern=r"/ezanvakti (.+)"))
async def ezan_vakti(event):
    # Kullanıcıdan şehir adını al
    input_text = event.pattern_match.group(1)
    city = input_text.strip()

    # API isteği için URL'yi hazırla
    params = {
        "city": city,
        "country": "Turkey",
        "method": 13  # Türkiye için uygun metod
    }

    try:
        # API'ye istek gönder
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        # API yanıtından ezan vakitlerini al
        timings = data['data']['timings']
        
        # Ezan vakitlerini formatla
        ezan_vakitleri = (
            f"**📌 {city.capitalize()} Ezan Vakitleri**\n\n"
            f"🌅 İmsak: {timings['Fajr']}\n"
            f"🌇 Güneş: {timings['Sunrise']}\n"
            f"🕌 Öğle: {timings['Dhuhr']}\n"
            f"🌆 İkindi: {timings['Asr']}\n"
            f"🌄 Akşam: {timings['Maghrib']}\n"
            f"🌌 Yatsı: {timings['Isha']}\n"
        )
        
        # Cevabı kullanıcıya gönder
        await event.reply(ezan_vakitleri)
    except requests.exceptions.RequestException as e:
        await event.reply("Ezan vakitleri alınamadı, lütfen daha sonra tekrar deneyin.")

@client.on(events.NewMessage(pattern=r'/komut'))
async def komut(event):
    await event.respond("**Selamın Aleyküm**\n⚙️__Komut Listesi__\n\n/hediye \n**Örnek:** ```/hediye @SakirBey```\n\n/tespih __Sanal Tespih Çekersiniz..__\n\n/zekat __Zekat Hesaplayıcı..__\n**Örnek:** ```/zekat 1400 200```\n\n/soru __Botumuza Eklediğim Soruları Bu Komut İle Sorabilirsiniz__\n**Örnek:** ```/soru namaz nasıl kılınır``` Soru Eklentileri Şunlardır->```namaz nasıl kılınır```,```oruç kimlere farzdır```\n\n/mezhep __Girdiğiniz Mezhep Hakkında Bilgi Getirir__\n**Örnek:** ```/mezhep hanefi``` Mezhepler Şunlardır -> ```hanefi``` , ```şafii``` , ```maliki``` , ```hanbeli``` , ```şii```\n\n/tarih __Güncel Miladi ve Hicri Takvimini Gösterir__\n\n/ösöz __Random Özlü Söz Getirir..__\n\n/hadis __Random Sahih Hadis Getirir..__\n\n/ayet __Random Ayet Getirir..__\n\n/sunnet __Random Peygamberimizin s.a.v Sünnetlerini Getirir..__\n\n/99 __Random Esmaül Hüsna Getirir..__\n\n/dua __Bu Komut İle Eklediğimiz Duaları Getirir..__\n**Örnek:** ```/dua sabah duası``` Eklenmiş olan dualar -> ```sabah duası``` , ```yolculuk duası``` , ```yatarken okunacak dua```\n\n/ilmihal __Eklediğimiz İlmihal Bilgilerini Getirir..__\n**Örnek:** ```/ilmihal oruç``` Kullanılan Cümleler -> ```oruç``` , ```zekat``` , ```imanın esasları``` , ```ibadetler``` , ```temizlik``` , ```ahlak``` , ```helal ve haram``` , ```nikah ve evlilik``` , ```ahiret inancı``` , ```muamelat```\n\n/sures\n\n/ezanvakti \n**Örnek:** ```/ezanvakti adana```\n\n")

hediyeler = [
    "seccade", "Kuran'ı kerim", "Elmas Yüzük", 
    "Çikolata Kutusu", "tespih", "araba", "Kupa", 
    "Telefon Kılıfı", "Çiçek Buketi"
]

# /hediye komutu
@client.on(events.NewMessage(pattern=r'/hediye (.+)'))
async def hediye_ver(event):
    # Komutu yazan kişi ve hediye verilecek kişi
    user_id = event.sender_id
    first_name = (await event.get_sender()).first_name
    hedef_kullanici = event.pattern_match.group(1)

    # Rastgele bir hediye seç
    hediye = random.choice(hediyeler)

    # Mesajı oluştur
    mesaj = f"🎁 {first_name} adlı kişi {hedef_kullanici} adlı kullanıcıya {hediye} hediye etti.\n\n**Hediyeleşin ki birbirinize sevginiz artsın. (Muvatta, Hüsnü’l-Hulk 16.)**"

    # Mesajı gönder
    await event.respond(mesaj)

@client.on(events.NewMessage(pattern="/id"))
async def _id(event):
    msg = await event.get_reply_message() or event.message
    out_str = "**User Info:**\n"
    out_str += f" ⚡️ __Group ID__ : `{(msg.forward.chat_id if msg.forward else msg.chat_id)}`\n"
    out_str += f" 💎 __Replied User Name__ : {msg.sender.first_name}\n"
    out_str += f" 💬 __Message ID__ : `{msg.forwarded.id if msg.forward else msg.id}`\n"
    if msg.sender_id:
        out_str += f" 🙋🏻‍♂️ __Replied User ID__ : `{msg.sender_id}`\n"

    await event.reply(out_str)


@client.on(events.NewMessage(pattern="/ping"))
async def pingy(event):
    start = datetime.now()
    hmm = await event.reply("Pong!")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await hmm.edit(
        f"█▀█ █▀█ █▄░█ █▀▀ █ \n█▀▀ █▄█ █░▀█ █▄█ ▄\n**Ping: {round(ms)} ms**"
    )

@client.on(events.NewMessage(pattern='/zekat (?P<wealth>\d+) (?P<debts>\d+)'))
async def zekat_handler(event):
    wealth = int(event.pattern_match.group('wealth'))
    debts = int(event.pattern_match.group('debts'))
    zekat = calculate_zekat(wealth, debts)
    await event.respond(f"Zekat miktarınız: {zekat} TL")

@client.on(events.NewMessage(pattern='/soru (?P<question>[\w\s]+)'))
async def soru_handler(event):
    question = event.pattern_match.group('question')
    await event.respond(get_faq(question))

@client.on(events.NewMessage(pattern='/ilmihal (?P<info>[\w\s]+)'))
async def ilmihal_handler(event):
    info = event.pattern_match.group('info')
    await event.respond(get_ilmihal(info))

weatherbit_api_key = '4b09195a74624b328d8f71a6e21b16d3'  # Weatherbit API anahtarınızı buraya girin

@client.on(events.NewMessage(pattern='/havadurumu'))
async def get_weather(event):
    # Kullanıcının şehir ismini öğrenin
    message = event.message.message.split()  # Komut ve şehir ismini ayrıştırmak için
    if len(message) < 2:
        await event.reply("Lütfen bir şehir belirtin! Örnek: /havadurumu İstanbul")
        return
    city = message[1].capitalize()

    # Weatherbit API'den hava durumu bilgisini alın
    weather_url = f'https://api.weatherbit.io/v2.0/current?city={city}&country=TR&key={weatherbit_api_key}&lang=tr'
    try:
        response = requests.get(weather_url)
        if response.status_code == 200:
            data = response.json()
            weather_info = data['data'][0]
            description = weather_info['weather']['description']
            temp = weather_info['temp']
            feels_like = weather_info['app_temp']
            humidity = weather_info['rh']

            # Hava durumu bilgisini kullanıcıya gönder
            weather_message = (f"{city} için hava durumu:\n"
                               f"Durum: {description}\n"
                               f"Sıcaklık: {temp}°C\n"
                               f"Hissedilen Sıcaklık: {feels_like}°C\n"
                               f"Nem: {humidity}%")
            await event.reply(weather_message)
        else:
            await event.reply("Hava durumu bilgisi alınamadı. Lütfen şehri kontrol edin veya daha sonra tekrar deneyin.")
    except Exception as e:
        await event.reply("Bir hata oluştu. Lütfen daha sonra tekrar deneyin.")


resim_dosyasi = 'videos/cuneyt.jpg'  # Klasördeki dosya yolunu belirtiyoruz

@client.on(events.NewMessage)
async def selam_komutu(event):
    # Gelen mesajın içeriğini küçük harfe çeviriyoruz
    mesaj = event.message.message.lower()
    
    # Mesaj 'selamın aleyküm' içeriyorsa yanıtla ve resim gönder
    if mesaj == '@SakirBey':
        await event.reply("Destur Esteuzubillah @SakirBey koş..")
        await client.send_file(event.chat_id, resim_dosyasi)

@client.on(events.NewMessage)
async def selam_komutu(event):
    # Gelen mesajın içeriğini küçük harfe çeviriyoruz
    mesaj = event.message.message.lower()
    
    # Mesaj 'selamın aleyküm' içeriyorsa yanıtla ve resim gönder
    if mesaj == 'Şakir':
        await event.reply("Destur Esteuzubillah @SakirBey koş..")
        await client.send_file(event.chat_id, resim_dosyasi)




allowed_group_ids = [-1002416358122, -1002382744304]  # Buraya istediğiniz diğer chat_id'leri ekleyin

@client.on(events.NewMessage(pattern='Lena'))
async def send_video(event):
    # Sadece izin verilen gruplarda komutun çalışması için kontrol
    if event.chat_id in allowed_group_ids:
        # Proje kök dizinine göre video yolunu ayarlayın
        video_path = os.path.join(os.path.dirname(__file__), 'videos/lena.mp4')
        # Videoyu komutu gönderen kişiye gönder
        await client.send_file(event.chat_id, video_path, caption="**Ben Lenaa**")

@client.on(events.NewMessage(pattern='lena'))
async def send_video(event):
    # Sadece izin verilen gruplarda komutun çalışması için kontrol
    if event.chat_id in allowed_group_ids:
        # Proje kök dizinine göre video yolunu ayarlayın
        video_path = os.path.join(os.path.dirname(__file__), 'videos/lena.mp4')
        # Videoyu komutu gönderen kişiye gönder
        await client.send_file(event.chat_id, video_path, caption="**Ben Lenaa**")

sudo_users = [5710250764, 7235469974, 1503631196, 7489011154]  # Replace these with your actual sudo user IDs

@client.on(events.NewMessage(pattern='/alive'))
async def alive(event):
    # Check if the sender's ID is in the sudo_users list
    if event.sender_id in sudo_users:
        await event.respond('**Hey! Sahibim Bot Çalışıyor**\n__Sürüm: 1.2__')
    else:
        await event.respond("Bu komutu yalnızca yetkili kullanıcılar çalıştırabilir.")

# Botu çalıştır
client.start()
print("Destur esteuzubillah bot çalışıyor mümin kardeşim benim..")
client.run_until_disconnected()
