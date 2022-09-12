import globalFunctions as gF

def login():
    reddit = gF.praw.Reddit(
        user_agent="sandboxing (by u/wemyx_TQ)",
        client_id="wMfPLvhn-uxA2YmxwlRq6w",
        client_secret='aI2GNGd5MhfWq6fVyCMrqX-ou7IF-g',
        username="wemyx_TQ",
        password="14789653eddiT!!",
    )
    return reddit

def getPosts(redSubName):
    posts = []
    redTexts = []
    reddit = login()
    thisSubreddit = reddit.subreddit(redSubName[2:])

    for post in thisSubreddit.top():
        print('rdF:', gF.lineno(), ' |', post.title)
        redTexts.append(post.title)
        try:
            submission = reddit.submission(url=post.url)
        except:
            print('rdF:', gF.lineno(), ' | ERROR_URL:', post.url)
            continue
        #submission.comments.replace_more(limit=100)
        for comment in submission.comments.list():
            try:
                redTexts.append(comment.body)
                print('rdF:', gF.lineno(), ' |', comment.body)
            except:
                print('rdF:', gF.lineno(), ' | ERROR_comment.body')
                continue

    return redTexts

def writeRedTxtFile(redSubName, redTexts):
    redFile = open('eng/data/textLibrary/'+redSubName+'.txt', 'w+', encoding='utf-8')
    for texts in redTexts:
        try:
            redFile.write(texts+'\n')
        except:
            print('rdF:', gF.lineno(), ' | ', texts)
            continue
## [post.title, post.score, post.id, post.subreddit, post.url,
##  post.num_comments, post.selftext, post.created])



##    submission.comments.replace_more(limit=None)
##    for top_level_comment in submission.comments:
##        print(top_level_comment.body)

