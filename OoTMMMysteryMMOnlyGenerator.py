import zlib
import base64
import json
import random

MinMysterySettings = 7
MysteryCount = 0
HardModeBalance = False

# HarderSettings get rolled first to allow limitations
HARDMODELIMIT = 2

HintToInsertBefore = {"type": "woth",
                    "amount": 4,
                    "extra": 1}

while MysteryCount < MinMysterySettings:
    MysteryCount = 0
    HardCounter = 99

    JunkList = [
        "MM Deku Playground Reward All Days",
        "MM Great Bay Great Fairy",
        "MM Honey & Darling Reward All Days",
        "MM Ikana Great Fairy",
        "MM Laboratory Zora Song",
        "MM Moon Fierce Deity Mask",
        "MM Mountain Village Frog Choir HP",
        "MM Ocean Spider House Wallet",
        "MM Southern Swamp Song of Soaring",
        "MM Snowhead Great Fairy",
        "MM Stock Pot Inn Couple\'s Mask",
        "MM Swamp Spider House Mask of Truth",
        "MM Town Archery Reward 2",
        "MM Waterfall Rapids Beaver Race 2",
        "MM Woodfall Great Fairy"]

    HintList = [{"type": "foolish",
                 "amount": 4,
                 "extra": 1},
                {"type": "always",
                 "amount": "max",
                 "extra": 1},
                {"type": "sometimes",
                 "amount": 3,
                 "extra": 1},
                {"type": "woth",
                 "amount": 4,
                 "extra": 1},
                {"type": "sometimes",
                 "amount": "max",
                 "extra": 1}]

    HintIndex = next((i for i, hint in enumerate(HintList) if hint == HintToInsertBefore), None)

    MoonConditions = {"count": 4,
                      "stones": False,
                      "medallions": False,
                      "remains": True,
                      "skullsGold": False,
                      "skullsSwamp": False,
                      "skullsOcean": False,
                      "fairiesWF": False,
                      "fairiesSH": False,
                      "fairiesGB": False,
                      "fairiesST": False,
                      "fairyTown": False,
                      "masksRegular": False,
                      "masksTransform": False,
                      "masksOot": False,
                      "triforce": False,
                      "coinsRed": False,
                      "coinsGreen": False,
                      "coinsBlue": False,
                      "coinsYellow": False}

    StartingItems = {
        "MM_OCARINA": 1,
        "MM_SONG_SOARING": 1,
        "MM_SONG_TIME": 1
    }

    preCompletedDungeons = False
    preCompletedDungeonsRemains = 0

    RandomStartingItem = random.choices(
        ["none", "MM_MASK_DEKU", "MM_MASK_GORON", "MM_MASK_ZORA", "MM_MASK_DEITY", "MM_BOW", "MM_HOOKSHOT", "MM_BOMB_BAG",
         "MM_MASK_BLAST", "MM_BOTTLE_EMPTY", "MM_MASK_BUNNY", "MM_GREAT_FAIRY_SWORD", "MM_MAGIC_UPGRADE"],
        [5, 10, 10, 10, 10, 10, 10, 5, 5, 10, 5, 5, 5])[0]
    if RandomStartingItem != "none":
        StartingItems[RandomStartingItem] = 1
    RandomStartingSong = random.choices(
        ["none", "MM_SONG_EPONA", "MM_SONG_HEALING", "MM_SONG_STORMS", "MM_SONG_AWAKENING", "MM_SONG_GORON", "MM_SONG_ZORA",
         "MM_SONG_EMPTINESS", "MM_SONG_ORDER"], [0, 40, 10, 10, 10, 10, 10, 10, 0])[0]
    if RandomStartingSong == "none":
        JunkList.remove("MM Southern Swamp Song of Soaring")
    if RandomStartingSong == "MM_SONG_ORDER":
        MoonConditions["count"] = 0
        MoonConditions["remains"] = False

    while HardCounter > HARDMODELIMIT:
        HardCounter = 0

        GrassShuffleWeight = [10, 90]
        GrassShuffle = random.choices([True, False], GrassShuffleWeight)[0]
        if GrassShuffle == True:
            HardCounter += 1
            MysteryCount += 1

        SKeyShuffleWeight = [60, 30, 10]
        SKeyShuffle = random.choices(["removed", "ownDungeon", "anywhere"], SKeyShuffleWeight)[0]
        BKeyShuffleWeight = [60, 30, 10]
        BKeyShuffle = random.choices(["removed", "ownDungeon", "anywhere"], BKeyShuffleWeight)[0]
        if SKeyShuffle != "removed" or BKeyShuffle != "removed":
            MysteryCount += 1
            if (SKeyShuffle == "anywhere" and BKeyShuffle == "anywhere"):
                HardCounter += 1

        ClockProgressiveSetting = "separate"
        ClockShuffle = random.choices([True, False], [10, 90])[0]
        if ClockShuffle == True:
            HardCounter += 1
            MysteryCount += 1
            ClockProgressiveSetting = random.choices(["ascending", "descending", "separate"], [20, 30, 50])[0]
            if ClockProgressiveSetting == "separate":
                StartingClock = random.choices(["MM_CLOCK1", "MM_CLOCK2", "MM_CLOCK3", "MM_CLOCK4", "MM_CLOCK5", "MM_CLOCK6"],
                               [10, 10, 10, 10, 10, 10])[0]
                StartingItems[StartingClock] = 1
                if StartingClock != "MM_CLOCK6":
                    HintList.insert(HintIndex, {"type": "item",
                                                "amount": 1,
                                                "extra": 1,
                                                "item": "MM_CLOCK6"})

        BossSoulsWeight = [10, 90]
        if BKeyShuffle == "anywhere":  # Having both Boss Souls and BK anywhere sounds like hell
            BossSoulsWeight[1] += BossSoulsWeight[0]
            BossSoulsWeight[0] = 0
        SharedBossSoulShuffle = random.choices([True, False], BossSoulsWeight)[0]
        if SharedBossSoulShuffle == True:
            HardCounter += 1
            MysteryCount += 1

        FreestandingShuffle = random.choices([True, False], [20, 80])[0]
        WonderSpotShuffle = random.choices([True, False], [20, 80])[0]
        if FreestandingShuffle != False or WonderSpotShuffle != False:
            MysteryCount += 1
            if FreestandingShuffle != False and WonderSpotShuffle != False:
                HardCounter += 1

        PotShuffle = random.choices([True, False], [15, 85])[0]
        if PotShuffle == True:
            MysteryCount += 1
            HardCounter += 1
            JunkList.append("MM Goron Race Reward")

        FriendSoulShuffle = False
        EnemySoulShuffle = False
        SoulShuffle = random.choices(["none", "friends", "enemies", "both"], [85, 5, 10, 0])[0]
        if SoulShuffle != "none":
            MysteryCount += 1
            HardCounter += 1
            if SoulShuffle == "friends":
                FriendSoulShuffle = True
            elif SoulShuffle == "enemies":
                EnemySoulShuffle = True
            else:
                FriendSoulShuffle = True
                EnemySoulShuffle = True

        LongQuest = random.choices(
            ["none", "MM Stock Pot Inn Couple\'s Mask", "MM Laboratory Zora Song", "MM Mountain Village Frog Choir HP"],
            [35, 20, 15, 30])[0]
        if LongQuest != "none" and LongQuest in JunkList:
            JunkList.remove(LongQuest)
            JunkList.append("MM Clock Tower Roof Skull Kid Song of Time")
            JunkList.append("MM Clock Tower Roof Skull Kid Ocarina")

        OverworldER = ["none", False]
        InteriorER = ["none", False]
        RegionsER = "none"
        # Overworld and Interior ER last because screw it
        EntranceRandomizer = \
        random.choices(["none", "Regions Only", "Exterior Only", "Interior Only", "All"], [70, 15, 6, 6, 3])[0]
        if EntranceRandomizer == "Regions Only":  # Not Hard due to only 5 entrances shuffling
            MysteryCount += 1
            RegionsER = "full"
        elif EntranceRandomizer == "Exterior Only":
            MysteryCount += 1
            HardCounter += 1
            OverworldER = ["full", True]
        elif EntranceRandomizer == "Interior Only":
            MysteryCount += 1
            HardCounter += 1
            InteriorER = ["full", True]
        elif EntranceRandomizer == "All":
            MysteryCount += 1
            HardCounter += 1
            OverworldER = ["full", True]
            InteriorER = ["full", True]

        # To add: Decoupled? - This would by itself make the Hard Counter explode
        # Also to add: Mixed?

    # Other Settings get Randomized here
    SongShuffle = random.choices(["songLocations", "anywhere"], [65, 35])[0]
    if SongShuffle == "anywhere":
        MysteryCount += 1
        if "MM Southern Swamp Song of Soaring" in JunkList:
            JunkList.remove("MM Southern Swamp Song of Soaring")
        if "MM Clock Tower Roof Skull Kid Song of Time" not in JunkList:
            JunkList.append("MM Clock Tower Roof Skull Kid Song of Time")
            JunkList.append("MM Clock Tower Roof Skull Kid Ocarina")

    TownFairy = "vanilla"
    StrayFairyShuffle = random.choices(["removed", "anywhere"], [70, 30])[0]
    if StrayFairyShuffle != "removed":
        MysteryCount += 1
        TownFairy = "anywhere"

    NoStartingWeapon = random.choices([True, False], [25, 75])[0]
    if NoStartingWeapon == False:
        StartingItems["MM_SWORD"] = 1
        StartingItems["MM_SHIELD_HERO"] = 1

    ExtraDungeonEntranceShuffle = False
    erDungeons = random.choices(["none", "full"], [45, 55])[0]
    if erDungeons == "full":
        ExtraDungeonEntranceShuffle = random.choices([True, False], [40, 60])[0]

    BossEntranceShuffle = random.choices(["none", "full"], [70, 30])[0]
    if BossEntranceShuffle == "full" or erDungeons == "full":
        MysteryCount += 1

    ScrubShuffle = False
    SharedShopShuffle = random.choices(["none", "full"], [60, 40])[0]
    if SharedShopShuffle != "none":
        ScrubShuffle = random.choices([True, False], [50, 50])[0]
        MysteryCount += 1

    SharedCowShuffle = random.choices([True, False], [30, 70])[0]
    if SharedCowShuffle == True:
        MysteryCount += 1

    SharedCratesAndBarrels = random.choices([True, False], [30, 70])[0]
    if SharedCratesAndBarrels == True:
        MysteryCount += 1

    SnowballWeight = [20, 80]
    if ClockShuffle == True:
        SnowballWeight = [5, 95]
    SnowballShuffle = random.choices([True, False], SnowballWeight)[0]
    if SnowballShuffle == True:
        MysteryCount += 1

    SkulltulaShuffle = random.choices(["none", "all"], [80, 20])[0]
    if SkulltulaShuffle == "all":
        MysteryCount += 1

    GrottoShuffle = random.choices(["none", "full"], [20, 80])[0]
    if GrottoShuffle == "full":
        MysteryCount += 1

    NoWalletShuffle = random.choices([True, False], [30, 70])[0]
    if NoWalletShuffle == True:
        MysteryCount += 1

    if HardCounter >= HARDMODELIMIT and HardModeBalance == True:
        preCompletedDungeons = True
        preCompletedDungeonsRemains = random.choices([1, 2], [80, 20])[0]

