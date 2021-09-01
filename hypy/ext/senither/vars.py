dungeon_weights = {
    "catacombs": 0.0002149604615,
    "healer": 0.0000045254834,
    "mage": 0.0000045254834,
    "berserk": 0.0000045254834,
    "archer": 0.0000045254834,
    "tank": 0.0000045254834,
}

slayer_weights = {
    "zombie": {"divr": 2208, "mod": 0.15},
    "spider": {"divr": 2118, "mod": 0.08},
    "wolf": {"divr": 1962, "mod": 0.015},
    "enderman": {"divr": 1430, "mod": 0.017},
}

skill_weights = {
    "mining": {
        "expo": 1.18207448,
        "divr": 259634,
        "lvl_cap": 60,
    },
    "foraging": {
        "expo": 1.232826,
        "divr": 259634,
        "lvl_cap": 50,
    },
    "enchanting": {
        "expo": 0.96976583,
        "divr": 882758,
        "lvl_cap": 60,
    },
    "farming": {
        "expo": 1.217848139,
        "divr": 220689,
        "lvl_cap": 60,
    },
    "combat": {
        "expo": 1.15797687265,
        "divr": 275862,
        "lvl_cap": 60,
    },
    "fishing": {
        "expo": 1.406418,
        "divr": 88274,
        "lvl_cap": 50,
    },
    "alchemy": {
        "expo": 1.0,
        "divr": 1103448,
        "lvl_cap": 50,
    },
    "taming": {
        "expo": 1.14744,
        "divr": 441379,
        "lvl_cap": 50,
    },
}

skills = [
    "fishing",
    "alchemy",
    "taming",
    "enchanting",
    "combat",
    "mining",
    "farming",
    "foraging",
]

slayers = ["wolf", "spider", "zombie", "enderman"]

lvl60 = 111672425
lvl50 = 55172425

lvl50dung = 569809640

classes = ["healer", "berserk", "archer", "mage", "tank", "catacombs"]
