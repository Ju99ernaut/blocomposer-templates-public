from constants import (
    TEMPLATES_TABLE,
    ASSETS_TABLE,
    BLOCKS_TABLE,
    BOOKMARKS_TABLE,
    COMMENTS_TABLE,
    USERS_TABLE,
    USERS_TOKENS_TABLE,
    ID_KEY,
    TOKEN_KEY,
    USER_KEY,
)

from utils.db import connect_db

"""Functions for managing a dataset SQL database
    # Schemas

    #################### templates ######################
    id
    name
    description
    assets
    template
    thumbnail
    pages
    styles
    updated_at

"""


@connect_db
def setup(db):
    db.create_table(TEMPLATES_TABLE, primary_id=ID_KEY, primary_type=db.types.string)
    db.create_table(ASSETS_TABLE, primary_id=ID_KEY, primary_type=db.types.string)
    db.create_table(BLOCKS_TABLE, primary_id=ID_KEY, primary_type=db.types.string)
    db.create_table(BOOKMARKS_TABLE, primary_id=ID_KEY, primary_type=db.types.string)
    db.create_table(COMMENTS_TABLE, primary_id=ID_KEY, primary_type=db.types.string)
    db.create_table(USERS_TABLE, primary_id=ID_KEY, primary_type=db.types.string)


@connect_db
def add_template(db, template):
    table = db[TEMPLATES_TABLE]
    template[ID_KEY] = str(template[ID_KEY])
    table.upsert(template, [ID_KEY])


@connect_db
def remove_template(db, uuid, user):
    table = db[TEMPLATES_TABLE]
    table.delete(id=str(uuid), user=user)


@connect_db
def get_template(db, uuid, user):
    table = db[TEMPLATES_TABLE]
    row = table.find_one(id=str(uuid), user=user)
    if row is not None:
        return row
    return None


@connect_db
def get_all_templates(db, user, limit, start):
    table = db[TEMPLATES_TABLE]
    return table.find(user=user, _limit=limit, _offset=limit * start)


@connect_db
def get_all_public_templates(db, limit, start):
    table = db[TEMPLATES_TABLE]
    return table.find(public=True, _limit=limit, _offset=limit * start)


############### assets ########################
@connect_db
def add_asset(db, asset):
    table = db[ASSETS_TABLE]
    asset[ID_KEY] = str(asset[ID_KEY])
    table.insert(asset)


@connect_db
def update_asset(db, asset):
    table = db[ASSETS_TABLE]
    asset[ID_KEY] = str(asset[ID_KEY])
    table.update(
        {"id": asset[ID_KEY], **{k: v for k, v in asset.items() if v is not None}},
        [ID_KEY],
    )


@connect_db
def remove_asset(db, uuid, user):
    table = db[ASSETS_TABLE]
    table.delete(id=str(uuid), user=user)


@connect_db
def get_asset(db, uuid, user):
    table = db[ASSETS_TABLE]
    row = table.find_one(id=str(uuid), user=user)
    if row is not None:
        return row
    return None


@connect_db
def get_all_assets(db, user, limit, start):
    table = db[ASSETS_TABLE]
    return table.find(user=user, _limit=limit, _offset=limit * start)


########################### bookmarks ##################################
@connect_db
def add_bookmark(db, bookmark):
    table = db[BOOKMARKS_TABLE]
    bookmark[ID_KEY] = str(bookmark[ID_KEY])
    table.insert(bookmark)


@connect_db
def update_bookmark(db, bookmark):
    table = db[BOOKMARKS_TABLE]
    bookmark[ID_KEY] = str(bookmark[ID_KEY])
    table.update(
        {
            "id": bookmark[ID_KEY],
            **{k: v for k, v in bookmark.items() if v is not None},
        },
        [ID_KEY],
    )


@connect_db
def remove_bookmark(db, uuid, user):
    table = db[BOOKMARKS_TABLE]
    table.delete(id=str(uuid), user=user)


@connect_db
def get_bookmark(db, uuid, user):
    table = db[BOOKMARKS_TABLE]
    row = table.find_one(id=str(uuid), user=user)
    if row is not None:
        return row
    return None


@connect_db
def get_all_bookmarks(db, user, limit, start):
    table = db[BOOKMARKS_TABLE]
    return table.find(user=user, _limit=limit, _offset=limit * start)


################################# blocks #################################
@connect_db
def add_block(db, block):
    table = db[BLOCKS_TABLE]
    block[ID_KEY] = str(block[ID_KEY])
    table.insert(block)


@connect_db
def update_block(db, block):
    table = db[BLOCKS_TABLE]
    block[ID_KEY] = str(block[ID_KEY])
    table.update(
        {"id": block[ID_KEY], **{k: v for k, v in block.items() if v is not None}},
        [ID_KEY],
    )


@connect_db
def remove_block(db, uuid, user):
    table = db[BLOCKS_TABLE]
    table.delete(id=str(uuid), user=user)


@connect_db
def get_block(db, uuid, user):
    table = db[BLOCKS_TABLE]
    row = table.find_one(id=str(uuid), user=user)
    if row is not None:
        return row
    return None


@connect_db
def get_all_blocks(db, user, limit, start):
    table = db[BLOCKS_TABLE]
    return table.find(user=user, _limit=limit, _offset=limit * start)


################################## comments ###################################
@connect_db
def add_comment(db, comment):
    table = db[COMMENTS_TABLE]
    comment[ID_KEY] = str(comment[ID_KEY])
    table.insert(comment)


@connect_db
def update_comment(db, comment):
    table = db[COMMENTS_TABLE]
    comment[ID_KEY] = str(comment[ID_KEY])
    table.update(
        {"id": comment[ID_KEY], **{k: v for k, v in comment.items() if v is not None}},
        [ID_KEY],
    )


@connect_db
def remove_comment(db, uuid, user):
    table = db[COMMENTS_TABLE]
    table.delete(id=str(uuid), user=user)


@connect_db
def get_comment(db, uuid, user):
    table = db[COMMENTS_TABLE]
    row = table.find_one(id=str(uuid), user=user)
    if row is not None:
        return row
    return None


@connect_db
def get_all_comments(db, user, limit, start):
    table = db[COMMENTS_TABLE]
    return table.find(user=user, _limit=limit, _offset=limit * start)


################################## users ###################################
@connect_db
def add_user(db, user):
    table = db[USERS_TABLE]
    table.upsert(user, [ID_KEY])


@connect_db
def get_user(db, user_id):
    table = db[USERS_TABLE]
    row = table.find_one(id=user_id)
    if row is not None:
        return row
    return None


@connect_db
def add_user_token(db, token, user_id):
    table = db[USERS_TOKENS_TABLE]
    table.upsert(
        {TOKEN_KEY: token, USER_KEY: user_id},
        [USER_KEY],
    )


@connect_db
def get_user_id(db, token):
    table = db[USERS_TOKENS_TABLE]
    row = table.find_one(token=token)
    if row is not None:
        return row[USER_KEY]
    return None