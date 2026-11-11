# UrbanBike AI — paketa e nisjes për studentët

Punoni në **laptopin tuaj**, me **llogarinë tuaj Figma** dhe me **repozitorin
tuaj GitHub**. Ndiqni prezantimin `UrbanBike_AI_Studentet_Hap_Pas_Hapi.pptx`.

## Dy paketa me role të ndryshme

- **UrbanBike_AI_Student_Start.zip**: datasetet reale dhe modeli i raportit.
  Këtu nuk ka kod Python të përfunduar. Kjo është paketa me të cilën filloni.
- **UrbanBike_AI_Student_Zgjidhja.zip**: kodi i plotë dhe rezultatet e
  ekzekutuara. Shërben për krahasim dhe kontroll në fund të aktivitetit.

Nxirreni paketën Start me **Extract All**. Në VS Code përdorni
**File → Open Folder** dhe hapni dosjen e brendshme `urbanbike-ai-student`.
Mos i përzieni dy paketat në të njëjtën dosje gjatë ndërtimit të parë.

## Para laboratorit 120 minuta

Përgatitni VS Code, Python 3.12, Git dhe shtesat Microsoft Python,
Python Debugger e Pylance. Krijoni/verifikoni dhe provoni hyrjen në
llogaritë personale GitHub dhe Figma. Prezantimi i shpjegon instalimet.

Në Windows, Python Install Manager merret nga
https://www.python.org/downloads/windows/ . Pas instalimit:

```powershell
pymanager install 3.12
py -3.12 --version
```

Përgatitja e mjedisit dhe instalimi i bibliotekave bëhen pasi të krijoni
`requirements.txt` sipas pjesës përgatitore të slajdeve:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Në VS Code zgjidhni `.venv` përmes **Python: Select Interpreter**.
Komandat e mësipërme përdorin mjedisin drejtpërdrejt dhe nuk kërkojnë
`Activate.ps1` ose ndryshim të Execution Policy.

## Si kopjohen pjesët e kodit

Çdo slajd kodi shënon emrin e skedarit dhe **Pjesa 1 nga N**, **Pjesa 2 nga N**,
e kështu me radhë. Në PowerPoint përdorni pamjen **Normal**, hyni brenda
kutisë së kodit dhe kopjoni vetëm kodin. Mos kopjoni titullin e slajdit.

1. Krijoni skedarin bosh me emrin e saktë.
2. Vendosni pjesën e parë.
3. Shtoni çdo pjesë tjetër në fund, pa fshirë pjesën e mëparshme.
4. Ruani indentimin, rreshtat dhe thonjëzat.
5. Ruajeni skedarin dhe ekzekutojeni vetëm pasi të jenë vendosur të gjitha pjesët.

Një pjesë mund të përfundojë në mes të një funksioni ose shprehjeje.
Prandaj një skedar ende i papërfunduar mund të tregojë vija të kuqe.
Skedarët përfundimtarë janë të plotë dhe nuk përmbajnë shenja `...` që
studenti duhet t'i plotësojë vetë.

## Rendi i skedarëve

| Skedari | Roli |
|---|---|
| `.gitignore` | Përjashton mjedisin, modelet dhe cache nga Git |
| `requirements.txt` | Përcakton gjashtë bibliotekat dhe versionet |
| `config/common.py` | Dosjet, kolonat, ndarjet kohore dhe përpunimi |
| `01_clean.py` | Bashkimi, kopja didaktike, pastrimi dhe lag-et |
| `02_visualize.py` | Tre grafikë nga periudha train |
| `03_train.py` | Modelet e regresionit dhe vlerësimi |
| `04_classify.py` | Demonstrimi fakultativ i klasifikimit |
| `app.py` | Aplikacioni lokal me formular, rezultate dhe grafikë |
| `run_all.py` | Përsërit fazat e përfunduara 01–04 |

Pas plotësimit të skedarëve, komandat kryesore janë:

```powershell
.\.venv\Scripts\python.exe 01_clean.py
.\.venv\Scripts\python.exe 02_visualize.py
.\.venv\Scripts\python.exe 03_train.py
.\.venv\Scripts\python.exe 04_classify.py
.\.venv\Scripts\python.exe app.py
```

Hapni **http://127.0.0.1:8000**. Ndaleni serverin me **Ctrl+C**.
Pasi të keni provuar fazat veçmas, `run_all.py` i përsërit me një komandë.

Në macOS/Linux përdorni Python 3.12 dhe `.venv/bin/python` në vend të
`.\.venv\Scripts\python.exe`. Pjesa kryesore e prezantimit shpjegon Windows.

## Të dhënat e përfshira

`data/raw/day.csv` vjen nga UCI Bike Sharing. `nasa_power_daily.json`
është përgjigjja origjinale NASA POWER. `nasa_weather.csv` është eksporti
i lexueshëm i të njëjtave matje NASA. Shihni `data/raw/SOURCES.md` për
atribimin dhe `provenance.json` për URL-të e hash-et.

Burimet mbeten të paprekura. Kodi krijon gabime të kontrolluara vetëm në
kopjen e ushtrimit `data/teaching/dirty.csv`, që pastrimi të demonstrohet.
Skedarët e përpunuar, raportet dhe modeli krijohen nga ekzekutimi juaj.

## Figma dhe GitHub-i im

Konceptin tuaj Figma e krijoni përmes https://figma.new . Vendosni lidhjen
te fusha **Figma** në `RAPORTI.md`.

Git inicializohet në dosjen tuaj. Në fund bëni commit dhe përdorni
**Publish to GitHub** në VS Code. Hyni me llogarinë tuaj dhe zgjidhni një
emër të lirë, p.sh. `urbanbike-ai-emri-yt`. Zgjidhni repozitor privat,
pastaj jepini pedagogut qasjen sipas kërkesës së lëndës. Nuk duhet të
krijoni paraprakisht të njëjtin repo në shfletues për këtë rrugë.

Framework-u shpjegues i përgatitur për lëndën:
https://www.figma.com/design/z0Gd9JEc8blzECI15sUyCr?node-id=11-116

Për dorëzim përfundoni `RAPORTI.md`, kontrolloni kodin dhe provat në
GitHub-in tuaj, dhe dorëzoni lidhjet e kërkuara. `.venv/` dhe `models/`
mbeten në laptop. Modeli rigjenerohet nga kodi.

## Organizimi i kohës

Laboratori 120 minuta supozon programet, bibliotekat dhe llogaritë të
përgatitura përpara orës. Gjatë laboratorit kopjoni pjesët e gatshme,
i ekzekutoni dhe interpretoni rezultatet. Shtypja manuale e të gjithë
kodit ose zgjerimi i dizajnit kërkon kohë shtesë.
