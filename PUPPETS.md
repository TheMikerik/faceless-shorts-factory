# Puppets

Knihovna postav v [puppets/](puppets/). Název složky popisuje vzhled, ne konkrétní osobu ani příběh, takže postavy jdou použít v jakémkoli vymyšleném příběhu.

Všechny lidské postavy mají výrazy ve `faces/`: `neutral`, `happy`, `nervous`, `shocked`, `shouting`, `confused`. Mají rig (`rig.json`) a vrstvy `head`, `body`, `armL/R`, `legL/R`. Zvířata z boku (krysy, kočka, pes, pták) mají jen dvě vrstvy (`body`, `head`) a žádné výrazy. Zdrojový obrázek je v každé složce jako `source.png`.

## HLAVNÍ POSTAVA (v každém videu)

| Složka | Jak vypadá | Role |
| --- | --- | --- |
| `main_hero_tlama` | **Tlama**: růžová kulatá hlava s obří pusou plnou velkých zubů, bílý plášť, plochá žlutá ochranná brýle na čele | hlavní hrdina **všech** příběhů, kanálu TlamaLabs. Každé video ji musí obsahovat |

- Výrazy (`faces/`): `happy`, `nervous`, `shocked`, `shouting`, `confused`, `neutral`. `neutral` je výchozí velký úsměv.
- Poznávací znaky, které se nesmí měnit: růžová hlava, obří pusa, žluté brýle na čele, bílý plášť. Případné další kostýmy dělej jako nové postavy, ale hrdina zůstává tahle.
- Při rozřezání bylo nutné použít `--stick 0.028` (ruce jsou větší než u ostatních postav, výchozí práh by je přiřadil k tělu): `python3 .claude/skills/ricksclips-short-style/scripts/stage/puppet.py slice puppets/main_hero_tlama/source.png puppets/main_hero_tlama --stick 0.028`.
- Další varianty návrhu jsou v `puppets/_candidates/` (jen pro archiv).

### Varianty Tlamy (odvozené lokálně, bez Higgsfieldu)

Kopie `main_hero_tlama` s rekvizitou dokreslenou přímo do vrstvy, takže se hýbe s postavou a po schování postavy (např. `to` pod zem) nezůstane viset ve vzduchu. Mají všechny výrazy jako originál. `_phone` a `_nest` dělá `scripts/puppet_variants.py`.

| Složka | Co má navíc | Poznámka |
| --- | --- | --- |
| `main_hero_tlama_phone` | červený mobil v pravé ruce | telefon stojí rovně při `"pose": {"armR": -105}` (ruka u obličeje). Hovory, telefonáty, selfie |
| `main_hero_tlama_nest` | ptačí hnízdo se dvěma vajíčky na hlavě | „zítřejší já“, gag s ptákem, druhá Tlama ve stejné scéně |
| `main_hero_tlama_snow` | hnízdo jako `_nest` + sníh na hnízdě | zimní scény (video 005). Vznikl jednorázově (skript už smazán) |

Vznikly skriptem s PIL (rozšíření plátna vrstvy `armR` / `head` a všech `faces/`, úprava `box`, `pivot` a `center` v `rig.json`). Stejným postupem jde přidat další rekvizitu (klobouk, náplast, korunu), aniž by bylo potřeba generovat novou postavu.

## Lidé

Moderní postavy jsou nahoře, starodávné (historická videa) dole. Starodávné kostýmy se nejlépe hodí do pohádkově-absurdních příběhů (král, hrad, městečko, trh).

| Složka | Jak vypadá | Povaha / role | Kdy použít |
| --- | --- | --- | --- |
| `yellow_hoodie_kid` | hnědé rozcuchané vlasy, žlutá mikina | veselé dítě (cca 8 let) | sestra, bratr, kamarád, svědek |
| `red_bun_mom` | vínový drdol, zelený svetr se zástěrou | laskavá, trochu unavená máma | máma, babička, sousedka, kuchařka |
| `grey_mustache_teacher` | kulaté brýle, šedý knír a vlasy po stranách, hnědé sako s červenou kravatou | přísný, podezíravý | učitel, ředitel, úředník, strážce pravidel |
| `dwarf_king` | zlatá koruna, červený nos, obří bílý plnovous, červený plášť | malý, hrdý, mrzutý | malý král ve zdi, šéf, vládce čehokoli |
| `purple_horned_monster` | fialová hlava se třemi očima a rohy, zelený chochol, zelené tělo s oranžovými skvrnami | hloupě přátelská příšera, ne strašidelná | příšera, záporák, který je ve skutečnosti hodný, vetřelec |
| `green_feather_noble` | zelený klobouk s bílým perem, zrzavé kníry, zelený kabát s krajkovým límcem | naštvaný, hrdý šlechtic | šéf, záporák, nafoukaný pán, rozzlobený soused |
| `black_hat_noble` | černý vysoký klobouk, bílá krézová (volánová) obojek, zlatý řetěz, bradka | přísný, vážný pán | starosta, soudce, přísný ředitel, někdo, kdo vydává pravidla |
| `maroon_cap_elder` | vínová čepice, šedý vous, volánový límec, vínový kabát | ustaraný, smutný stařík | vystrašený nebo nešťastný pomocník, moudrý dědeček, oběť pozdních novinek |
| `maroon_cap_elder_nocap` | stejný stařík bez čepice (holá hlava, všechny výrazy) | stejný jako `maroon_cap_elder` | výměna za `maroon_cap_elder` + `prop_cap` pro gag „čepice odletěla“ |
| `feather_beret_clerk` | černý baret s hnědým perem, hnědá vesta, bílý límec, mladý | zmatený, nenápadný mladík | kamarád hrdiny, úředník, svědek, ten, kdo nechápe, co se děje. Má navíc výraz `burnt` (spálený obličej) pro gagy s výbuchem nebo požárem |
| `pith_helmet_official` | bílá tropická helma, černé kníry | sebejistý úředník / průzkumník | úředník, vedoucí akce, vynálezce, cestovatel, šéf kanceláře |
| `straw_hat_peasant` | kónický slaměný klobouk, modré oblečení s páskem | klidný, skromný člověk | lovec, farmář, prodavač, obyčejný hrdina, dav (použít vícekrát) |

