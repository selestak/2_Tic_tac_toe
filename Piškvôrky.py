import random
from time import sleep


# Uvedomujem si hroznú dĺžku kódu, pardón. Cieľom bolo vytvoriť čo najviac autentickú hru, ktorá by
# sa podobala reálnej hre, s výberom pre single alebo multiplayer (aj keď to nebolo v zadaní),
# zobrazením prípravy hry a podobne. Bez toho všetkého by to šlo skrátiť aj o viac než 100 riadkov.

def main():
    """ Hlavná riadaca jednotka hry Piškvôrky, ktorá prebieha v smyčke while loopu """
    # Hlavné premenné - pozície obsadených polí konkrétnym znakom a voľné miesta na ploche
    pozicia = {1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: ''}
    volne_miesta = list(range(1, 10))
    # Zobrazí sa iba raz, keďže je mimo hlavného while loopu
    uvodna_hlavicka()
    while True:
        # Užívateľ si vyberie počet hráčov
        pocet_hracov = vyber_poctu_hracov()
        # Ďalej si vyberie svoj hrací znak, znak súpera je mu automaticky priradený
        hraci = vyber_si_symbol()
        # V prípade single player hry (pre pobavenie) kód vyberie meno protivníka
        nahodny_super = vyber_nahodneho_supera()
        # Pre efekt reálnej hry sa "načítava" hracia plocha so všetkými dátami
        priprava_zapasu(pocet_hracov, hraci, nahodny_super)
        # Globálne premenné sa prečistia v prípade opakovanej hry
        cistky(pozicia, volne_miesta)
        # Na základne počtu hráčov prebehne single alebo multiplayer hra
        if pocet_hracov == 1:
            hra_pre_jedneho(pozicia, hraci, volne_miesta, nahodny_super)
        else:
            hra_pre_dvoch(pozicia, hraci, volne_miesta)
        # Po výhre / remíze vyzve užívateľa na ďalšiu hru
        este_jednu()


def oddelovac(i: int) -> None:
    """ Pomocná funkcia príjma integer 0 alebo 1, pre efektívne vystisknutí hrubého / tenkého oddeľovača """
    print('=' * 60) if i == 1 else print('-' * 60)


def uvodna_hlavicka() -> None:
    """ Uvítanie a oboznámenie hráča s pravidlami hry """
    oddelovac(1)
    print(">>> VITAJTE V TIC TAC TOE <<<".center(60))
    oddelovac(1)
    print(">> PRAVIDLÁ HRY <<".center(60))
    pravidla_text = ("Hráči označia jedno herné pole vlastným znakom zadaním čísla\n"
                     "políčka. Polia sú radené od ľavého horného rohu (1) po pravý\n"
                     "spodný roh (9). Vyhráva ten, ktorému sa podarí horizontálne,\n"
                     "veritkálne alebo diagonálne spojiť tri rovnaké symboly.")
    print(pravidla_text.center(60))
    oddelovac(1)


def vyber_poctu_hracov() -> int:
    """ Funkcia vracia počet hráčov (integer 1 alebo 2) na základe vstupu užívateľa """
    # Nie elegantné zmeny dátoveho typu, chcel som sa udržať v loope a vyhnúť sa ValueError pri chybnom zadaní
    # Mohol som použiť try a expect, rozhodol som sa pre túto cestu aby podmienky vstupov boli jednotné v celom kóde
    while True:
        pocet_hracov = input('| Zadaj počet hráčov [ 1 alebo 2 ]: ')
        if pocet_hracov == str(1) or pocet_hracov == str(2):
            break
        else:
            print('| Nesprávna voľba. Skús to znova!')
            oddelovac(0)
    return int(pocet_hracov)


def vyber_si_symbol() -> tuple:
    """ Možnosť výberu hracieho znaku pre hráča č. 1, druhému je znak priradený. Vracia tuple znakov oboch hráčov """
    while True:
        hrac_1 = input('| Prvý hráč, zadaj svoju voľbu [ X alebo O ]: ').upper()
        if hrac_1 == 'X' or hrac_1 == 'O':
            break
        else:
            print('| Nesprávna voľba. Skús to znova!')
            oddelovac(0)

    hrac_2 = 'X' if hrac_1 == 'O' else 'O'  # Druhý hráč automaticky dostane zvyšný znak z ponuky, 'X' alebo 'O'
    hraci = hrac_1, hrac_2
    return hraci


