"""
 Constants useful for data module
"""
TEMPLATES_TABLE = "templates"
ASSETS_TABLE = "assets"
BLOCKS_TABLE = "blocks"
BOOKMARKS_TABLE = "bookmarks"
COMMENTS_TABLE = "comments"
USERS_TABLE = "users"
USERS_TOKENS_TABLE = "users_tokens"
AUTHORS_TABLE = "authors"
EMAILS_TABLE = "emails"

ASSETS_KEY = "assets"
ID_KEY = "id"
UID_KEY = "uid"
UUID_KEY = "uuid"
NAME_KEY = "name"
DESCRIPTION_KEY = "description"
TEMPLATE_KEY = "template"
THUMBNAIL_KEY = "thumbnail"
PAGES_KEY = "pages"
STYLES_KEY = "styles"
URL_KEY = "url"
UPDATED_KEY = "updated_at"
USER_KEY = "user"
AUTHOR_KEY = "author"
SIZE_KEY = "size"
PUBLIC_KEY = "public"
BOOKMARKS_KEY = "bookmarks"
COMMENT_KEY = "comment"
TOKEN_KEY = "token"
FULL_NAME_KEY = "full_name"
AVATAR_URL_KEY = "avatar_url"
EMAIL_KEY = "email"

API_TAGS_METADATA = [
    {"name": "user", "description": "User profile"},
    {"name": "templates", "description": "Blocomposer user templates"},
    {"name": "assets", "description": "Blocomposer user assets"},
    {"name": "blocks", "description": "Blocomposer user blocks"},
    {"name": "bookmarks", "description": "Blocomposer user bookmarks"},
    {"name": "comments", "description": "Blocomposer user comments"},
    {"name": "newsletter", "description": "Register/Unregister newsletter"},
]

GJS_PREFIX = "gjs-"