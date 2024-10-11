# 不是这怎么这么难用啊
# taskkill /PID 17308 /F
from enum import Enum
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# 请求体
@app.post("/items/")
async def create_item(item: Item):
    item.price = item.name + item.price
    return item

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

