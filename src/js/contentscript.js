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

async function getJson(sentence) {
  sentence = sentence.replace(/ /g, '+');
  console.log("sending sentence " + sentence);
  let response = await fetch(`https://testi1220.herokuapp.com/agent?sentence=${sentence}`);
  console.log(response);
  let obj = await response.json();
  console.log(obj);

  htmlStr = "";
  for (const emoji of obj["emojis"]) {
    console.log(emoji);
    htmlStr += addImg(emoji[0]);
  }
  return htmlStr;
}

const filter = async function() {
  try {
    console.log("filtering");
    const allPost = document.getElementsByTagName('main')[0].children[0].children[0].children[0].children[0].children[0].children[3].children[0].children[0].getElementsByTagName('div')[0].children[0].children[0].children;
    for (const post of allPost) {
      try {
        const tweet = post.querySelector('[data-testid="tweet"]').children[1].children[1].children[0].children[0].children[0];
        console.log(tweet.innerHTML);
        htmlstr = await getJson(tweet.innerHTML);
        tweet.innerHTML = htmlstr;
      } catch (e) {
        console.log(e);
      }
    }
  } catch (e) {
    console.log(e);
  }
}

document.addEventListener("click", filter);