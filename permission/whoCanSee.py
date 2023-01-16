from typing import Set, Any


Data = Any


class LevelAndGroups:
    def __init__(self, oml: str, cml: str, groups: Set[int], users: Set[int]) -> None:
        self.oml = oml
        self.cml = cml
        self.groups = groups
        self.users = users


class AccessRecord:
    def __init__(self, type: str, levelAndGroups: LevelAndGroups) -> None:
        self.type = type
        self.levelAndGroups = levelAndGroups


def whoCanSee(fqfields: Set[str], data: Data) -> Set[AccessRecord]:
    result = set()
    for fqfield in fqfields:
        parts = fqfield.split("/")
        collectionString = parts[0]
        id = parts[1]
        field = parts[2]
        collection = getCollection(collectionString, int(id), data)
        ar = AccessRecord(
            collection.getType(field), collection.getLevelAndGroups(field)
        )
        result.add(ar)

    return result


class Collection:
    def __init__(self, id: int, data: Data) -> None:
        self.id = id
        self.data = data

    def getType(self, field: str) -> str:
        raise NotImplementedError

    def getLevelAndGroups(self, field: str) -> LevelAndGroups:
        raise NotImplementedError

    def getMeetingId(self) -> int:
        # use self.data and maybe also hardcoded definitions of the models.yml to get the meeting id.
        return 42

    def getAllGroups(self) -> Set[int]:
        meetingId = self.getMeetingId()
        # use meetingId and self.data to get all groups in this meeting
        return set([73, 16, 15])

    def hasPerm(self, groupID: int, perm: str) -> bool:
        allPerms = ["get", "all", "perms", "from", "self.data"]
        return perm in allPerms


def getCollection(collection: str, id: int, data: Data) -> Collection:
    collectionMap = {
        "topic": Topic(id, data),
        "user": User(id, data),
        "organization": Organization(id, data),
    }
    return collectionMap[collection]


class Topic(Collection):
    def getType(self, field: str) -> str:
        return "levelAndGroups"

    def getLevelAndGroups(self, field: str) -> LevelAndGroups:
        groups = self.getAllGroups()
        res = (group for group in groups if self.hasPerm(group, "agenda_item.can_see"))
        return LevelAndGroups(oml="superuser", cml="", groups=set(res), users=set())


class User(Collection):
    def getType(self, field: str) -> str:
        if field == "password":
            return "nobody"
        return "levelAndGroups"


class Organization(Collection):
    def getType(self, field: str) -> str:
        if field == "theme":
            return "all"
        return "levelAndGroups"
