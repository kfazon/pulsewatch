# PulseWatch — konkurencija, ponuda i 90-dnevni poslovni plan

**Datum provjere tržišta:** 2026-08-17  
**Izdavatelj:** INMAR d.o.o.  
**Odgovorna osoba:** Kristijan Fažon, direktor

## Odluka na jednoj stranici

| Pitanje | Odluka |
|---|---|
| Što prodajemo? | Upravljanu funkciju tržišnog nadzora: provjeren signal, dokaz, poslovno značenje, preporučena akcija i praćenje ishoda. |
| Kome prvo? | Regionalni vlasnici brendova, ekskluzivni distributeri i specijalizirani trgovci kojima promjene cijena, promocija, dostupnosti, asortimana ili prodajne poruke neposredno utječu na maržu ili prodaju. |
| Glavni paket | **PulseWatch Managed — 1.490 EUR/mj. + PDV**, najmanje 3 mjeseca. |
| Ulaz | **Plaćeni 30-dnevni pilot — 1.500 EUR + PDV**, unaprijed. |
| Lite | **690 EUR/mj. + PDV**, asinkron i strogo ograničen; nuditi tek nakon pilota i stabilne automatizacije. |
| Ciljni MRR | **9.000–10.500 EUR bez PDV-a**, ne 3.500 EUR. Točan cilj ovisi o stvarnom ukupnom trošku Kristijanove isplate koji treba potvrditi računovođa. |
| Put do cilja | Najzdravije: 6 Managed klijenata = 8.940 EUR MRR ili miks 5 Managed + 3 Lite = 9.520 EUR MRR. |
| Trenutačna odluka | **GO za plaćenu validaciju, ne GO za SaaS build.** |

## IMAM / NEMAM

### IMAM

- funkcionalne tehničke komponente za capture, screenshot, diff, AI pomoć, alert i izvršni PDF;
- profesionalni INMAR report s dokazima i jasno navedenim izdavateljem;
- potvrđeno tržište jeftinih web-change alata, specijaliziranih price-monitoring alata i skupih enterprise CI platformi;
- jasan prostor za testiranje productized usluge između DIY alata i enterprise projekta;
- model isporuke koji agent može većinski operativno voditi uz Kristijanovu komercijalnu i završnu kontrolu.

### NEMAM

- niti jednog nepovezanog kupca koji je platio PulseWatch;
- potvrđenu willingness-to-pay cijenu od 1.490 EUR/mj.;
- izmjerene sate, false-positive stopu, source-failure stopu i doprinosnu maržu po stvarnom klijentu;
- dokaz da je odabrana niša dovoljno bolna i hitna;
- pravo zvati proizvod samouslužnim SaaS-om;
- porezno potvrđen izračun koliko INMAR mora prihodovati da bi Kristijanu ostalo 3.500 EUR osobnog novca.

## 1. Što konkurencija stvarno prodaje

### 1.1 Jeftini web-change i scraping alati

Ovaj sloj prodaje automatizirano otkrivanje promjene, screenshot, povijest i obavijest. To je komoditizirani sloj i PulseWatch ne može opravdati cijenu od 1.490 EUR samo boljim alertom.

| Konkurent | Javna cijena, provjereno 2026-08-17 | Što nudi | Što kupac i dalje mora raditi |
|---|---:|---|---|
| Visualping | Free; Personal od 14 USD/mj.; Business od 140 USD/mj.; Solutions na upit.[1][22] | Vizualne/tekstualne promjene, AI, timovi, integracije i alerti. | Odabrati prave stranice, razlikovati buku od signala i odlučiti što napraviti. |
| Distill | Free; plaćeni planovi od 15 USD/mj.[2] | Praćenje stranica i lokalni/cloud monitori s obavijestima. | Konfiguracija, održavanje monitora i poslovna interpretacija. |
| ChangeTower | Lite od 12 USD/mj.; viši planovi i enterprise postoje.[16] | Change monitoring, arhiva, uvjeti, alerti i enterprise mogućnosti. | Pretvoriti promjenu u prioritet i odgovornu akciju. |
| Wachete | Free i niski usage planovi; službena stranica prikazuje mjesečne/godišnje pretplate bez limita ukupnih provjera.[9] | Promjene, cijene, dostupnost, compliance arhiva, e-mail/mobile/chat alerti. | Kontrola usporedivosti, lažnih alarma i posljedica za posao. |
| Hexowatch | Planovi postoje; pouzdan aktualni iznos nije potvrđen iz dostupne službene HTML stranice.[8] | Vizualni, sadržajni, cjenovni, source-code, technology i WHOIS monitoring. | Analitičku provjeru i upravljanje odlukama. |
| Browse AI | Free; Personal 19 USD/mj.; Professional od 69 USD/mj.; premium managed extraction od 500 USD/mj. prema službenoj pricing stranici.[30] | No-code scraping/monitoring, AI change detection, web-to-API i integracije; skuplji sloj uključuje upravljanu ekstrakciju. | Specifičnu tržišnu interpretaciju i executive decision workflow. |
| changedetection.io | Open-source/self-hosted i hosted opcija.[34] | Promjene, restock/price alerti i prilagodljivi filteri. | Hosting ili konfiguraciju, QA i sve poslovne odluke. |
| PageCrawl | Javno pozicioniran za competitor monitoring, AI sažetke, importance scoring i team alerts.[17] | Cijene, proizvodi, sadržaj, AI sažeci i digest. | Human QA, owner/action i praćenje rezultata odluke. |
| Competely | Transparentni self-serve planovi od 39 USD/mj.; periodički competitor briefs.[18] | Strukturirana AI analiza konkurenata i kontinuirano praćenje. | Dokaznu disciplinu, prilagodbu stvarnom operativnom procesu i odgovornost za akciju. |
| Versionista | Službene stranice potvrđuju monitoring i OSINT use case; aktualna javna cijena nije potvrđena.[10] | Change tracking, alerti i roll-up sažeci. | Analitički i akcijski sloj. |

