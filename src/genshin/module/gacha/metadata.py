"""gacha data struct"""


GACHA_QUERY_TYPE_IDS = ["100", "200", "301", "302"]

GACHA_QUERY_TYPE_NAMES = ["新手祈愿", "常驻祈愿", "角色活动祈愿", "武器活动祈愿"]

GACHA_QUERY_TYPE_DICT = dict(zip(GACHA_QUERY_TYPE_IDS, GACHA_QUERY_TYPE_NAMES))

GACHA_TYPE_DICT = {
    "100": "新手祈愿",
    "200": "常驻祈愿",
    "301": "角色活动祈愿",
    "302": "武器活动祈愿",
    "400": "角色活动祈愿-2",
}
