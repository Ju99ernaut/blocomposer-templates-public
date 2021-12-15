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

ASSETS_KEY = "assets"
ID_KEY = "id"
NAME_KEY = "name"
DESCRIPTION_KEY = "description"
TEMPLATE_KEY = "template"
THUMBNAIL_KEY = "thumbnail"
PAGES_KEY = "pages"
STYLES_KEY = "styles"
URL_KEY = "url"
UPDATED_KEY = "updated_at"
USER_KEY = "user"
SIZE_KEY = "size"
PUBLIC_KEY = "public"
BOOKMARKS_KEY = "bookmarks"
COMMENT_KEY = "comment"
TOKEN_KEY = "token"

API_TAGS_METADATA = [
    {"name": "user", "description": "User profile"},
    {"name": "templates", "description": "Blocomposer user templates"},
    {"name": "assets", "description": "Blocomposer user assets"},
    {"name": "blocks", "description": "Blocomposer user blocks"},
    {"name": "bookmarks", "description": "Blocomposer user bookmarks"},
    {"name": "comments", "description": "Blocomposer user comments"},
]

GJS_PREFIX = "gjs-"