**Zaključak:** tehnički monitoring može se kupiti za desetke ili niske stotine eura mjesečno. PulseWatch zato ne smije prodavati broj provjera, screenshotove ili “AI sažetke” kao glavnu vrijednost.

### 1.2 Specijalizirani price/catalog monitoring

| Konkurent | Javna cijena | Fokus | Implikacija za PulseWatch |
|---|---:|---|---|
| Prisync | Professional 99 USD/mj. do 100 proizvoda; Premium 199 USD/mj. do 1.000; Platinum 399 USD/mj. do 5.000.[6][19][20] | Competitor price/stock tracking i dynamic pricing. | Ako kupac želi samo masovno praćenje cijena, Prisync je bolji i jeftiniji izbor. |
| Price2Spy | Starter/Basic/Premium slojevi; aktualni iznos treba uzeti sa službenog konfiguratora ili sales upita.[7][21] | Price monitoring, comparison, repricing i dodatni moduli. | Ne natjecati se u čistom repricingu bez boljeg product matchinga i integracije. |
| Minderest | Cijena na upit.[14] | Enterprise price, promotion, catalogue i marketplace intelligence. | PulseWatch može ciljati manji mid-market kojem je enterprise projekt prevelik. |
| NetRivals / Lengow | Cijena na upit.[15] | Retail price intelligence i actionable insights. | Isto: ne obećavati enterprise skalu, nego brzu i ograničenu upravljanu funkciju. |

### 1.3 Enterprise competitive/market intelligence platforme

Crayon i Kompyte javno pozicioniraju platforme za centraliziranje, kuriranje i distribuciju competitive intelligencea, ali ne objavljuju standardni javni iznos.[3][4]

Comintelli, Contify i Northern Light također koriste modularni ili prilagođeni prodajni model.[5][11][12]

Valona javno opisuje value-driven/custom pricing i širi market-intelligence program.[13][24]

| Konkurent | Javni model cijene | Ključna ponuda | Zašto nije isti kupac kao prvi PulseWatch kupac |
|---|---|---|---|
| Crayon | Prilagođena cijena / pricing inquiry.[4] | Širok CI program, neograničeni intelligence asseti i stakeholder access. | Tipično zahtijeva zreliji CI program i veći budžet. |
| Kompyte | Cijena ovisi o konkurentima, licencama, SSO-u i permissionima; godišnji planovi.[3] | Automatizirani CI, battlecards i sales enablement. | Primarno GTM/sales enablement platforma. |
| Comintelli Intelligence2day | Modularna/scalable cijena na upit.[5] | Enterprise intelligence portal i knowledge workflow. | Složeniji deployment i organizacijska adopcija. |
| Contify | Cijena na upit.[11][26] | Platforma plus analyst hours, custom reporti, dashboardi i battlecards. | Širi enterprise program; PulseWatch mora pobijediti brzinom i jasnim ograničenim outcomeom. |
| Northern Light SinglePoint | Prilagođena cijena.[12] | Centralizirani OS za market research i enterprise CI. | Namijenjeno velikim organizacijama i licenciranom internom sadržaju. |
| Valona | Value-driven/custom pricing.[24] | Globalni market/competitive intelligence, izvori i analitičari. | Širi i skuplji program nego uska operativna watchlista. |

