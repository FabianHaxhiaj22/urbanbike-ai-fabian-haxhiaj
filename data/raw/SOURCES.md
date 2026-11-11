# Burimet e të dhënave

1. Fanaee-T, H. (2013). *Bike Sharing* [Dataset]. UCI Machine Learning
   Repository. https://doi.org/10.24432/C5W894
   Faqja: https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset
   Licenca: CC BY 4.0. day.csv dhe Readme.txt janë kopje të origjinaleve.
   uci_bike_sharing.zip ruan arkivin origjinal.

2. NASA Langley Research Center POWER Project. *Daily meteorological data*
   për Washington D.C., 2011–2012. https://power.larc.nasa.gov/
   API: https://power.larc.nasa.gov/docs/services/api/temporal/daily/
   Koordinatat 38.9072, −77.0369. Standardi kohor LST.
   T2M: temperatura në 2 m, °C. PRECTOTCORR: reshjet, mm/ditë.
   WS2M: shpejtësia e erës në 2 m, m/s.
   Atribim NASA POWER. Politika e aksesit dhe licencimit:
   https://registry.opendata.aws/nasa-power/

nasa_power_daily.json është përgjigjja origjinale. nasa_weather.csv është
eksporti i saj i lexueshëm: date, temp_c, rain_mm, wind_ms. Janë të njëjtat
matje nga NASA, jo një burim i tretë dhe jo të dhëna të simuluara.
CSV-ja u kontrollua kundrejt JSON-it. provenance.json ruan URL-të, kohën e
marrjes, hash-et e origjinaleve dhe hash-in e CSV-së së derivuar.

01_clean.py krijon veçmas kopjen didaktike data/teaching/dirty.csv.
Mungesat, teksti i pavlefshëm dhe dublimet e asaj kopjeje janë injektuar
qëllimisht. Burimet reale të ruajtura këtu nuk ndryshohen.
