<img src="/readme_content/Jecna_logo.png" alt="SPŠE Ječná"/>

# PV-Game

Klienta si můžete stáhnou na naší [webové stránce](https://www.spsejecna.cz).


- [Klient](#klient)
    - [Podporované operační systémy](#kop)
    - [Konfigurace](#klient_konfig)

TODO
----
- [x] přihlášení
- [x] registrovat
- [x] hashování hesel
- [x] mapa
- [x] přechod do jiných lokacích
- [x] vstup do budov
- [x] questy
- [x] inventář
- [x] profil
- [x] používání itemů
- [x] NPC
- [x] koupě piva v hospodě
- [x] ukládání uživatele
- [x] NPC souboj
- [ ] zresetování účtu uživatele po smrti
- [ ] používání abilit v souboji
- [ ] multiplayer souboj


## CLIENT <a name="klient"></a>
Napsaný v jazyce :snake: Python 3.10.10

### PODPOROVANÉ OPERAČNÍ SYSTÉMY <a name="kop"></a>
:window: Windows 10, Windows 11

:penguin: Debian

### Kofigurace: <a name="klient_konfig"></a>

| Nastavení           | Hodnota                         |
|---------------------|---------------------------------|
| server_address      | `ip adresa serveru`             |
| server_port         | `port serveru`                  |
| response_size       | `velikost přijímaných zpráv`    |
| time_delay          | `pauza po zpracování protokolu` |

## SERVER

od serveru jde zprava ve formátu ==> @|start|@prompt@@value@@next_message@@typ@|end|@
po přijetí serveru se odešle zpráva |||doručeno|||

## Hra

### Třídy
- warrior
- assasin
- wizard

### Lokace
- Hlavní město
- Route1
- Les
- Route2
- Rubínové město

### Budovy
- hopoda -> hlavním městě a rubínové městě

### Questy
- Capital_city_tawern_quest->zachránit hospodského z hlavního města a otevřít si tím lokaci hospody v hlavním městě

### Itemy ve hře
| item              | kod  | typ itemu         | player hp | player damage | player mana | player speed | abilita                                               |
|-------------------|------|-------------------|-----------|---------------|-------------|--------------|-------------------------------------------------------|
|bronzový meč       | 0001 | zbraň             | +0        | +12           | +0          | -10          | -                                                     |
|zlatý meč          | 0002 | zbraň             | +0        | +20           | +0          | -15          | -                                                     |
|diamantový meč     | 0003 | zbraň             | +0        | +30           | +0          | -25          | -                                                     |
|kouzelný proutek   | 0004 | zbraň             | +0        | +15           | +30         | +0           | -                                                     |
|kouzelnická hůl    | 0005 | zbraň             | +0        | +50           | +45         | -10          | -                                                     |
|zlatá přilba       | 0006 | přilba            | +15       | +0            | +0          | -2           | -                                                     |
|kožené boty        | 0007 | boty              | +0        | +0            | +0          | +5           | -                                                     |
|hermesovy boty     | 0008 | boty              | +0        | +0            | +0          | +50          | -                                                     |
|léčivý lektvar     | 0009 | useable           | +20       | +0            | +0          | +0           | -                                                     |
|mana lektvar       | 0010 | useable           | +0        | +0            | +30         | +0           | -                                                     |
|energy drink       | 0011 | combat_useable    | +0        | +0            | +0          | +10          |efekt trvá po dobu 3 kol                               |
|kouzelnický klobouk| 0012 | přilba            | +20       | +5            | +10         | -5           | -                                                     |
|pivo               | 0013 | useable           | +50       | +0            | +0          | +0           | -                                                     |
|ohnivá koule svitek| 0014 | non_combat_useable| +0        | +0            | +0          | +0           |získáte schopnost "ohnivá koule"                       |