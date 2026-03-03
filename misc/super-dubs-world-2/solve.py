import os
import shutil
import zipfile
import pdfplumber
import base64

ref = r"""

                                           -++++++++-                                       
                                       .++++++####++++++++-                                  
                                     +++++++++###++++++++++++.                               
                 +ФАЙЛ+            ++#+++++#####+++++++++++++++.                             
                +#-..-##-        +###ΑΡΧΕΙΟ#+.        +++++++++++                            
                #-     -##     .###BESTAND+  .-..--..-. .-+++++++++            .              
               .-        -#.  -##ФАЙЛ###++   |W\/WW\/W|  -+++++++++        +ΑΡΧΕΙΟ.          
               --         -#--##FICHIER#+-   \W|WW|W|W/  .++++++++++     -#+-.   -+          
               -.          -###ARCHIVO##++    \WW/\WW/   .+++++++++++  -#-       --          
               .    .       +###DATEI####++.   --  --   .++++++++++++##+         .-          
               -    .-.     .##ΑΡΧΕΙΟ##++++++++++++++++++++++++++++++#.          ..          
               -   .---   .-######+++++++++++++++++++++++#++++++++++#+           -.          
                    .--...######+++++++++++++++++++++++++++##+++++###.     ...   -           
                    .----###FICHIER##+#DATEI#############++++##+####+.   .---.   .           
                    .+ΑΡΧΕΙΟ##ФАЙЛ##+--++####ΑΡΧΕΙΟ###ARCHIVO#++++###+..--+-.    -           
                  .+#####ARCHIVO#+-..   -##ФАЙЛ######DATEI###FICHIER##-----.                 
                 -####BESTAND###+.       -#####FICHIER#+-..-+##BESTAND##+--.                 
               .-##DATEI########-         -#ARCHIVO##+.    .-+###ФАЙЛ###+-.                 
              -+#ФАЙЛ#BESTAND##+-.        .#ARCHIVO##+       .###FICHIER###-.                
             -####ΑΡΧΕΙΟ#######+-.        .+###DATEI+        .+####DATEI####+.               
            -###FICHIER#######-.          .+#ФАЙЛ##+-        .-###ARCHIVO####+.              
           .-##ARCHIVO#ΑΡΧΕΙΟ.  ----+-    .-FICHIER+.        .-+####ΑΡΧΕΙΟ#####+-             
           -+##ARCHIVO#####+--##+#####-.---+ΑΡΧΕΙΟ++.    .     -##FICHIER##DATEI-            
           -####DATEI####+--..##++##+##++++ARCHIVO#++-.-#####+  +ΑΡΧΕΙΟ##ФАЙЛ###-            
          .+##FICHIER###.     .+#######-..-BESTAND--+######+-##-++#+##BESTAND###+.           
           -#ARCHIVO#+.  ...   ....--#-   .+######-..-+#######. ..++###BESTAND###-           
          .+ФАЙЛ###-.    ..        .-.    .+#ФАЙЛ+-   .+.---.     .+#####FICHIER#+.          
          -ΑΡΧΕΙΟ-.     .                -#BESTAND#+.    .        .  -DATEI#ФАЙЛ###-.         
        .-DATEI+.                       .++-+DATEI+.           ...    -##ARCHIVO##+-.        
       .-+####+.                           .      ..            .      .-+##BESTAND-.        
        -+ФАЙЛ-.                        -##ARCHIVO-                        .+ΑΡΧΕΙΟ+-        
       --####+-                        ######++#####.                      .-+DATEI#-.       
      .-DATEI+-                       .#ФАЙЛ#++#####-                       -+######--.      
      .-+###+-                         +####+#DATEI+.                       -FICHIER+-       
      ..-##++-.                        -#++-+#++++++                       .-+##ФАЙЛ#-.      
      .-++###-.                        .-+FICHIER#-                        .-+ARCHIVO+.      
      .-#ФАЙЛ-.                .        --++####--.                        .-+#ΑΡΧΕΙΟ+-.     
      ..-+###+-                .       .-+++--++--                        ---+BESTAND-.      
       .-+###+-                ...     .-++###+---                        -+#ARCHIVO##-      
        .-+##+..                .+----.-###BESTAND-.    .                 .-+FICHIER#+--     
         .-##+-.                .++--+..---+#+++#+-++---.                 .--##DATEI#+-..    
          .-++-.                 -#+-  --.---.-.--...-+-                 ..-+###ФАЙЛ##+.     
           .-++-.                 .++...-----.--...---.                ..-#ARCHIVO#++-.     
            ----.                   .#. .----.-.. -###-                ..-###ΑΡΧΕΙΟ###--     
            .-+-.                   -+#-.------. --                    ..+#BESTAND##+----    
            .--+-.                   +#-#+------+#-                   -+##ARCHIVO######-.    
             .+#+-.                    ++###ФАЙЛ+.                .-++#DATEI###FICHIER#+-.   
            ..-###+-                      .-..                  .-+####ФАЙЛ###+--+++####+-.  
         ... .DATEI-.                                          ..-+##ARCHIVO##-.---+++###+-. 
       ..--...+####+-..                                         --+##ΑΡΧΕΙΟ#-.......-+++###+.
      .----...BESTAND+.                                         -+FICHIER##-.........----+#+-
     ..-..--++####+#++-    ...                            .  ..--+##DATEI#----..--..-----+-##
     ....----+####+.-+-++-+-----..                      ...---+##BESTAND#+-++++----....--++##
      ..-----+ФАЙЛ -W-..-#+-#++--..                  ....-++++####ФАЙЛ###+---++---++--.----++
      .-----++###+ .WWWWWW.##+##++++-....---+....--.-----++#ARCHIVO######+-+++-----------+-+#
    .-++--.++ΑΡΧΕΙΟ--WWW--.##.----DATEI##ФАЙЛ#+###ARCHIVO##########ARCHIVO###++++------++###+
    .-++-.-+ARCHIVO--WW--++#.WWWW.###.-W--##BESTAND###DATEI##ΑΡΧΕΙΟ####ΑΡΧΕΙΟ+++++-+--+ΑΡΧΕΙΟ
    .+++-.++##DATEI-WWW.+## WWWWW.##--WWWWW-.#####ФАЙЛ##ΑΡΧΕΙΟ#ФАЙЛ#########++++#++---+######
   --++-.-#+FICHIER.WWW +#.WWWWWW.##+- -WWWW +DATEI#####FICHIER###BESTAND++-----+++--+BESTAND
   -###-.++###ФАЙЛ#.WWW + WW.WWWW.###.-WW +.+######BESTAND###DATEI###+--##+-...----++#ФАЙЛ###
   -###+-##ΑΡΧΕΙΟ##.WWW  WW .WWWW.## -W-.####ARCHIVO####BESTAND#######+--...   .--++###DATEI#
   +##+-.#ARCHIVO##.WWW WW ..WWWW + WW--########FICHIER#####ФАЙЛ####-..       ..--+###FICHIER
  -+##+-.####ФАЙЛ#+.WWWWW #..WWWW  WW -#####ARCHIVO####ΑΡΧΕΙΟ######-.         .-+##ΑΡΧΕΙΟ####
 .-###+--DATEI####-.WWWW ## -WWW--WW ##ФАЙЛ#####DATEI###ARCHIVO---.         .-++####ΑΡΧΕΙΟ###
 .+####+-##BESTAND#+  .- +#+ WWWWWW-.ΑΡΧΕΙΟ#BESTAND#--.-+###+--.-..         ..-######BESTAND#
 .+####++ΑΡΧΕΙΟ#FICHIER###+ -WWWW.+#####ARCHIVO##.+--+- #+-.          ....--++##ARCHIVO######
 .+#ФАЙЛ#+#+#####.. --+#DATEI+-. +####ΑΡΧΕΙΟ#######++-+--.            .--++######DATEI#ΑΡΧΕΙΟ
 .+DATEI#+BESTAND.D.- U- . -###FICHIER#######ΑΡΧΕΙΟ###-.            ..-+#######BESTAND##ФАЙЛ#
 .+---+###++####- D .-U +..B... S-+####+++#BESTAND#---.         ....-+++#FICHIER#####DATEI###
 .-..---+++ARCHIVO++--- + -B.- -S-###+.  -++#####+-...     . .--+-ΑΡΧΕΙΟ######ARCHIVO########
  .    .. .+#+#ФАЙЛ#####+ . . #- +###+   ---ФАЙЛ.          -#++++++####BESTAND########FICHIER
          .-####DATEI#######+---ΑΡΧΕΙΟ--+#+###+          --+###+-..-+++---+++#ARCHIVO########
           .-##ARCHIVO####FICHIER##########-         ..---+---.    ... .....-##ФАЙЛ##ΑΡΧΕΙΟ+
             +ΑΡΧΕΙΟ######+-+#####ФАЙЛ####.     . . ..---.....               .-++##BESTAND##+
              ###ARCHIVO##. .+#ARCHIVO#+-... .    ...-..                     .-++#DATEI#####+
              .#+BESTAND#+   .+DATEI+-..... .                                .-+###ΑΡΧΕΙΟ##+
               +##ФАЙЛ####+---####-                                          .-+++###ARCHIVO+
                #FICHIER#ΑΡΧΕΙΟ#-                                            -+FICHIER#####+-
  ..            .###ΑΡΧΕΙΟ####-                                             .-+++##BESTAND#--
  .              -####DATEI###-                                            .-++ФАЙЛ#+####+---
   ..             +#BESTAND###+                                           --+--+##--++##++-..
   ..              ####ARCHIVO+                                          .--++--++++++##-----
"""

