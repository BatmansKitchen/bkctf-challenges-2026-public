# Scryfall Wizard — BKCTF 2026

**Flag:** `bkctf{blockers_is_for_mathing}`

## Overview

Inspired by BuckeyeCTF 2023's [birdwatching](https://github.com/cscosu/buckeyectf-2023-public/tree/master/forensics-birdwatching), this challenge presented a series of images — mostly MTG cards, with some non-MTG images acting as underscores in the flag. Each MTG card was identified using [Scryfall search syntax](https://scryfall.com/docs/syntax), where every search returned exactly one unique card.

## Solution

| # | Card | How to Find |
|---|------|-------------|
| 1 | **Blood Artist** | Alchemy variant — only card with that artist |
| 2 | **Lost Mine of Phandelver** | Dungeon card |
| 3 | **Our Market Research...** | Sideways text |
| 4 | **Chrome Courier** | Brothers' War Commander — only multicolored common |
| 5 | **Kudzu** | Alpha — artist signature + leaf art |
| 6 | **Eladamri's Call** | MH1 set number |
| 7 | **Ral, Monsoon Mage** | Loyalty 2 red planeswalker starting with R (Rowan also worked here, since they're the only 2-loyalty red planeswalkers.) |
| 8 | **Sliver Overlord** | Art + power/toughness |
| 9 | **_** | Non-MTG (Jinx from Riftbound) |
| 10 | **Indicate** | Flavor text |
| 11 | **Sol Ring** | Freebie |
| 12 | **_** | Non-MTG (Effect Veiler from Yu-Gi-Oh!) |
| 13 | **False Orders** | Rulings text, can use text search or oracle. |
| 14 | **Ojer Kaslem** | `t:land c:green` with a fancy border |
| 15 | **Revelation** | "Enchant world" + stained glass frame |
| 16 | **_** | (`_______` from Unhinged) |
| 17 | **Mom's Goblin Waiters** | Half mana cost |
| 18 | **Asmoranomardicadaistinaculdacar** | Reverse image search, or "art:scorpion" |
| 19 | **Tamiyo** | Emblem, MH3 |
| 20 | **Hired Muscle // Scarmaker** | Legendary Spirit flip card |
| 21 | **Inkmoth Nexus** | Phyrexian land tapping for colorless |
| 22 | **Nikara, Lair Scavenger** | "Partner with Yannik" reminder text |
| 23 | **Golos, Tireless Pilgrim** | Banlist |

The bolded keywords from each card name spell out the flag: `bkctf{blockers_is_for_mathing}`