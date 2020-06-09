// var s = document.createElement('script');
// // TODO: add "script.js" to web_accessible_resources in manifest.json
// s.src = chrome.runtime.getURL('js/assistant.js');
// s.onload = function() {
//     this.remove();
// };
// (document.head || document.documentElement).appendChild(s);

console.log("test");

function addImg(url) {
  return "<img src='" + url + "'>";
}

function shouldOmmit(str) {
  return str.indexOf("http://") == 0 || str.indexOf("https://") == 0
}

async function getJson(sentence) {
  sentence = sentence.replace(/ /g, '+');
  console.log("sending sentence " + sentence);
  let response = await fetch(`https://testi1220.herokuapp.com/agent?sentence=${sentence}`);
  console.log("received emoji response: " +response);
  let obj = await response.json();
  console.log("parsed res into json: " + obj);

  htmlStr = "";
  for (const emoji of obj["emojis"]) {
    htmlStr += addImg(emoji[0]);
  }
  return htmlStr;
}

const filter = async function() {
  try {
    if (firstTime) {
      console.log("removing side bar ");
      let sideBar = document.getElementsByTagName("main")[0].children[0].children[0].children[0].children[1].children[0].children[1].children[0].children[0].children[0]
      sideBar.removeChild(sideBar.children[2]) // trending
      sideBar.removeChild(sideBar.children[2]) // who to follow
      firstTime = false
    }

    //document.getElementsByTagName('main')[0].children[0].children[0].children[0].children[1].innerHTML = "";

    console.log("replacing texts with emojis");
    const allPost = document.getElementsByTagName('main')[0].children[0].children[0].children[0].children[0].children[0].children[3].children[0].children[0].getElementsByTagName('div')[0].children[0].children[0].children;
    for (const post of allPost) {
      try {
        const tweet = post.querySelector('[data-testid="tweet"]').children[1].children[1].children[0].children[0].children;
        for (const line of tweet) {
          if (line.innerText.length > 0 && !shouldOmmit(line.innerText)) {//for special elements like emojis and hashtags have innerText = ""
            console.log("found post text in tweet: " + line.innerText);
            emoji = await getJson(line.innerText);
            line.innerHTML = emoji;
          }
        }
      } catch (e) {
        console.log(e);
      }
    }
  } catch (e) {
    console.log(e);
  }
}


var firstTime = true
document.addEventListener("click", filter);
