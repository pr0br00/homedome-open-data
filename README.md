# HOMEDOME — відкриті дані про енергетику України

Первинні й зведені дані, на яких HOMEDOME (Дніпро, сонячні станції й накопичувачі з 2019 року) рахує
окупність станцій і накопичувачів. Ті самі цифри, що на сайті [homedome.com.ua](https://homedome.com.ua),
у машиночитному вигляді. Оновлюється щотижня автоматично з сайту.

Ліцензія — [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): можна використовувати, змінювати й
публікувати, зокрема комерційно, з посиланням на джерело.

## Що всередині

| Набір | Файли | Що це | Звідки |
|---|---|---|---|
| Індекс спредів РДН | `data/rdn-spread-index/daily.csv`, `monthly.csv`, `spread-index.json` | Добові спреди цін ринку «на добу наперед» (max − min за добу), чистий спред після тарифів і втрат циклу, години мінімуму й максимуму — з 01.01.2025 | Власний розрахунок з погодинних результатів торгів [АТ «Оператор ринку»](https://www.oree.com.ua/index.php/control/results_mo/DAM) |
| Тарифи на розподіл за регіонами | `data/osr-distribution-tariffs/tariffs.csv` | Тарифи 22 операторів систем розподілу (1 і 2 клас напруги) і тариф на передачу, грн/МВт·год, з номером постанови | Постанови НКРЕКП |
| Модель арбітражу накопичувача за регіонами | `data/osr-distribution-tariffs/bess-arbitrage-model-by-region.csv` | **Модель, не замір**: чистий спред, цикли на рік, виручка й окупність кабінету 125 кВт / 261 кВт·год у кожному регіоні | Розрахунок HOMEDOME на даних двох наборів вище |
| Генерація сонячної станції | `data/solar-generation/dnipro-10kw-measured-monthly.csv` | **Замір**: помісячна генерація станції 10 кВт, Дніпропетровська область | Дані моніторингу станції |
| Питома генерація за містами | `data/solar-generation/annual-yield-by-city-estimate.csv` | **Оцінка, не замір**: кВт·год з 1 кВт на рік, за якою HOMEDOME рахує пропозиції; метод — у `.meta.json` поруч | Калібрування на станції 78,74 кВт у Дніпрі + поправка за ДСТУ-Н Б В.1.1-27:2010 |

Методика індексу спредів: спред = max(година) − min(година) за добу; чистий спред = max × 0,85 − min − 2 903
(0,85 — ККД циклу накопичувача, 2 903 грн/МВт·год — передача й розподіл). Детально — на сторінці
[Індекс спредів РДН](https://homedome.com.ua/indeks-spredu-rdn) і [Карта арбітражу](https://homedome.com.ua/karta-arbitrazhu).

## Як цитувати

> HOMEDOME (2026). HOMEDOME Open Energy Data (Ukraine). https://github.com/pr0br00/homedome-open-data. Ліцензія CC BY 4.0.

Формат для менеджерів бібліографії — у [`CITATION.cff`](CITATION.cff). Постійний DOI (Zenodo) зʼявиться з першим релізом.

## Оновлення

GitHub Actions щосереди забирає з сайту `spread-index.json`, `region-economics.json` і `statystyka.json`
та перебудовує CSV (`scripts/onovyty.py`, лише стандартна бібліотека Python). Щомісяця — реліз з тегом `рррр.мм`.

Помітили помилку? Відкрийте issue або напишіть на homedome.com.ua@gmail.com.

---

## English

Open data behind HOMEDOME's solar and battery payback calculations (Ukraine), mirrored weekly from
[homedome.com.ua](https://homedome.com.ua). License: CC BY 4.0.

- **Day-ahead market (DAM) spread index** — daily max − min hourly price and net spread after grid tariffs and
  round-trip losses, since 2025-01-01. Derived from hourly results published by Market Operator JSC (oree.com.ua).
- **Distribution tariffs by region** — 22 Ukrainian DSOs, voltage classes 1 and 2, plus transmission tariff (UAH/MWh), with NEURC resolution numbers.
- **BESS arbitrage model by region** — model output, not measurements: net spread, cycles/year, revenue and payback of a 125 kW / 261 kWh cabinet.
- **Solar generation** — measured monthly output of a 10 kW station (Dnipro region) and an *estimated* specific yield by city (kWh/kWp/year).

Cite as: HOMEDOME (2026). HOMEDOME Open Energy Data (Ukraine). https://github.com/pr0br00/homedome-open-data
