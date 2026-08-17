# PulseWatch report value contract

| Polje | Odluka |
|---|---|
| Datum istraživanja | 17.08.2026. |
| Cilj | Report koji klijentu pomaže donijeti i zatvoriti bolju odluku, a ne inventar javnih podataka |
| Poslovni model | Premium managed intelligence usluga, podržana PulseWatch softverom |
| Primarni korisnik | Direktor/vlasnik poslovanja i imenovani vlasnici kategorija/procesa |
| Glavna mjera vrijednosti | Dokumentirana odluka ili akcija i njezin mjerljiv poslovni/operativni rezultat |
| Najvažnije ograničenje | Javni izvori sami ne mogu dokazati prihod, maržu, zalihu, konverziju ni uzročnost |

## Izvršna odluka

PulseWatch ne treba prodavati PDF. Treba prodavati **zatvorenu upravljačku petlju**:

> signal → dokaz → poslovno značenje → odluka → vlasnik i rok → provedba → rezultat → prilagodba monitoringa

Vodeći CI pružatelji vrijednost vežu uz usvajanje i poslovne ishode, uključujući prihod, win-rate i trajanje prodajnog ciklusa, a ne samo uz količinu sadržaja.[1] Forrester izričito navodi da se vrijednost pomiče od isporuke informacija prema implikacijama te preporučuje da se intelligence metrike vežu uz poslovne ishode stakeholdera.[6]

**BAT baseline je dobar dokaz kvalitete istraživanja, ali još nije potpuni dokaz klijentske vrijednosti.** Ima širok scope, službene izvore, ograničenja, prioritete i preporučene akcije. Nema potvrđene klijentove odluke, status provedbe, početni KPI, cilj, izmjeren rezultat ni konzervativnu atribuciju PulseWatchu.

## 1. Što tržišni lideri rade bolje od običnog reportinga

| Obrazac | Javni dokaz | PulseWatch primjena |
|---|---|---|
| Mjere usvajanje i poslovni učinak | Klue spaja adoption s prihodom, win-rateom i trajanjem ciklusa.[1] | Mjeriti je li signal otvoren, prihvaćen, dodijeljen i proveden te koji se KPI promijenio. |
| Intelligence stavljaju u stvarnu odluku | Autodesk case opisuje kvartalne win/loss izvještaje, promjene sentimenta i korištenje nalaza u ključnim poslovnim odlukama.[2] | Svaki signal mora navesti odluku koju može promijeniti i osobu koja je može donijeti. |
| Održavaju visoku kadencu i traže feedback | Crayonov 2026 survey povezuje tjedno dijeljenje, ažuriranje i traženje feedbacka s većom vjerojatnošću revenue impacta i adoptiona.[3] | Tjedni verified digest + kratki feedback; mjesečni executive review; kvartalna promjena scopea. |
| Prilagođavaju output ulozi i prioritetu | Contify javno pozicionira ready-to-use insight prilagođen timu, funkciji i strateškom prioritetu.[5] | Direktor, marketing, nabava i voditelj odjela ne dobivaju isti prikaz ni isti CTA. |
| Interpretiraju, ne prepisuju | Forrester navodi da najcjenjeniji outputi interpretiraju informacije, a prijelaz prema implikacijama je središnji za vrijednost.[6] | Nijedan signal ne ulazi u glavni report bez odgovora “što to znači” i “što sada”. |
| Dizajn služi odgovoru i akciji | Tableau navodi da i lijep dashboard postaje beskoristan ako korisnik iz njega ne može izvesti odgovor.[4] | Maksimalno tri izvršna prioriteta na prvoj stranici; detalji i svi izvori u dodatku/portalu. |

Napomena: vendor case studies i vendor surveyji pokazuju način pozicioniranja i njihove prijavljene ishode; nisu nezavisni dokaz da će isti učinak nastati kod PulseWatch klijenta.

## 2. BAT report — što zadržati, što popraviti

