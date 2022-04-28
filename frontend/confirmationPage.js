let order_receipt = localStorage.getItem('order_receipt')
let user_email = localStorage.getItem("user_email");
console.log(order_receipt)


fetch("https://qz1ngk3uy3.execute-api.us-east-1.amazonaws.com/default/cart-confirmation_page",
{
    method: "POST",
    body: JSON.stringify({user_email: user_email, order_hist_numb: String(order_receipt)})
})
.then((res) => res.json())
.then((data) => {
    console.log(data);
    
    if (data.status === 200) {
        let cart_list = data.body;
        
        let output = "";
        // use this poulate the html in cofirmation page
        cart_list.forEach(function(menu) {
        //   console.log(menu);
          output += `
          <tr>
            <td>${menu.food_name}</td>
            <td>${menu.rest_name}</td>
            <td>${menu.quantity}</td>
            <td>${menu.price}</td>
          </tr>
          `
        });
        document.getElementById("food_list").innerHTML += output;

    } else {
        console.log(data.statusText);
    }
})