def vyber_nahodneho_supera() -> str:
    """ V prípade singleplayer hry vracia táto funkcia náhodne vybrané meno protivníka """
    protivnici = ['HAL 9000', 'Skynet', 'Deus Ex Machina', 'GLaDOS', 'GERTY 3000']
    nahodny_super = random.choice(protivnici).upper()
    return nahodny_super


def priprava_zapasu(pocet_hracov: int, hraci: tuple, nahodny_super: str) -> None:
    """ Na základe prijatých dát o počte hráčov, ich hracích znakov a prípadne mena náhodného
        súpera táto funkcia "pre efekt" zobrazí prípravu hracej plochy """
    oddelovac(0)
    if pocet_hracov == 1:
        print("Vyberáme ti protivníka hodného tvojích síl...".center(60))
        sleep(2)
        print(f"ČLOVEK [ {hraci[0]} ] vs. {nahodny_super} [ {hraci[1]} ]".center(60))
    else:
        print("Pripravujeme pre Vás hraciu plochu...".center(60))
        sleep(1)
        print(f"HRÁČ 1 [ {hraci[0]} ] vs. HRÁČ 2 [ {hraci[1]} ]".center(60))
    oddelovac(1)


def cistky(pozicia: dict, volne_miesta: list) -> None:
    """ V prípade opakovanej hry prebehne "vyčistenie" dát predchádzajucej hry - obsadených a voľných miest """
    for hodnota in pozicia:  # Vyčistenie slovníka od hodnôt 'X' alebo 'O'
        pozicia[hodnota] = ''
    for cislo in list(range(1, 10)):  # Obnovenie listu voľných miest pre novú hru
        if cislo not in volne_miesta:
            volne_miesta.append(cislo)


def hracia_plocha(pozicia: dict) -> None:
    """ Grafické vytisknutie aktuálneho statusu hry na základe hodnôt slovníka pozície """
    plocha = (""" 
                    +-----+-----+-----+
                    |{:^5}|{:^5}|{:^5}|
                    +-----+-----+-----+
                    |{:^5}|{:^5}|{:^5}|
                    +-----+-----+-----+
                    |{:^5}|{:^5}|{:^5}|
                    +-----+-----+-----+
                    """.format(*pozicia.values()))
    print(plocha)


def kompletny_tah(pozicia: dict, aktualny_hrac: str, volne_miesta: list) -> None:
    """ Funkcia bežiaca v smyčke while loopu kontroluje zadaný vstup. Ak je správny, dáta uloží do slovníka
        pozícií a zároveň ho odstráni ho z voľných miest. Ak je nesprávny, užívateľ musí voľbu opakovať """
    while True:
        vstup = input(f'| HRÁČ {aktualny_hrac} | ZADAJ SVOJU VOĽBU: ')
        oddelovac(0)
        if vstup in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            vstup = int(vstup)
            if vstup not in list(range(1, 10)):
                pass
            elif vstup not in volne_miesta:
                print('>> OBSAZENO! SKÚS TO ZNOVA <<'.center(60))
                oddelovac(0)
                continue
            else:
                pozicia[vstup] = aktualny_hrac
                volne_miesta.remove(vstup)
                break
        print('>> NESPRÁVNA VOĽBA, ZADAJ ČÍSLA OD 1 DO 9 <<'.center(60))
        oddelovac(0)


def zmena_hraca(aktualny_hrac: str) -> str:
    """ Príjem a vracanie hracieho znaku aktuálneho hráča, ktorý sa samozrejme po každom ťahu mení """
    if aktualny_hrac != 'X':
        aktualny_hrac = 'X'
    else:
        aktualny_hrac = 'O'
    return aktualny_hrac


def ide_pocitac(pozicia, aktualny_hrac, volne_miesta, nahodny_super):
    """" Riadi priebeh ťahu počítača založenom na náhodnom výbere """
    print(f'| HRÁČ {nahodny_super} | ZADAJ SVOJU VOĽBU: ')
    oddelovac(0)
    sleep(1)
    volba_pocitac = random.choice(volne_miesta)  # Náhodný výber
    pozicia[volba_pocitac] = aktualny_hrac  # Zápis do obsadených
    volne_miesta.remove(volba_pocitac)  # Preč z voľných
    hracia_plocha(pozicia)  # Zobrazí hru


