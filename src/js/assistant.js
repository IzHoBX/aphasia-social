async function getJson(sentence) {
  sentence = sentence.replace(/ /g, '+');
  console.log("sending sentence " + sentence);
  let proxy_url = "https://cors-anywhere.herokuapp.com/";
  let url = proxy_url + `https://testi1220.herokuapp.com/agent?sentence=${sentence}`;
  let response = await fetch(`https://testi1220.herokuapp.com/agent?sentence=${sentence}`);
  console.log(response);
  let obj = await response.json();
  //console.log(obj);
  return obj;
}

function addImg(url) {
  return "<img src='" + url + "'>";
}

const filter = async function() {
  try {
    console.log("filtering");
    const allPost = document.getElementsByTagName('main')[0].children[0].children[0].children[0].children[0].children[0].children[3].children[0].children[0].getElementsByTagName('div')[0].children[0].children[0].children;
    for (const post of allPost) {
      try {
        const tweet = post.querySelector('[data-testid="tweet"]').children[1].children[1].children[0].children[0].children[0];
        console.log(tweet.innerHTML);
        getJson(tweet.innerHTML);
        tweet.innerHTML = addImg();
      } catch (e) {
        console.log(e);
      }
    }
  } catch (e) {
    console.log(e);
  }
}

// window.onload = function() {
//   document.getElementsByTagName('main')[0].children[0].children[0].children[0].children[1].innerHTML = "";

//   document.addEventListener("click", filter);
// }

document.addEventListener("click", filter);