def extract_text_from_pdf(pdf_path):
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        return ""


def compare_strings(pdf_text, comparison_string):
    differences = {
        'match': pdf_text == comparison_string,
        'pdf_text': pdf_text,
        'comparison_string': comparison_string,
        'pdf_length': len(pdf_text),
        'comparison_length': len(comparison_string)
    }
    
    for i, (c1, c2) in enumerate(zip(pdf_text, comparison_string)):
        if c1 != c2:
            differences['first_diff_position'] = i
            differences['first_diff_pdf_char'] = c1
            differences['first_diff_comparison_char'] = c2
            break
    
    return differences


def unzip_file(zip_path, extract_to=None):
    if extract_to is None:
        extract_to = os.path.dirname(zip_path)
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
            extracted_files = [os.path.join(extract_to, name) for name in zip_ref.namelist()]
            return extracted_files
    except Exception as e:
        return None


def process_level(level_num, comparison_string, final, working_dir="."):
    print(f"LEVEL {level_num}")
    
    jpg_path = os.path.join(working_dir, f"level{level_num}.jpg")
    pdf_path = os.path.join(working_dir, f"level{level_num}.pdf")
    zip_path = os.path.join(working_dir, f"level{level_num}.zip")
    
    if not os.path.exists(jpg_path):
        return False, None
    
    try:
        shutil.move(jpg_path, pdf_path)
    except Exception as e:
        return False, None
    
    pdf_text = extract_text_from_pdf(pdf_path)
    
    comparison = compare_strings(pdf_text, comparison_string)
    
    if not comparison['match']:
        if 'first_diff_position' in comparison:
            final = comparison['first_diff_pdf_char']

    try:
        shutil.move(pdf_path, zip_path)
    except Exception as e:
        return False, final
   
    extracted_files = unzip_file(zip_path, working_dir)
    
    if extracted_files is None:
        return False, final
    next_jpg = os.path.join(working_dir, f"level{level_num + 1}.jpg")
    os.remove(os.path.join(working_dir, f"level{level_num}.zip"))
    if os.path.exists(next_jpg):
        return True, final
    else:
        for extracted in extracted_files:
            if extracted.endswith('.jpg'):
                shutil.move(extracted, next_jpg)
                return True, final
        
        return False, final


def main():
    working_dir = "."
    final = ""
    comparison_string = extract_text_from_pdf(os.path.join(working_dir, "sample.pdf")) 
    start_level = 1
    
    level = start_level
    max_levels = 200
    while level <= max_levels:
        success, final2 = process_level(level, comparison_string, final, working_dir)
        final += final2
        
        if not success:
            print(f"done at level {level}")
            break
        
        level += 1
    else:
        print("Reached maximum level limit")
    
    print("processing complete")
    print(final)
    print(base64.b64decode(final.encode("ascii")).decode("ascii"))


if __name__ == "__main__":
    main()