### 1.4 Managed analyst/consulting usluge

U ovom sloju konkurenti ne prodaju samo software. Contify nudi managed services i analyst support, a Valona analitičare i market research.[25][26]

Evalueserve, Proactive Worldwide i Aqute nude prilagođeni competitive-intelligence rad.[27][28][29] Javne standardne cijene uglavnom **nisu objavljene**.

| Ponuđač | Ljudski sloj | Cijena | PulseWatch diferencijacija koju moramo dokazati |
|---|---|---|---|
| Contify | Bundled analyst hours, secondary research, custom reports, dashboardi i battlecards.[26] | Contact sales | Transparentan ograničeni paket za mid-market, brži onboarding i dokaz svake tvrdnje. |
| Valona | Analitičari rade uz platformu i izvore.[25] | Contact sales | Uža watchlista i neposrednija operativna akcija umjesto širokog MI programa. |
| Evalueserve | Competitive intelligence research i kontinuirani programi.[27] | Contact sales | Manji opseg, niži commitment i direktan rad s direktorom. |
| Proactive Worldwide | Continuous competitor monitoring/tracking i strateška analiza.[28] | Contact sales | Productized, transparentna isporuka i mjesečna cijena za srednje tvrtke. |
| Aqute | Prilagođeno competitor research i kontinuirano praćenje.[29] | Contact sales | Više automatiziran dokazni trag i strogo definiran scope. |
| InfoDesk | Managed/professional intelligence usluge uz platformu.[31] | Contact sales | Brži pilot bez enterprise implementacije. |
| J.S. Held | Competitive intelligence i advisory angažmani.[32] | Contact sales | Ne natjecati se u dubokom investigativnom radu; ostati na javnim i odobrenim izvorima. |
| M-Brain / market research ponuda | Prilagođeni market-research rad i analitička isporuka.[33] | Contact sales | PulseWatch mora ostati uži, operativniji i transparentno paketiran. |
| Researchly Competitive Brief | DACH pozicioniranje kontinuiranog AI competitor monitoringa i briefa.[23] | Javni standardni iznos nije potvrđen | Ovo je blizak DACH benchmark; PulseWatch mora dodati dokaz, human QA, owner/action i mjerljiv poslovni ishod. |

## 2. Zašto bi netko uzeo baš PulseWatch?

### Iskren odgovor

Nitko nas **ne mora** uzeti. Kupac će nas uzeti samo ako u plaćenom pilotu pokažemo da:

1. otkrivamo relevantnu promjenu prije njegova postojećeg procesa;
2. dokaz je dovoljno precizan da ga zaposlenik može odmah koristiti;
3. signal vodi konkretnoj odluci ili zaštitnoj akciji;
4. vrijednost te akcije je veća od mjesečne cijene;
5. kupac troši manje vlastitog vremena nego s DIY alatom.

### Pozicijska rečenica

> **PulseWatch je vanjski market-watch desk za regionalne brendove, distributere i specijalizirane trgovce: otkrivamo važne javne tržišne promjene, provjeravamo dokaz i pretvaramo ih u vlasnika, rok i sljedeću akciju.**

### Naša pozicija između dvije krajnosti

| Jeftini alat | PulseWatch | Enterprise CI |
|---|---|---|
| Daje diff i alert | Daje provjeren signal, dokaz, značenje, akciju i praćenje | Daje široku platformu, integracije i enterprise program |
| Kupac sve konfigurira | INMAR postavlja i održava watchlistu | Implementacija i više stakeholdera |
| 5–400 EUR/USD mjesečno | 690–2.490 EUR mjesečno | Uglavnom contact-sales / godišnji ugovori |
| Nema odgovornog analitičara | Imenovana odgovorna osoba: Kristijan Fažon | Tim analitičara / customer success |
| Alert noise ostaje kupcu | Human QA prije isporuke | Šira kuracija i governance |
| Ne prati poslovni ishod | Signal → owner → rok → status → rezultat | Programski KPI i organizacijski workflow |

### Pet diferencijatora koje report i prodaja moraju pokazati

1. **Dokaz prije AI teksta** — screenshot/HTML/PDF, vrijeme, URL i before/after; LLM nije izvor činjenice.
2. **Human-reviewed, ne raw alert** — kupac ne plaća da bi pregledavao našu buku.
3. **Akcija ima vlasnika i rok** — svaki važan signal završava s “tko radi što i do kada”.
4. **Transparentan productized scope** — nema višemjesečne enterprise nabave ni nejasnog consulting računa.
5. **Direktna odgovornost direktora INMAR-a** — u ranoj fazi Kristijan osobno kontrolira finalne kritične signale i odnos s kupcem.

