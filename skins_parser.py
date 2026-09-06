from collections import defaultdict
import json
import os


path = '/sdcard/b9225992870ce094dbe590033320ec95'
out = '/sdcard/parse.txt'


tiers = {
    1: '⚪',
    2: '🟢',
    3: '🔵',
    4: '🟣',
    5: '🟡',
    6: '🟠',
    7: '🔴',
}


if not os.path.exists(path):
    print('Check input files directory.')
    exit()


def get_symbol(tier):
    return tiers.get(tier, '⚪')


def json_redo(content):
    start = content.find('{')
    if start == -1:
        return None
    content = content[start:]
    brace = content.rfind('}')
    if brace != -1:
        content = content[:brace + 1]
    return content


def get_name(display_header):
    if not display_header:
        return 'unknown'
    name = display_header.strip().upper()
    mapping = {
        'XD .45': 'XD45',
        'DUAL MTX': 'DUALMTX',
        'MR 96': 'MR96',
        'SG 551': 'SG551',
        'GSR 1911': 'GSR1911',
        'SUPER 90': 'SUPER90',
        'DEAGLE': 'DEAGLE',
        'TRG 22': 'TRG22',
        'AR-15': 'AR15',
        'SCAR-H': 'SCARH',
        'M1887': 'M1887',
        'AK-47': 'AK47',
        'M4': 'M4',
        'M14': 'M14',
        'MP5': 'MP5',
        'MP7': 'MP7',
        'FP6': 'FP6',
        'P90': 'P90',
        'P250': 'P250',
        'SA58': 'SA58',
        'URATIO': 'URATIO',
        'VECTOR': 'VECTOR',
        'MPX': 'MPX',
        'SVD': 'SVD',
        'KSG': 'KSG',
        'KNIFE': 'KNIFE',
        'KUKRI': 'KUKRI',
        'REMIX': 'REMIX',
        'TAC-TOOL': 'TACTOOL',
        'KARAMBIT': 'KARAMBIT',
        'BALISONG': 'BALISONG',
        'PIPE WRENCH': 'PIPEWRENCH',
        'SHORT SWORD': 'SHORTSWORD',
        'TOMAHAWK': 'TOMAHAWK',
        'MEAT CLEAVER': 'MEATCLEAVER',
        'JAMBIYA': 'JAMBIYA',
        'PUSH DAGGERS': 'PUSHDAGGERS',
        'TANTO': 'TANTO',
        'MANIAGO': 'MANIAGO',
        'DRAGONMOURN': 'DRAGONMOURN',
        'C4': 'C4',
        'FLASHBANG GRENADE': 'FLASHBANG',
        'FRAG GRENADE': 'FRAG',
        'PRACTICE GRENADE': 'PRACTICE',
        'SMOKE GRENADE': 'SMOKE',
        'FIRE BOMB': 'FIREBOMB',
        'INCENDIARY GRENADE': 'INCENDIARY',
        'ZOMBIE HANDS': 'ZOMBIEHANDS',
        'EMPTY HANDS': 'EMPTYHANDS',
    }
    for key, value in mapping.items():
        if name == key:
            return value
    return name.replace(' ', '')


def parse_skins(data):
    weapons = defaultdict(list)
    for category in data.get('item_types', []):
        category_name = category.get('name', '')
        for item in category.get('items', []):
            if 'id' not in item or 'display_name' not in item:
                continue
            weapon_name = get_name(item.get('display_header'))
            if weapon_name == 'unknown':
                if 'knife' in category_name.lower() or 'melee' in category_name.lower():
                    weapon_name = 'MELEE'
                elif 'grenade' in category_name.lower():
                    weapon_name = 'GRENADE'
                else:
                    weapon_name = category_name.upper()
            tier = item.get('tier', 1)
            skin_data = {
                'id': item['id'],
                'display_name': item['display_name'].upper(),
                'tier': tier,
            }
            weapons[weapon_name].append(skin_data)
    for weapon in weapons:
        weapons[weapon] = sorted(weapons[weapon], key=lambda x: x['id'])
    return weapons


def format_output(weapons):
    lines = []
    for weapon_name in sorted(weapons.keys()):
        if not weapons[weapon_name]:
            continue
        lines.append(f"function {weapon_name}(x)\nm_{weapon_name} = gg.choice({{")
        for skin in weapons[weapon_name]:
            symbol = get_symbol(skin['tier'])
            lines.append(f"[{skin['id']}] = '{symbol} {skin['display_name']}',")
        lines.append('},nil,')
        lines.append(f"'{weapon_name} Menu')\n\nend")
        lines.append('')
    return '\n'.join(lines)


# noinspection bad-argument-type,none-function-assignment
def goto():
    try:
        with open(path, 'rb') as f:
            x = f.read()
        content = None
        encodings = ['utf-8', 'latin-1', 'cp1251', 'iso-8859-1']
        for enc in encodings:
            try:
                content = x.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        if content is None:
            content = x.decode('utf-8', errors='ignore')
        clean_json = json_redo(content)
        data = json.loads(clean_json)
        weapons = parse_skins(data)
        output = format_output(weapons)
        with open(out, 'w+', encoding='utf-8') as f:
            f.write(output)
    except Exception as nil:
        print(f'Error: {nil}')
        exit()
    print('Done!')
    return None


goto()