# Rest of the settings are not stored already so are randomised here. To add:
settings_data = {
    "games": "mm",
    "goal": "majora",
    "extraHintRegions": True,
    "hintImportance": True,
    "songs": SongShuffle,
    "housesSkulltulaTokens": SkulltulaShuffle,
    "tingleShuffle": "starting",
    "mapCompassShuffle": "starting",
    "smallKeyShuffleMm": SKeyShuffle,
    "bossKeyShuffleMm": BKeyShuffle,
    "townFairyShuffle": TownFairy,
    "strayFairyChestShuffle": "starting",
    "strayFairyOtherShuffle": StrayFairyShuffle,
    "dungeonRewardShuffle": "dungeonbluewarps",
    "scrubShuffleMm": ScrubShuffle,
    "cowShuffleMm": SharedCowShuffle,
    "shopShuffleMm": SharedShopShuffle,
    "owlShuffle": "none",
    "shufflePotsMm": PotShuffle,
    "shuffleCratesMm": SharedCratesAndBarrels,
    "shuffleBarrelsMm": SharedCratesAndBarrels,
    "shuffleHivesMm": False,
    "shuffleGrassMm": GrassShuffle,
    "shuffleFreeRupeesMm": FreestandingShuffle,
    "shuffleFreeHeartsMm": FreestandingShuffle,
    "shuffleWonderItemsMm": WonderSpotShuffle,
    "shuffleSnowballsMm": SnowballShuffle,
    "shuffleMerchantsMm": ScrubShuffle,
    "fairyFountainFairyShuffleMm": False,
    "clearStateDungeonsMm": "both",
    "beneathWell": "vanilla",
    "majoraChild": "custom",
    "freeScarecrowMm": True,
    "preCompletedDungeons": preCompletedDungeons,
    "preCompletedDungeonsRemains": preCompletedDungeonsRemains,
    "mmPreActivatedOwls": {"type": "none",
                           "values": ["clocktown"]},
    "csmcSkulltula": True,
    "csmcCow": True,
    "keepItemsReset": True,
    "fastMasks": True,
    "fierceDeityAnywhere": True,
    "hookshotAnywhereMm": "off",
    "climbMostSurfacesMm": False,
    "fillWallets": True,
    "progressiveGoronLullaby": "single",
    "progressiveClocks": ClockProgressiveSetting,
    "bottleContentShuffle": True,
    "shortHookshotMm": True,
    "childWallets": NoWalletShuffle,
    "colossalWallets": True,
    "bombchuBagMm": True,
    "spellFireMm": True,
    "spellWindMm": True,
    "spellLoveMm": True,
    "bootsIronMm": True,
    "bootsHoverMm": True,
    "tunicGoronMm": True,
    "tunicZoraMm": True,
    "scalesMm": True,
    "strengthMm": True,
    "soulsEnemyMm": EnemySoulShuffle,
    "soulsBossMm": SharedBossSoulShuffle,
    "soulsNpcMm": FriendSoulShuffle,
    "soulsMiscMm": False,
    "clocks": ClockShuffle,
    "lenientSpikes": False,
    "erBoss": BossEntranceShuffle,
    "erDungeons": erDungeons,
    "erGrottos": GrottoShuffle,
    "erMixed": "none",
    "erMixedDungeons": False,
    "erMixedOverworld": False,
    "erMixedIndoors": False,
    "erMixedGrottos": False,
    "erMajorDungeons": erDungeons == "full",
    "erSpiderHouses": ExtraDungeonEntranceShuffle,
    "erPirateFortress": ExtraDungeonEntranceShuffle,
    "erBeneathWell": ExtraDungeonEntranceShuffle,
    "erIkanaCastle": ExtraDungeonEntranceShuffle,
    "erSecretShrine": ExtraDungeonEntranceShuffle,
    "erRegions": RegionsER,
    "erOverworld": OverworldER[0],
    "erIndoors": InteriorER[0],
    "erIndoorsMajor": InteriorER[1],
    "erIndoorsExtra": InteriorER[1],
    "erOneWays": False,
    "erOneWaysMajor": False,
    "erOneWaysIkana": False,
    "erOneWaysAnywhere": False,
    "startingItems": StartingItems,
    "junkLocations": JunkList,
    "tricks": ["MM_EVAN_FARORE",
               "MM_LENS",
               "MM_NO_SEAHORSE",
               "MM_ONE_MASK_STONE_TOWER",
               "MM_PALACE_BEAN_SKIP",
               "MM_SOUTHERN_SWAMP_SCRUB_HP_GORON",
               "MM_TUNICS",
               "MM_ZORA_HALL_SCRUB_HP_NO_DEKU"
               ],
    "specialConds": {
        "MOON": MoonConditions,
        "MAJORA": {"count": 4,
                   "stones": False,
                   "medallions": False,
                   "remains": True,
                   "skullsGold": False,
                   "skullsSwamp": False,
                   "skullsOcean": False,
                   "fairiesWF": False,
                   "fairiesSH": False,
                   "fairiesGB": False,
                   "fairiesST": False,
                   "fairyTown": False,
                   "masksRegular": False,
                   "masksTransform": False,
                   "masksOot": False,
                   "triforce": False,
                   "coinsRed": False,
                   "coinsGreen": False,
                   "coinsBlue": False,
                   "coinsYellow": False}},
    "plando": {"locations": {"MM Initial Song of Healing":RandomStartingSong}},
    "hints": HintList,
}

