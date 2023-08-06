# CrackWatchers

This is a simple wrapper of CrackWatch, maybe.

### Installation:</br>
```
pip install crackwatchers
```

### Usage:
So, you can get imformation about Cracked/Uncracked/Unreleased games. For each type of status game you can make an import.

**Cracked Games**

```
from crackwatchers import CrackedGames

info = CrackedGames() #page=0, count=0, sort_by='release_date', is_aaa='false'

print(info.get_title)              #Space Live - Advent of the Net Idols
print(info.get_slug)               #space-live-advent-of-the-net-idols
print(info.get_release_date)       #2019-11-26
print(info.get_crack_date)         #2019-11-26
print(info.get_cracked_after)      #0 day
print(info.get_version)            #[]
print(info.get_scene_group)        #DARKZER0
print(info.status)                 #CRACKED
print(info.get_protection)         #['steam']
print(info.get_price)              #N/A
print(info.get_image)              #https://b2.crackwatch.com/file/crackwatch-temp/6yinhqp7c.jpg
print(info.get_poster)             #https://b2.crackwatch.com/file/crackwatch-temp/ajqh7aopd.jpg
print(info.is_aaa)                 #False
print(info.get_comments_count)     #0
print(info.get_followers_count)    #0
print(info.get_price)              #N/A
print(info.get_id)                 #6s8aESAWtchQPXfsc
print(info.get_url)                #https://crackwatch.com/game/space-live-advent-of-the-net-idols
```
---
**Uncracked Games**


```
from crackwatchers import UncrackedGames

info = UncrackedGames(count=2, is_aaa='true') #page=2, count=0, sort_by='release_days', is_aaa='true'

print(info.get_title)            #Red Dead Redemption 2
print(info.get_slug)             #red-dead-redemption-2
print(info.get_release_date)     #2019-11-05
print(info.get_date_counting)    #22 days
print(info.get_protection)       #Rockstar
print(info.get_version)          #['false']
print(info.get_image)            #https://b2.crackwatch.com/file/crackwatch-temp/ll3zu7ffh.jpg
print(info.get_poster)           #https://b2.crackwatch.com/file/crackwatch-temp/y0zccxi9d.jpg
print(info.is_aaa)               #True
print(info.get_comments_count)   #81392
print(info.get_followers_count)  #61947
print(info.get_status)           #UNCRACKED
print(info.get_id)               #NsTb69wT9ap7v9rut
```

---

***Unreleased Games***

```
from crackwatchers import UnreleasedGames

info = UnreleasedGames(page=1, count=18,  is_aaa='true') #page=1, count=18, sort_by='release_date', is_aaa='true'

print(info.get_title)            #Cyberpunk 2077
print(info.get_slug)             #cyberpunk-2077
print(info.get_release_date)     #2020-04-16
print(info.get_counting)         #141 days
print(info.get_protection)       #['NO-DRM']
print(info.get_version)          #[]
print(info.get_image)            #https://b2.crackwatch.com/file/crackwatch-temp/86ygvr7lh.jpg
print(info.get_poster)           #https://b2.crackwatch.com/file/crackwatch-temp/guf7c6okt.jpg
print(info.is_aaa)               #True
print(info.get_comments_count)   #5179
print(info.get_followers_count)  #40309
print(info.get_url)              #https://crackwatch.com/game/cyberpunk-2077
print(info.get_id)               #mnuALvwHfec8stGHX
print(info.status)               #UNRELEASED
```
