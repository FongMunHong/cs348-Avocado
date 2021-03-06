const user_email = localStorage.getItem("user_email")
const account = document.getElementById("account");
const loading_screen = document.getElementById("loading_container");

disableScroll();

if (user_email == null){
  console.log("NOT LOGGED IN!");
  account.innerHTML = 'Log-In';
} else {
  console.log("LOGGED IN!");
  account.innerHTML = user_email;
  account.href = "signout.html";
}

async function most_popular_list() {
    const ele = document.getElementById("most_popular");

    const data = {};

    fetch('https://5kwlyceua3.execute-api.us-east-1.amazonaws.com/default/home-most_popular', {
          method: 'POST',
          body: JSON.stringify(data)
      }).then((res) => res.json())
      .then((data) => {

          if (data.status == 200) {
              let val = data.body;
              let output = "";
              val.forEach(function(restaurant) {
                  output += `
                  <div class="rest_container">
                      <a id=${restaurant.rest_id} class="rest_link" href="restaurant.html"><img class="rest_image" src=${restaurant.image}
                       alt="Red dot" /></a>
                      ${restaurant.rest_name}
                  </div>`
              });

              document.getElementById('most_popular').innerHTML = output;
              let btn = document.getElementsByClassName('rest_link');
              for (var i = 0; i < btn.length; i++) {
                  btn[i].addEventListener('click', clickFunc);
              }
          }
          finishLoading();
      })
}

async function order_again() {

    const data = {
        // user_email: "munhong@gmail.com"
        user_email: user_email
    };


    fetch('https://mso6sc71q3.execute-api.us-east-1.amazonaws.com/default/home-order_again', {
          method: 'POST',
          body: JSON.stringify(data)
      }).then((res) => res.json())
      .then((data) => {

          console.log(data)
          if (data.status == 200) {
              if (data.body.length != 0) {
                let title = `
                    <div class="category">
                    <h1>Order Again</h1>
                    </div>
                    <section id="Order Again" class="main_container">
                    </section>
                `;
                document.getElementById("place_holder_order_again").innerHTML = title;

                const ele = document.getElementById("Order Again");

                let val = data.body;
                let output = "";
                val.forEach(function(restaurant) {
                    output += `
                    <div class="rest_container">
                        <a id=${restaurant.rest_id} class="rest_link" href="restaurant.html"><img class="rest_image" src=${restaurant.image}
                        alt="Red dot" /></a>
                        ${restaurant.rest_name}
                    </div>`
                });

                document.getElementById("Order Again").innerHTML = output;
                let btn = document.getElementsByClassName('rest_link');
                for (var i = 0; i < btn.length; i++) {
                    btn[i].addEventListener('click', clickFunc);
                }
            }
        }
    })
}


async function food_list(food_type) {
    const ele = document.getElementById(food_type);

    const data = {
        rest_type: food_type
    };


    fetch('https://m77sejmw7h.execute-api.us-east-1.amazonaws.com/default/home-category', {
          method: 'POST',
          body: JSON.stringify(data)
      }).then((res) => res.json())
      .then((data) => {

        console.log(data);

          if (data.status == 200) {
              let val = data.body;
              let output = "";
              val.forEach(function(restaurant) {
                  output += `
                  <div class="rest_container">
                      <a id=${restaurant.rest_id} class="rest_link" href="restaurant.html"><img class="rest_image" src=${restaurant.image}
                       alt="Red dot" /></a>
                      ${restaurant.rest_name}
                  </div>`
              });

              document.getElementById(food_type).innerHTML = output;
              let btn = document.getElementsByClassName('rest_link');
              for (var i = 0; i < btn.length; i++) {
                  btn[i].addEventListener('click', clickFunc);
              }
          }
    })
}

if (user_email != null) {
    order_again();
}
most_popular_list();
food_list("Fast Food");
food_list("Asian");

function finishLoading(){
  console.log("fetch complete");
  loading_screen.style.zIndex = "-100";
  loading_screen.style.opacity = "0";
  enableScroll();
}


function disableScroll() {
    // Get the current page scroll position
    scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    scrollLeft = window.pageXOffset || document.documentElement.scrollLeft,

        // if any scroll is attempted, set this to the previous value
        window.onscroll = function() {
            window.scrollTo(scrollLeft, scrollTop);
        };
}

function enableScroll() {
    window.onscroll = function() {};
}

const checkpoint = 200;
const title = document.getElementById('banner_title');
var opacity = 0;

window.addEventListener("scroll", () => {
  const currentScroll = window.pageYOffset;
  if (currentScroll <= checkpoint) {
    opacity = 1 - currentScroll / checkpoint;
  } else {
    opacity = 0;
  }
//   console.log(opacity)
  title.style.opacity = opacity;
});