## 3. Točan početni kupac i problem

### Idealni prvi profil kupca

- regionalni vlasnik brenda, ekskluzivni distributer ili specijalizirani trgovac;
- 20–500 zaposlenih ili dovoljno velik promet da 1.490 EUR/mj. nije eksperiment bez vlasnika;
- 5+ važnih konkurenata, marketplace sellera ili ovlaštenih prodavača;
- javne cijene, promocije, asortiman, availability ili komercijalne poruke mijenjaju se barem tjedno;
- danas se praćenje radi ručno, stihijski ili nitko nije jasno odgovoran;
- postoji komercijalni direktor/category manager/e-commerce direktor koji može djelovati;
- jedna propuštena promjena može vrijediti više od 1.500 EUR kroz maržu, izgubljenu prodaju, pogrešnu kampanju ili zakašnjelu reakciju.

### Ne uzimati kao prvi projekt

- kupca koji želi “sve konkurente i cijeli internet”;
- kupca bez osobe koja će donositi odluke;
- kupca koji treba samo 10 price alertova — neka koristi jeftini alat;
- duboke sigurnosne, pravne ili forenzičke zaključke;
- privatne izvore bez jasne autorizacije;
- use case bez načina da se izmjeri akcija ili izbjegnuti gubitak/prilika.

## 4. Razrađeni paketi

### 4.1 PulseWatch Paid Pilot — 1.500 EUR + PDV jednokratno

| Element | Uključeno |
|---|---|
| Trajanje | 30 dana, plaćeno unaprijed |
| Scope | Jedna poslovna odluka/watchlista; klijent + do 5 konkurenata/sellera; do 30 javnih URL-ova |
| Baseline | Početno stanje, prioriteti, dostupnost izvora i dokazni paket |
| Isporuka | Do 2 tjedna reviewed briefa, hitan alert samo za dogovoreni prag i završni executive report |
| Sastanci | Kickoff 60 min + završna decision sesija 60 min |
| Metrike | Capture success, source failures, raw changes, accepted signals, false positives, analyst minutes, akcije kupca |
| PASS | Najmanje jedan signal korišten za dokumentiranu odluku/akciju i kupac prihvaća cijenu nastavka |
| STOP | Nema vrijedne odluke, nema akcijskog vlasnika, izvori ne daju dokaz ili kupac želi samo jeftini dashboard |

Pilot nije besplatan demo. Besplatno se može pokazati samo **jedan bounded sample signal iz javnih podataka**, bez mjesec dana rada.

### 4.2 PulseWatch Managed — 1.490 EUR + PDV/mj.

**Glavni proizvod; minimalno 3 mjeseca nakon pilota.**

| Element | Uključeno |
|---|---|
| Watchlista | Jedna poslovna watchlista; klijent + do 5 konkurenata/sellera |
| Izvori | Do 50 odobrenih javnih URL-ova; daily check gdje izvor dopušta |
| Teme | Do 3 dogovorene teme, npr. cijene/promocije, asortiman/dostupnost, messaging/kampanje |
| Reviewed signali | Do 12 važnih provjerenih signala mjesečno; višak se grupira u digest ili aktivira scope review |
| Hitni alert | Unutar radnog dana za unaprijed definirani high-severity prag; nije 24/7 SOC SLA |
| Tjedno | Kratki digest: što se promijenilo, dokaz, zašto je bitno, preporučena akcija |
| Mjesečno | Executive PDF + akcijski status + 45-min decision meeting |
| Dokaz | URL, vrijeme, before/after, screenshot/artefakt i confidence/ograničenja |
| Upravljanje | Signal owner, rok, stanje: new/reviewed/sent/actioned/closed/false positive |
| Podrška | Jedan imenovani kontakt kupca; do 2 kratka ad-hoc pitanja mjesečno |
| Nije uključeno | ERP/CRM integracije, exact local stock bez dokaza, pravna/forenzička tvrdnja, masovni SKU repricing, novi izvorni tipovi bez re-scopea |

**Cilj vremena:** nakon stabilizacije najviše 4,5–5 sati ljudskog rada po klijentu/mj. Ako dva ciklusa prelaze 6 sati, podiže se cijena, smanjuje scope ili automatizira konkretno usko grlo.

### 4.3 PulseWatch Lite — 690 EUR + PDV/mj.

**Nije jeftinija verzija Manageda s istim očekivanjima. To je strogo asinkron watchlist proizvod.**

