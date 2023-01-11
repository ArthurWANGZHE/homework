from fastapi import FastAPI
from pydantic import BaseModel
import pymysql

cnx = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='todo')
cursor = cnx.cursor()


class Item(BaseModel):
    id: int
    title: str
    content: str
    state: bool
    begin: str
    end: str


class Menu(BaseModel):
    type: str
    id: int
    keyword: str
    page: int


app = FastAPI


@app.post("/add")
async def add(item: Item):
    item_dict = item.dict()
    result = {}
    try:
        await cursor.execute("INSERT INTO todo(id, title, content,state, begin, end)"
                             "VALUES (%s,%s,%s,%s,%s,%s)",
                             (item.id, item.title, item.content, item.state, item.begin, item.end))
        await cnx.commit()
        search_ = """
                    SELECT * FROM todo
                    WHERE id = {0};
                    """
        await cursor.execute(search_.format(item.id))
        data = await cursor.fetchone()
        result["code"] = 200
        result["msg"] = "success"
        result["data"] = data
        return result
    except:
        await cnx.rollback()
        result["code"] = 404
        result["msg"] = "This id is already exist"
        return result


@app.post("/delete")
async def delete(menu: Menu):
    result = {}
    if menu.type == "id":
        delete_ = """
                    DELETE FROM todo WHERE id = {0};
                    """
        cursor.execute(delete_.format(menu.id))
        cnx.commit()
        result["code"] = 200
        result["msg"] = "success"
        return result
    if menu.type == "Delete":
        delete_ = """
                    DELETE FROM todo;
                    """
        cursor.execute(delete_.format(menu.id))
        cnx.commit()
        result["code"] = 200
        result["msg"] = "success"
        return result
    if menu.type == "Delete all finished":
        delete_ = """
                    DELETE FROM todo WHERE state = "finished";
                    """
        cursor.execute(delete_.format(menu.id))
        cnx.commit()
        result["code"] = 200
        result["msg"] = "success"
        return result
    if menu.type == "Delete all unfinished":
        delete_ = """
                    DELETE FROM todo WHERE state = "unfinished";
                    """
        cursor.execute(delete_.format(menu.id))
        cnx.commit()
        result["code"] = 200
        result["msg"] = "success"
        return result
    else:
        result["code"] = 404
        result["msg"] = "Unknown act"
        return result


@app.post("/update")
async def update(item: Item):
    result = {}
    if item.state != None:
        update_ = """
                    UPDATE todo SET state="{0}"
                    WHERE id = "{1}";
                    """
        cursor.execute(update_.format(item.state, item.id))
        cnx.commit()
        search_ = """
                                    SELECT * FROM todo
                                    WHERE id = {0};
                                    """
        cursor.execute(search_.format(item.id))
        data = cursor.fetchone()
        result["code"] = 200
        result["msg"] = "success"
        result["data"] = data
        return result
    else:
        result["code"] = 404
        result["msg"] = "Unknown act"
        return result


@app.post("/search")
async def search(menu: Menu):
    result = {}
    if menu.type == "Search all":
        search_ = """
                    SELECT * FROM todo
                    LIMIT {1},5
                    """
        cursor.execute(search_.format(menu.keyword, (menu.page - 1) * 5))
        data = cursor.fetchall()
        result["code"] = 200
        result["msg"] = "success"
        if len(data) != 0:
            result["data"] = data
        else:
            result["data"] = "FInd nothing"
        return result

    if menu.type == "Search for finished":
        search_ = """
                    SELECT * FROM todo
                    WHERE state = "finished"
                    LIMIT {1},5
                    """
        cursor.execute(search_.format(menu.keyword, (menu.page - 1) * 5))
        data = cursor.fetchall()
        result["code"] = 200
        result["msg"] = "success"
        if len(data) != 0:
            result["data"] = data
        else:
            result["data"] = "Find nothing"
        return result

    if menu.type == "Search for unfinished":
        search_ = """
                    SELECT * FROM todo
                    WHERE state = "unfinished"
                    LIMIT {1},5
                    """
        cursor.execute(search_.format(menu.keyword, (menu.page - 1) * 5))
        data = cursor.fetchall()
        result["code"] = 200
        result["msg"] = "success"
        if len(data) != 0:
            result["data"] = data
        else:
            result["data"] = "Find nothing"
        return result

    if menu.type == "search for keywords":
        searchsql = """
                    SELECT * FROM todo 
                    WHERE title LIKE "%{0}%"
                    LIMIT {1},5
                    """
        cursor.execute(searchsql.format(menu.keyword, (menu.page - 1) * 5))
        data = cursor.fetchall()
        result["code"] = 200
        result["msg"] = "success"
        if len(data) != 0:
            result["data"] = data
        else:
            result["data"] = "Find nothing about" + menu.keyword
        return result

    if menu.type == "search id":
        search_ = """
                        SELECT * FROM todo
                        WHERE id = {0};
                        """
        cursor.execute(search_.format(menu.id))
        data = cursor.fetchall()
        result["code"] = 200
        result["msg"] = "success"
        if len(data) != 0:
            result["data"] = data
        else:
            result["data"] = "Find nothing under this id"
        return result
    else:
        result["code"] = 404
        result["msg"] = "Unknown act"
        return result
