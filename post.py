import re

class Post:
    def __init__(self, nroom, text):
        self.text = text
        self.nroom = nroom

    def count_word(self):
        #print(self.text)
        return len(re.findall(r'\w+', self.text))


def append_post(text, nroom, posts):
    post = Post(nroom, text)
    posts.append(post)
    #print(post.count_word())


def byword(i, category, p):
    if (p.count_word() > i*10):
        category[i].append(p)
    else:
        if (i-1 < 0):
            return
        byword(i-1, category, p)


def categorize(posts):

    ncategory = 5
    category = [[] for i in range(ncategory)]

    for p in posts:
        i = ncategory - 1
        byword(i, category, p)

    print(len(category[0]))
    print(len(category[1]))
    print(len(category[2]))
    print(len(category[3]))
    print(len(category[4]))

    for c in category[1]:
        print(c.text)
    
