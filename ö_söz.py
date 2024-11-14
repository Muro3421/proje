import random


def get_random_quote():
    quotes = [
    "Dil, gönlün terazisidir. Dili doğru olanın, gönlü de doğru olur.\n\n  **İmam Gazali**",
    "Sabır, iki kısımdır. Bir musibetlere sabır, diğeri ise haramlardan kaçınmaya sabırdır. \n\n  **Hz.Ali(r.a)**",
    "Bir işin sonunu görmeden yapma, işin sonu seni pişman eder\n\n  **İmam Şafii**",
    "İlim bir denizdir, onun sonu yoktur. Bu yüzden sabırlı ol \n\n  **İmam Malik**",
    "Kişi, kendi ilmine güvenip kibirlenmemeli; bilakis Allah’a karşı her daim mütevazı olmalıdır \n\n  **İmmam Ebu Hanife**",
    "Allah’ın sana verdiği her şeyde hikmet vardır, o yüzden sabretmeyi öğren \n\n  **İbn Arabi**",
    "Dünyayı terk etmek zenginlikle değil, kalbin dünyadan kopmasıyladır \n\n  **Hasan Basri**",
    "Sakın arşın nurundan ümit kesme. \n __Vermeyi istemeseydi, istemeyi vermezdi..__",
    "Zorlayınca olmaz. \nNasibinse olur. \nAma zorlamadan da nasip olmaz.\n__Çünkü; Kader gayrete aşıktır.__",
    "Dua et fakat ecele etme, zamanın sahibi **Allah'tır**",
    "Zor yollar, her zaman en  güzel yollara götürür..",
    "Allah seni yaralı yerinden çiçeklendirecek __Sabret..__",
    "Nasipten öte yol yoktur.",
    "Velhasıl herşey nasip..",
    "Allah iyi niyetle çabalayan hiç bir kalbe yolunu şaşırtmaz",
    "kalbini yaratan, kalbinde ki dertleri bilmez mi? __Sabret..__",
    "Son çare **Allah** değil tek çare **Allah**..",
    "Kimseden bir şey bekleme, güzel şeyler daima **Allah'tan** gelir.",
    "Canı Yanan Sabretsin Can Yakan Canının Yanacağı Günü Beklesin..",
]
    return random.choice(quotes)