| Element | Uključeno |
|---|---|
| Dostupnost | Tek nakon plaćenog pilota ili za potpuno standardizirani use case |
| Watchlista | Jedna tema; do 3 konkurenata/sellera |
| Izvori | Do 20 javnih URL-ova; 2–3 provjere tjedno, ne daily po defaultu |
| Reviewed signali | Do 5 provjerenih signala mjesečno |
| Isporuka | Mjesečni decision memo/PDF; hitni alert nije uključen |
| Sastanci | Nema redovnog sastanka; kvartalni 30-min review samo uz obnovu ili kao add-on |
| Custom research | Nije uključeno |
| Podrška | Jedan asinkron scope upit mjesečno |
| Upgrade trigger | Potreba za hitnim alertima, više od 3 konkurenata, više od 5 signala, action tracking ili sastanak znači Managed |

**Cilj vremena:** najviše 1,5–2 sata ljudskog rada po klijentu/mj. Lite se ne smije prodavati prije nego pipeline automatski složi dokaz i draft reporta.

### 4.4 PulseWatch Managed Plus — 2.490 EUR + PDV/mj.

Za kupca koji ima dvije odvojene watchliste ili veći prihod pod rizikom:

- do 10 konkurenata/sellera i 100 URL-ova;
- do 2 watchliste i 25 reviewed signala/mj.;
- prioritetni radni-dan alert;
- tjedni decision desk call od 30 min;
- mjesečni executive report i kvartalni trend review;
- do 2 imenovana stakeholdera i ograničena prilagodba izvještaja.

## 5. Financijski cilj: koliko treba poslovanju

### Zašto 3.500 EUR MRR nije dovoljno

3.500 EUR osobnog novca nije isto što i prihod INMAR-a. Poslovanje mora pokriti:

- ukupni trošak Kristijanove isplate/plaće ili drugi zakoniti oblik isplate;
- delivery vrijeme i eventualnu pomoć;
- servere, AI, storage, backup i alate;
- prodaju i akviziciju;
- računovodstvo, banku, pravne dokumente, loša potraživanja i churn;
- poreze prema stvarnoj strukturi INMAR-a.

Ovaj dokument nije porezni savjet. Računovođa mora potvrditi koliki je **ukupni trošak društva** da Kristijanu mjesečno ostane 3.500 EUR.

### Planski raspon

Pretpostavke: 70% doprinosna marža nakon direktne isporuke, 15% prihoda ostaje kao prodajna/churn rezerva i 500 EUR fiksnih troškova mjesečno.

| Ukupni mjesečni trošak željene Kristijanove isplate | Potreban MRR bez PDV-a |
|---:|---:|
| 4.500 EUR | 8.403 EUR |
| 5.000 EUR | 9.244 EUR |
| 5.500 EUR | 10.084 EUR |
| 6.000 EUR | 10.924 EUR |

**Operativni cilj dok računovođa ne potvrdi broj: 9.500–10.500 EUR MRR.**

### Scenariji paketa

| Miks | MRR | Planski direktni trošak | 15% rezerva | Fiksno | Ostaje prije stvarnog owner/tax obračuna |
|---|---:|---:|---:|---:|---:|
| 6 × Managed | 8.940 | 2.100 | 1.341 | 500 | 4.999 |
| 5 × Managed + 3 × Lite | 9.520 | 2.170 | 1.428 | 500 | 5.422 |
| 4 × Managed + 2 × Managed Plus | 10.940 | 2.400 | 1.641 | 500 | 6.399 |
| 7 × Managed | 10.430 | 2.450 | 1.565 | 500 | 5.916 |

Directni troškovi u tablici su planske pretpostavke (Managed 350 EUR, Lite 140 EUR, Plus 500 EUR po klijentu/mj.), ne izmjereni troškovi.

### Realan vremenski put

- **0–30 dana:** cilj je 1 plaćeni pilot, ne osobna isplata 3.500 EUR.
- **31–60 dana:** 2–3 ukupno plaćena pilota i prva konverzija na recurring.
- **61–90 dana:** cilj 3 Managed ekvivalenta, približno 4.470 EUR MRR.
- **4.–6. mjesec:** cilj 6 Managed ekvivalenata, približno 8.940 EUR MRR; zatim povećanje do potvrđenog 9.500–10.500 EUR.

Do 3.500 EUR osobnog novca “kroz par mjeseci” je **moguće, ali nije dokazano**. Ovisi o zatvaranju 6–7 flagship klijenata i stvarnom trošku isplate. Ne treba planirati životne troškove na jednokratnim pilotima.

