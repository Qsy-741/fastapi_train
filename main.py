# 不是这怎么这么难用啊
# taskkill /PID 17308 /F
from enum import Enum
from typing import Union, Annotated, Literal, Any
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from fastapi import FastAPI, Query, Path, Body, Cookie, Header, Response
from fastapi.responses import JSONResponse, RedirectResponse


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Image(BaseModel):
    url: HttpUrl
    name: str


# class Item(BaseModel):
#     name: str = Field(examples=["dsy"])
#     description: Union[str, None] = Field(default=None, examples=["a very nice item"])
#     price: float = Field(gt=0, description="The price must be greater than zero", examples=[1.0])
#     tax: Union[float, None] = None
#     tags: set[str] = set()
#     image: Union[Image, None] = None

    # model_config = {
    #     "json_schema_extra": {
    #         "examples": [
    #             {
    #                 "name": "Foo",
    #                 "description": "A very nice Item",
    #                 "price": 35.4,
    #                 "tax": 3.2,
    #                 "tags": ["a", "b", "c", "a"],
    #                 "image": {
    #                     "url": "http://example.com/image.jpg",
    #                     "name": "Foo",
    #                 },
    #             }
    #         ]
    #     }
    # }


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None


class FileterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: set[str] = set()


class Cookies(BaseModel):
    session_id: str
    fatebook_tracker: Union[str, None] = None
    googall_tracker: Union[str, None] = None


class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: Union[str, None] = None
    traceparent: Union[str, None] = None
    x_tag: list[str] = []


class MimaIn(BaseModel):
    name: str
    passwd: str


class MimaOut(BaseModel):
    name: str


# class BaseUser(BaseModel):
#     username: str
#     email: str
#     full_name: Union[str, None] = None
#
#
# class UserIn(BaseUser):
#     password: str


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float = 10.5


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None

class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: Union[str, None] = None

def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


app = FastAPI()

@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

# @app.get("/items/{item_id}/name", response_model=Item, response_model_include={"name", "description"})
# async def read_item_name(item_id: str):
#     return items[item_id]
#
# @app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
# async def read_item_public_data(item_id: str):
#     return items[item_id]

# @app.get("/portal")
# async def get_portal(teleport: bool = False) -> Response:
#     if teleport:
#         return RedirectResponse(url="https://www.baidu.com/")
#     return JSONResponse(content={"message": "Here is your interdimensional portal."})

# @app.post("/user/")
# async def create_user(user: UserIn) -> BaseUser:
#     return user

# @app.post("/items/", response_model=MimaOut)
# async def create_item(mima: MimaIn) -> Any:
#     return mima


# @app.get("/items/", response_model=list[Item])
# async def read_items() -> Any:
#     return [
#         Item(name="Portal Gun", price=24.0),
#         Item(name="Plumbus", price=32.0),
#     ]

# @app.get("/items/")
# async def read_items(Headers: Annotated[CommonHeaders, Header()]):
#     return Headers

# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
#     results = {"item_id": item_id, "item": item}
#     return results

# @app.put("/items/{item_id}")
# async def update_item(item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
#                       # q: Annotated[Union[str, None], Body()] = None,
#                       item: Item,
#                       user: Union[User, None] = None,
#                       ):
#     results = {"item_id": item_id}
#     # if q:
#     #     results.update({"q": q})
#     if item:
#         results.update({"item": item})
#     if user:
#         results.update({"user": user})
#     return results

# @app.get("/items/")
# async def read_items(fileter_query: Annotated[FileterParams, Query()]):
#     return fileter_query

# @app.get("/items/{item_id}")
# async def read_item(item_id: Annotated[int, Path(title="The ID of the item to get", ge=1, le=1000)], q: str,
#                     size: Annotated[Union[float, None], Query(gt=0, lt=10.5)]):
#     result = {"item_id": item_id}
#     if q:
#         result.update({"q": q})
#     if size:
#         result.update({"size": size})
#     return result

# @app.get("/items/{item_id}")
# async def read_items(*, item_id: int = Path(title="The ID of the item to get"), q: str):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     return results

# @app.get("/items/{item_id}")
# async def read_item(
#         item_id: Annotated[int, Path(title="The ID of the item to get")],
#         q: Annotated[Union[str, None], Query(alias="item-query")] = None,
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     return results

# @app.get("/items/")
# async def read_item(q: Annotated[Union[str, None], Query(
#     alias="item-query",
#     title="Query String",
#     description="Query for the items",
#     min_length=3,
#     include_in_schema=False
#     )] = None,
# ):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# @app.get("/items/")
# async def read_item(q: Annotated[Union[list[str], None], Query()] = ...):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# @app.get("/items/")
# async def read_items(q: Annotated[Union[str, None], Query(min_length=2, max_length=5)] = None):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
#
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     return {"item_id": item_id, **item.dict()}

# 请求体
# @app.post("/items/")
# async def create_item(item: Item):
#     item_dict = item.dict()
#     if item.tax:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict

# # 必须的查询参数
# @app.get("/items/{item_id}")
# async def read_user_item(item_id: str, needy: str | None = None):
#     item = {"item_id": item_id, "needy": needy}
#     return item
#
#
# # 查询参数类型转换
# @app.get("/users/{user_id}/items/{item_id}")
# async def read_item(user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False):
#     item = {"item_id": item_id, "owner_id": user_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item
#
# # 可选参数
# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: Union[str, None] = None):
#     if q:
#         return {"item_id": item_id, "q": q}
#     return {"item_id": item_id}
#
# # 查询参数
# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip:skip + limit]
#
# # 路径参数
# @app.get("/files/{file_path:path}")
# async def read_file(file_path: str):
#     return {"file_path": file_path}
#
#
# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     if model_name is ModelName.alexnet:
#         return {"model_name": model_name, "message": "Deep Learning FTW!"}
#     if model_name.value == "lenet":
#         return {"model_name": model_name, "message": "LeCNN all the images"}
#
#     return {"model_name": model_name, "message": "Have some residuals"}
#
#
# @app.get("/users")
# async def read_user(user_id: str):
#     return {"user_id"}
#
#
# @app.get("/users")
# async def read_user_me():
#     return ["user_id", "the current user"]
