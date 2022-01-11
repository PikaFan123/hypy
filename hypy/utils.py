import re
from typing import Union, Tuple
from io import BytesIO
from base64 import b64decode
from datetime import datetime
from nbt.nbt import TAG_Compound, TAG_List
from nbt import nbt
from .vars import (
    xp_cumulative,
    cata_xp_cumulative,
    cosmetic_xp_cumulative,
    item_id_table,
)
from .hypixelresources import SkyBlockResources
from .exceptions import MalformedIDException

uuid_regex = re.compile(
    r"[0-9A-Za-z]{8}-?[0-9A-Za-z]{4}-?4[0-9A-Za-z]{3}-?[89ABab][0-9A-Za-z]{3}-?[0-9A-Za-z]{12}"
)

DATETIME_FORMAT = r"%m/%d/%y %I:%M %p"
AUC_DATETIME_FORMAT = r"%d/%m/%y %H:%M"

LORE_REGEX = re.compile(r"§.")

# https://stackoverflow.com/a/10371921/10962150
def resolve_dict_path(dictionary, path):
    for item in path.split('.'):
        dictionary = dictionary[item]
    return dictionary

def get_auction_lores(auctions):
    """return lore for each auction, use asyncio.to_thread for this"""
    return [get_safe_content(i["item_lore"]) for i in auctions]


def get_safe_content(content) -> str:
    """get safe content"""
    return LORE_REGEX.sub("", content)


def is_uuid(uuid: str) -> bool:
    """Check if parameter is a UUID"""
    # maybe a better function name? could be misleading
    return bool(re.fullmatch(uuid_regex, uuid))


username_regex = r"\w{3,16}"


def is_username(username) -> bool:
    """Check if parameter is a username"""
    # maybe a better function name? could be misleading
    return bool(re.fullmatch(username_regex, username))


def lvlCalc(xp: Union[int, float], skilltype: str) -> float:
    """calculate level for any given skill"""
    xp = int(xp)
    min_lvl = -1
    rel_xp_cumulative = xp_cumulative
    if skilltype in ["catacombs"]:
        rel_xp_cumulative = cata_xp_cumulative
    if skilltype in ["social", "runecrafting"]:
        rel_xp_cumulative = cosmetic_xp_cumulative
    for i in range(62):
        if i not in rel_xp_cumulative:
            rel_xp_cumulative[i] = 11167242500000000000000000000  # ridic high number
    if xp is None:
        return 0.0
    for _, xp_req in rel_xp_cumulative.items():
        if xp_req < xp:
            min_lvl += 1
    if min_lvl < 0:
        return 0.0
    xp_diff = rel_xp_cumulative[min_lvl + 1] - rel_xp_cumulative[min_lvl]
    xp_to_next = rel_xp_cumulative[min_lvl + 1] - xp
    min_lvl_fraction = 1 - (xp_to_next / xp_diff)
    real_level = min_lvl + min_lvl_fraction
    # If skill is level 50, note that and continue (yes im very lazy)
    if real_level > 50:
        if skilltype not in ["enchanting", "farming", "mining"]:
            return 50.0
    if real_level > 60:
        return 60.0
    return float(real_level)


def item_id_to_name(item_id) -> Tuple[str, str]:
    """Return name for given item id"""
    default = "stone"
    default_display = "Error parsing lol"
    i_pair = str(item_id).split(":")
    if len(i_pair) == 1:
        item_ids = [x for x in item_id_table if x["type"] == int(i_pair[0])]
        if len(item_ids) == 0:
            return default, default_display
        return str(item_ids[0]["text_type"]), str(item_ids[0]["name"])
    elif len(i_pair) == 2:
        i_list = [x for x in item_id_table if x["type"] == int(i_pair[0])]
        if len(i_list) == 0:
            return default, default_display
        i_listm = [x for x in i_list if x["meta"] == int(i_pair[1])]
        if len(i_listm) == 0:
            return default, default_display
        return str(i_listm[0]["text_type"]), str(i_listm[0]["name"])
    else:
        raise MalformedIDException(item_id)


def decode_nbt(raw_data):
    """Decode NBT data"""
    nbtdata = nbt.NBTFile(fileobj=BytesIO(b64decode(raw_data)))
    return nbtdata


# https://github.com/twoolie/NBT/blob/master/examples/utilities.py
def unpack_nbt(tag):
    """
    Unpack an NBT tag into a native Python data structure.
    """

    if isinstance(tag, TAG_List):
        return [unpack_nbt(i) for i in tag.tags]
    elif isinstance(tag, TAG_Compound):
        return dict((i.name, unpack_nbt(i)) for i in tag.tags)
    else:
        return tag.value


class Utils:
    """Some misc functions used in hypy"""

    def __init__(self, resources: SkyBlockResources):
        self.resources = resources

    def lvlCalc(self, xp, skilltype) -> float:
        """calculate level for any given skill using cumulative xp from the api"""
        xp = int(xp)
        min_lvl = -1
        if xp is None:
            return 0
        rel_xp_cumulative_data = self.resources.cumulative_xp[skilltype]
        rel_xp_cumulative = rel_xp_cumulative_data["levels"]
        for _, xp_req in rel_xp_cumulative.items():
            if xp_req < xp:
                min_lvl += 1
        if min_lvl < 0:
            return 0
        if min_lvl >= rel_xp_cumulative_data["details"]["max_level"]:
            return rel_xp_cumulative_data["details"]["max_level"]
        xp_diff = rel_xp_cumulative[min_lvl + 1] - rel_xp_cumulative[min_lvl]
        xp_to_next = rel_xp_cumulative[min_lvl + 1] - xp
        min_lvl_fraction = 1 - (xp_to_next / xp_diff)
        real_level = min_lvl + min_lvl_fraction
        # If skill is level 50, note that and continue (yes im very lazy)
        if real_level > rel_xp_cumulative_data["details"]["max_level"]:
            return rel_xp_cumulative_data["details"]["max_level"]
        return float(real_level)


def parse_timestamp(to_parse: str) -> datetime:
    """Return datetime for given timestamp"""
    if any([x in to_parse for x in ["AM", "PM"]]):
        dt = datetime.strptime(to_parse, DATETIME_FORMAT)
    else:
        dt = datetime.strptime(to_parse, AUC_DATETIME_FORMAT)
    return dt
    # dt = dt.replace(tzinfo=pytz.timezone('America/New_York'))
    # print(dt)
    ##print(datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, tz=pytz.timezone('America/New_York')).strftime(datetime_format))
    # exit(0)
    # return dt.astimezone(tz=None)
