# Raporti i studentit: UrbanBike AI

Studenti: Fabian Haxhiaj
Grupi (nëse punohet në grup):
Roli në aktivitet: punë individuale; përgatita mjedisin, vendosa kodin nga slajdet me ndihmën e Claude Code, kontrollova rezultatet me numrat e slajdeve dhe rishikova raportin.
Data: 2026-11-11
GitHub-i im: https://github.com/FabianHaxhiaj22/urbanbike-ai-fabian-haxhiaj
Figma: https://www.figma.com/design/zKrSuz05QZnVkusGThjnCS

## Qëllimi

Problemi që zgjidhim: Sa qira biçikletash priten për ditën pasuese në Washington, D.C.?
Target-i y: `rentals` (numri total i qirave në ditë, kolona `cnt` e UCI).
Predictorët X: `rentals_lag1`, `rentals_lag7`, `rentals_mean7`, `temp_c_lag7`, `rain_mm_lag7`, `wind_ms_lag7`, `trend_days` (numerikë) dhe `weekday`, `month`, `workingday`, `holiday` (kategorikë).
Koha kur parashikojmë dhe çfarë informacioni është i njohur: parashikojmë një ditë përpara. Supozohen të njohura qiratë deri dje (lag1, lag7, mesatarja e 7 ditëve të kaluara), kalendari i ditës që parashikohet dhe moti NASA me vonesë 7-ditore (t−7). Moti i së njëjtës ditë nuk përdoret.

## Pastrimi

Burimet reale dhe çelësi i bashkimit: UCI Bike Sharing `day.csv` (731 ditë, 2011–2012) dhe NASA POWER `nasa_weather.csv` (731 ditë, °C, mm/ditë, m/s). Bashkimi bëhet sipas `date` (`dteday` → `date`) me `validate="one_to_one"`; rezultati ka 731 rreshta.
Dallimi mes origjinaleve dhe kopjes didaktike: origjinalet te `data/raw/` nuk ndryshohen. Kodi krijon veçmas `data/teaching/dirty.csv` (seed 42) me probleme të injektuara qëllimisht: 18 temperatura bosh, 12 reshje bosh, 6 temperatura me tekstin "gabim" dhe 12 rreshta të dubluar.
Rreshtat para/pas: origjinali UCI 731 rreshta, 0 mungesa → kopja didaktike 743 rreshta → pas heqjes së dublimeve 731 rreshta → pas lag-eve (hiqen 7 ditët e para pa histori) 724 rreshta.
Dublimet: 12 dublime identike u hoqën me `drop_duplicates()`; pas kësaj çdo datë është unike dhe ditët vijnë pa boshllëqe (diferenca 1 ditë).
Mungesat para/pas konvertimit: para konvertimit 30 qeliza bosh (18 `temp_c` + 12 `rain_mm`), dhe `temp_c` ishte `object` për shkak të tekstit "gabim". Pas `pd.to_numeric(errors="coerce")` 6 tekstet bëhen NaN, pra mbeten 36 mungesa meteorologjike. `date` kalon nga `object` në `datetime64[ns]`, `temp_c` nga `object` në `float64`. Mungesat nuk trajtohen si 0 °C.
Arsyeja e imputimit vetëm me train: mungesat plotësohen me medianën brenda `Pipeline` (`SimpleImputer`, me `add_indicator=True`), e cila mësohet vetëm nga train. Nëse mediana do të llogaritej nga i gjithë dataseti, informacion nga validation dhe test (e ardhmja) do të rridhte te modeli dhe rezultatet do të dukeshin më të mira se në realitet.

## Grafikët

Vëzhgimi 1 dhe figura përkatëse: `reports/figures/01_demand.png` — kërkesa ka prirje rritëse dhe sezonalitet: më pak qira në dimër, më shumë në verë, dhe në pranverën 2012 kërkesa është më e lartë se në 2011. Ka edhe rënie të mprehta në disa ditë, që mesatarja 7-ditore i zbut.
Vëzhgimi 2 dhe figura përkatëse: `reports/figures/03_weather.png` — ditët me temperaturë NASA t−7 më të lartë kanë zakonisht më shumë qira, por shpërndarja është e gjerë. Nga `02_workingday.png`: ditët e punës kanë mesatare pak më të lartë se fundjavat/festat, por ndryshimi është i vogël.
Pse një lidhje e dukshme nuk provon shkakësi: temperatura dhe qiratë ndryshojnë të dyja me stinën dhe me rritjen e përgjithshme të shërbimit në kohë. Lidhja mund të vijë nga këta faktorë të përbashkët (p.sh. ditë më të gjata, pushime, më shumë stacione), jo vetëm nga temperatura. Grafiku tregon bashkëndryshim, jo një eksperiment të kontrolluar.

## Vlerësimi