| Element | BAT sada | Procjena vrijednosti | V2 odluka |
|---|---|---:|---|
| Scope poslovnice i cijele ponude | Vrlo detaljan, 15 odjela | Visoko za baseline | Zadržati u onboarding baselineu; ne ponavljati cijeli inventar svaki mjesec. |
| Izvori i ograničenja | Jasni, 18 izvora | Visoko povjerenje | Zadržati evidence ledger; u bodyju prikazati samo dokaz uz aktivne signale. |
| Konkurentski radar | PEVEX + BAUHAUS + lokalni kontekst | Srednje | Zaključati samo konkurente i kategorije koje utječu na klijentove prioritete. |
| Signal → impact → action | Postoji | Visoka osnova | Dodati confidence, izvor, vrijeme detekcije, owner, rok i decision status. |
| Prioriteti | P1/P2 | Srednje | Uvesti materijalnost: prihod/marža, kupac, operativni rizik, hitnost i reverzibilnost. |
| KPI baseline i cilj | Nema | Kritični nedostatak | Ne preporučivati pilot bez početnog KPI-ja i cilja za svaku testiranu akciju. |
| Decision/action log | Nema | Kritični nedostatak | Pratiti `new → reviewed → accepted/rejected → actioned → measured → closed`. |
| Rezultat i vrijednost | Nema | Kritični nedostatak | U sljedećem reportu prikazati rezultat prethodnih akcija, ne samo nove signale. |
| Klijentski feedback | Nije strukturiran | Kritični nedostatak | Nakon tjednog digesta jedan klik: korisno / nije korisno / treba dublje. |
| Interni podaci | Nisu korišteni | Javni baseline je ograničen | Za paid pilot tražiti minimalne agregirane KPI-je bez osobnih podataka. |

## 3. Novi obvezni format svakog vrijednog signala

| Polje | Obvezni sadržaj |
|---|---|
| Signal | Jedna materijalna promjena ili potvrđena prilika/problem |
| Dokaz | URL, timestamp, before/after snapshot, citat i status izvora |
| Entity/SKU match | `exact`, `variant` ili `family`, uz confidence; za proizvode navesti brand/model/EAN gdje postoji, pakiranje, kanal i lokaciju |
| Klasifikacija | Potvrđeno / opažanje / hipoteza / ograničenje |
| Confidence | Visok / srednji / nizak, uz razlog |
| Poslovni kontekst | Koji klijentov cilj, kategoriju ili proces signal dodiruje |
| Potencijalni učinak | Prihod, marža, trošak, rizik, kupac ili brzina; raspon, ne lažna preciznost |
| Opcije | `ne reagirati`, `provjeriti`, `brza akcija`, `testirati` |
| Preporuka | Jedna preporučena opcija i zašto |
| Owner + rok | Imenovana funkcija/osoba i datum odluke/provedbe |
| KPI | Baseline, cilj, izvor mjerenja i prozor mjerenja |
| Status | New / reviewed / accepted / rejected / actioned / measured / closed |
| Rezultat | Što se dogodilo; odvojiti opaženu korelaciju od dokazive uzročnosti |
| PulseWatch doprinos | Detektirao / ubrzao / prioritizirao / verificirao / nije utvrđeno |

### Primjer prema BAT-u

| Korak | Primjer sadržaja |
|---|---|
| Signal | PEVEX uvodi materijalnu akciju na unaprijed zaključanu kategoriju kosilica. |
| Dokaz | Dva službena snapshot-a, cijena/pakiranje/EAN, datum početka i završetka. |
| Poslovno značenje | Preklapa se s BAT-ovom sezonskom kategorijom visokog prioriteta. |
| Preporuka | U 24 sata provjeriti pet usporedivih SKU-ova i odlučiti: bez reakcije, value bundle ili ciljana komunikacija. |
| Owner + rok | Voditelj vrta + marketing; odluka do sljedećeg radnog dana u 12:00. |
| Baseline | Prodane jedinice, bruto marža i raspoloživost prethodna četiri usporediva tjedna. |
| Target | Očuvati dogovorenu maržu i prodajne jedinice bez općeg popusta. |
| Rezultat | Nakon akcije: jedinice, marža, stockout, promet upita i klijentova ocjena korisnosti. |
| Atribucija | PulseWatch je ubrzao odluku ako je klijent ranije nije imao iz drugog kanala; financijski učinak se ne prisvaja bez kontrolnog dokaza. |

### Product-level quality gate

Kod usporedbe cijene, promocije ili dostupnosti obvezno zapisati:

- match class: `exact`, `variant` ili `family`;
- brand, model i EAN/SKU kada postoje;
- količinu, veličinu, pakiranje i uključenu dodatnu opremu;
- web/fizički kanal, lokaciju i trenutak opažanja;
- cijenu s/bez PDV-a kada je primjenjivo;
- dostavu, loyalty uvjet i trajanje promocije;
- javno prikazanu dostupnost odvojeno od potvrđene fizičke zalihe.

