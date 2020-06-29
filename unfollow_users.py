from apis import *

while True:
    try:
        unfollow_users()
    except Exception as e:
        print(str(e))