## 6. Uloge i odgovornost

### 6.1 Kristijan Fažon — direktor, prodaja i završna odgovornost

| Kristijan je vlasnik | Konkretna obveza |
|---|---|
| Izbor tržišta | Odobrava jednu nišu i odbija scope creep. |
| Prodaja | Vodi discovery, komercijalni razgovor, cijenu i zatvaranje pilota. |
| Ugovor i novac | INMAR potpisuje ugovor, izdaje račun, upravlja naplatom i odobrava trošak. |
| Odnos s klijentom | Imenovani executive kontakt i voditelj mjesečne decision sesije. |
| Kritični signali | U prva 3 mjeseca odobrava svaki high-severity alert i finalni executive zaključak. |
| Kvaliteta | Donosi konačnu odluku kada je signal osjetljiv, dvosmislen ili reputacijski rizičan. |
| Product odluke | Odobrava što se automatizira tek nakon izmjerenog ponavljanja. |
| Dokaz vrijednosti | Na svakom reviewu pita: “Koju je odluku ovo promijenilo i koliko približno vrijedi?” |

**Tjedni Kristijanov ritam u prva 3 mjeseca:**

- 8–12 sati prodaja i razgovori;
- 3–5 sati finalni QA i klijenti;
- 2 sata pricing/pipeline review;
- 1 sat product prioritizacija;
- bez ručnog svakodnevnog skeniranja stranica osim QA iznimki.

### 6.2 Hermes/PulseWatch agent — istraživanje, operacije i priprema odluke

| Agent samostalno vodi | Granica |
|---|---|
| Prikupljanje javnih ili izričito odobrenih izvora | Ne koristi privatne podatke ili credentials bez autorizacije. |
| Capture, screenshot, hash, diff i source-health provjeru | Ne izmišlja činjenicu kada je izvor nedostupan. |
| Deduplikaciju, klasifikaciju i preliminarni severity/confidence | High-severity prije klijenta odobrava Kristijan dok ne postoji provjeren SOP. |
| Evidencijski paket i citate | AI tekst se jasno odvaja od dokaza. |
| Draft tjednog digesta, mjesečnog reporta i akcijskog statusa | Finalni strateški zaključak u ranoj fazi potpisuje Kristijan. |
| Interni QA: missing evidence, stale source, clipping, broken URL, kontradikcije | Ne daje pravnu, sigurnosnu ili forenzičku garanciju. |
| CRM research, account scoring i personalizirani draft outreach poruke | Ne šalje masovne poruke; vanjska komunikacija ide kroz odobreni račun i zakoniti kanal. |
| Repo, testove, metrike, runbook i incident popravke | Produkcijske promjene se verificiraju i ostavljaju audit trag. |

### 6.3 Klijent

Klijent mora imenovati:

- jednog decision ownera;
- jednog operativnog korisnika signala;
- mjeru vrijednosti (marža, prihod, vrijeme reakcije, compliance/protective action);
- pravila što je hitno;
- potvrdu je li akcija provedena i kakav je bio ishod.

Bez klijentova ownera PulseWatch postaje newsletter i vjerojatno churn-a.

### 6.4 Buduća pomoć

Angažirati part-time research/delivery operatora tek kada se dogodi jedno od sljedećeg:

- 3 uzastopna mjeseca iznad 8.000 EUR MRR;
- više od 60 sati mjesečno ljudskog deliveryja;
- prodajni pipeline pada jer Kristijan radi operativu;
- dva report ciklusa zaredom kasne.

Za DACH prodaju angažirati native-language QA/partnera prije slanja osjetljivih prodajnih i executive materijala ako Kristijan ne može sam potvrditi poslovni njemački.

## 7. Kako sustav treba raditi od prodaje do obnove

### Korak 1 — account selection

Agent priprema listu ciljnih tvrtki samo iz odabrane niše i boduje ih prema broju relevantnih sellera/konkurenata, učestalosti javnih promjena, vidljivom decision owneru i mogućoj vrijednosti reakcije. Kristijan odobrava prvih 30.

### Korak 2 — bounded sample

Za svaki visokoprioritetni prospect agent izrađuje najviše jedan javni sample signal:

- činjenica i screenshot;
- kada je uočeno;
- zašto bi moglo biti bitno;
- što se ne može zaključiti;
- jedno discovery pitanje.

Ne izrađuje se besplatni kompletni report.

### Korak 3 — discovery i paid pilot

Kristijan vodi 30-min razgovor i mora dobiti odgovore:

1. Koju promjenu danas često saznate prekasno?
2. Tko zbog nje mijenja cijenu, kampanju, prodaju ili nabavu?
3. Koliko često se događa?
4. Kolika je vrijednost jedne bolje/brže odluke?
5. Koje izvore smijemo pratiti?
6. Što bi 30-dnevni pilot morao dokazati da biste nastavili za 1.490 EUR/mj.?

Pilot se pokreće tek nakon uplate i potpisanog scopea.

### Korak 4 — onboarding

- zamrznuti watchlistu, URL-ove, teme i hitne pragove;
- zabilježiti baseline, capture frequency i ograničenja;
- odvojiti tenant/workspace i retention;
- potvrditi decision ownera i delivery kanal;
- testirati jedan capture → signal → review → delivery ciklus.

### Korak 5 — dnevna operativa

1. scheduler pokreće capture;
2. source-health provjera odvaja kvar od poslovne promjene;
3. deterministic rules i diff stvaraju raw event;
4. agent deduplicira i priprema evidence packet;
5. agent klasificira činjenicu/interpretaciju/hipotezu;
6. review queue prihvaća, odbija ili vraća signal;
7. samo reviewed signal ide kupcu;
8. svaka akcija dobiva ownera, rok i status.

### Korak 6 — delivery ritam

- **odmah/radni dan:** samo unaprijed definiran high-severity alert;
- **tjedno:** reviewed digest, ili “nema važne promjene” bez buke;
- **mjesečno:** executive PDF, trendovi, akcijski status i decision session;
- report datumi se raspoređuju po četiri tjedne kohorte da se sustav ne zaguši.

### Korak 7 — mjerenje

Po klijentu se automatski bilježi:

- capture runs i failures;
- storage i AI usage;
- raw events, duplicates i reviewed signals;
- false positives i rejections;
- analyst/QA/report/meeting minute;
- broj poslanih signala;
- broj actioned/closed signala;
- procijenjena ili potvrđena vrijednost akcije;
- MRR, naplata, renewal datum i razlog churn-a.

### Korak 8 — renewal

30 dana prije isteka Kristijan daje value recap, ne feature prezentaciju:

- što je otkriveno;
- što je kupac poduzeo;
- što je izbjegnuto ili ostvareno;
- gdje je bilo buke;
- što ostaje ista watchlista;
- što je novi plaćeni scope.

## 8. 90-dnevni plan do stvarnog biznisa

### Tjedni 1–2: zaključavanje ponude i niše

- odabrati samo jednu beachhead nišu;
- potvrditi računovođi ukupni trošak 3.500 EUR osobne isplate;
- završiti one-page ponudu, pilot scope, ugovor/DPA/retention minimum i sample;
- napraviti 50 account universe i odabrati 30 najjačih;
- tehnički implementirati signal schema, evidence links, dedupe i time tracking prije novih dashboard featurea.

**Gate:** 30 imenovanih accounta s decision ownerom i barem jednom hipotezom vrijedne promjene.

### Tjedni 3–4: prodajni test

- 30 personaliziranih kontakata kroz zakonit i provjeren kanal;
- cilj 5 smislenih pozitivnih odgovora;
- najmanje 2 discovery razgovora;
- najmanje 1 plaćeni pilot od 1.500 EUR unaprijed.

**STOP:** nema uplate nakon 30 preciznih kontakata i najmanje 10 stvarnih razgovora; ne graditi dalje dashboard nego promijeniti buyer/problem/ponudu.

### Tjedni 5–8: isporuka i ponovljivost

- isporučiti prvi pilot end-to-end;
- mjeriti svaki ljudski minut i svaki false positive;
- paralelno prodati još 1–2 pilota;
- automatizirati samo usko grlo koje se ponovilo najmanje 3 puta;
- tražiti dopuštenje za anonimni ili imenovani case study samo nakon stvarne akcije.

**Gate:** barem jedan actioned signal, evidence completeness 100%, capture success cilj ≥98% za podržane izvore, false-positive stopa prihvatljiva kupcu i delivery unutar scope vremena.

### Tjedni 9–12: konverzija i MRR

- pretvoriti najmanje 2 od 3 uspješna pilota u tromjesečni Managed;
- imati ukupno 3 Managed ekvivalenta u pipelineu/ugovoru;
- staggerati report datume;
- završiti renewal/value recap template;
- odlučiti koja jedna komponenta ide prema portal/SaaS iskustvu.

**90-dnevni PASS:** najmanje 3 plaćena pilota, najmanje 2 recurring konverzije, najmanje 3 actioned signala ukupno i doprinosna marža po klijentu ≥65% uz ≤6 ljudskih sati/Managed/mj.