`Variant` i `family` match ne smiju proizvesti tvrdnju “konkurent je jeftiniji” bez eksplicitne napomene o neusporedivosti. Jednokratni screenshot bez identiteta artikla i vremenskog konteksta nije dokaz tržišnog pomaka.

## 4. Arhitektura klijentskog reporta

### Stranica 1 — Decision brief

Samo tri najvažnije stvari:

1. što se promijenilo;
2. zašto je materijalno za klijenta;
3. koja se odluka traži, od koga i do kada.

Uz svaki prioritet prikazati confidence, mogući raspon učinka i link na dokaz. Ako nema materijalne promjene, napisati **“Nema akcije — monitoring nastavlja”**. Ne puniti report šumom radi dojma aktivnosti.

### Stranica 2 — Što je PulseWatch već proizveo

- prethodne prihvaćene odluke;
- status provedbe;
- promjena KPI-ja;
- otvoreni blocker;
- konzervativna vrijednost: potvrđena / procijenjena / nije mjerljiva.

### Stranice 3–4 — Verified signal cards

Najviše pet materijalnih kartica. Sve ostalo ide u dodatak ili portal. Kartica koristi obvezna polja iz prethodnog poglavlja.

### Stranica 5 — Competitive/category radar

Ne popis cijelog tržišta, nego klijentove zaključane bitke:

- 3–5 prioritetnih kategorija;
- 2–5 stvarno relevantnih konkurenata;
- cijena/ponuda/usluga/dostupnost samo kada su usporedivi;
- gdje BAT ima obrambenu prednost;
- što bi promijenilo preporuku.

### Stranica 6 — Decision & action register

| ID | Odluka | Owner | Rok | Status | KPI | Sljedeći dokaz |
|---|---|---|---|---|---|---|

### Dodatak

Metodologija, svi izvori, blocked sourceovi, detaljne tablice, niski prioriteti i raw before/after dokaz. Izvršni dio ne smije postati evidence dump.

## 5. Kadenca i service level — PulseWatch prijedlog

Ovo su predloženi, a ne tržišno potvrđeni SLA-i. Zaključavaju se po pilotu tek nakon mjerenja stvarne pouzdanosti izvora i delivery kapaciteta.

| Sloj | Predložena kadenca/SLA | Svrha |
|---|---|---|
| P1 alert | Do 4 radna sata nakon verificirane detekcije | Akcija koja gubi vrijednost čekanjem mjesečnog reporta |
| P2 signal | Sljedeći radni dan | Materijalno, ali nije hitno |
| Tjedni digest | Isti dan svaki tjedan; maksimalno 5 signala | Odluke, feedback i promjena prioriteta |
| Mjesečni executive report | Fiksni datum + 45 min review | Rezultati, otvorene akcije, novi prioriteti i value scorecard |
| Kvartalni strategy review | Svaka tri mjeseca | Promjena konkurenata, kategorija, KPI-ja i komercijalnog scopea |
| Client feedback | Nakon svakog signala/reporta | Useful / not useful / deeper analysis + razlog |

## 6. Value scorecard

### A. Pouzdanost usluge

- planirani captureovi uspješno završeni;
- udio signala s potpunim before/after dokazom;
- vrijeme od detekcije do verificirane isporuke;
- materijalni promašaji koje je klijent pronašao prije PulseWatcha;
- false-positive / not-useful stopa.

### B. Usvajanje

- udio signala pregledanih u dogovorenom roku;
- udio signala prihvaćenih za akciju ili namjerno odbijenih s razlogom;
- vrijeme od alerta do odluke;
- broj otvorenih odluka bez ownera ili roka;
- sponsor value score 1–10.

### C. Operativni rezultat

Za BAT primjere:

- pokrivenost i sinkronizacija akcije po kanalima;
- vrijeme odgovora na odjelni upit;
- stopa upita → ponuda → kupnja;
- vrijeme potvrde zalihe/rezervacije;
- svježina kataloga i broj zastarjelih javnih elemenata;
- stockout ili dostupnost zaključanih SKU-ova/košarica.

### D. Poslovni rezultat

Samo uz agregirane interne podatke:

- prihod i bruto marža prioritetne kategorije;
- promo contribution, ne samo promet;
- prosječna košarica;
- konverzija upita/ponude;
- izbjegnuti nepotrebni široki popust;
- dokumentirani time saved;
- konzervativno procijenjen ili potvrđen financijski učinak.

### E. Izričita potvrda zadovoljstva

