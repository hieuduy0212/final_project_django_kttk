function showLoading(s) {
  if (s) {
    document.getElementById("overlay").style.display = "flex";
    document.getElementById("loading").style.display = "block";
  } else {
    document.getElementById("overlay").style.display = "none";
    document.getElementById("loading").style.display = "none";
  }
}

// function checkLoginStatus() {
//   const token = localStorage.getItem("jwt");
//   let content = ``;
//   if (token) {
//     content = `<a class="btn btn-outline-dark" href="http://localhost:8000/cart">
//                     <i class="bi-cart-fill me-1"></i>
//                     Cart
//                     <span class="badge bg-dark text-white ms-1 rounded-pill" id="size-cart">0</span>
//                 </a>
//                 <button class="btn btn-outline-dark" onclick="sign_out()">
//                     <i class="bi-box-arrow-left me-1"></i>
//                     Sign out
//                 </button>`;

//     getCart();
//   } else {
//     content = `<a class="btn btn-outline-dark" href="http://localhost:8000/login">
//                     <i class="bi-user-plus me-1"></i>
//                     Sign in
//                 </a>
//                 <a class="btn btn-outline-dark"  href="http://localhost:8000/register">
//                     <i class="bi-user me-1"></i>
//                     Sign up
//                 </a>`;
//   }
//   document.getElementById("right-header").innerHTML = content;
// }
// checkLoginStatus();

// function sign_out() {
//   let sign_out_url = "http://localhost:8001/users/api/logout";
//   fetch(sign_out_url, {
//     method: "POST",
//     headers: {
//       Authorization: `Bearer ${localStorage.getItem("jwt")}`,
//     },
//   }).then((response) => {
//     if (response.ok) {
//       localStorage.removeItem("jwt");
//       window.location.href = "http://localhost:8000";
//     }
//   });
// }

// async function getCart() {
//   let cart_url = "http://localhost:8003/carts/api/";

//   const response = await fetch(cart_url, {
//     method: "GET",
//     headers: {
//       Authorization: `Bearer ${localStorage.getItem("jwt")}`,
//     },
//   });

//   const data = await response.json();
//   document.getElementById("size-cart").innerText = data.length;
// }
