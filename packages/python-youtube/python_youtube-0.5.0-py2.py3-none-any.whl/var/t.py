@dataclass
class BaseResource(BaseModel):
    """
    This is the resource base model with some common fields.

    Refer: https://google-developers.appspot.com/youtube/v3/docs/#resource-types
    """
    kind: Optional[str] = field(default=None)
    etag: Optional[str] = field(default=None, repr=False)
    id: Optional[str] = field(default=None)