Nakon svakog mjesečnog reviewa klijent odgovara:

1. Koju ste novu stvar saznali koju prije niste znali?
2. Koju je odluku PulseWatch promijenio ili ubrzao?
3. Što idući mjesec trebamo prestati, nastaviti i početi pratiti?

Ako nema odgovora na prva dva pitanja, sponsor score sam po sebi nije dokaz vrijednosti.

### F. Održivost isporuke za INMAR

Po klijentu interno pratiti:

- analitičke sate po signalu, reportu i reviewu;
- trošak terenske provjere i vanjskih izvora;
- udio ručnog rada koji se može standardizirati bez pada kvalitete;
- bruto contribution nakon stvarnog delivery troška;
- scope creep i broj zahtjeva izvan paketa;
- razlog za upsell: više odluka/lokacija/kategorija, a ne samo veći PDF.

Veći resource spend je opravdan u pilotu i kod premium klijenta ako stvara dokazivu vrijednost i učenje. Trajno neograničen ručni scope bez pozitivne delivery ekonomike nije premium usluga nego skriveni gubitak.

## 7. Pravila atribucije — bez lažnog ROI-ja

| Razina | Što smijemo tvrditi |
|---|---|
| 0 — Nije utvrđeno | Signal je isporučen; nema dokaza da je utjecao na odluku. |
| 1 — Informed | Klijent potvrđuje da je signal korišten u odluci. |
| 2 — Accelerated | Klijent potvrđuje da je odluka donesena ranije zbog signala. |
| 3 — Influenced | Akcija je provedena i KPI se promijenio u očekivanom smjeru; drugi uzroci nisu isključeni. |
| 4 — Demonstrated | Kontrolni period/skupina ili drugi čvršći dizajn podržava uzročni učinak. |

PulseWatch ne prisvaja cijeli prihod akcije. Prikazuje bruto promjenu, poznate druge utjecaje, raspon i razinu dokaza.

## 8. Minimalni interni podaci za plaćenu vrijednost

Bez osobnih podataka i bez pune ERP integracije, jednom tjedno po prioritetnoj kategoriji:

- prihod;
- prodane jedinice;
- bruto marža ili barem margin band;
- dostupnost/stockout za zaključane artikle;
- broj upita, ponuda i realizacija za projektne usluge;
- aktivne akcije i trošak/popust;
- potvrda je li PulseWatch signal bio nov, koristan i actioned.

Ako klijent ne daje nijedan interni KPI, usluga ostaje korisna za risk/market awareness, ali financijski ROI mora biti označen **NEMAM**.

## 9. Pilot acceptance i renewal gate

### 30-dnevni pilot — PASS

Svi uvjeti:

1. 100% isporučenih P1/P2 signala ima dokaz, timestamp, klasifikaciju i ograničenje.
2. Najmanje 90% ugovorenih planiranih provjera izvršeno je ili je iznimka zabilježena s razlogom.
3. Najmanje 90% P1/P2 isporuka koje ovise o PulseWatch procesu ispunilo je ugovoreni SLA.
4. Nema poznatog materijalnog promašaja u zaključanom scopeu zbog PulseWatch procesa.
5. Najmanje tri signala klijent je eksplicitno ocijenio kao relevantna ili je dokumentirano da nije bilo materijalne promjene.
6. Najmanje 60% pregledanih signala owner je označio kao novo ili korisno; `unreviewed` se ne računa kao korisno.
7. Najmanje dvije signalne ili monitoring-review kartice završile su dokumentiranom odlukom, testom ili svjesnom odlukom `ne reagirati / nastaviti bez promjene`.
8. Za barem jednu akciju postoji baseline, cilj i dogovoren mjerni prozor.
9. Sponsor ocjenjuje korisnost najmanje 8/10 i potvrđuje prioritete za idući ciklus.

### Pilot — STOP/REDESIGN

- signali su uglavnom javne informacije koje je klijent već znao;
- više od 20% pregledanih signala označeno je netočno/neusporedivo;
- nema pristupa osobi koja može donijeti odluku;
- klijent ne može navesti nijednu odluku koju bi report mogao promijeniti;
- delivery trošak prelazi paket bez realnog puta standardizacije ili upsella.

### 90-dnevna obnova

Obnova se ne temelji na broju stranica. Traži se:

- pozitivan trend relevance/action ratea;
- najmanje tri dokumentirano podržane odluke u 90 dana;
- barem jedan izmjeren operativni ili poslovni KPI;
- sponsor value score ≥8/10;
- jasan sljedeći skup odluka koje monitoring može poboljšati.

