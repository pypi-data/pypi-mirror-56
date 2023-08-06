import dataclasses
from dataclasses import dataclass, asdict, field

from typing import List


def dicts_to_dataclasses(instance):
    """Convert all fields of type `dataclass` into an instance of the
    specified data class if the current value is of type dict."""
    cls = type(instance)
    for f in dataclasses.fields(cls):
        if not dataclasses.is_dataclass(f.type) or not isinstance(f.default, ()):
            continue

        value = getattr(instance, f.name)
        if isinstance(value, dict):
            new_value = f.type(**value)
            setattr(instance, f.name, new_value)
        elif isinstance(value, (tuple, list)):
            new_value = [f.type(**value) for value in value]
            setattr(instance, f.name, new_value)


@dataclass
class Base:
    def __post_init__(self):
        dicts_to_dataclasses(self)

    def as_dict(self):
        return asdict(self)


@dataclass
class Cover(Base):
    cover_id: str = field(repr=False, )
    offset_x: str = None
    offset_y: str = None
    source: str = None
    id: str = None


@dataclass
class Point(Base):
    x: int = None
    y: int = None


@dataclass
class Page(Base):
    # id: str = None
    # about: str = field(default=None, repr=False)
    # birthday: str = field(default=None, repr=False)
    # name: str = None
    # username: str = None
    # fan_count: int = field(default=None, repr=False)
    # cover: Cover = field(default=None, repr=False)
    point_list: List[Point] = field(default_factory=list, repr=False)


if __name__ == '__main__':
    data = {
        # "id": "20531316728",
        # "about": "The Facebook Page celebrates how our friends inspire us, support us, and help us discover the world when we connect.",
        # "birthday": "02/04/2004",
        # "name": "Facebook",
        # "username": "facebookapp",
        # "fan_count": 214643503,
        # "cover": {
        #     "cover_id": "10158913960541729",
        #     "offset_x": 50,
        #     "offset_y": 50,
        #     "source": "https://scontent.xx.fbcdn.net/v/t1.0-9/s720x720/73087560_10158913960546729_8876113648821469184_o.jpg?_nc_cat=1&_nc_ohc=bAJ1yh0abN4AQkSOGhMpytya2quC_uS0j0BF-XEVlRlgwTfzkL_F0fojQ&_nc_ht=scontent.xx&oh=2964a1a64b6b474e64b06bdb568684da&oe=5E454425",
        #     "id": "10158913960541729"
        # },
        "point_list": [
            {"x": 1, "y": 2},
            {"x": 3, "y": 4},
        ]
    }
    p = Page(**data)
    print(p)
