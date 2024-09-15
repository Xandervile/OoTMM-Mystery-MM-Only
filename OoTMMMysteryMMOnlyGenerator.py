import zlib
import base64
import json
import random


MinMysterySettings = 7
MysteryCount = 0
HardCounter = 99

# HarderSettings get rolled first to allow limitations
HARDMODELIMIT = 2

DefaultJunkList = [
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

DefaultHintList = [{"type": "foolish",
                    "amount": 4,
                    "extra": 1},
                   {"type": "woth",
                    "amount": 4,
                    "extra": 1},
                   {"type": "always",
                    "amount": "max",
                    "extra": 1},
                   {"type": "sometimes",
                    "amount": "max",
                    "extra": 1}]

HintToInsertBefore = {"type": "woth",
                      "amount": 4,
                      "extra": 1}

DefaultMoonConditions = {"count": 4,
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

DefaultStartingItems = {
    "MM_OCARINA": 1,
    "MM_SONG_SOARING": 1,
    "MM_SONG_TIME": 1
}

DefaultPlando = {"locations": {}}

def add_location(location_header, location_name, location_value):
    location_header["locations"][location_name] = location_value

while MysteryCount < MinMysterySettings or HardCounter > HARDMODELIMIT:
    MysteryCount = 0
    HardCounter = 0
    HardModeBalance = False
    RemainHunt = False
    FairyHunt = False

    JunkList = DefaultJunkList.copy()
    HintList = DefaultHintList.copy()
    HintIndex = next((i for i, hint in enumerate(HintList) if hint == HintToInsertBefore), None)
    MoonConditions = DefaultMoonConditions.copy()
    StartingItems = DefaultStartingItems.copy()
    Plando = DefaultPlando.copy()

    HintRegions = False

    ChestFairy = "starting"
    StrayFairyRewardCount = 15

    preCompletedDungeons = False
    preCompletedDungeonsRemains = 0

    ModeSettings = random.choices(["Default", "Remains Hunt", "Fairy Hunt"], [0, 15, 0])[0]
    if ModeSettings == "Remains Hunt":
        RemainsHunt = True
        RemainsLocation = "anywhere"
    elif ModeSettings == "Fairy Hunt":
        FairyHunt = True
        RemainsLocation = "anywhere"
        add_location(Plando, "MM Woodfall Great Fairy", "MM_REMAINS_ODOLWA")
        JunkList.remove("MM Woodfall Great Fairy")
        add_location(Plando, "MM Snowhead Great Fairy", "MM_REMAINS_GOHT")
        JunkList.remove("MM Snowhead Great Fairy")
        add_location(Plando, "MM Great Bay Great Fairy", "MM_REMAINS_GYORG")
        JunkList.remove("MM Great Bay Great Fairy")
        add_location(Plando, "MM Ikana Great Fairy", "MM_REMAINS_TWINMOLD")
        JunkList.remove("MM Ikana Great Fairy")
        StartingItems["MM_MASK_GREAT_FAIRY"] = 1
        ChestFairy = "anywhere"
        HardModeBalance = True
    else:
        RemainsLocation = "dungeonbluewarps"
                
    RandomStartingItem = random.choices(
        ["none", "MM_MASK_DEKU", "MM_MASK_GORON", "MM_MASK_ZORA", "MM_MASK_FIERCE_DEITY", "MM_BOW", "MM_HOOKSHOT",
         "MM_BOMB_BAG",
         "MM_MASK_BLAST", "MM_BOTTLE_EMPTY", "MM_MASK_BUNNY", "MM_GREAT_FAIRY_SWORD", "MM_WALLET", "MM_MAGIC_UPGRADE"],
        [0, 10, 10, 10, 10, 10, 10, 5, 5, 10, 5, 5, 10, 0])[0]
    if RandomStartingItem != "none":
        StartingItems[RandomStartingItem] = 1

    RandomStartingSong = random.choices(
        ["MM_RECOVERY_HEART", "MM_SONG_EPONA", "MM_SONG_HEALING", "MM_SONG_STORMS", "MM_SONG_AWAKENING", "MM_SONG_GORON",
         "MM_SONG_ZORA",
         "MM_SONG_EMPTINESS", "MM_SONG_ORDER"], [0, 40, 10, 10, 10, 10, 10, 10, 0])[0] #[0, 40, 10, 10, 10, 10, 10, 10, 0]
    add_location(Plando, "MM Initial Song of Healing", RandomStartingSong)
    if RandomStartingSong == "MM_RECOVERY_HEART":
        JunkList.remove("MM Southern Swamp Song of Soaring")
    if RandomStartingSong == "MM_SONG_ORDER":
        MoonConditions["count"] = 0
        MoonConditions["remains"] = False

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
            StartingClock = \
            random.choices(["MM_CLOCK1", "MM_CLOCK2", "MM_CLOCK3", "MM_CLOCK4", "MM_CLOCK5", "MM_CLOCK6"],
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
        HintRegions = True
        if FreestandingShuffle != False and WonderSpotShuffle != False:
            HardCounter += 1

    PotShuffle = random.choices([True, False], [15, 85])[0]
    if PotShuffle == True:
        HintRegions = True
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
        [35, 20, 15, 30])[0] #[35, 20, 15, 30]
    if LongQuest != "none" and LongQuest in JunkList:
        JunkList.remove(LongQuest)
        if LongQuest == "MM Laboratory Zora Song":
            JunkList.append("MM Clock Tower Roof Skull Kid Song of Time")
            JunkList.append("MM Clock Tower Roof Skull Kid Ocarina")

    OverworldER = ["none", False]
    InteriorER = ["none", False]
    RegionsER = "none"
    # Overworld and Interior ER last because screw it
    EntranceRandomizer = \
        random.choices(["none", "Regions Only", "Exterior Only", "Interior Only", "All"], [70, 15, 6, 6, 3])[0] #[70, 15, 6, 6, 3]
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
    SongShuffle = random.choices(["songLocations", "anywhere"], [65, 35])[0] #[65, 35]
    if SongShuffle == "anywhere":
        MysteryCount += 1
        if "MM Southern Swamp Song of Soaring" in JunkList:
            JunkList.remove("MM Southern Swamp Song of Soaring")
        if "MM Clock Tower Roof Skull Kid Song of Time" not in JunkList:
            JunkList.append("MM Clock Tower Roof Skull Kid Song of Time")
            JunkList.append("MM Clock Tower Roof Skull Kid Ocarina")

    TownFairy = "vanilla"
    FairyWeight = [70, 30]
    if FairyHunt == True:
        FairyWeight = [0, 100]
    StrayFairyShuffle = random.choices(["removed", "anywhere"], FairyWeight)[0]
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
        HintRegions = True
        MysteryCount += 1

    GrottoShuffle = random.choices(["none", "full"], [80, 20])[0]
    if GrottoShuffle == "full":
        MysteryCount += 1

    OwlWeight = [10, 90]
    if EntranceRandomizer == "full" or "Exterior Only":
        OwlWeight = [0, 100]
    OwlShuffle = random.choices(["anywhere", "none"], OwlWeight)[0]
    if OwlShuffle == "anywhere":
        MysteryCount += 1
        StartingItems["MM_OWL_CLOCK_TOWN"] = 1

    WalletShuffleWeight = [30, 70]
    if RandomStartingItem == "MM_WALLET":
        WalletShuffleWeight[1] += WalletShuffleWeight[0]
        WalletShuffleWeight[0] = 0
    NoWalletShuffle = random.choices([True, False], WalletShuffleWeight)[0]
    if NoWalletShuffle == True:
        MysteryCount += 1

    if HardCounter >= HARDMODELIMIT and HardModeBalance == True:
        if FairyHunt == False:
            preCompletedDungeons = True
            preCompletedDungeonsRemains = random.choices([1, 2], [80, 20])[0]
        else:  
            StrayFairyRewardCount= 10

# Rest of the settings are not stored already so are randomised here. To add:
settings_data = {
    "games": "mm",
    "goal": "majora",
    "extraHintRegions": HintRegions,
    "hintImportance": True,
    "songs": SongShuffle,
    "housesSkulltulaTokens": SkulltulaShuffle,
    "tingleShuffle": "starting",
    "mapCompassShuffle": "starting",
    "smallKeyShuffleMm": SKeyShuffle,
    "bossKeyShuffleMm": BKeyShuffle,
    "townFairyShuffle": TownFairy,
    "strayFairyChestShuffle": ChestFairy,
    "strayFairyOtherShuffle": StrayFairyShuffle,
    "dungeonRewardShuffle": RemainsLocation,
    "scrubShuffleMm": ScrubShuffle,
    "cowShuffleMm": SharedCowShuffle,
    "shopShuffleMm": SharedShopShuffle,
    "owlShuffle": OwlShuffle,
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
    "strayFairyRewardCount": StrayFairyRewardCount,
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
    "plando": Plando,
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
#print(HardCounter)
#print(MysteryCount)

#seed_string ="v1.eJztV8GOo0gM/RXEYffSh93VnPpGCJ1kQ0IE9EYzoxaqgJMwKcqoqmgGtebfxwUJkHTvSHPpU1+S4tnlctnPxrzYB1aAsu/torDv7AMybtbsG0pGz8dc6EVRotRMpGDfa1nBna1zceAQHav9nhNoK82kwWhDwUoXi5Ip9aZ4h0otoTnLVgVJJRT4DBkJlZaseWC5bNwjKP2mgUEn0EeQg85gJqvEAVCEUDOZDQpMNDXtAGMkldVu5EN3qxTrV5g6Yjl2dl9xTgaw5m8b7sBIYL1jnKuxoc4IyPTIhB5JUg5MRpppmHaOtzKKlD628TSZcI85zwhMK6XR5GkvAaKUSUgl1oOtothIcFKdP5O5LKg5JfbF1k1p/BQojI/PjFcm4V/pZExPGmthP/0gP1SRRie6n644650j0MX68ngCKBcaChWCAn1B90zpFVMn1QM5XROmkOvGuQSnF3G+pdCA7rVLiQcJSuXPMEOJwicf2K4xeW951tJGaw4uCg1i4EWfIqnniCda6FFYTchuTkqRE//YrQM7LHbpsZqwwyhfJXD+kEu4gba5yG4gn3g3QDtErRZ0jRtoTlpywHQl8rS97g32hdI9OiBlHMY00hLEQR8HhIPITVDK/GSyumdcEQpyJilmqAbOggzhkBO9BuhSV21KDVNWq2QSxLHvJd5qE3+27/++M1g0X3j+NJl7YXCBAtcJF2un19gG4bR/CNYz+jEKsyssXqy83sDWT1w/cJdJHGzXhBIFv1Xi5GPKdOfmV9KzpnCqrA1nzUFiJTKrK2vL4dyaskbZxpg1k8C0NWHNedU2iE40J9Y31h+kLDld9e39ixMT7PVen+0oGxplY5m0WBG2PYgkK0RhPbQ0t1qeW6YAOlmQAhMWJSQDScdXCqyOcJ3YNIcjsOz1cRFWpqfR3poVZXuahXv6ZzK/HBxpqllrg9paCGG5WJUc/lSj0897x6cboTEUy6rtKaQVU9VbDvUioLudQ/JPJ9pS65BEI26FjKwoawKMqEtPdNeLDmLWqozv8EQMlnl6Omcu8f5z1smDEwah1+5KfG8ddat1kESeMw/C6CwK1l6ycqJlEsVmSZTwwk6ycXzH9ZKJR8ai5WJjn+n0GBMdCdo6q00SueHjJJlvklkQButOJX5cL9zzeV+C0Enmju8PmuTC1Fs+Gq+pitOccWovWVsFk3AxnXlmlRLlqM39ZUqFeDTUVwEZXb+j6RmiFxDLR8/K9FI1Q9O4r6A2QzdYy5ke21M8c1Dbh1skmt8is8krnfgKaUyqB79Nm6Y+QC1eXoOxZELtURbXcIC6Byi7pGDGgDOQIl04hOwaIE6AuIYm9Mq5Rj5T4zTvlRaj0l8FlLch4p9+K+Ln3vgR8N8IOFVV9EHx94z4zFkH62Sy/Ij6uzYW519q/h+t5d1CTjEvORMZmpjzYZp7aQctkWt61fazzRyYmcpoJL3MiN4moLHSWDHfnmaW6D9g9og8V2aCYUWfS/hOX4Tt+Njr1d2n06+VGK+78e+iRjH6br+pqrAAnZuv5P/XfvrxE2v0SG4="
# Remove the 'v1.' prefix
if seed_string.startswith('v1.'):
   seed_string = seed_string[3:]

# Add padding back if needed
seed_string += '=' * (-len(seed_string) % 4)

# Base64 decode
decoded_bytes = base64.urlsafe_b64decode(seed_string)

# Decompress using zlib
decompressed_bytes = zlib.decompress(decoded_bytes)

# Convert bytes to JSON string
settings_json = decompressed_bytes.decode('utf-8')

# Parse the JSON string into Python dictionary
settings_data = json.loads(settings_json)

# Print the result
print(settings_data)
