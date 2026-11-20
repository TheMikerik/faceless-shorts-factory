# Content creator projekt – YouTube Shorts

## O projektu

Můj content creator projekt zaměřený hlavně na **YouTube Shorts**. Tento repozitář slouží jako pracovní složka pro nápady, skripty, assety a výrobu videí.

## Kanál

- **Aktivní kanál:** [@TlamaLabs](https://www.youtube.com/@TlamaLabs)
- **Aktuální stav:** 24 odběratelů, 6 Shorts (všechny z Robloxu, už neodpovídají novému směru)
- **Záměr:** začít vydávat **faceless Shorts** (animované, bez obličeje autora) pomocí skillu `ricksclips-short-style`

## Vize a cíle

- **Hlavní cíl:** monetizace YouTube (splnit podmínky YPP – odběratelé + zhlédnutí Shorts – a vydělávat z reklam)
- **Zaměření:** úplná změna. Roblox obsah je minulost, kanál dostane novou identitu (faceless fakta/zajímavosti). Stávající Roblox Shorts už nejsou směr.
- **Téma a jazyk:** fakta/zajímavosti v **angličtině**, formát paradox → stupňující se detaily → vysvětlení → twist (globální publikum, vyšší RPM)
- **Frekvence:** **denně** 1 Short. Výroba proto musí být co nejrychlejší: knihovna (postavy, textury, pozadí) se staví jednou a znovu používá, nové video = jen nový skript, hlas a `short.json`.
- **Důsledek:** preferuj opakovatelné, automatizovatelné postupy před jednorázovou dokonalostí. Navrhuj, jak zkrátit čas na jedno video.

## Obsah složky

| Cesta | Popis |
| --- | --- |
| `brainstorming.md` | Nápady na obsah a reference na inspirační kanály |
| `.claude/skills/ricksclips-short-style/` | Hlavní skill pro výrobu faceless Shorts ve stylu @RicksClips3000 |
| `.claude/skills/outcut-cartoon-shorts/` | Alternativní skill: 2D cut-out kreslené Shorts (Higgsfield + Remotion) |

## Hlavní workflow: faceless Shorts ve stylu RicksClips

Používej skill **`ricksclips-short-style`** (`.claude/skills/ricksclips-short-style/SKILL.md`). Před jakoukoli prací na videu si ho přečti a řiď se jím.

Stručně: ploché 2D doodle postavy ve slunečném 3D světě, celé sestavené v kódu (three.js stage). Assety (postavy, textury, 3D modely, pozadí, hlas, hudba) se generují přes **Higgsfield connector**, scéna se skládá do `short.json` a renderuje přes `scripts/stage/render.mjs`.

Formát: 1080x1920, 30 fps, cca 60 s, titulky po 1–2 slovech.

Kroky workflow (podrobně ve skillu):
1. Hlavní postava → 2. emotion sheet → 3. slice na vrstvy / rig puppetu → 4. textury → 5. 3D modely → 6. pozadí → 7. skript, hlas, hudba, timing → 8. scéna v `short.json` → 9. stop-frame kontrola (`--stills`) → 10. render → 11. porovnání s referencí → 12. další video

### Struktura složky kanálu (podle skillu)

Jedna složka na kanál, znovupoužitelná pro všechna videa. Knihovna se staví jednou, pro nové video se mění jen `audio/` a `short.json`.

```
puppets/<postava>/   rig.json, vrstvy PNG, faces/
textures/            wood.png, stone.png ...
models/              *.glb
bg/                  pozadí
audio/               voice.mp3, music.mp3, script.txt, words.json
short.json           scéna pro aktuální video
```

### Skript – vzorec

1. paradox hned v první větě, bez úvodu
2. dva až tři stupňující se detaily
3. zlom „You see…“, kde začíná vysvětlení
4. pointa/twist v poslední větě těsně před loopem

Cca 4 slova za sekundu, žádné prázdné místo. **Každé datum, jméno a číslo fakticky ověř, než ho napíšeš.**

## Pravidla stylu (zkráceně)

- Postavy: ploché 2D výřezy s velkými kulatými hlavami (hlava cca stejně široká jako trup), reálné stíny v 3D
- Linky: tlusté, rovnoměrné, švestkově černé `#271925`, nikdy čistá černá
- Barvy: teplé slunce vs. chladné stíny, stíny nezvedat do čisté černé
- Kamera: pohyb v každém záběru, převážně přibližování, žádné tvrdé střihy

## Technické požadavky

- Higgsfield connector musí být zapnutý (bez něj nejdou generovat assety; samotný render funguje i bez něj)
- Setup (jednou): `cd scripts/stage && npm install && npx playwright install chromium`, `pip install numpy pillow scipy opencv-python-headless`, `ffmpeg` a `ffprobe` v PATH
- Před každým plným renderem vždy `--stills` kontrola

## Inspirace

- **RicksClips3000** – https://www.youtube.com/@RicksClips3000/shorts – vizuální styl, který kopíruju
- **theboov_** – https://www.youtube.com/@theboov_/shorts – nápad na redabbing (kopíruje zahraniční videa 1:1 a jen je předabovává)

## Jak se mnou pracovat

- Komunikuj česky, pokud nenapíšu jinak. Skripty, hlas, titulky, názvy a popisky videí piš **anglicky**.
- Respektuj monetizační cíl: originální obsah (ne 1:1 kopie cizích videí), fakta ověřená, žádné porušování pravidel YouTube (reused content, copyright u hudby).
- Když pošlu jen skript, spusť kroky 7–10 s existující knihovnou a nic se neptej předem.
- Při nejasnostech ohledně stylu vycházej ze skillu a `references/style-rules.md`, ne z odhadu.
- Nové nápady na obsah zapisuj do `brainstorming.md`.
