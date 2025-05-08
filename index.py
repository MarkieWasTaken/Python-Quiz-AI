import os
import time
from datetime import datetime
from PIL import ImageGrab, Image
import pytesseract
import openai
import keyboard
import tkinter as tk
from plyer import notification

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

openai.api_key = "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"

screenshot_dir = "screenshot-history"
os.makedirs(screenshot_dir, exist_ok=True)

screenshot_region = None

def extract_text_from_image(image: Image.Image) -> str:
    return pytesseract.image_to_string(image)

def ask_chatgpt(question_text: str) -> str:
    prompt = f"""
    Odgovori na spodnja vprašanja z ustrezno ČRKO (A, B, C ali D), če je mogoče. Če vprašanje ne vsebuje možnosti odgovorov, odgovori kratko in natančno. Če je vprašanje že med primeri, uporabi enak odgovor. Če ga ni, odgovori sam in navedi, koliko % si prepričan v svoj odgovor.

    Primeri:

    Vprasanje: Izvedli smo test delovanja delovnega pomnilnika. Kateri tip delovnega pomnilnika smo testirali?
    Odgovor: DDR2

    Vprasanje: Katera komponenta računalnika za delovanje uporablja VRAM?
    Odgovor: grafična kartica

    Vprasanje: Jožek nam dostavi novi ključek USB kapacitete 64 GB. Nanj želi kopirati arhivske dokumente v skupni datoteki ZIP velikosti 5 GiB. Pri tem naleti na napako, saj naj bi bilo na voljo premalo prostora za izvedeno operacijo. Pred poskusom kopiranja je bilo izvedeno formatiranje ključka. Kaj je razlog, da se kopiranje ne izvede?
    Odgovor: D

    Vprasanje: Izvedli smo postopek defragmentacije (angl. defragmentation) trdega diska. Kaj predstavlja zapisani postopek?
    Odgovor: B

    Vprasanje: Katero vrsto signala lahko prenaša prikazani vmesnik?
    Odgovor: C

    Vprasanje: V BIOS/UEFI smo izvedli konfiguracijo štirih diskov v diskovnem polju RAID6. Katera izmed podanih trditev ni resnična?
    Odgovor: A

    Vprasanje: Stereo zvok z zunanje mešalne mize želimo povezati na vhod računalnika, kjer bomo izvajali snemanje zvoka. Kateri vhod zvočne kartice moramo uporabiti?
    Odgovor: B

    Vprasanje: S katero izmed naštetih naprav izvaja procesor neposredno komunikacijo?
    Odgovor: C

    Vprasanje: Imamo naslovno območje 189.23.1.0/24. Koliko bitov naslova je namenjeno za gostitelje?
    Odgovor: B

    Vprasanje: Katera naprava omogoča povezovanje v brezžično omrežje?
    Odgovor: C

    Vprasanje: Kaj se nahaja v tabeli MAC na mrežnem stikalu?
    Odgovor: B in D

    Vprasanje: Kateri stavki SQL sodijo v skupino ukazov SQL DML?
    Odgovor: C

    Vprasanje: V katero skupino ukazov spada stavek DROP?
    Odgovor: SQL DDL

    Vprasanje: Popravite spodnji stavek SELECT tako, da bo izpisal vse stolpce iz tabele avtomobili. Izpišite samo vrstice, ki nimajo podatka o izpustu CO2.
    Odgovor: SELECT * FROM avtomobili WHERE izpust IS NULL;

    Vprasanje: Skicirajte tabelo glede na spodnjo kodo HTML.
    Odgovor: (ni črkovnega odgovora – zahteva skico)

    Vprasanje: V dokument HTML želimo dodati meta oznako za ključne besede spletne strani. Dopolnite spodnjo kodo.
    Odgovor: name, content

    Vprasanje: Kaj je rezultat izraza 16 % 3 oziroma 16 mod 3 v izbranem programskem/skriptnem jeziku?
    Odgovor: A

    Vprasanje: Spodnjo kodo pretvorite v enakovredno zanko while v izbranem računalniškem jeziku.
    Odgovor: (ni črkovnega odgovora – gre za programsko pretvorbo)

    Vprasanje: Zapišite primer procesorskosistemskega vodila, ki običajno povezuje CPU in pomnilnik.  
    Odgovor: FSB

    Vprasanje: Zapišite primer shranjevanja podatkov, pri katerem se podatki shranijo trajno, vendar zaradi zaporednega zapisa do njih dostopamo razmeroma počasi.  
    Odgovor: kaseta

    Vprasanje: Kaj pomeni izraz kotna vidljivost, kadar se pogovarjamo o specifikaciji zaslona LCD?  
    Odgovor: C

    Vprasanje: Polde je kupil ključek USB s kapaciteto 64 GB. Nanj je želel kopirati datoteko velikosti 6,32 GiB. Ob tem je prejel obvestilo o napaki, da tega ni mogoče narediti. Kaj bi lahko bil najverjetnejši razlog za to?  
    Odgovor: D

    Vprasanje: Kaj predstavlja pojem particioniranje trdega diska?  
    Odgovor: B

    Vprasanje: Imamo trdi disk kapacitete 1 TB. Koliko podatkov lahko zapišemo nanj?  
    Odgovor: A

    Vprasanje: Kateri barvni model se običajno uporablja v postopku tiska na tiskalniku?  
    Odgovor: D

    Vprasanje: S pomočjo zvočne kartice izvajamo zajem zvoka. S katero enoto označujemo pogostost zajema ali frekvenco vzorčenja?  
    Odgovor: C

    Vprasanje: Podan je naslov omrežja 200.2.1.128/27. Kateri izmed spodnjih naslovov IP je v obsegu naslovov tega omrežja?  
    Odgovor: B

    Vprasanje: V katerem primeru bi v omrežju uporabili omrežno stikalo L2?  
    Odgovor: C

    Vprasanje: Katera od spodaj naštetih protokolov sta protokola transportne plasti modela OSI?  
    Odgovor: D in F

    Vprasanje: Pravkar smo s stavkom CREATE kreirali podatkovno bazo Ljubljana2105, a ker smo podatkovno bazo že imeli, bi pravkar kreirano želeli izbrisati. Kateri ukaz bi uporabili?  
    Odgovor: DROP DATABASE Ljubljana2105;

    Vprasanje: Stavki jezika SQL so razdeljeni v več skupin. Kateri stavki SQL sodijo v skupino DDL?  
    Odgovor: D

    Vprasanje: Katera izmed spodnjih podatkovnih tipov sta numerična podatkovna tipa?  
    Odgovor: B in E

    Vprasanje: Obkrožite črko pred odgovorom, ki označuje začetek neurejenega seznama v spletnem dokumentu.  
    Odgovor: D

    Vprasanje: V dokument HTML želimo vstaviti povezavo, ki se bo odprla v novem zavihku. Dopolnite spodnjo kodo.  
    Odgovor: href, target="_blank"

    Vprasanje: Spremenljivki X, ki je celoštevilskega tipa, želimo prirediti sedemkratnik števila X. Katera izmed možnosti je ustrezna?  
    Odgovor: A

    Vprasanje: Spodnji algoritem (diagram poteka) pretvorite v enakovredno kodo z zanko while v poljubnem programskem/skriptnem jeziku.  
    Odgovor:  
    A = 121  
    while(A > 80):  
        print(A)  
        A -= 11

    Vprasanje: Računalnik ima frekvenco vodila QPI 3200 MHz s širino 32 bitov. Kakšna je prepustnost vodila, če upoštevamo podano hitrost? Rešitev naj bo podana v GB/s za enosmerno komunikacijo.  
    Odgovor: 25,6 GB/s

    Vprasanje: Koliko naprav lahko teoretično priključimo na priključek USB tretje generacije?  
    Odgovor: 1 do 127

    Vprasanje: Kateri izmed datotečnih sistemov načeloma ne potrebuje postopka defragmentacije trdega diska?  
    Odgovor: C

    Vprasanje: Katero vodilo bi uporabili na prenosnem računalniku, da bi lahko priključili pogon SSD manjših dimenzij?  
    Odgovor: D

    Vprasanje: Kako se imenuje integrirano vezje, ki upravlja s prekinitvami naprav, da se CPE ustrezno odzove?  
    Odgovor: A

    Vprasanje: Katera izmed naštetih kratic ponazarja kompleksnost nabora ukazov, načina naslavljanja operandov in sorodnih značilnosti procesorjev?  
    Odgovor: B

    Vprasanje: Na računalniku želimo vzpostaviti diskovno polje tipa RAID 10. Koliko diskov najmanj potrebujemo?  
    Odgovor: A

    Vprasanje: Na novo kupljen računalnik ima procesor s hitrostjo 4200 MHz. Koliko časa potrebuje procesor, da izvede en strojni cikel?  
    Odgovor: B

    Vprasanje: Kateri izmed naštetih naslovov je zasebni naslov IP?  
    Odgovor: C

    Vprasanje: Na kateri plasti modela OSI se izvaja pravilo na požarnem zidu, ki ne prepušča prometa na določen naslov IP?  
    Odgovor: B

    Vprasanje: Kaj od spodaj naštetega ne bo več delovalo, če v omrežju onemogočimo promet protokolov HTTP in FTP?  
    Odgovor: D in E

    Vprasanje: S stavkom CREATE smo kreirali tabelo Novatabela. Kako preverimo njen opis?  
    Odgovor: DESCRIBE Nova tabela;

    Vprasanje: Kateri SQL ukaz ne vpliva na vsebino podatkov v tabeli?  
    Odgovor: D

    Vprasanje: Dopolnite SQL kodo, da atributu EMSO spremenimo podatkovni tip v varchar(13).  
    Odgovor: ALTER, varchar(13)

    Vprasanje: Obkrožite črko pred odgovorom, ki v jeziku HTML označuje začetek neurejenega seznama.  
    Odgovor: D

    Vprasanje: Dopolnite HTML kodo za sliko z atributoma za pot in nadomestno besedilo.  
    Odgovor: src, alt

    Vprasanje: Kateri izmed spodnjih odgovorov ne sodi med osnovne gradnike diagrama poteka?  
    Odgovor: B

    Vprasanje: Pretvorite for zanko v while zanko: for(int i=18;i>1;i-=2) {{ izpis(i); }}  
    Odgovor:  
    int i=18;  
    while(i>1) {{  
        izpis(i);  
        i-=2;  
    
    }}
    Vprasanje: Kateri barvni model je običajno uporabljen pri prikazovanju slike na zaslonu?  
    Odgovor: RGB

    Vprasanje: Katero vrsto napetosti različnih vrednosti potrebujejo računalniške komponente za svoje delovanje?  
    Odgovor: Enosmerno napetost

    Vprasanje: Izračunajte vsoto: 11110011[2] + 0×AB[16].  
    Odgovor: B

    Vprasanje: Kaj predstavlja binarni vzorec: 01000011 01000010 01000001?  
    Odgovor: D

    Vprasanje: Koliko je velikost datoteke, če hitrost prenosa znaša 8 Mb/s in traja 2 min 53 s?  
    Odgovor: B

    Vprasanje: Katere vrste napravo je Polde dodal v računalnik na priključek M.2?  
    Odgovor: A

    Vprasanje: Zakaj 32-bitni OS na 64-bitnem računalniku s 16 GB RAM vidi le 4 GB?  
    Odgovor: C

    Vprasanje: Katera kratica predstavlja kompleksnejši nabor ukazov v procesorju?  
    Odgovor: D

    Vprasanje: Kdaj uporabimo omrežni usmerjevalnik?  
    Odgovor: C

    Vprasanje: Katera programska vrata je treba zapreti, da onemogočimo SMTP?  
    Odgovor: B

    Vprasanje: Katera izmed danih naslovov sta zasebna naslova IP?  
    Odgovor: A in E

    Vprasanje: Kako se imenuje postopek, ki izboljšuje kakovost logičnega modela baze?  
    Odgovor: B

    Vprasanje: V katero skupino SQL ukazov spada stavek DROP?  
    Odgovor: D

    Vprasanje: Kaj moramo dodati v CREATE TABLE, da je ID auto_increment in Ime NOT NULL?  
    Odgovor: auto_increment in not null

    Vprasanje: Kateri CSS zapis določa modro ozadje vsem odstavkom?  
    Odgovor: C

    Vprasanje: Dopolni HTML za sliko z naslovom 'Tukaj je slika' in širino 200 px.  
    Odgovor: img, title="Tukaj je slika"

    Vprasanje: Kolikokrat se v splošnem izvede zanka do while?  
    Odgovor: B

    Vprasanje: Pretvori for zanko `for(int i=15;i>5;i-=2)` v zanko while.  
    Odgovor:  
    int i=15;  
    while(i>5) {{
        izpis(i);  
        i=i-2;  
    }}

    Vprasanje: Stranka bi rada tiskala fotografije z brizgalnim tiskalnikom. Kateri barvni model se uporablja pri tiskanju?  
    Odgovor: CMY oz. CMYK

    Vprasanje: Kako bi s strokovnim terminom skupaj poimenovali funkcionalnost operacijskih sistemov ReFS, UFS2 in ext4?  
    Odgovor: datotečni sistemi

    Vprasanje: Kaj predstavlja pojem ostranjevalne datoteke (angl. pagefile)?  
    Odgovor: C

    Vprasanje: Vsebine katerega izmed naštetih pomnilnikov ni mogoče spreminjati?  
    Odgovor: B

    Vprasanje: Na katerem izmed naštetih pomnilnih medijev bi lahko izvedli postopek defragmentacije?  
    Odgovor: D

    Vprasanje: Katero izmed naštetih naprav bi lahko še vedno našli na priključku vrste PS/2?  
    Odgovor: A

    Vprasanje: Katero polje RAID bo najbolje zadostilo zahtevam stranke za hitrost in zanesljivost?  
    Odgovor: C

    Vprasanje: Katera izmed spodnjih kratic pomeni nabor enostavnejših ukazov glede na kompleksnost?  
    Odgovor: A

    Vprasanje: Kateri je ustrezen desetiški zapis omrežne pripone /28?  
    Odgovor: D

    Vprasanje: V kateri plasti modela OSI se izvaja pravilo, da ne prepušča prometa spletnih strani?  
    Odgovor: C

    Vprasanje: Protokola aplikacijske in transportne plasti za pošiljanje elektronske pošte od odjemalca na strežnik?  
    Odgovor: B in D

    Vprasanje: Zapišite ukaz SQL, ki izbriše tabelo Novatabela.  
    Odgovor: DROP TABLE Novatabela

    Vprasanje: V katero skupino uvrščamo stavek ALTER TABLE?  
    Odgovor: B

    Vprasanje: Kaj moramo dodati, da bodo vsi dijaki privzeto iz občine Maribor?  
    Odgovor: DEFAULT 'Maribor'

    Vprasanje: Katera CSS koda določi rdečo barvo ozadja vsem <h1> elementom?  
    Odgovor: C

    Vprasanje: Dopolnite HTML kodo za sliko slika.png s širino 200px in besedilom 'Tukaj je slika'.  
    Odgovor: img, title='Tukaj je slika'

    Vprasanje: Kolikokrat se v splošnem izvede zanka do while?  
    Odgovor: D

    Vprasanje: Pretvori for zanko `for(int i=5;i<20;i+=2)` v while zanko.  
    Odgovor:  
    int i=5;  
    while(i<20) {{
        izpis(i);  
        i+=2;  
    }}




    Vprasanje: {question_text.strip()}
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.2,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"[ERROR] Failed to get response: {e}"

def handle_screenshot():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    filepath = os.path.join(screenshot_dir, filename)

    if screenshot_region:
        screenshot = ImageGrab.grab(bbox=screenshot_region)
    else:
        screenshot = ImageGrab.grab()

    screenshot.save(filepath)
    print(f"[+] Screenshot saved: {filepath}")

    extracted_text = extract_text_from_image(screenshot)
    print(f"[?] Extracted Text:\n{extracted_text}")

    if extracted_text.strip():
        answer = ask_chatgpt(extracted_text)
        print(f"\n💡 Answer from ChatGPT:\n{answer}\n")
        notification.notify(
            title="Quiz Answer",
            message=answer,
            timeout=10 
        )
    else:
        print("[!] No text found in the screenshot.")

def define_screenshot_region():
    def on_drag(event):
        nonlocal start_x, start_y
        canvas.delete("selection")
        canvas.create_rectangle(start_x, start_y, event.x, event.y, outline='red', width=2, tag="selection")

    def on_click(event):
        nonlocal start_x, start_y
        start_x, start_y = event.x, event.y

    def on_release(event):
        global screenshot_region
        end_x, end_y = event.x, event.y
        root.destroy()
        screenshot_region = (min(start_x, end_x), min(start_y, end_y),
                             max(start_x, end_x), max(start_y, end_y))
        print(f"[📐] Region set: {screenshot_region}")

    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.attributes('-alpha', 0.3)
    root.configure(background='gray')
    canvas = tk.Canvas(root, cursor="cross")
    canvas.pack(fill="both", expand=True)

    start_x = start_y = 0
    canvas.bind("<Button-1>", on_click)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<ButtonRelease-1>", on_release)

    root.mainloop()

keyboard.add_hotkey('ctrl+alt+s', handle_screenshot)
keyboard.add_hotkey('ctrl+alt+d', define_screenshot_region)

print("📸 Listening for Ctrl + Alt + S to take a screenshot and solve quiz...")
print("💝  Press Ctrl + Alt + D to define screenshot region.")
print("🔴 Press ESC to quit.")
print("🔴 V2")
keyboard.wait('esc')