def podmienky_vyhry(pozicia: dict, aktualny_hrac: str) -> bool:
    """ V prípade splnenia podmienok na výhru vyvolá funckiu víťaz, ktorá ukončí hru. Od hora
        prebieha horizontálna, vertikálna a diagonálna kontrola troch rovnakých znakov """
    if pozicia[1] == pozicia[2] == pozicia[3] != '' \
            or pozicia[4] == pozicia[5] == pozicia[6] != '' \
            or pozicia[7] == pozicia[8] == pozicia[9] != '':
        return vitaz(aktualny_hrac)  # horizontálny víťaz
    elif pozicia[1] == pozicia[4] == pozicia[7] != '' \
            or pozicia[2] == pozicia[5] == pozicia[8] != '' \
            or pozicia[3] == pozicia[6] == pozicia[9] != '':
        return vitaz(aktualny_hrac)  # vertikálny víťaz
    elif pozicia[1] == pozicia[5] == pozicia[9] != '' \
            or pozicia[3] == pozicia[5] == pozicia[7] != '':
        return vitaz(aktualny_hrac)  # diagonálny víťaz


def vitaz(aktualny_hrac: str) -> bool:
    """ Jednoduchá funkcia vyvolaná ak sú podmienky výhry splnené. Vracia boolean hodnotu, ktorá pomáha
        vo funkciách hry pre jedného a dvoch vyvolať break na ukončenie celej hry """
    oddelovac(0)
    print(f'>> VYHÁVA HRÁČ {aktualny_hrac}! <<'.center(60))
    return True


def remiza(volne_miesta: list) -> bool:
    """ Kontrola množstva voľných miest. Ak už žiadne nezostali, nastáva remíza a táto funkcia vráti
        boolean hodnotu, ktorá vyvolá break na ukončenie celej hry """
    if len(volne_miesta) == 0:
        print('>> REMÍZA <<'.center(60))
        return True


def hra_pre_jedneho(pozicia: dict, hraci: tuple, volne_miesta: list, nahodny_super: str) -> None:
    # V hre stále začína prvý hráč
    aktualny_hrac = hraci[0]
    hracia_plocha(pozicia)
    # Celá hra prebieha na while loope, ktorý prebieha až kým sa nenájde víťaz alebo nenastane
    # remíza, ktorá vyvolá break a celú hru ukončí. Po každom ťahu hráča alebo počítača musí
    # nastať zmena znaku, aby nasledujúci hráč hral už so správnym znakom.
    while True:
        # Prvý hráč vloží svoj vstup (ťah), hracia plocha vstup zobrazí, nastáva následná kontrola podmienok výhry
        kompletny_tah(pozicia, aktualny_hrac, volne_miesta)
        hracia_plocha(pozicia)
        if podmienky_vyhry(pozicia, aktualny_hrac) or remiza(volne_miesta):
            oddelovac(0)
            break
        aktualny_hrac = zmena_hraca(aktualny_hrac)
        # Na rade je počítač, prebehne jeho ťah a rovnako znova nastáva kontrola podmienok výhry + zmena znaku
        ide_pocitac(pozicia, aktualny_hrac, volne_miesta, nahodny_super)
        if podmienky_vyhry(pozicia, aktualny_hrac) or remiza(volne_miesta):
            oddelovac(0)
            break
        aktualny_hrac = zmena_hraca(aktualny_hrac)


def hra_pre_dvoch(pozicia: dict, hraci: tuple, volne_miesta: list) -> None:
    # V hre stále začína prvý hráč
    aktualny_hrac = hraci[0]
    hracia_plocha(pozicia)
    # Celá hra prebieha na while loope, ktorý prebieha až kým sa nenájde víťaz alebo nenastane
    # remíza, ktorá vyvolá break a celú hru ukončí.
    while True:
        kompletny_tah(pozicia, aktualny_hrac, volne_miesta)
        hracia_plocha(pozicia)
        if podmienky_vyhry(pozicia, aktualny_hrac) or remiza(volne_miesta):
            oddelovac(0)
            break
        # Po každom ťahu hráča while loop ide od znova, s novým hráčom (hracím znakom)
        aktualny_hrac = zmena_hraca(aktualny_hrac)


def este_jednu() -> None:
    """ Výzva užívateľovi o novú hru. Ak áno, pokračuje v hlavnom while loope vo funkcii main().
        Ak nie, poďakuje hráčovi za hru a celý program ukončí """
    repete = input('| DÁME SI EŠTE JEDNU HRU? [ A / N ] : ')
    if repete in ['a', 'ano', 'y', 'yes']:
        oddelovac(0)
        pass
    elif repete in ['n', 'ne', 'no', 'nein']:
        oddelovac(1)
        print('>> VĎAKA ZA HRU, GG <<'.center(60))
        oddelovac(1)
        exit()


main()
