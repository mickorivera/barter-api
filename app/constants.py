class ConstBaseMeta(type):
    def __init__(cls, *args, **kwargs):
        cls_dict = cls.__dict__
        cls._attributes = tuple(
            cls_dict[k] for k in cls_dict.keys() if not k.startswith("_")
        )
        super().__init__(cls)

    def __getitem__(cls, index):
        return cls._attributes[index]

    def __len__(self):
        return len(self._attributes)

    def __repr__(cls):
        return ",".join(cls._attributes)


class Currency(metaclass=ConstBaseMeta):
    PHP = "PHP"


class ItemCondition(metaclass=ConstBaseMeta):
    NEW = "NEW"
    USED = "USED"


class ItemStatus(metaclass=ConstBaseMeta):
    RESERVED = "RESERVED"
    AVAILABLE = "AVAILABLE"
    EXCHANGED = "EXCHANGED"


class UserRole(metaclass=ConstBaseMeta):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"
