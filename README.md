# Project Apahsia Social - Emoji Translator

A context-aware Emoji Translator Chrome Extension built using word2vec.

This is one out of 2 part that helps Aphasia patients to engage with others on social media. To find out more about the project, please see our [video](https://youtu.be/PoPWcYbTgzE)

## Trying out the app

The app itself is delivered in the form of Chrome extension. It is only implemented for [Twitter](twitter.com) for the time being.

To use it,

1. Goes to `releases`. Under `assets` of the top most (i.e. most recent) version, click on `Aphasia.Social.zip` to download it.
2. After the download is completed, unzip the file into anywhere you like. When it is done, you'll see a `/Aphasia Social` folder appears.
2. Open [Chrome Extension Management Tab](chrome://extensions/) in Google Chrome.
3. Turn on developer mode on upper right corner.
4. Click `load unpacked` on upper left corner.
5. Navigate to `/Aphasia Social`.
6. Import is done. Visit the [Twitter](twitter.com) and click anywhere on the webpage to activate the extension to see the effect.

The recommendation bar on your right should disappear right away - and that means the extension has started working.
Note that the server could be slow in the first run, so don't panic if you don't see the texts translated within the first 10 seconds.

## About the code

### Front end
A google extension that extracts the sentences of posts on Twitter thorugh the HTML structure of the homepage. All of its code can be found in `/Aphasia Social`.

### Back end
**Please switch to branch S1** for the running back end codes.

The backend handles the sentences extracted by the front end and returns data links of emojis. It is built on python Django framework, more particularly, Django-Heroku as we have chosen to host it on [Heroku](https://testi1220.herokuapp.com/). There are different folders containing all the scripts and codes that we used during the project.

If you are interested in using the code, make sure you have Python 3.7 [installed locally](http://install.python-guide.org). Then, **please install all the packages in requirements.txt** At the time of this writing, it is fine that you just install the latest version of the packages through pip. If you intends to re-host this under your own account on Heroku, we recommend install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) for easy management, although it is not mandatory.

#### Framework files

The code that serves the API calls live in `/hello`.

For those that are new to Heroku-Django, this is the sequence of execution that results in our code in `/hello` being loaded as an app on Heroku.

```
Procfile > /GettingStarted/wsgi.py > /GettingStarted/settings.py > hello
```

When a HTTP Request API call is received, the Django framework will wraps it as `Django-Request` class and parse it according to rules stipulated in `/GettingStarted/settings.py`. To call to our API, use the path /agent, followed by a sentence to translate, with space being subsitutued with `+`. For example,
```
https://testi1220.herokuapp.com/agent?sentence=A+sentence+to+translate
```

#### Extracting Keywords
After extracting the sentence sent over HTTP, the keywords in the sentences is extracted using */KeywordExtract/ExtractKeyword.py*. It is a Part-Of-Speech based algortihm developed through referencing https://github.com/minimaxir/gpt-2-keyword-generation.

#### Word to Emoji
There are several files in this section:
Filename | Purpose
---------|--------
FullTable.html | It is the html scrap from [Unicode's Official Emoji website](https://unicode.org/emoji/charts/full-emoji-list.html).
extract.py | To extract the descriptions of emojis as well as data rendering links  `FullTable.html` into `table.csv`.
table.csv | The extracted contents. Open this in Microsoft Excel for easy updating the emoji descriptions.
UpdateAnnotate.py | This is a script that takes the content in table.csv and turns it into a python dictionary form and pickles it into `emojilib`.
resetspace.py | This script reads all emojis in emojilib and obtain their embeddings through querying the spaCy large model with their description names. All the embeddings are then plotted in a vector KNeighbors space, which is pickled into `emojispace`
EmojiVec.py | The class that performs the translation. Given a list of keywords, it will extract the embeddings from our database hosted at Google Cloud Firestore. The vector will the be plotted in `emojispace` and the nearest emoji neighbor is returned.
LocalEmojiVec.py | A variant of `EmojiVec.py` that retrieves keyword embeddings from a local spaCy model instead. Not used deployment because of slow loading of models on Heroku.
emojilib | A pre-trained set of emoji embeddings downloaded from https://github.com/uclnlp/emoji2vec. It is trained using word2vec models by treating each emoji as a word token, but unfortunately accuracy is below our method of using description of emojis.
auth.json | Required to call to our Firestore database. A server client API is used and hence this file exposes our API key. This is a hacky work around for the fact that there is no Firestore client API in python. It will be removed once alternative is found or abusing use is discovered.

## Next Steps
1. Checks if the HTML structure of twitter.com homepage is the same for any region/computer/browser/OS. If it is not, devise device-specific approach or a more robust text detection and retrieval approach.
2. Improves annotation for Emoji descriptions.
3. Extends Abstract keyword list. 

## Questions
If you have any questions about the repo, please reach out to us through the issue tracker.