### Mjeseci 4–6: do održivog prihoda

- cilj 6 Managed ekvivalenata i 8.940+ EUR MRR;
- zadržati najmanje 80% pilot → recurring samo za uspješne/fit pilote;
- angažirati operativnu pomoć prema gateu, ne unaprijed;
- u DACH ući s jednim jezično i industrijski kompetentnim partnerom ili native QA;
- SaaS onboarding, billing i tenant UI graditi tek nakon najmanje 3 nepovezana recurring kupca i 2 obnove istog workflowa.

## 9. Prodajna poruka

### Ne govoriti

- “AI prati sve vaše konkurente.”
- “Naš dashboard daje sve uvide.”
- “Garantiramo da ništa nećete propustiti.”
- “Jeftiniji smo od Visualpinga/Prisynca.”

### Govoriti

> Vaš tim može kupiti page-monitoring alat za nekoliko desetaka eura. Problem je što tada vaš tim još mora odabrati izvore, očistiti lažne promjene, dokazati što se dogodilo i odlučiti tko reagira. PulseWatch preuzima taj operativni sloj. U 30-dnevnom plaćenom pilotu pratimo jednu jasno definiranu komercijalnu odluku i dokazujemo vodi li barem jedan signal stvarnoj akciji. Ako ne vodi, ne preporučujemo nastavak.

## 10. Najveći rizik i najbolja alternativa

**Fatalni rizik:** gradimo lijep report za informaciju koju kupac ne koristi. Tada smo skupi newsletter i churn je neizbježan.

**Najbolja obrana:** svaki projekt počinje jednom učestalom odlukom, imenovanim ownerom i ekonomskom vrijednošću. Svaki report prikazuje signal → dokaz → akciju → ishod.

**Najbolja alternativa ako generic competitor monitoring ne prođe:** zadržati isti evidence/action engine, ali suziti se na compliance/MAP/promotion watch za regionalne vlasnike brendova i ekskluzivne distributere, gdje je dokaz promjene direktno upotrebljiv komercijalnom timu.

## 11. Sljedeće konkretne akcije

1. Računovođa: dati ukupni mjesečni trošak društva za cilj od 3.500 EUR osobnog novca.
2. Kristijan: odabrati jednu početnu nišu između regionalnog vlasnika brenda, ekskluzivnog distributera i specijaliziranog trgovca.
3. Agent: pripremiti 50-account universe i 30 prioriteta iz izabrane niše.
4. Agent: dovršiti signal/evidence/dedupe/time-metering operativnu jezgru.
5. Kristijan + agent: izraditi 3 bounded sample signala i prodajni one-pager.
6. Kristijan: voditi discovery i zatvoriti prvi pilot; agent priprema sve istraživanje, materijal i follow-up draft.
7. Ne graditi dodatni SaaS UI dok barem jedan nepovezani kupac ne plati i ne upotrijebi signal.

## Sources

[1] https://visualping.io/pricing
[2] https://distill.io/pricing
[3] https://www.kompyte.com/plans
[4] https://www.crayon.co/pricing-inquiry
[5] https://comintelli.com/platform-pricing
[6] https://prisync.com/pricing
[7] https://www.price2spy.com/pricing
[8] https://hexowatch.com
[9] https://www.wachete.com
[10] https://versionista.com/pricing
[11] https://www.contify.com/platform
[12] https://www.northernlight.com/singlepoint-platform
[13] https://valonaintelligence.com
[14] https://www.minderest.com
[15] https://www.lengow.com/solutions/netrivals
[16] https://changetower.com/pricing
[17] https://pagecrawl.io/use-cases/competitive-intelligence
[18] https://competely.ai/pricing
[19] https://prisync.com/price-tracking-software
[20] https://prisync.com/compare-plans
[21] https://www.price2spy.com/pricing.html
[22] https://visualping.io/blog/visualping-pricing-explained
[23] https://competitive-intelligence.researchly.at
[24] https://valonaintelligence.com/market-intelligence-software/pricing
[25] https://valonaintelligence.com/services/analyst-services
[26] https://www.contify.com
[27] https://www.evalueserve.com/competitive-intelligence
[28] https://www.proactiveworldwide.com/competitive-intelligence-services/competitive-monitoring-and-tracking-programs
[29] https://www.aqute.com/competitive-intelligence-services
[30] https://www.browse.ai/pricing
[31] https://www.infodesk.com/intelligence-activation/managed-professional-services
[32] https://www.jsheld.com/areas-of-expertise/competitive-intelligence
[33] https://www.m-brain.com/market-research
[34] https://changedetection.io
