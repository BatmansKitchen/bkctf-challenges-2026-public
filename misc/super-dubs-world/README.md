# Super Dubs World — BKCTF 2026

**Flag:** `bkctf{p01ygl0ts_l0v3_dub5!}`

## Overview

Dubs recently started learning about ASCII art and decided to make a self-portrait! He says it's inspired by his favorite game franchise and his trips around the world.

The result is a single file that's… unique, to say the least. Dubs seems very proud of it!

Looks like he ate something strange, too. Maybe look into that?

Players are then given dubs.pdf!

This challenge plays off the idea of ***Polyglot Files***, where a file can appear as many different files depending on the extension.

Opening the PDF, we see the first part of the flag `1: bkctf{`, and a ASCII art image of dubs!

Looking into the art, we can see a bunch of words in different languages. Google translate translates these as all saying *file*, which indicates the polyglot file.

So, it's time to try different extensions to find parts of the flag!

The second part of the flag can be found if you change the extension to **mp4**, where a photo of dubs with the number *2* on his hat. Playing the audio repeats a bunch of Mario "yahoo!" sound bites. Translated into morse, provides the second part of the flag: `p01yg`!

The third part of the flag can be found if you change the exteension to **png/jpg**, where the classic image of "Thank you Mario, but our princess is in another castle!" gets switched to "Thank you Dubs, but our flag is in another file!" Looking into this image, you can see a faint question part after the sentence, and looking in the top left reveals a faint text for the third part of the flag: `l0ts_`!

The fourth part of the flag can be found if you change the extension to **zip**, and unzip the resulting file. This reveals another *dubs.pdf* where, instead of `bkctf{`, dubs is showing the fourth part of the flag: `l0v3_`!

The fifth and final part of the flag is quite tricky, as you are meant to change the extension of the file *inside* of the zip file (the pdf used to find part 4). Changing this file into a **png/jpg** reveals a different image, congratulating dubs for reaching the end of the quest and provides the final part of the flag: `DUB5!}`

The final image says to input the flag in all lowercase, leaving us with the final flag!

Flag: `bkctf{p01ygl0ts_l0v3_dub5!}`