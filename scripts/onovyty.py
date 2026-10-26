#!/usr/bin/env python3
"""
Оновлення відкритих даних HOMEDOME з живого сайту homedome.com.ua.

Джерело правди — сайт: ті самі JSON, що бачать люди й пошуковики. Скрипт лише
забирає їх і робить зручні CSV. Запускається щотижня в GitHub Actions
(.github/workflows/onovlennya.yml); локально: python3 scripts/onovyty.py
Лише стандартна бібліотека Python.
"""
import csv
import json
import os
import urllib.request

SAYT = 'https://homedome.com.ua'
KORIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(KORIN, 'data')


def vzyaty(shlyakh):
    req = urllib.request.Request(SAYT + shlyakh, headers={'User-Agent': 'homedome-open-data/1.0'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode('utf-8'))


def zapysaty_json(shlyakh, dani):
    os.makedirs(os.path.dirname(shlyakh), exist_ok=True)
    with open(shlyakh, 'w', encoding='utf-8') as f:
        json.dump(dani, f, ensure_ascii=False, indent=1)
        f.write('\n')


def zapysaty_csv(shlyakh, polya, ryadky):
    os.makedirs(os.path.dirname(shlyakh), exist_ok=True)
    with open(shlyakh, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=polya, extrasaction='ignore')
        w.writeheader()
        for r in ryadky:
            w.writerow(r)


def spredy():
    s = vzyaty('/spread-index.json')
    d = os.path.join(DATA, 'rdn-spread-index')
    zapysaty_json(os.path.join(d, 'spread-index.json'), s)
    zapysaty_csv(os.path.join(d, 'daily.csv'),
                 ['date', 'min', 'max', 'spread', 'netSpread', 'minHour', 'maxHour', 'avg'], s['daily'])
    misyatsi = s['monthly']
    zapysaty_csv(os.path.join(d, 'monthly.csv'), list(misyatsi[0].keys()), misyatsi)
    return s['meta']['coverage']


def taryfy():
    r = vzyaty('/region-economics.json')
    d = os.path.join(DATA, 'osr-distribution-tariffs')
    meta = r['meta']
    ryadky, model = [], []
    for kod, x in r['regions'].items():
        ryadky.append({
            'region_code': kod, 'region': x['region'], 'operator': x['operator'],
            'distribution_class1_uah_mwh': x['distributionClass1'],
            'distribution_class2_uah_mwh': x['distributionClass2'],
            'transmission_uah_mwh': meta['transmissionUahMwh'],
            'period': meta['tariffPeriod'], 'resolution': x['resolution'],
        })
        model.append({
            'region_code': kod, 'region': x['region'],
            'grid_cost_uah_mwh': x['gridCost'], 'avg_net_spread_uah_mwh': x['avgNetSpread'],
            'profitable_days_share_pct': x['profitableShare'], 'cycles_per_year': x['cyclesPerYear'],
            'cabinet_revenue_uah_year': x['cabinetRevenueUah'], 'payback_years': x['paybackYears'],
        })
    pole = ['region_code', 'region', 'operator', 'distribution_class1_uah_mwh', 'distribution_class2_uah_mwh',
            'transmission_uah_mwh', 'period', 'resolution']
    zapysaty_csv(os.path.join(d, 'tariffs.csv'), pole, sorted(ryadky, key=lambda x: x['distribution_class2_uah_mwh']))
    zapysaty_csv(os.path.join(d, 'bess-arbitrage-model-by-region.csv'), list(model[0].keys()),
                 sorted(model, key=lambda x: x['payback_years']))
    zapysaty_json(os.path.join(d, 'region-economics.json'), r)
    return meta['tariffPeriod']


def heneratsiya():
    s = vzyaty('/statystyka.json')
    d = os.path.join(DATA, 'solar-generation')
    g = s['monthlyGeneration10kw']
    zapysaty_csv(os.path.join(d, 'dnipro-10kw-measured-monthly.csv'), ['month', 'kwh', 'pctOfPeak'], g['data'])
    m = s.get('annualYieldByCity')
    if m:
        dani = m.get('data') or m.get('cities') or []
        if dani:
            zapysaty_csv(os.path.join(d, 'annual-yield-by-city-estimate.csv'), list(dani[0].keys()), dani)
        zapysaty_json(os.path.join(d, 'annual-yield-by-city-estimate.meta.json'), {k: v for k, v in m.items() if k not in ('data', 'cities')})


if __name__ == '__main__':
    pokryttya = spredy()
    period = taryfy()
    heneratsiya()
    print(f"РДН: {pokryttya['from']} — {pokryttya['to']} ({pokryttya['days']} діб); тарифи ОСР: {period}")
