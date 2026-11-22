# Content creator projekt – YouTube Shorts

## O projektu

Můj content creator projekt zaměřený hlavně na **YouTube Shorts**. Tento repozitář slouží jako pracovní složka pro nápady, skripty, assety a výrobu videí.

## Kanál

- **Aktivní kanál:** [@TlamaLabs](https://www.youtube.com/@TlamaLabs)
- **Aktuální stav:** 24 odběratelů, 6 Shorts (všechny z Robloxu, už neodpovídají novému směru)
- **Záměr:** začít vydávat **faceless Shorts** (animované, bez obličeje autora) pomocí skillu `ricksclips-short-style`

## Vize a cíle

- **Hlavní cíl:** monetizace YouTube (splnit podmínky YPP – odběratelé + zhlédnutí Shorts – a vydělávat z reklam)
- **Zaměření:** úplná změna. Roblox obsah je minulost, kanál dostane novou identitu (faceless absurdní vymyšlené příběhy). Stávající Roblox Shorts už nejsou směr.
- **Téma a jazyk:** **vymyšlené absurdní příběhy, které se nikdy nestaly** (žádná historie, žádná reálná fakta, žádní skuteční lidé). Vždy v **angličtině**, formát silný hook → stupňující se absurdita → zlom „You see…“ → twist (globální publikum, vyšší RPM)
- **Hlavní postava:** `puppets/main_hero_tlama` (Tlama, růžová hlava s obří pusou a žlutými brýlemi) je hrdina **každého** videa. Vždy ji použij jako hlavní postavu. Detaily v `PUPPETS.md`
- **Hlas:** hlas si **generuji sám** a nahraji ho do projektu (`audio/voice.mp3`). **Hlas negeneruj** (žádné `generate_audio` ani jiný TTS), ani ho nenavrhuj generovat. Dodej jen textový skript. Hlas generuj **pouze tehdy, když to výslovně řeknu**. V tom případě použij **Miles** z Higgsfieldu (`voice_id: e18664a7-ee4f-5273-acf8-533eb24cd366`, `voice_type: preset`)
- **Hlavní cíl videa:** co nejvyšší retence. Divák musí zůstat u Shortu až do konce (a ideálně ho pustit znovu v loopu)
- **Úroveň angličtiny:** jednoduchá, srozumitelná pro všechny (viz sekce „Jednoduchá angličtina“)
- **Frekvence:** **denně** 1 Short. Výroba proto musí být co nejrychlejší: knihovna (postavy, textury, pozadí) se staví jednou a znovu používá, nové video = jen nový skript, hlas a `short.json`.
- **Důsledek:** preferuj opakovatelné, automatizovatelné postupy před jednorázovou dokonalostí. Navrhuj, jak zkrátit čas na jedno video.

## Obsah složky

| Cesta | Popis |
| --- | --- |
| `brainstorming.md` | Reference na inspirační kanály a staré nápady (nové nápady sem nezapisovat, jen na výslovné přání) |
| `.claude/skills/ricksclips-short-style/` | Hlavní skill pro výrobu faceless Shorts ve stylu @RicksClips3000 |
| `.claude/skills/outcut-cartoon-shorts/` | Alternativní skill: 2D cut-out kreslené Shorts (Higgsfield + Remotion) |
| `PUPPETS.md` | Přehled postav ve `puppets/` (kdo je kdo a kdy ho použít). Po přidání nové postavy ho doplň |

## Hlavní workflow: faceless Shorts ve stylu RicksClips

Používej skill **`ricksclips-short-style`** (`.claude/skills/ricksclips-short-style/SKILL.md`). Před jakoukoli prací na videu si ho přečti a řiď se jím.

Stručně: ploché 2D doodle postavy ve slunečném 3D světě, celé sestavené v kódu (three.js stage). Assety (postavy, pozadí, hlas) se generují přes **Higgsfield connector**, scéna se skládá do `short.json` a renderuje přes `scripts/stage/render.mjs`.

Formát: 1080x1920, 30 fps, cca 60 s, titulky po 1–2 slovech.

Kroky workflow (podrobně ve skillu):
1. Hlavní postava → 2. emotion sheet → 3. slice na vrstvy / rig puppetu → 4. pozadí → 5. skript, hlas, timing → 6. scéna v `short.json` → 7. stop-frame kontrola (`--stills`) → 8. render → 9. porovnání s referencí → 10. **uložení do `videos/`** (viz „Po vyrenderování videa“) → 11. **publikace** (viz „Publikace přes Buffer“, nikdy automaticky, až po mé kontrole videa) → 12. další video

**Negenerují se:** hudba, textury ani 3D modely. Video má hlas, ploché barvy, rekvizity z primitiv stage (bedna, sud, zeď, dům…) a **hotové 3D modely (GLB) z knihovny `props/`**, které dodávám ručně (stažené free packy, CC0). Nové 3D modely negeneruj, jen používej ty z knihovny.

### Knihovna 3D modelů (`props/`)

- Jedna složka na pack (např. `props/basic_scene/` = hradní sada Kenney), uvnitř `*.glb` a `Textures/` (GLB odkazuje na `Textures/colormap.png`, nemazat).
- **`props/catalog.json`** = seznam všech modelů s rozměry (jednotka stage, hrdina má 1,8). **`props/<pack>/0_preview.jpg`** = náhledový list všech modelů. Před stavbou scény je přečti a vybírej z nich.
- Po přidání nového packu spusť `.venv/bin/python scripts/props_catalog.py` (obnoví katalog i náhled).
- **Kombinuj:** modely z `props/` a primitiva stage (bedna, sud, zeď, dům, strom…) se používají společně, ne místo sebe. Modely nejsou povinné, primitiva dál platí (zdi, podlahy, velké tvary, absurdní předměty). Vyber, co se pro scénu hodí; typicky primitiva na stavbu místa + modely na detaily a rekvizity.
- **Packy se kombinují:** modely nemusíš brát jen z jedné složky. Ve scéně (i v jednom záběru) mísi packy podle potřeby, např. nábytek + jídlo + hřbitov. Cesta v `file` vždy obsahuje složku packu.
- Použití v `short.json`: `{"type": "model", "file": "props/basic_scene/wall.glb", "pos": [x, 0, z], "scale": 3, "rotY": 30}`. Kenney modely jsou malé (dlaždice 1×1), obvykle `scale` 2–3, nebo `height` v jednotkách stage.

### Struktura složky kanálu (podle skillu)

Jedna složka na kanál, znovupoužitelná pro všechna videa. Knihovna se staví jednou, pro nové video se mění jen `audio/` a `short.json`.

```
puppets/<postava>/   rig.json, vrstvy PNG, faces/
bg/                  pozadí
audio/               voice_original.mp3 (raw), voice.mp3 (upravený), script.txt, words.json
short.json           scéna pro aktuální video
```

### Skript – vzorec (vymyšlený absurdní příběh)

1. **hook** hned v první větě, bez úvodu: absurdní, konkrétní situace, která vyvolá otázku „cože? jak?“ (např. „Every night, my cat pays rent to a tiny king who lives in my wall.“)
2. dva až tři stupňující se detaily: každý je absurdnější než předchozí
3. zlom „You see…“, kde začíná (absurdní, ale uvnitř příběhu logické) vysvětlení
4. pointa/twist v poslední větě těsně před loopem, ideálně navazuje na hook, aby se video přirozeně pustilo znovu

### Pravidla pro příběhy

- **Vše je vymyšlené.** Žádné skutečné události, historické postavy, data, reálné značky ani skuteční lidé. Nic nesmí vypadat jako pravdivé tvrzení o světě. Nehledej a neověřuj fakta, příběh si prostě vymysli.
- **Absurdní, ale uvnitř konzistentní.** Příběh má svá vlastní pravidla a ta se dodržují (absurdita funguje, když dává vnitřní smysl).
- **Silný hook.** První věta (do ~2 s) musí zastavit scroll: konkrétní, bizarní, bez úvodu. Žádné „Hey guys“, žádné „Today I will tell you“.
- **Retence.** Každé 2–3 věty nová zápletka, odhalení nebo eskalace („open loop“: slib něco, co se vysvětlí až později). Nikdy nevysvětluj vše hned. Žádný hluchý moment, žádná vata. Poslední věta se vrací k začátku, aby se video loopovalo.
- **Jeden hrdina, jedna situace.** Jednoduchý příběh, který se dá vizuálně vyprávět jednou postavou a pár rekvizitami.
- **Bezpečný obsah.** Bez násilí, nenávisti a sexuálního obsahu (monetizace, YPP). Vhodné i pro mladší diváky.

### Silné hooky (musí přimět zůstat)

První věta rozhoduje, jestli divák odscrolluje. Každý hook musí splnit **aspoň 3 z 5**:
1. **Začíná uprostřed děje** (něco se právě děje, žádné „Once upon a time“, žádné představování).
2. **Přehnané a konkrétní** (obří, nemožné, s číslem nebo časem: „60 seconds“, „every adult in the world“).
3. **Sázky nebo hodinky:** hrozí něco, co se musí vyřešit hned („before the moon falls“, „only I can fix it“).
4. **Otevírá smyčku:** vzbudí otázku, kterou zodpoví až konec („Why did every cat look at my house?“).
5. **Vypravěč je v ohrožení nebo v centru dění** („I“ = Tlama), ne popis světa zvenčí.

Max. 15 slov, jednoduchá angličtina. Příběh pak hook splní v zlomu „You see…“ a vrátí se k němu v twistu.

#### 23 ukázkových hooků (+ nápad na twist)
1. "At 3 AM, my cat looked at me and whispered: 'Run. They are inside the walls.'" / "They" are tiny workers building a pool for the cat. The cat wanted to warn me about the noise.
2. "Today at 8 AM, every adult in the world turned into a potato. Only I can fix it." / The cure is a hug from a kid. At the end, I turn into a potato too, and my little sister has to hug me.
3. "I have 60 seconds before the moon falls on my house." / The moon is only looking for its lost sock. It finds it, and I wake up with a moon-shaped sock in my bed.
4. "A giant chicken has followed me for three days, and today it learned my name." / Each lie I told made it bigger. I tell the truth, and it shrinks. Last line: I lie again.
5. "My shadow packed a bag and said: 'Do not look for me.'" / The shadow got a job with a taller person. At the end, my new shadow is a very small one.
6. "The sun did not come up today, and only I know where it went." / The sun overslept in my bed. I sing it awake, and now it follows me to school.
7. "I woke up and my whole house was on the moon, and my mom did not care at all." / Mom already knew. The moon has the best Wi-Fi. At the end, the house is on Mars.
8. "Do NOT open the fridge. It already knows your name." / The fridge only wants a friend. It lets me in, and inside it is a snowy city for tiny penguins.
9. "My teacher is a dragon, and today he finds out that I know." / He is scared of me, because I am a kid with a pencil. He gives everyone an A to stay quiet.
10. "A tiny king moved into my wall, and today he asked me for one million dollars." / He pays the cat rent with my money. At the end, the cat is the king's boss.
11. "Tonight, everyone in my town has the same dream, and I am the monster in it." / In the dream, I am a kind monster who saves everyone. The town wakes up and they all clap.
12. "My phone just sent me a photo of my room, taken one minute from now." / In the photo, a giant pizza sits on my bed. I run to the kitchen, and now there is a pizza on the table, too.
13. "The mailman gave me a letter. It says: 'You have 10 minutes to hide the last cookie.'" / A cookie thief is a very polite bear. At the end, the bear delivers the next letter.
14. "I sneezed once, and now a pigeon is the mayor of my city." / Every sneeze changes who leads the town. At the end, I sneeze again, and a whale is the mayor.
15. "Yesterday, the ducks took over my town. I am their only hope, and I only have bread." / The ducks only want bread for a giant party. I join them, and I am the guest of honor.
16. "My brother sold me to a pigeon for three coins." / The pigeon planet has a very bad Wi-Fi. At the end, my brother is sold to a squirrel.
17. "There is a red button in my school. It says: DO NOT PRESS. Today, I pressed it." / The school turned upside down. Everyone is on the ceiling, and the lunch is falling like rain.
18. "My grandma's soup makes you invisible, and my sister just drank the whole pot." / She is invisible for a week. At the end, grandma drinks the second pot, and so does the dog.
19. "Every night, all the colors leave my city. Tonight, I follow them." / The colors go to a secret party. At dawn, my city is back, but my hair is now green.
20. "I told one tiny lie, and now a chicken the size of a house is knocking on my door." / The truth makes it small. I say it, and the chicken becomes a chick, and then the chick lies to me.
21. "The goldfish at my school is secretly the principal, and today I caught him without his hat." / He gives me a deal: keep the secret, get free pizza for life. Final scene: the pizza is delivered by the goldfish.
22. "Why did every cat in the world look at my house at exactly 7 PM?" / They are all waiting for my cat, who is the cat king. He walks out, and they all bow, and he asks me for a snack.
23. "I found a door in my school that opens to yesterday, and yesterday's me was waiting with a warning." / The warning: "Do not eat the blue cake." Today, I eat the blue cake anyway, and it is amazing.

### ElevenLabs tagy ve skriptu

Textový skript **vždy piš rovnou s ElevenLabs audio tagy** v hranatých závorkách, aby ho šlo vložit do ElevenLabs bez úprav. Tagy piš anglicky, vkládej je před větu/frázi, které se týkají, a nepřeháněj (cca 1 tag na 1–2 věty, ať hlas nezní přehrávaně). Dialog v uvozovkách zůstává normální text.

Používej hlavně tyto tagy:
- **Emotion:** `[weak]` `[angry]` `[bored]` `[menacing]` `[playful]` `[tired]` `[excited]`
- **Vocalizations:** `[clears throat]` `[coughing]` `[chuckling]` `[sighing]` `[sniffling]` `[yawning]` `[laughing]` `[sharp exhale]` `[scoffing]` `[humming]` `[panting]` `[gasping]`
- **Delivery:** `[whispering]` `[singing]` `[slowly]` `[softly]` `[pause]` `[voice breaking]`
- **Character:** `[sleepy drowsy voice]` `[witch voice]` `[drunken voice]`
- **Sound effects:** `[keyboard typing]` `[echoing]` `[knocking on door]` `[bell ringing]` `[phone ringing]` `[dog barking]` `[crowd cheering]` `[applause]` `[rain falling]` `[drum roll]` `[heartbeat]` `[engine starting]`

Ukázkový skript (styl a hustota tagů):

```
[thoughtful] I built the best invention in the world, but nobody can see it. [sighs] Not even me. [short pause] This morning, the mayor heard about it. [excited] He ran in and shouted, "I will pay a thousand coins for it!" [chuckles] I said, "Great! Just one problem. I lost it." [short pause] Then he walked right into it. [sound of impact] Bonk! [surprised] He fell on the floor, and his hat flew out the window. [sighs] So I ran to the middle of the room. Nothing. [anxious] Oh no. I gave it little wheels. Big mistake. [short pause] At lunch, the baker hit it on the street. All his bread flew into the sky. [chuckles] Then my friend Bob hit it at the market and landed in a barrel of fish. [annoyed] The whole town was angry. "What is this thing?" [thoughtful] You see, I built a machine that makes things invisible. [sighs] And the first thing it made invisible was itself. [anxious] The mayor gave me one hour. "Find it, or no coins." [inhales deeply] I looked everywhere, on my hands and knees. [surprised] Then I touched something warm. It was buzzing. [excited] My machine! [thoughtful] I found two buttons. A small one and a big one. [thoughtful] One makes things come back. But which one? [short pause] I pressed the big one. [sound of electricity] There was a bright flash. [surprised] And the whole town was gone. The houses. The people. The mayor. [short pause] Then, from nowhere, I heard his voice. [muffled] "Amazing! I will pay two thousand coins!" [sighs] So now I have the best town in the world, but nobody can see it. Not even me.
```

Ukázka smí používat i další přirozené tagy mimo seznam (`[thoughtful]`, `[surprised]`, `[anxious]`, `[annoyed]`, `[short pause]`, `[inhales deeply]`, `[muffled]`, `[sound of impact]`), ale seznam výše je základ.

**Pozor při časování a titulcích:** tagy se nikdy nezobrazují jako titulky a nepočítají se do tempa (~4 slova/s). Před `words` / `words.json` si uložit `audio/script.txt` **bez tagů** (nebo tagy odfiltrovat), jinak se zarovnání slov rozbije.

### Zvuková stopa: raw + lokální úprava

- Nahraný hlas je vždy **raw** a ukládá se jako `audio/voice_original.mp3`. Nikdy ho neupravuj přes Higgsfield ani jiný online nástroj.
- Úpravu dělej **lokálně na tomhle počítači** přes `ffmpeg`: `scripts/voice.sh` (výstup `audio/voice.mp3`, raw soubor se nepřepisuje).
  1. odstraní mezery/ticho mezi větami (`silenceremove`, zbyde jen ~0,06 s),
  2. zrychlí (`atempo`, výška hlasu se nemění) tak, aby výsledek měl **max 60 s** (cíl ~59,5 s). Pokud už je kratší, nezrychluje.
- Až potom spusť `words` pro `audio/words.json` nad **upraveným** `voice.mp3` (časování musí sedět na finální stopu).
- Spuštění: `scripts/voice.sh` (výchozí cesty), případně `scripts/voice.sh raw.mp3 out.mp3 60`.

### Po vyrenderování videa (povinné)

Po každém dokončeném renderu (`out.mp4`) hned vytvoř složku videa v `videos/`, bez ptaní:

- Název: `videos/NNN-nazev-videa/`, kde `NNN` je další pořadové číslo (podle nejvyššího čísla v `videos/`) a název je krátký anglický slug (např. `003-invisible-invention`).
- Obsah: **jen tyto tři soubory**:
  1. `video.mp4`: kopie finálního `out.mp4`,
  2. `script.txt`: kopie `audio/script.txt` (finální skript bez tagů),
  3. `metadata.md`: anglicky, **zvlášť pro každou platformu** (každá má jiné konvence). Přesná struktura (nadpisy nech beze změny, publikační skript je podle nich parsuje):

     ```
     # NNN – Název videa

     ## YouTube
     ### Title
     jediný název (s emoji, max ~70 znaků), žádné alternativy

     ### Description
     krátký popisek, který otevře smyčku („Watch till the end…“), na konci 3–5 hashtagů (první vždy #shorts)

     ### Tags
     shorts, story, funny   (stejná slova jako hashtagy bez #; Buffer je neposílá, jen pro ruční vložení)

     ## Instagram
     ### Caption
     první řádek je hook, pak krátký popisek, na konci 3–5 hashtagů (bez #shorts)

     ## TikTok
     ### Caption
     velmi krátký popisek (1–2 věty), na konci 3–5 hashtagů
     ```
- Hashtagy jsou jednoslovné (bez mezer). Každá platforma má vlastní text, nekopíruj mechanicky stejný popisek třikrát.

### Publikace přes Buffer (jen na výslovný pokyn)

Videa se publikují skriptem `scripts/publish/publish.mjs` (nahraje `video.mp4` na Cloudflare R2 a zařadí ho přes Buffer API do fronty na YouTube, Instagram a TikTok). Klíče jsou v `.env` (nikdy je nečti ani nevypisuj).

- **Nikdy nepublikuj automaticky.** Nejdřív si video nechám zkontrolovat já. Publikaci spusť až po mém výslovném pokynu (např. „publikuj 004“), protože jde na veřejné sítě.
- Před ostrým spuštěním vždy nejdřív `--dry NNN` a ukaž mi výpis.
- Spuštění: `node scripts/publish/publish.mjs NNN` (zařadí do dalšího volného slotu ve frontě v Bufferu, časy se neřeší). Více videí najednou: `... 004 005 006`. Pevné časy jen na přání (`--start`, `--time`).
- Skript podle `.published.json` už publikovaná videa přeskočí. Video na R2 nemaž, dokud nevyjde.

### Jednoduchá angličtina

Skript musí pochopit každý, včetně mladších diváků a lidí, pro které angličtina není hlavní jazyk (úroveň A2, max. B1).

- Krátká slova a krátké věty (ideálně do ~10 slov). Jedna myšlenka na větu.
- Běžná slova z každodenního života. Žádná složitá nebo vzácná slovíčka (místo „consequently“ → „so“, místo „purchase“ → „buy“, místo „enormous“ → „huge“).
- Jednoduché časy (present simple, past simple). Žádné složité větné konstrukce, vedlejší věty v řetězcích ani trpný rod bez nutnosti.
- Žádné idiomy, slang, frázová slovesa ani slovní hříčky, které cizinec nepochopí („kick the bucket“, „spill the beans“…).
- Žádná odborná terminologie ani složitá jména. Jména postav krátká a snadno vyslovitelná (Tom, Mia, Bob).
- Čísla jednoduše (ne „1,347“, ale „a thousand“).
- Před odevzdáním skript zkontroluj: kdyby ho slyšelo desetileté dítě nebo začátečník v angličtině, pochopil by každou větu? Pokud ne, zjednoduš.

Cca 4 slova za sekundu, žádné prázdné místo.

## Pravidla stylu (zkráceně)

- Postavy: ploché 2D výřezy s velkými kulatými hlavami (hlava cca stejně široká jako trup), reálné stíny v 3D
- Linky: tlusté, rovnoměrné, švestkově černé `#271925`, nikdy čistá černá
- Barvy: teplé slunce vs. chladné stíny, stíny nezvedat do čisté černé
- Živé scény: záběr každé 1–3 s, v každém záběru se něco změní (úhel, výraz, pozadí, světlo), kulisy ve třech vrstvách (popředí, střed, pozadí), 3–5 míst na video, 1–3 vedlejší postavy. Podrobně ve skillu („Keep every scene alive“)
- Kamera: pohyb v každém záběru, převážně přibližování, žádné tvrdé střihy

## Technické požadavky

- Higgsfield connector musí být zapnutý (bez něj nejdou generovat assety; samotný render funguje i bez něj)
- Setup (jednou): `cd scripts/stage && npm install && npx playwright install chromium`, `pip install numpy pillow scipy opencv-python-headless`, `ffmpeg` a `ffprobe` v PATH
- Python skripty skillu spouštěj přes `.venv/bin/python` (je v něm `faster-whisper` pro přesné časování slov ve `words.json`; systémový `python3` ho nemá a spadne na odhad podle hlasitosti)
- Před každým plným renderem vždy `--stills` kontrola

## Inspirace

- **RicksClips3000** – https://www.youtube.com/@RicksClips3000/shorts – vizuální styl, který kopíruju
- **theboov_** – https://www.youtube.com/@theboov_/shorts – nápad na redabbing (kopíruje zahraniční videa 1:1 a jen je předabovává)

## Jak se mnou pracovat

- Komunikuj česky, pokud nenapíšu jinak. Skripty, hlas, titulky, názvy a popisky videí piš **anglicky**.
- Respektuj monetizační cíl: originální obsah (ne 1:1 kopie cizích videí), žádná reálná fakta ani skuteční lidé (vše vymyšlené, takže nic k ověřování), žádné porušování pravidel YouTube (reused content, copyright u hudby).
- Když pošlu jen skript, spusť kroky 7–10 s existující knihovnou a nic se neptej předem.
- Při nejasnostech ohledně stylu vycházej ze skillu a `references/style-rules.md`, ne z odhadu.
- Nové nápady na videa **nezapisuj** do `brainstorming.md` ani nikam jinam. Jen mi je napiš do chatu. Do `brainstorming.md` zapisuj jen, když to výslovně řeknu.
- Když chci nápad nebo skript, dodej **jen textový skript** (a případně hook/twist). Hlas negeneruj, nahraju ho sám.