## Zvířata

Zvířata jsou z boku a **koukají doprava** (doleva je otoč pomocí `flip`). Kočka a pes mají čtyři nohy, pták dvě. Stejný styl jako zbytek (tlusté tmavé linky, ploché barvy, jeden stín). Mají jen dvě vrstvy `body` a `head` (hlava se na krku mírně naklání), **žádné výrazy** a žádné ruce. Velikost nastav přes `height` v `short.json` (celková výška vč. ocasu).

| Složka | Jak vypadá | Kdy použít |
| --- | --- | --- |
| `rat` | hnědá krysa s růžovým ocasem | krysa, myš, malé zvíře, které se množí nebo utíká |
| `rat_notail` | stejná krysa bez ocasu | gag „krysa bez ocasu“, druhá varianta pro zástup krys |
| `orange_tabby_cat` | oranžová mourovatá kočka s bílou hrudí a tlapkami, zvednutý ocas | kočka, kočičí král, šéf |
| `dog_floppy_ears` | světle hnědý pes s velkým klapatým uchem, krémová hruď, černý nos | pes, věrný parťák, postava v pozadí |
| `grey_bird` | neutrální bílošedý pták, oranžový zobák a nohy, křídlo na boku | základ pro holuba, kachnu i kuře. Na jiný druh vyrob variantu: přegeneruj `source.png` přes Higgsfield s přebarvením a znovu rozřež |

**Přebarvené varianty pro davy** (vznikly jednorázově, posun barvy srsti, linky a bílá zůstávají):
- kočky: `cat_grey`, `cat_black`, `cat_white`, `cat_brown`, `cat_cream`, `cat_blue` (oranžová `orange_tabby_cat` tak zůstává v davu jedinečná),
- psi: `dog_brown`, `dog_white`, `dog_grey`, `dog_golden`, `dog_black`.

Náhled všech: `puppets/_cat_puppets_preview.jpg`.

## Rekvizitové loutky (`prop_*`)

Obrázek jako „postava“ (vrstva `head` = obrázek, `body` = 1 px). Na rozdíl od statických rekvizit v `props` se dají hýbat a schovat přes `to` (padat, letět, přistát), a kamera je umí sledovat přes `target`. Vznikly jednorázově lokálním skriptem (už smazán).

| Složka | Co to je | Typická `height` |
| --- | --- | --- |
| `prop_cap` | vínová čepice staříka (odlétá při kýchnutí) | 0.2 |
| `prop_fly` | moucha | 0.12 |
| `prop_fish` | modrá ryba | 0.13 |
| `prop_snow` | průhledná karta se sněhovými vločkami; padání = opakované `to` shora pod zem, `idle: false` | 2.8 |
| `prop_pancake` | palačinka s máslem (z boku) | 0.15 |
| `prop_cake` | třípatrový růžový narozeninový dort se svíčkami | 1.45 |
| `prop_crumbs` | talíř s drobky a jednou svíčkou (snědený dort, výměna za `prop_cake`) | 0.22 |
| `prop_can_cat` / `prop_can_cat_open` | konzerva kočičího žrádla zavřená / otevřená (otevřená je vyšší kvůli víčku, `height` × 1.31) | 0.42 |
| `prop_can_dog` | modrá konzerva psího žrádla s kostí | 0.42 |

## Poznámky

- Chybí zatím: poštář, obří zvíře (např. kuře velikosti domu), babička, další moderní postavy do davu. Nové postavy dělej podle skillu (`ricksclips-short-style`, krok 1–3) a doplň je sem.
- Složka `puppets/` je v `.gitignore`, takže tento soubor je jediný záznam o tom, kdo je kdo.
