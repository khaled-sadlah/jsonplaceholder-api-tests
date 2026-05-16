BASE_URL = "https://jsonplaceholder.typicode.com"

# Posts endpoints
POSTS_URL              = f"{BASE_URL}/posts"
POST_BY_ID_URL         = f"{BASE_URL}/posts/{{id}}"
POSTS_BY_USER_ID_URL   = f"{BASE_URL}/posts?userId={{userId}}"

# Comments endpoints
COMMENTS_URL             = f"{BASE_URL}/comments"
COMMENT_BY_ID_URL        = f"{BASE_URL}/comments/{{id}}"
COMMENTS_BY_POST_ID_URL  = f"{BASE_URL}/comments?postId={{postId}}"

# Albums endpoints
ALBUMS_URL             = f"{BASE_URL}/albums"
ALBUM_BY_ID_URL        = f"{BASE_URL}/albums/{{id}}"
ALBUMS_BY_USER_ID_URL  = f"{BASE_URL}/albums?userId={{userId}}"

# Photos endpoints
PHOTOS_URL             = f"{BASE_URL}/photos"
PHOTO_BY_ID_URL        = f"{BASE_URL}/photos/{{id}}"
PHOTOS_BY_ALBUM_ID_URL = f"{BASE_URL}/photos?albumId={{albumId}}"

# Todos endpoints
TODOS_URL            = f"{BASE_URL}/todos"
TODO_BY_ID_URL       = f"{BASE_URL}/todos/{{id}}"
TODOS_BY_USER_ID_URL = f"{BASE_URL}/todos?userId={{userId}}"
TODOS_COMPLETED_URL  = f"{BASE_URL}/todos?completed={{completed}}"

# Users endpoints
USERS_URL              = f"{BASE_URL}/users"
USER_BY_ID_URL         = f"{BASE_URL}/users/{{id}}"
USER_BY_USERNAME_URL   = f"{BASE_URL}/users?username={{username}}"
