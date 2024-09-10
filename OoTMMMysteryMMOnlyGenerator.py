import zlib
import base64
import json
import random

MinMysterySettings = 5
MysteryCount = 0
HardModeReached = False

#HarderSettings get rolled first to allow limitations
HARDMODELIMIT = 2

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

HintList = [{"type":"foolish",
"amount":8,
"extra":1},
{"type":"always",
"amount":"max",
"extra":1},
{"type":"sometimes",
"amount":3,
"extra":1},
{"type":"item",
"amount":1,
"extra":1,
"item":"MM_SONG_ORDER"},
{"type":"playthrough",
"amount":4,
"extra":1},
{"type":"woth",
"amount":9,
"extra":1},
{"type":"sometimes",
"amount":"max",
"extra":1}]

HintToInsertBefore = {"type":"playthrough",
"amount":4,
"extra":1}

HintIndex = next((i for i, hint in enumerate(HintList) if hint == HintToInsertBefore), None)

MoonConditions = {"count":4,
"stones":False,
"medallions":False,
"remains":True,
"skullsGold":False,
"skullsSwamp":False,
"skullsOcean":False,
"fairiesWF":False,
"fairiesSH":False,
"fairiesGB":False,
"fairiesST":False,
"fairyTown":False,
"masksRegular":False,
"masksTransform":False,
"masksOot":False,
"triforce":False,
"coinsRed":False,
"coinsGreen":False,
"coinsBlue":False,
"coinsYellow":False}

StartingItems = {
"MM_OCARINA":1,
"MM_SONG_SOARING":1,
    }

RandomStartingItem = random.choices(["none", "MM_MASK_DEKU", "MM_MASK_GORON", "MM_MASK_ZORA", "MM_MASK_DEITY", "MM_BOW", "MM_HOOKSHOT", "MM_BOMB_BAG", "MM_MASK_BLAST", "MM_BOTTLE_EMPTY", "MM_MASK_BUNNY", "MM_GREAT_FAIRY_SWORD", "MM_MAGIC_UPGRADE"], [5,10,10,10,10,10,10,5,5,10,5,5,5])[0]
if RandomStartingItem != "none":
    StartingItems[RandomStartingItem] = 1
RandomStartingSong = random.choices(["none", "MM_SONG_EPONA", "MM_SONG_HEALING", "MM_SONG_STORMS", "MM_SONG_AWAKENING", "MM_SONG_GORON", "MM_SONG_ZORA", "MM_SONG_EMPTINESS", "MM_SONG_ORDER"], [0,40,10,10,10,10,10,10,0])[0]
if RandomStartingSong != "none":
    StartingItems[RandomStartingSong] = 1
    if RandomStartingSong == "MM_SONG_ORDER":
        HintList.remove({"type":"item",
            "amount":1,
            "extra":1,
            "item":"MM_SONG_ORDER"})
        MoonConditions["count"] = 0
        MoonConditions["remains"] = False


while MysteryCount < MinMysterySettings:
    MysteryCount = 0
    HardCounter = 99

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
                StartingClock = random.choices(["MM_CLOCK1", "MM_CLOCK2", "MM_CLOCK3", "MM_CLOCK4", "MM_CLOCK5", "MM_CLOCK6"], [10, 10, 10, 10, 10, 10])[0]
                StartingItems[StartingClock] = 1
                if StartingClock != "MM_CLOCK6":
                    HintList.insert(HintIndex, {"type":"item",
                        "amount":1,
                        "extra":1,
                        "item":"MM_CLOCK6"})



        BossSoulsWeight = [10, 90]
        if BKeyShuffle == "anywhere":                                               #Having both Boss Souls and BK anywhere sounds like hell
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
            JunkList.append("MM Goron Race")
            

        FriendSoulShuffle = random.choices([True, False], [8, 92])[0]
        if FriendSoulShuffle == True:
            MysteryCount += 1
            HardCounter += 1
            
        LongQuest = random.choices(["none", "MM Stock Pot Inn Couple\'s Mask", "MM Laboratory Zora Song", "MM Mountain Village Frog Choir HP"], [35, 20, 15, 30])[0]
        if LongQuest != "none" and LongQuest in JunkList:
            JunkList.remove(LongQuest)

        
        OverworldER = ["none", False]
        InteriorER = ["none", False]
        RegionsER = "none"
        #Overworld and Interior ER last because screw it
        EntranceRandomizer = random.choices(["none", "Regions Only", "Exterior Only", "Interior Only", "All"], [80, 10, 4, 4, 2])[0]
        if EntranceRandomizer == "Regions Only":            #Not Hard due to only 5 entrances shuffling
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
            
        #To add: Decoupled? - This would by itself make the Hard Counter explode
        #Also to add: Mixed?
        

    #Other Settings get Randomized here
    SongShuffle = random.choices(["songLocations", "anywhere"], [65, 35])[0]
    if SongShuffle == "anywhere":
        MysteryCount += 1

    StrayFairyShuffle = random.choices(["removed","anywhere"], [70, 30])[0]
    if StrayFairyShuffle != "removed":
        MysteryCount += 1
            
    NoStartingWeapon = random.choices([True, False], [25, 75])[0]
    if NoStartingWeapon == False:
        StartingItems["MM_SWORD"] = 1
        StartingItems["MM_SHIELD_HERO"] = 1

    ExtraDungeonEntranceShuffle = False
    erDungeons = random.choices(["none", "full"], [45, 55])[0]
    if erDungeons == "full":
        ExtraDungeonEntranceShuffle = random.choices([True, False], [50, 50])[0]

    BossEntranceShuffle = random.choices(["none","full"],[70, 30])[0]
    if BossEntranceShuffle == "full" or erDungeons == "full":
        MysteryCount += 1

    ScrubShuffle = False
    SharedShopShuffle = random.choices(["none", "full"],[60, 40])[0]
    if SharedShopShuffle != "none":
        ScrubShuffle = random.choices([True, False], [50, 50])[0]
        MysteryCount += 1
        
    SharedCowShuffle = random.choices([True, False],[30, 70])[0]
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
        

        

