from constants import (
    TEMPLATES_TABLE,
    ASSETS_TABLE,
    BLOCKS_TABLE,
    BOOKMARKS_TABLE,
    COMMENTS_TABLE,
    USERS_TABLE,
    USERS_TOKENS_TABLE,
    AUTHORS_TABLE,
    EMAILS_TABLE,
    UID_KEY,
    UUID_KEY,
    TOKEN_KEY,
    USER_KEY,
    FULL_NAME_KEY,
    AVATAR_URL_KEY,
    EMAIL_KEY,
    TEMPLATE_KEY,
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
def add_template(db, template):
    table = db[TEMPLATES_TABLE]
    template[UUID_KEY] = str(template[UUID_KEY])
    table.upsert(
        {
            "uuid": template[UUID_KEY],
            **{k: v for k, v in template.items() if v is not None},
        },
        [UUID_KEY],
    )


@connect_db
def remove_template(db, uuid, author):
    table = db[TEMPLATES_TABLE]
    table.delete(uuid=str(uuid), author=author)


@connect_db
def get_template(db, uuid):
    table = db[TEMPLATES_TABLE]
    row = table.find_one(uuid=str(uuid))
    if row is not None:
        return row
    return None


@connect_db
def get_all_templates(db, author, page, size):
    table = db[TEMPLATES_TABLE]
    return table.find(author=author, _limit=size, _offset=page * size)


@connect_db
def get_templates_by_category(db, category, page, size):
    table = db[TEMPLATES_TABLE]
    return table.find(category=category, _limit=size, _offset=page * size)


@connect_db
def get_all_public_templates(db, page, size):
    table = db[TEMPLATES_TABLE]
    return table.find(public=True, _limit=size, _offset=page * size)


@connect_db
def get_templates_length(db):
    return len(db[TEMPLATES_TABLE])


@connect_db
def get_user_templates_count(db, author):
    table = db[TEMPLATES_TABLE]
    return table.count(author=author)


############### assets ########################
@connect_db
def add_asset(db, asset):
    table = db[ASSETS_TABLE]
    table.insert(asset)


@connect_db
def update_asset(db, asset):
    table = db[ASSETS_TABLE]
    table.update(
        {"uid": asset[UID_KEY], **{k: v for k, v in asset.items() if v is not None}},
        [UID_KEY],
    )


@connect_db
def remove_asset(db, uid, author):
    table = db[ASSETS_TABLE]
    table.delete(uid=uid, author=author)


@connect_db
def get_asset(db, uid, author):
    table = db[ASSETS_TABLE]
    row = table.find_one(uid=uid, author=author)
    if row is not None:
        return row
    return None


@connect_db
def get_all_assets(db, author, page, size):
    table = db[ASSETS_TABLE]
    return table.find(author=author, _limit=size, _offset=page * size)


@connect_db
def get_assets_length(db):
    return len(db[ASSETS_TABLE])


@connect_db
def get_user_assets_count(db, author):
    table = db[ASSETS_TABLE]
    return table.count(author=author)


########################### bookmarks ##################################
@connect_db
def add_bookmark(db, bookmark):
    table = db[BOOKMARKS_TABLE]
    bookmark[UUID_KEY] = str(bookmark[UUID_KEY])
    bookmark[TEMPLATE_KEY] = str(bookmark[TEMPLATE_KEY])
    table.insert(bookmark)


@connect_db
def update_bookmark(db, bookmark):
    table = db[BOOKMARKS_TABLE]
    bookmark[UUID_KEY] = str(bookmark[UUID_KEY])
    table.update(
        {
            "uuid": bookmark[UUID_KEY],
            **{k: v for k, v in bookmark.items() if v is not None},
        },
        [UUID_KEY],
    )


@connect_db
def remove_bookmark(db, uuid, author):
    table = db[BOOKMARKS_TABLE]
    table.delete(uuid=str(uuid), author=author)


@connect_db
def get_bookmark(db, uuid, author):
    table = db[BOOKMARKS_TABLE]
    row = table.find_one(uuid=str(uuid), author=author)
    if row is not None:
        return row
    return None


@connect_db
def get_all_bookmarks(db, author, page, size):
    table = db[BOOKMARKS_TABLE]
    return table.find(author=author, _limit=size, _offset=page * size)


@connect_db
def get_bookmarks_length(db):
    return len(db[BOOKMARKS_TABLE])


@connect_db
def get_user_bookmarks_count(db, author):
    table = db[BOOKMARKS_TABLE]
    return table.count(author=author)


@connect_db
def get_template_bookmarks_count(db, template):
    table = db[BOOKMARKS_TABLE]
    return table.count(template=str(template))


################################# blocks #################################
@connect_db
def add_block(db, block):
    table = db[BLOCKS_TABLE]
    block[UUID_KEY] = str(block[UUID_KEY])
    block[TEMPLATE_KEY] = str(block[TEMPLATE_KEY])
    table.insert(block)


@connect_db
def update_block(db, block):
    table = db[BLOCKS_TABLE]
    block[UUID_KEY] = str(block[UUID_KEY])
    table.update(
        {"uuid": block[UUID_KEY], **{k: v for k, v in block.items() if v is not None}},
        [UUID_KEY],
    )


@connect_db
def remove_block(db, uuid, author):
    table = db[BLOCKS_TABLE]
    table.delete(uuid=str(uuid), author=author)


@connect_db
def get_block(db, uuid, author):
    table = db[BLOCKS_TABLE]
    row = table.find_one(uuid=str(uuid), author=author)
    if row is not None:
        return row
    return None


@connect_db
def get_all_blocks(db, author, page, size):
    table = db[BLOCKS_TABLE]
    return table.find(author=author, _limit=size, _offset=page * size)


@connect_db
def get_blocks_length(db):
    return len(db[BLOCKS_TABLE])


@connect_db
def get_user_blocks_count(db, author):
    table = db[BLOCKS_TABLE]
    return table.count(author=author)


################################## comments ###################################
@connect_db
def add_comment(db, comment):
    table = db[COMMENTS_TABLE]
    comment[UUID_KEY] = str(comment[UUID_KEY])
    comment[TEMPLATE_KEY] = str(comment[TEMPLATE_KEY])
    table.insert(comment)


@connect_db
def update_comment(db, comment):
    table = db[COMMENTS_TABLE]
    comment[UUID_KEY] = str(comment[UUID_KEY])
    table.update(
        {
            "uuid": comment[UUID_KEY],
            **{k: v for k, v in comment.items() if v is not None},
        },
        [UUID_KEY],
    )


@connect_db
def remove_comment(db, uuid, author):
    table = db[COMMENTS_TABLE]
    table.delete(uuid=str(uuid), author=author)


@connect_db
def get_comment(db, uuid, author):
    table = db[COMMENTS_TABLE]
    row = table.find_one(uuid=str(uuid), author=author)
    if row is not None:
        return row
    return None


@connect_db
def get_all_template_comments(db, template, page, size):
    table = db[COMMENTS_TABLE]
    return table.find(template=str(template), _limit=size, _offset=page * size)


@connect_db
def get_all_comments(db, author, page, size):
    table = db[COMMENTS_TABLE]
    return table.find(author=author, _limit=size, _offset=page * size)


@connect_db
def get_comments_length(db):
    return len(db[COMMENTS_TABLE])


@connect_db
def get_user_comments_count(db, author):
    table = db[COMMENTS_TABLE]
    return table.count(author=author)


################################## users ###################################
@connect_db
def add_user(db, user):
    table = db[USERS_TABLE]
    table.upsert(user, [UID_KEY])


@connect_db
def get_user(db, user_id):
    table = db[USERS_TABLE]
    row = table.find_one(uid=user_id)
    if row is not None:
        return row
    return None


@connect_db
def get_users_length(db):
    return len(db[USERS_TABLE])


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


@connect_db
def get_user_tokens_length(db):
    return len(db[USERS_TOKENS_TABLE])


@connect_db
def add_author(db, user_id, full_name, avatar_url):
    table = db[AUTHORS_TABLE]
    table.upsert(
        {UID_KEY: user_id, FULL_NAME_KEY: full_name, AVATAR_URL_KEY: avatar_url},
        [UID_KEY],
    )


@connect_db
def get_author(db, user_id):
    table = db[AUTHORS_TABLE]
    row = table.find_one(uid=user_id)
    if row is not None:
        return row
    return None


@connect_db
def get_authors_length(db):
    return len(db[AUTHORS_TABLE])


################################## emails ###################################
@connect_db
def add_email(db, email):
    table = db[EMAILS_TABLE]
    email[UUID_KEY] = str(email[UUID_KEY])
    table.upsert(email, [EMAIL_KEY])


@connect_db
def remove_email(db, email):
    table = db[EMAILS_TABLE]
    table.delete(email=email)


@connect_db
def get_all_emails(db):
    table = db[EMAILS_TABLE]
    return table.find()