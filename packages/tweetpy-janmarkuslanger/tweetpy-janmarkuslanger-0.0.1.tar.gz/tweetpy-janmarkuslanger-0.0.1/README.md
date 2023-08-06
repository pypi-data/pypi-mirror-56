# tweetpy

Create your own bot without the api.

> Use at your own risk!

## Example

``` python
import time
from tweetpy import Twitter

hashtags = ('development', 'software', 'selenium', 'python')

while True:
    with Twitter(username='myusername', password='mypassword') as bot:
        bot.login()

        for hashtag in hashtags:
            bot.retweet_by_tag(hashtag, max=10) # retweets the newest hashtags

        time.sleep(3600) # sleep for an hour

```