# Convert the settings into a JSON string (or similar format if required)
settings_json = json.dumps(settings_data)

# Compress the settings using zlib
compressed_data = zlib.compress(settings_json.encode())

# Base64 encode the compressed data
encoded_data = base64.urlsafe_b64encode(compressed_data).decode()

# Remove any unnecessary padding (optional, as the decoder will usually handle it)
encoded_data = encoded_data.rstrip("=")

# Format the final seed string (prepend 'v1.' to the encoded string)
seed_string = f"v1.{encoded_data}"

# Output the result
print("Encoded Seed String:")
print(seed_string)

# seed_string = "v1.eJztV0uP4jgQ/itWDruXPuzr1LcAgbANBCX0oJ1RKzJJARkcV2Q7zUSj+e9bzhNodqW59Kkv4HxVLpe/etj+7hx4Dtp5dPLceXAOyIUd86+oOH3DN6O4n0kTwiFDSXpGlfDgHAma5wUqw2UCHWoyeRAQHcv9XhDoaMOVxchQzosx5gXX+q5Y51yIJ6ha4TInsYIcXyEl6Q61/k+hwbOc8kxVg2Euq/MRFFjD5H9Vi8dH0Ob+4r1OYGjaXTsJni+Wb7arGyCSeN6R+3qQJAK4igw3MCnlAYi42ukdmmPNhWV3fMxESmBSaoOW+70CiBKuIFF4Hmzl+VqBm5jslcylwVlQEL47piqshxKl9e6Vi9IG8QutjMnJUuK8/CA/dJ5Ep1IIUwreO0fgGM/d5wmgmBvIdQgaTIfuuTZLrk99xPcZqAQmkJnK7WjpRUJsiQAwvXah8KBA6+wVZqhQLsgHvqss73WO1EE1RsAYpQE5xKVjljLLRzzRwFzQaim7WSlBQdnBbx3YYb5LjuWIHy7iVYAQ00zBDbTNZHoDLSi5BmiHaPSctnED+aSlBsyUMkvq7d5gnyncFwskXMBFslD6gTyY4wWCpdAj2tYNtCqSAREgM8tckZ1s6PdcaEJB2XnE854YtwWsZoqIxguoy/w66DaXlst46UZP8SwIg5Xz+PuDRSJ/7i0mse+FQQcFYzecr9xeYxuEk/4jWM3oxyrMrrDNfOkRQMn4tZSnBSbcNI3kC6mwCZxKtha8OigsZcpCOHOVMlcINuGVdqwdVlPKQp5AK29hBdywEa/aUV3BjcinsqjYL2RDCdrpfbPzE5f87dwF31G4DKqK2bixCOsmQZIlkhvTug5YXQjMVkgnK6XhmWSfqBj4AdiUKoCNj5gp5q8bnSABLhkFLAUCsdTAmqxtxLaPHIGnb12KsLSNieaeeV7UHjHc0z9XWedcZKjw2RoNm0vJxlgWAn7VFx62cy9Xt0JraKPKujGR1oZaB3NVQstVHW1/NKIt9R9FaSYoFGRFsxFwyv8mMJ0OYlqrXO7hhcpAZcmpDXrsfXJX8dQNg9CrZ8ULbxU1o1UQR57rB2HUioKV1yRntLHDTbD1wkaydhfu2ItHHhmLnuYNx5RzzxvKWYK27nIdR+PweRT76za3a5XN82o+btf7HIRu7LuLxaBJLky8p2frNbWCJOOCelRaF8oonE9mnh0lNtzO42+2mijXhvrLIaXtNxneQnRUUWIM39o2ZD1D2/2voDpCN1idMz22Jz4z0NvpLRL5t8hs9EZnc4VUNtSD37bX0yFP54S6BjeKS71HlV/DAZoeoOiSgr0HtECCtOEQ0muAcgLkNTSic+sa+Ye6rz2caoy6xjKwPaln/K+fYrztnR+E/wThVFXRR4q/J+MzdxWs4tHTB+vv2ljcv6n5f7SWd6OcOC8ElylazsVwEfxeX8ZkZuio7e82PnB7c6Nba3+53AThMnKsGfv6tJeJ/hm0RxSZtlcYnvfBrN+u9dWz1+Pi3Fz/OjXa/zfnrqrGHExmn8aD9p93Nc/Nq+7/V75n7nbxlx//AsJDX6g="
# Remove the 'v1.' prefix
#if seed_string.startswith('v1.'):
#    seed_string = seed_string[3:]

# Add padding back if needed
#seed_string += '=' * (-len(seed_string) % 4)

# Base64 decode
#decoded_bytes = base64.urlsafe_b64decode(seed_string)

# Decompress using zlib
#decompressed_bytes = zlib.decompress(decoded_bytes)

# Convert bytes to JSON string
#settings_json = decompressed_bytes.decode('utf-8')

# Parse the JSON string into Python dictionary
#settings_data = json.loads(settings_json)

# Print the result
#print(settings_data)