# Rest of the settings are not stored already so are randomised here. To add: 
settings_data = {
"games":"mm",
"goal":"majora",
"extraHintRegions":True,
"hintImportance":True,
"songs":SongShuffle,
"housesSkulltulaTokens":SkulltulaShuffle,
"tingleShuffle":"starting",
"mapCompassShuffle":"starting",
"smallKeyShuffleMm":SKeyShuffle,
"bossKeyShuffleMm":BKeyShuffle,
"townFairyShuffle":"vanilla",
"strayFairyChestShuffle":"starting",
"strayFairyOtherShuffle":StrayFairyShuffle,
"dungeonRewardShuffle":"dungeonbluewarps",
"scrubShuffleMm":ScrubShuffle,
"cowShuffleMm":SharedCowShuffle,
"shopShuffleMm":SharedShopShuffle,
"owlShuffle":"none",
"shufflePotsMm":PotShuffle,
"shuffleCratesMm":SharedCratesAndBarrels,
"shuffleBarrelsMm":SharedCratesAndBarrels,
"shuffleHivesMm":False,
"shuffleGrassMm":GrassShuffle,
"shuffleFreeRupeesMm":FreestandingShuffle,
"shuffleFreeHeartsMm":FreestandingShuffle,
"shuffleWonderItemsMm":WonderSpotShuffle,
"shuffleSnowballsMm":SnowballShuffle,
"shuffleMerchantsMm":ScrubShuffle,
"fairyFountainFairyShuffleMm":False,
"clearStateDungeonsMm":"both",
"beneathWell":"vanilla",
"majoraChild":"custom",
"freeScarecrowMm":True,
"mmPreActivatedOwls":{"type":"none",
"values":["clocktown"]},
"csmcSkulltula":True,
"csmcCow":True,
"keepItemsReset":True,
"fastMasks":True,
"fierceDeityAnywhere":True,
"hookshotAnywhereMm":"off",
"climbMostSurfacesMm":False,
"fillWallets":True,
"progressiveGoronLullaby":"single",
"progressiveClocks":ClockProgressiveSetting,
"bottleContentShuffle":True,
"shortHookshotMm":True,
"childWallets":NoWalletShuffle,
"colossalWallets":True,
"bombchuBagMm":True,
"spellFireMm":True,
"spellWindMm":True,
"spellLoveMm":True,
"bootsIronMm":True,
"bootsHoverMm":True,
"tunicGoronMm":True,
"tunicZoraMm":True,
"scalesMm":True,
"strengthMm":True,
"soulsEnemyMm":False,
"soulsBossMm":SharedBossSoulShuffle,
"soulsNpcMm":FriendSoulShuffle,
"soulsMiscMm":False,
"clocks":ClockShuffle,
"lenientSpikes":False,
"erBoss":BossEntranceShuffle,
"erDungeons":erDungeons,
"erGrottos":GrottoShuffle,
"erMixed":"none",
"erMixedDungeons":False,
"erMixedOverworld":False,
"erMixedIndoors":False,
"erMixedGrottos":False,
"erMajorDungeons":erDungeons == "full",
"erSpiderHouses":ExtraDungeonEntranceShuffle,
"erPirateFortress":ExtraDungeonEntranceShuffle,
"erBeneathWell":ExtraDungeonEntranceShuffle,
"erIkanaCastle":ExtraDungeonEntranceShuffle,
"erSecretShrine":ExtraDungeonEntranceShuffle,
"erRegions": RegionsER,
"erOverworld":OverworldER[0],
"erIndoors":InteriorER[0],
"erIndoorsMajor":InteriorER[1],
"erIndoorsExtra":InteriorER[1],
"erOneWays":OverworldER[0],
"erOneWaysMajor":OverworldER[1],
"erOneWaysIkana":OverworldER[1],
"erOneWaysAnywhere":OverworldER[1],
"startingItems":StartingItems,
"junkLocations":JunkList,
"tricks":["MM_EVAN_FARORE",
"MM_LENS",
"MM_NO_SEAHORSE",
"MM_ONE_MASK_STONE_TOWER",
"MM_PALACE_BEAN_SKIP",
"MM_SOUTHERN_SWAMP_SCRUB_HP_GORON",
"MM_TUNICS",
"MM_ZORA_HALL_SCRUB_HP_NO_DEKU"
],
"specialConds":{
"MOON": MoonConditions,
"MAJORA":{"count":4,
"stones":False,
"medallions":False,
"remains":True,
"skullsGold":False,
"skullsSwamp":False,
"skullsOcean":False,
"fairiesWF":False,
"fairiesSH":False,
"fairiesGB":False,
"fairiesST":False,
"fairyTown":False,
"masksRegular":False,
"masksTransform":False,
"masksOot":False,
"triforce":False,
"coinsRed":False,
"coinsGreen":False,
"coinsBlue":False,
"coinsYellow":False}},
"plando":{"locations":{"MM Initial Song of Healing":"MM_SONG_TIME"}},
"hints":HintList,
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

seed_string = "v1.eJztV01vo0gQ/SuIw55y2NkdrXZzA4yNN7axwBlrZxShCpTtHjfdVncTD4rmv281GIOdSLu55JQT8OrRVL/66OLZ3UKJ2r11y9K9cbcSuL2H71IBPeMPoyBiwiS4ZVIQz6gKb9wdQdPyIJUBkWOHaim2dikQ9XGHCmkBw8SWY7qrNhtOPFcbUBYjUwmHQJYH0PpVs6Yv12Ngqg52qM1/cGJDH+w5Ckv5hIWltFigwKCel2dXW9gHpZAP8JwjqNQQeVSJLdKWrc19lGbXuGx1CXaMFwTmlTbSqrZRiGkOCnMlj/1aZblU6OWGPdFyRXzkpM2za+qD9VBIYfV5Al5Z+b/Rl2W+N/Io3Ief5Icu83RfcW4qDmfnCAzksXvcIx6mBkudoEbToRvQZg56f47VhqHKcYTM1F4XmLOJ8zVwjubMPii5Vag1e8KJVFLMyAd4rK3uTSjdC0pgnbYh13gAKzGZSStDgkthUPRh62SnlImk3NONGaguudQarn15lOVjvqt82A4Cd0DOx0zhFbRmoriCZpQCPfQopdFT2tEVFBFL9ZipBMubnV9hXynygw/kwC/yySgUW7MbZlIrTfvEUTArx4Htbbg3wDWhqHzaN8m3IZVtuaku64bYRJGi8gKa20Tsue03qAAOrEAVyUrjAF0yG5kxKW+j1uM+CgSzW5NUPTjdg4CAcqgPGq1LmY0US8VEH8pTGTYZaBN7Ps/mXnqX+TMvXbm3n24sksaLSRYu44V3RqJpOBtlUZjEHRQHXjIdMNZxMrpYII0tYUIYlcb3SuxnMgfTNqRvxHJGuK+cJYd6q2QlCifBI6jC8Th3RlBr1y7lTBRt1/GhPt01jaM1RVSNtfMLkRWnPb3+fiPNy3dn8EipYaSqHZsjTiqb3kSWuZTCGTfl5zT159jC7GyVMMCE84VqELbojKmqnGAnmXKiZcuJcwThtEF1mqg6bYW05lRIqmYoXrqUysr2Q3r3COWh8ciRG7qCYp1zJ9Nwceud5a1U1bQ7Yq2oITmeymm1ulPlt9a0pqRSlMjcSYBW0Y6PQKVET7TdjiNl0VCGLj5QRSnWFIcNXhZ+8RbZ2EviJGzeymbhIm3vFnGWhl4UJ+nJFC/CNsvSlb1dxeswaS1Lb+YFYeaHtFh6N20lpMy5X1GqEbT25sssDZJ7P4uW2SRO4kVLWd0vpsHpe1/jxMsibzbrmeTCKLy7t15TV8kZcGptRZPxfjIdTUJ7l9toure/2rKgVOorvMSCtt9m6gmis4ni3j9r2+b1RNoz5QJqInSFNSlxxjakJ0O9Hl8jaXSNTPwXnNUFUttQ937bE4QOfTp91CW4UiD0RqryEo6lOQMUXSLYueAE5JI2nGBxCVBOoLiEfDoNL5F/qDvZI6/BqPrnMcWtV/zzmxQ/da4Pwd8gOFVV+pHi76n4xFvEi8y/+1D9XRuL9zc1/4/W8m6Sk+YHDqKQVnPeD3TPzawlmKGj9jy6RAh2MKMZuJsJV9N56NpF7L+oHSXOv1YbKTnTdoCBsg3ln6c/2WaAPPOAH9vZrqPR7n+4r1K1LNEw+6Pcs39/lcloHB6QPvWkm9bW74CmXBpe3vxuMIuDuz+G75GMtdnR5Lsdbvrzq/4d2z/ZjvTX/97utTgPP/8FtlaZDA=="
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