Financijski cilj može biti konzervativna dokumentirana vrijednost veća od naknade, ali nije obvezno izmišljati 3× ROI ako mjerenje to ne može dokazati.

## 10. Kako biti bolji od drugih

1. **Human-verified, ne AI dump.** Svaki materijalni signal provjerava analitičar i nosi confidence/limitation.
2. **Client-specific decision map.** Monitoring počinje od odluka, ne od URL-ova.
3. **Internal + external evidence.** Javni signal se spaja s minimalnim internim KPI-jima.
4. **Closed-loop accountability.** PulseWatch pamti što je klijent prihvatio, odbio, proveo i izmjerio.
5. **Field verification kao premium dodatak.** Dopuštena fizička provjera cijene, dostupnosti i kupovnog puta kada javni web nije dovoljan; nikad se ne predstavlja kao web-dokaz.
6. **No-noise promise.** Ako nema materijalne promjene, klijent dobiva kratku potvrdu, ne umjetno napuhan report.
7. **Transparent uncertainty.** Blokiran izvor, neusporediv SKU i nepoznata zaliha ostaju jasno označeni.
8. **Resource investment tamo gdje klijent osjeti razliku.** Ručna QA, redundantni izvori, kategorijska analiza, brži verificirani alert i management review imaju prednost nad većim brojem generičkih monitora.
9. **Learning contract.** Svaki feedback mijenja prioritete, pragove i format sljedeće isporuke.
10. **Upsell iz dokazane potrebe.** Više konkurenata, SKU-ova, lokacija, field checks, internal-data povezivanje i dashboard ulaze tek kad postoje dokazani recurring decisions.

## 11. Što izbaciti iz glavnog reporta

- cijeli inventar kategorija nakon baseline mjeseca;
- generičke vijesti bez odluke koju mijenjaju;
- screenshotove bez interpretacije;
- preporuke bez ownera, roka i KPI-ja;
- velike tablice koje samo dokazuju koliko je istraživanja napravljeno;
- nizak prioritet samo zato da report izgleda pun;
- vendor marketing brojke kao obećanje PulseWatch rezultata;
- financijski ROI bez klijentovih internih podataka i pravila atribucije.

## 12. Implementacijski redoslijed

| Faza | Promjena | Gate |
|---|---|---|
| 1 | Proširiti JSON signal/action schema obveznim value poljima | Validacija odbija signal bez dokaza, ownera/roka ili KPI plana kada se traži akcija |
| 2 | Dodati decision/action register u report i persistent storage | Status preživljava između reporta |
| 3 | Uvesti weekly feedback i usefulness reason | Svaki signal dobiva client feedback ili ostaje `unreviewed` |
| 4 | Dodati value scorecard i attribution level | Report razdvaja output, adoption, operation i business outcome |
| 5 | Pilotirati s jednim klijentom i 3–5 odluka | Renewal gate prolazi bez ručnog uljepšavanja rezultata |
| 6 | Tek nakon ponovljivosti graditi portal/dashboard | Klijent razumije vrijednost bez stalnog objašnjavanja analitičara |

## Zaključak

Najbolji PulseWatch report nije najduži ni najširi. Najbolji je onaj u kojem klijent za 5 minuta vidi:

- što se dogodilo;
- zašto je to važno baš njemu;
- koju odluku treba donijeti;
- tko je provodi i do kada;
- kako ćemo znati je li uspjelo;
- koliki je dokumentirani doprinos PulseWatcha.

BAT treba ostati kvalitetan baseline primjer, ali sljedeća verzija mora dodati **decision register, KPI baseline/target/result, client feedback i value attribution**. To je prijelaz iz istraživačkog PDF-a u uslugu koju racionalan klijent može obnavljati i širiti.

## Sources

[1] https://klue.com/product/measure — Klue — Measure business impact
[2] https://klue.com/case-study/driving-double-digit-increases-to-win-rates — Klue — Autodesk case study
[3] https://www.crayon.co/state-of-competitive-intelligence-2026 — Crayon — 2026 State of Competitive Intelligence
[4] https://help.tableau.com/current/blueprint/en-us/bp_visual_best_practices.htm — Tableau Blueprint — Visual Best Practices
[5] https://www.contify.com/platform — Contify platform
[6] https://www.forrester.com/blogs/five-findings-about-todays-market-and-competitive-intelligence-programs — Forrester — Five Findings About M&CI Programs
