<img src="/readme_content/Jecna_logo.png" alt="SPŠE Ječná"/>

# PV-Game

Klienta si můžete stáhnou na [Odkaz na stránky](https://www.spsejecna.cz).

## CLIENT

### PODPOROVANÉ OPERAČNÍ SYSTÉMY
:window: Windows 10, Windows 11

:penguin: Debian

### Kofigurace:

| Nastavení           | Hodnota              |
|---------------------|----------------------|
| server_address      | `ip adresa serveru` |
| server_port         | `port serveru` |
| response_size       | `velikost přijímaných zpráv` |
| time_delay          | `pauza po zpracování protokolu` |

Pro náš veřejný server
```
{
    "server_address":"127.0.0.1",
    "server_port":5000,
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

### Typy itemů
| zbraňe | damage | mana | speed | ability |
|--------|--------|-------|---------|------|
|bronzový meč|  30    |   0    |   -5      | -   |
|zlatý meč|   50    |     0  |       -10  | - |
|diamantový meč| 80      |  0     |     -40    |   |
|kouzelný proutek| 25     |   20    |     0    | každé kouzlo stojí o 10 many méně |
|kouzelnická hůl|  45     |    40   |    -10     | každé kouzlo stojí o 5 many méně a přidá 10 poškození |
- helma
- zbroj
- kalhoty
- boty
- useable:
    - v kombatu
    - mimo kombat