#!/usr/bin/env python3
"""
Fix double-encoded emoji characters across all HTML files.
The emojis were UTF-8 encoded, then their bytes were interpreted as cp1252/Latin-1,
and re-saved as UTF-8, resulting in garbled text.
Fix: for each emoji, generate its garbled form and replace with the correct emoji.
"""
import glob

EMOJIS = [
    '\U0001F389',  # party popper
    '\U0001F4CB',  # clipboard
    '\U0001F3E0',  # house
    '\U0001F4A1',  # light bulb
    '\U0001F527',  # wrench
    '\U0001F50D',  # magnifying glass
    '\U0001F3AF',  # bullseye
    '\U0001F680',  # rocket
    '\U0001F4AA',  # flexed bicep
    '\U0001F504',  # counterclockwise arrows
    '\U0000274C',  # cross mark (red X)
    '\U00002705',  # check mark
    '\U0001F9E9',  # puzzle piece
    '\U0001F3C6',  # trophy
    '\U0001F3AE',  # video game
    '\U0001F4CA',  # bar chart
    '\U0001F4BB',  # laptop
    '\U0001F4DD',  # memo
    '\U0001F525',  # fire
    '\U0001F4B0',  # money bag
    '\U0001F381',  # gift
    '\U0001F517',  # link
    '\U0001F5D1',  # wastebasket
    '\U0001F4F1',  # mobile phone
    '\U0001F512',  # locked
    '\U0001F513',  # unlocked
    '\U0001F4BE',  # floppy disk
    '\U0001F30D',  # earth globe
    '\U0001F4C5',  # calendar
    '\U0001F440',  # eyes
    '\U0001F44B',  # waving hand
    '\U0001F916',  # robot
    '\U0001F44D',  # thumbs up
    '\U0001F44E',  # thumbs down
    '\U00002764',  # heart
    '\U0001F4AF',  # 100
    '\U0001F6A7',  # construction
    '\U00002B50',  # star
    '\U0001F4E2',  # loudspeaker
    '\U0001F4E3',  # megaphone
    '\U0001F4AC',  # speech bubble
    '\U00002139',  # information
    '\U000026A0',  # warning sign
    '\U00002714',  # heavy check mark
    '\U00002716',  # heavy multiplication x
    '\U000021A9',  # leftwards arrow with hook
    '\U00002022',  # bullet
    '\U000000D7',  # multiplication sign (x)
    '\U00002019',  # right single quotation mark
    '\U0000201C',  # left double quotation mark
    '\U0000201D',  # right double quotation mark
    '\U00002013',  # en dash
    '\U00002014',  # em dash
    '\U0001F4E9',  # envelope with arrow
    '\U0001F4E8',  # incoming envelope
    '\U0001F4E7',  # e-mail
    '\U0001F4C1',  # file folder
    '\U0001F4C2',  # open file folder
    '\U0001F5C2',  # card index dividers
    '\U0001F50F',  # lock with ink pen
    '\U0001F510',  # closed lock with key
    '\U0001F511',  # key
    '\U0001F6AA',  # door
    '\U0001F6B6',  # pedestrian
    '\U0001F3C3',  # runner
    '\U0001F4B3',  # credit card
    '\U0001F4E6',  # package
    '\U0001F4A5',  # collision
    '\U0001F4A6',  # splashing sweat symbol
    '\U0001F4A7',  # droplet
    '\U0001F4AF',  # hundred points
    '\U0001F4B9',  # chart with upwards trend and yen sign
    '\U0001F4C8',  # chart with upwards trend
    '\U0001F4C9',  # chart with downwards trend
    '\U0001F4CE',  # paperclip
    '\U0001F4CF',  # straight ruler
    '\U0001F4D0',  # triangular ruler
    '\U0001F4D1',  # bookmark tabs
    '\U0001F4D2',  # ledger
    '\U0001F4D3',  # notebook
    '\U0001F4D4',  # notebook with decorative cover
    '\U0001F4D5',  # closed book
    '\U0001F4D6',  # open book
    '\U0001F4D7',  # green book
    '\U0001F4D8',  # blue book
    '\U0001F4D9',  # orange book
    '\U0001F4DA',  # books
    '\U0001F4DB',  # name badge
    '\U0001F4DC',  # scroll
    '\U0001F4DE',  # telephone receiver
    '\U0001F4DF',  # pager
    '\U0001F4E0',  # fax machine
    '\U0001F4E1',  # satellite antenna
    '\U0001F4EA',  # closed mailbox with lowered flag
    '\U0001F4EB',  # closed mailbox with raised flag
    '\U0001F4EC',  # open mailbox with raised flag
    '\U0001F4ED',  # open mailbox with lowered flag
    '\U0001F4EE',  # postbox
    '\U0001F4EF',  # postal horn
    '\U0001F4F0',  # newspaper
    '\U0001F4F2',  # mobile phone with rightwards arrow at left
    '\U0001F4F3',  # vibration mode
    '\U0001F4F4',  # mobile phone off
    '\U0001F4F5',  # no mobile phones
    '\U0001F4F6',  # antenna with bars
    '\U0001F4F7',  # camera
    '\U0001F4F8',  # camera with flash
    '\U0001F4F9',  # video camera
    '\U0001F4FA',  # television
    '\U0001F4FB',  # radio
    '\U0001F4FC',  # videocassette
    '\U0001F4FD',  # film projector
    '\U0001F50A',  # speaker with three sound waves
    '\U0001F50B',  # battery
    '\U0001F50C',  # electric plug
    '\U0001F50E',  # right-pointing magnifying glass
    '\U0001F50F',  # lock with ink pen
    '\U0001F514',  # bell
    '\U0001F515',  # bell with cancellation stroke
    '\U0001F516',  # bookmark
    '\U0001F518',  # radio button
    '\U0001F519',  # back with leftwards arrow above
    '\U0001F51A',  # end with leftwards arrow above
    '\U0001F51B',  # on with exclamation mark with left right arrow above
    '\U0001F51C',  # soon with rightwards arrow above
    '\U0001F51D',  # top with upwards arrow above
    '\U0001F51E',  # no one under eighteen symbol
    '\U0001F51F',  # keycap ten
    '\U0001F520',  # input symbol for latin capital letters
    '\U0001F521',  # input symbol for latin small letters
    '\U0001F522',  # input symbol for numbers
    '\U0001F523',  # input symbol for symbols
    '\U0001F524',  # input symbol for latin letters
    '\U0001F526',  # electric light bulb
    '\U0001F528',  # hammer
    '\U0001F529',  # nut and bolt
    '\U0001F52A',  # hocho
    '\U0001F52B',  # pistol
    '\U0001F52C',  # microscope
    '\U0001F52D',  # telescope
    '\U0001F52E',  # crystal ball
    '\U0001F52F',  # six pointed star with middle dot
    '\U0001F530',  # japanese symbol for beginner
    '\U0001F531',  # trident emblem
    '\U0001F532',  # black square button
    '\U0001F533',  # white square button
    '\U0001F534',  # large red circle
    '\U0001F535',  # large blue circle
    '\U0001F536',  # large orange diamond
    '\U0001F537',  # large blue diamond
    '\U0001F538',  # small orange diamond
    '\U0001F539',  # small blue diamond
    '\U0001F53A',  # up-pointing red triangle
    '\U0001F53B',  # down-pointing red triangle
    '\U0001F53C',  # up-pointing small red triangle
    '\U0001F53D',  # down-pointing small red triangle
    '\U0001F550',  # clock face one oclock
    '\U0001F5A5',  # desktop computer
    '\U0001F5BC',  # frame with picture
    '\U0001F5D2',  # spiral note pad
    '\U0001F5D3',  # spiral calendar pad
    '\U0001F5E1',  # dagger knife
    '\U0001F5E3',  # speaking head in silhouette
    '\U0001F5F3',  # ballot box with ballot
    '\U0001F600',  # grinning face
    '\U0001F601',  # grinning face with smiling eyes
    '\U0001F602',  # face with tears of joy
    '\U0001F603',  # smiling face with open mouth
    '\U0001F604',  # smiling face with open mouth and smiling eyes
    '\U0001F605',  # smiling face with open mouth and cold sweat
    '\U0001F606',  # smiling face with open mouth and tightly-closed eyes
    '\U0001F607',  # smiling face with halo
    '\U0001F608',  # smiling face with horns
    '\U0001F609',  # winking face
    '\U0001F60A',  # smiling face with smiling eyes
    '\U0001F60B',  # face savouring delicious food
    '\U0001F60C',  # relieved face
    '\U0001F60D',  # smiling face with heart-shaped eyes
    '\U0001F60E',  # smiling face with sunglasses
    '\U0001F60F',  # smirking face
    '\U0001F610',  # neutral face
    '\U0001F611',  # expressionless face
    '\U0001F612',  # unamused face
    '\U0001F613',  # face with cold sweat
    '\U0001F614',  # pensive face
    '\U0001F615',  # confused face
    '\U0001F616',  # confounded face
    '\U0001F617',  # kissing face
    '\U0001F618',  # face throwing a kiss
    '\U0001F619',  # kissing face with smiling eyes
    '\U0001F61A',  # kissing face with closed eyes
    '\U0001F61B',  # face with stuck-out tongue
    '\U0001F61C',  # face with stuck-out tongue and winking eye
    '\U0001F61D',  # face with stuck-out tongue and tightly-closed eyes
    '\U0001F61E',  # disappointed face
    '\U0001F61F',  # worried face
    '\U0001F620',  # angry face
    '\U0001F621',  # pouting face
    '\U0001F622',  # crying face
    '\U0001F623',  # persevering face
    '\U0001F624',  # face with look of triumph
    '\U0001F625',  # disappointed but relieved face
    '\U0001F626',  # frowning face with open mouth
    '\U0001F627',  # anguished face
    '\U0001F628',  # fearful face
    '\U0001F629',  # weary face
    '\U0001F62A',  # sleepy face
    '\U0001F62B',  # tired face
    '\U0001F62C',  # grimacing face
    '\U0001F62D',  # loudly crying face
    '\U0001F62E',  # face with open mouth
    '\U0001F62F',  # hushed face
    '\U0001F630',  # face with open mouth and cold sweat
    '\U0001F631',  # face screaming in fear
    '\U0001F632',  # astonished face
    '\U0001F633',  # flushed face
    '\U0001F634',  # sleeping face
    '\U0001F635',  # dizzy face
    '\U0001F636',  # face without mouth
    '\U0001F637',  # face with medical mask
    '\U0001F638',  # grinning cat face with smiling eyes
    '\U0001F440',  # eyes
    '\U0001F44C',  # ok hand sign
    '\U0001F44F',  # clapping hands sign
    '\U0001F450',  # open hands sign
    '\U0001F451',  # crown
    '\U0001F452',  # womans hat
    '\U0001F453',  # eyeglasses
    '\U0001F454',  # necktie
    '\U0001F455',  # t-shirt
    '\U0001F456',  # jeans
    '\U0001F457',  # dress
    '\U0001F458',  # kimono
    '\U0001F459',  # bikini
    '\U0001F45A',  # womans clothes
    '\U0001F45B',  # purse
    '\U0001F45C',  # handbag
    '\U0001F45D',  # pouch
    '\U0001F45E',  # mans shoe
    '\U0001F45F',  # athletic shoe
    '\U0001F460',  # high-heeled shoe
    '\U0001F461',  # womans sandal
    '\U0001F462',  # womans boots
    '\U0001F463',  # footprints
    '\U0001F464',  # bust in silhouette
    '\U0001F465',  # busts in silhouette
    '\U0001F466',  # boy
    '\U0001F467',  # girl
    '\U0001F468',  # man
    '\U0001F469',  # woman
    '\U0001F46A',  # family
    '\U0001F46B',  # man and woman holding hands
    '\U0001F46C',  # two men holding hands
    '\U0001F46D',  # two women holding hands
    '\U0001F46E',  # police officer
    '\U0001F46F',  # woman with bunny ears
    '\U0001F470',  # bride with veil
    '\U0001F471',  # person with blond hair
    '\U0001F472',  # man with gua pi mao
    '\U0001F473',  # man with turban
    '\U0001F474',  # older man
    '\U0001F475',  # older woman
    '\U0001F476',  # baby
    '\U0001F477',  # construction worker
    '\U0001F478',  # princess
    '\U0001F479',  # japanese ogre
    '\U0001F47A',  # japanese goblin
    '\U0001F47B',  # ghost
    '\U0001F47C',  # baby angel
    '\U0001F47D',  # extraterrestrial alien
    '\U0001F47E',  # alien monster
    '\U0001F47F',  # imp
    '\U0001F480',  # skull
    '\U0001F481',  # information desk person
    '\U0001F482',  # guardsman
    '\U0001F483',  # dancer
    '\U0001F484',  # lipstick
    '\U0001F485',  # nail polish
    '\U0001F486',  # face massage
    '\U0001F487',  # haircut
    '\U0001F488',  # barber pole
    '\U0001F489',  # syringe
    '\U0001F48A',  # pill
    '\U0001F48B',  # kiss mark
    '\U0001F48C',  # love letter
    '\U0001F48D',  # ring
    '\U0001F48E',  # gem stone
    '\U0001F48F',  # kiss
    '\U0001F490',  # bouquet
    '\U0001F491',  # couple with heart
    '\U0001F492',  # wedding
    '\U0001F493',  # beating heart
    '\U0001F494',  # broken heart
    '\U0001F495',  # two hearts
    '\U0001F496',  # sparkling heart
    '\U0001F497',  # growing heart
    '\U0001F498',  # heart with arrow
    '\U0001F499',  # blue heart
    '\U0001F49A',  # green heart
    '\U0001F49B',  # yellow heart
    '\U0001F49C',  # purple heart
    '\U0001F49D',  # heart with ribbon
    '\U0001F49E',  # revolving hearts
    '\U0001F49F',  # heart decoration
]

