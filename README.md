<img src="/readme_content/Jecna_logo.png" alt="SPŠE Ječná"/>

# PV-Game

Klienta si můžete stáhnou na naší [webové stránce](https://www.spsejecna.cz).

TODO
----
- [x] přihlášení
- [x] registrovat
- [x] mapa
- [x] přechod do jiných lokacích
- [x] vstup do budov
- [x] inventář
- [ ] používání itemů
- [ ] NPC
- [ ] koupě piva v hospodě
- [ ] NPC souboj
- [ ] multiplayer souboj


## CLIENT
Napsaný v jazyce :snake: Python 3.10.10

### PODPOROVANÉ OPERAČNÍ SYSTÉMY
:window: Windows 10, Windows 11

:penguin: Debian

### Kofigurace:

| Nastavení           | Hodnota                         |
|---------------------|---------------------------------|
| server_address      | `ip adresa serveru`             |
| server_port         | `port serveru`                  |
| response_size       | `velikost přijímaných zpráv`    |
| time_delay          | `pauza po zpracování protokolu` |

Pro náš veřejný server:
```JSON
{
    "server_address":"dev.spsejecna.net",
    "server_port":20148,
    "response_size":4096,
    "time_delay":0.01
}
```

## SERVER

od serveru jde zprava ve formátu ==> @|start|@prompt@@value@@next_message@@typ@|end|@
po přijetí serveru se odešle zpráva |||doručeno|||

## Hra

### Třídy
- warrior
- assasin
- wizard

### Ability

### Itemy

### Lokace
- Hlavní město
- Route1
- Les života
- Route2
- Rubínové město

### Budovy
- hopoda -> nachází se v hlavním městě a rubínové městě

### Questy
- Capital_city_tawern_quest->zachránit hospodského z hlavního města a otevřít si tím lokaci hospody v hlavním městě

### Itemy ve hře
| item              | kod  | typ itemu | player hp | player damage | player mana | player speed | abilita                                               |
|-------------------|------|-----------|-----------|---------------|-------------|--------------|-------------------------------------------------------|
|bronzový meč       | 0001 | zbraň     | +0        | +12           | +0          | -10          | -                                                     |
|zlatý meč          | 0002 | zbraň     | +0        | +20           | +0          | -15          | -                                                     |
|diamantový meč     | 0003 | zbraň     | +0        | +30           | +0          | -25          | -                                                     |
|kouzelný proutek   | 0004 | zbraň     | +0        | +15           | +30         | +0           | každé kouzlo stojí o 10 many méně                     |
|kouzelnická hůl    | 0005 | zbraň     | +0        | +50           | +45         | -10          | každé kouzlo stojí o 5 many méně a přidá 10 poškození |
|zlatá přilba       | 0006 | přilba    | +15       | +0            | +0          | -2           | -                                                     |
|kožené boty        | 0007 | boty      | +0        | +0            | +0          | +5           | -                                                     |
|hermesovy boty     | 0008 | boty      | +0        | +0            | +0          | +50          | -                                                     |
|léčivý lektvar     | 0009 | useable   | +20       | +0            | +0          | +0           | -                                                     |
|mana lektvar       | 0010 | useable   | +0        | +0            | +30         | +0           | -                                                     |
|energy drink       | 0011 | useable   | +0        | +0            | +0          | +10          |efekt trvá po dobu 3 kol                               |
|kouzelnický klobouk| 0012 | přilba    | +20       | +5            | +10         | -5           | -                                                     |
|pivo               | 0013 | useable   | +50       | +0            | +0          | +0           | -                                                     |