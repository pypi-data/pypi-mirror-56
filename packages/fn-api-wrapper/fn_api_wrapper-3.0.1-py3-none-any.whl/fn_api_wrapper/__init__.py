import requests

FNAPI = "https://fortnite-api.com"
apikey = "Follow @LupusLeaks on Twitter"

def SetItem(self,Item):
    self.id = Item["id"]
    self.type = Item["type"]
    self.backendType = Item["backendType"]
    self.rarity = Item["rarity"]
    self.backendRarity = Item["backendRarity"]
    self.name = Item["name"]
    self.shortDescription = Item["shortDescription"]
    self.description = Item["description"]
    self.set = Item["set"]
    self.series = Item["series"]
    self.backendSeries = Item["backendSeries"]
    self.images = Item["images"]
    self.variants = Item["variants"]
    self.gameplayTags = Item["gameplayTags"]
    self.displayAssetPath = Item["displayAssetPath"]
    self.definition = Item["definition"]
    self.builtInEmoteId = Item["builtInEmoteId"]
    self.requiredItemId = Item["requiredItemId"]
    self.path = Item["path"]
    self.lastUpdate = Item["lastUpdate"]
    self.added = Item["added"]

def getCosmetic(self,params):
    if "id" in params:
        try:
            Cosmetics = requests.get(f"{FNAPI}/cosmetics/br/search/ids", params=params, headers={"x-api-key" : apikey}).json()
        except:
            self.status = 404
            return
    else:
        try:
            Cosmetics = requests.get(f"{FNAPI}/cosmetics/br/search/all", params=params, headers={"x-api-key" : apikey}).json()
        except:
            self.status = 404
            return

    self.status = Cosmetics["status"]
    if Cosmetics["status"] == 200:
        for Cosmetic in Cosmetics["data"]:
            SetItem(self,Cosmetic)
            return

class FortniteAPI:
    def __init__(self,api_key=""):
        global apikey
        apikey = api_key

    class GetSkin:
        def __init__(self,**kwargs):
            params = {"backendType" : "AthenaCharacter"}
            for key, value in kwargs.items():
                params[key] = value

            getCosmetic(self,params)

    class GetBackpack:
        def __init__(self,**kwargs):
            params = {"backendType" : "AthenaBackpack"}
            for key, value in kwargs.items():
                params[key] = value

            getCosmetic(self,params)

    class GetPickaxe:
        def __init__(self,**kwargs):
            params = {"backendType" : "AthenaPickaxe"}
            for key, value in kwargs.items():
                params[key] = value

            getCosmetic(self,params)

    class GetEmote:
        def __init__(self,**kwargs):
            params = {"backendType" : "AthenaDance"}
            for key, value in kwargs.items():
                params[key] = value

            getCosmetic(self,params)

    class GetGlider:
        def __init__(self,**kwargs):
            params = {"backendType" : "AthenaGlider"}
            for key, value in kwargs.items():
                params[key] = value

            getCosmetic(self,params)

    class GetEmoji:
        def __init__(self,**kwargs):
            params = {"backendType" : "AthenaEmoji"}
            for key, value in kwargs.items():
                params[key] = value

            getCosmetic(self,params)

    class GetLoadingScreen:
        def __init__(self,**kwargs):
            params = {"backendType" : "AthenaLoadingScreen"}
            for key, value in kwargs.items():
                params[key] = value

            getCosmetic(self,params)

    class GetContrail:
        def __init__(self,**kwargs):
            params = {"backendType" : "AthenaSkyDiveContrail"}
            for key, value in kwargs.items():
                params[key] = value

            getCosmetic(self,params)

    class GetWrap:
        def __init__(self,**kwargs):
            params = {"backendType" : "AthenaItemWrap"}
            for key, value in kwargs.items():
                params[key] = value

            getCosmetic(self,params)

    class GetMusic:
        def __init__(self,**kwargs):
            params = {"backendType" : "AthenaMusicPack"}
            for key, value in kwargs.items():
                params[key] = value

            getCosmetic(self,params)

    class GetPet:
        def __init__(self,**kwargs):
            params = {"backendType" : "AthenaPetCarrier"}
            for key, value in kwargs.items():
                params[key] = value

            getCosmetic(self,params)

    class GetSpray:
        def __init__(self,**kwargs):
            params = {"backendType" : "AthenaSpray"}
            for key, value in kwargs.items():
                params[key] = value
    
            getCosmetic(self,params)

    class GetToy:
        def __init__(self,**kwargs):
            params = {"backendType" : "AthenaToy"}
            for key, value in kwargs.items():
                params[key] = value

            getCosmetic(self,params)

    class GetBanner:
        def __init__(self,**kwargs):
            params = {"backendType" : "banner"}
            for key, value in kwargs.items():
                params[key] = value

            getCosmetic(self,params)

    class GetBattleRoyaleNews:
        def __init__(self,**kwargs):
            params = {}
            for key, value in kwargs.items():
                params[key] = value
            
            r = requests.get(f"{FNAPI}/news/br", params=params, headers={"x-api-key" : apikey}).json()
    
            self.status = r["status"]
            if r["status"] == 200:
                self.lastModified = r["data"]["lastModified"]
                self.messages = r["data"]["messages"]
                self.images = []
                #self.Image = CreateNewsImageFN

                for Message in r["data"]["messages"]:
                    self.images.append(Message["image"])

    class GetCreativeNews:
        def __init__(self,**kwargs):
            params = {}
            for key, value in kwargs.items():
                params[key] = value
            
            r = requests.get(f"{FNAPI}/news/creative", params=params, headers={"x-api-key" : apikey}).json()
    
            self.status = r["status"]
            if r["status"] == 200:
                self.lastModified = r["data"]["lastModified"]
                self.messages = r["data"]["messages"]
                self.images = []

                for Message in r["data"]["messages"]:
                    self.images.append(Message["image"])
    
    class GetSaveTheWorldNews:
        def __init__(self,**kwargs):
            params = {}
            for key, value in kwargs.items():
                params[key] = value
            
            r = requests.get(f"{FNAPI}/news/stw", params=params, headers={"x-api-key" : apikey}).json()
    
            self.status = r["status"]
            if r["status"] == 200:
                self.lastModified = r["data"]["lastModified"]
                self.messages = r["data"]["messages"]
                self.images = []

                for Message in r["data"]["messages"]:
                    self.images.append(Message["image"])

    class GetShop:
        def __init__(self,**kwargs):
            params = {}
            for key, value in kwargs.items():
                params[key] = value
            
            r = requests.get(f"{FNAPI}/shop/br", params=params, headers={"x-api-key" : apikey}).json()
    
            self.status = r["status"]
            if r["status"] == 200:
                self.hash = r["data"]["hash"]
                self.date = r["data"]["date"]
                self.votes = r["data"]["votes"]
                self.voteWinners = r["data"]["voteWinners"]

                self.featured = r["data"]["featured"]
                self.daily = r["data"]["daily"]