def byte_to_garbled_char(b):
    """Convert a single byte to the Unicode char it would become after cp1252 misread.
    Uses cp1252 mapping where defined, falls back to raw Latin-1 code point otherwise."""
    try:
        return bytes([b]).decode('cp1252')
    except (UnicodeDecodeError, ValueError):
        # Byte is undefined in cp1252 - use raw Latin-1 code point
        return chr(b)

def build_replacements():
    """Build a mapping from garbled utf-8 (misread as cp1252) to correct emoji.
    Uses hybrid cp1252/latin-1 decoding matching how the files were corrupted."""
    replacements = {}
    for emoji in EMOJIS:
        try:
            utf8_bytes = emoji.encode('utf-8')
            # Convert each byte using cp1252 (with latin-1 fallback for undefined bytes)
            garbled = ''.join(byte_to_garbled_char(b) for b in utf8_bytes)
            if garbled != emoji:  # Only add if it actually differs
                replacements[garbled] = emoji
        except (UnicodeDecodeError, UnicodeEncodeError):
            pass  # Skip if can't be converted
    return replacements

def fix_file(filepath, replacements):
    """Fix garbled emojis in a file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print(f"  Error reading {filepath}: {e}")
        return False
    
    original = content
    
    # Sort by length descending to handle longer sequences first
    for garbled, correct in sorted(replacements.items(), key=lambda x: len(x[0]), reverse=True):
        content = content.replace(garbled, correct)
    
    if content != original:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Fixed: {filepath}")
            return True
        except Exception as e:
            print(f"  Error writing {filepath}: {e}")
            return False
    return False

if __name__ == '__main__':
    replacements = build_replacements()
    print(f"Generated {len(replacements)} emoji replacements")
    
    # Find all relevant files
    all_files = (
        glob.glob('**/*.html', recursive=True) +
        glob.glob('**/*.js', recursive=True) +
        glob.glob('**/*.css', recursive=True) +
        glob.glob('**/*.py', recursive=True)
    )
    
    print(f"Processing {len(all_files)} files...")
    fixed_count = 0
    for f in sorted(all_files):
        if fix_file(f, replacements):
            fixed_count += 1
    
    print(f"\nDone! Fixed {fixed_count} files.")
