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
| server_address      | `<span style="color:red">ip adresa serveru</span>` |
| server_port         | `<span style="color:red">port serveru</span>` |
| response_size       | `<span style="color:red">velikost přijímaných zpráv</span>` |

```
{
    "server_address":ip adresa serveru,
    "server_port":port serveru,
    "response_size":velikost přijímaných zpráv
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