| Modeli | Validation MAE | Test MAE | Test RMSE | Test R² |
|---|---:|---:|---:|---:|
| Yesterday | 775.203 | 916.402 | 1330.386 | 0.539 |
| DummyMean | 2953.866 | 2494.628 | 2790.064 | -1.027 |
| Ridge | 687.558 | 893.251 | 1252.655 | 0.591 |
| RandomForest | 1821.528 | 1671.499 | 2042.654 | -0.087 |

Ndarjet kohore: train 2011-01-08 – 2012-04-30 (479), validation 2012-05-01 – 2012-08-31 (123), test 2012-09-01 – 2012-12-31 (122).

Modeli i zgjedhur nga validation dhe arsyeja: Ridge. Mes dy kandidatëve ML ka MAE më të ulët në validation (687.558 kundrejt 1821.528 të Random Forest), dhe e mund edhe baseline-in Yesterday (775.203). Zgjedhja bëhet vetëm sipas validation; testi nuk përdoret për zgjedhjen.
Rezultati i provës me Random Forest: Random Forest doli më keq se Ridge dhe madje më keq se baseline-i Yesterday, si në validation (MAE 1821.528) ashtu edhe në test (MAE 1671.499, R² -0.087). Arsyeja e mundshme: pemët nuk ekstrapolojnë jashtë vlerave të train. Kërkesa në 2012 u rrit përtej nivelit të train, ndërsa Ridge e kap prirjen me `trend_days`. Një model më kompleks nuk është automatikisht më i mirë.
Interpretimi i gabimit në qira për ditë: në test, Ridge gabon mesatarisht 893 qira në ditë (MAE). RMSE (1252.655) është më e lartë se MAE, që tregon disa ditë me gabime të mëdha (p.sh. ditë me mot të keq ose festa). Ridge e mund baseline-in Yesterday vetëm pak (893 kundrejt 916). Shembull nga aplikacioni: për 2012-09-01 parashikimi është 6834.73, vlera reale 6140, gabimi absolut 694.73.
Rezultati i klasifikimit, nëse u realizua: po. Pragu = mediana e train = 3907 qira; "e lartë" nëse rentals ≥ 3907. Në test ka 103 ditë të larta dhe 19 normale. DummyMostFrequent: accuracy 84.43%, balanced accuracy 50.00%, macro-F1 0.458 (nuk dallon asnjë ditë normale). LogisticRegression: accuracy 91.80%, balanced accuracy 77.98%, macro-F1 0.820. Matrica e konfuzionit `[[11, 8], [2, 101]]`: 8 ditë normale u parashikuan të larta, 2 të larta u parashikuan normale (`reports/figures/05_confusion.png`). Për shkak të klasave të pabalancuara, accuracy duhet lexuar bashkë me balanced accuracy dhe macro-F1.

## Kufizimet

1. Një qytet dhe periudhë historike: të dhënat janë vetëm për Washington, D.C., 2011–2012. Modeli nuk është testuar për qytete të tjera, vite të tjera ose për kërkesën e sotme.
2. NASA POWER përdor rrjet meteorologjik (reanalizë me rezolucion të ulët, për koordinatat 38.9072, −77.0369) dhe ditë sipas LST. Kjo nuk është matje e saktë e stacionit në çdo pikë të qytetit. Vonesa lag7 shmang përdorimin e motit të së njëjtës ditë, por nuk zgjidh çdo kufizim të reanalizës historike.
3. Parashikimi njëditor supozon se numrat e qirave të ditës së djeshme janë të njohura. Në një shërbim real këto mund të vijnë me vonesë ose të jenë të paplota. Aplikacioni është demonstrim historik vetëm për datat e testit, jo shërbim i drejtpërdrejtë.

## Kontributet individuale

| Studenti | Skedari/ekrani | Puna dhe vendimi | Commit/prova |
|---|---|---|---|
| Fabian Haxhiaj | `.venv`, `requirements.txt`, `.gitignore` | Përgatita Python 3.12 dhe bibliotekat në Linux (komandat Linux në vend të PowerShell). | `pip check` pa gabime |
| Fabian Haxhiaj | `config/common.py`, `01_clean.py`–`04_classify.py`, `app.py`, `run_all.py` | Kodin nga slajdet e vendosa me ndihmën e Claude Code. Kontrollova çdo rezultat me numrat e slajdeve (731/724 rreshta, ndarjet 479/123/122, MAE 893.251, pragu 3907). | `reports/`, commit-i i parë |
| Fabian Haxhiaj | `RAPORTI.md`, Figma | Rishikova interpretimin e grafikëve, zgjedhjen e Ridge nga validation dhe kufizimet; ndërtova konceptin e ndërfaqes në Figma. | commit-i "Shtoj lidhjen time GitHub" |

## Burimet

UCI: https://doi.org/10.24432/C5W894
NASA: https://power.larc.nasa.gov/docs/services/api/temporal/daily/
Provenienca lokale: data/raw/provenance.json
