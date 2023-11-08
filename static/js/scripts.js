$("form[name=signup_form]").submit(function(e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/signup",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      window.location.href = "/dashboard/";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});

$("form[name=login_form]").submit(function(e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/login",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      window.location.href = "/dashboard/";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});

 
document.getElementById("login").onclick = function() {
    window.location.href = "/home/"; 
};

var login_card =document.getElementById("log_in");
var signup_card =document.getElementById("sign_up");
var forgot_card=document.getElementById("forgot_card");


document.getElementById("change_card").onclick = function() {
  login_card.style.display="none";
  signup_card.style.display="flex";
}

document.getElementById("forgot_change").onclick = function() {
  login_card.style.display="none";
  forgot_card.style.display="flex";
  
}

$("form[name=password_form]").submit(function(e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/reset_pass/",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      console.log(resp);
      window.location.href = "/home/";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});

function process_transfer() {
  event.preventDefault();

  var data = {
    number: $("#phone_no").val(),
    pass:$("#password").val(),
    amount:$("#amount").val(),
  };
  console.log(data);

  $.ajax({
    url: "/transfer/",
    contentType: "application/json;charset=utf-8",
    type: "POST",
    data: JSON.stringify(data),
    dataType: "json",
    success: function (resp) {
      console.log(resp);
      window.location.reload();
      
    },
    error: function (xhr, status, error) {
      console.log("Error:", error.getJSON);
      $error.text("An error occurred. Please try again.").removeClass("error--hidden");
    }
  });
}


function process_topup() {
  event.preventDefault();

  var data = {
    amount:$("#amount_topup").val(),
  };
  console.log(data);

  $.ajax({
    url: "/topup/",
    contentType: "application/json;charset=utf-8",
    type: "POST",
    data: JSON.stringify(data),
    dataType: "json",
    success: function (resp) {
      console.log(resp);
      window.location.reload();
      
    },
    error: function (xhr, status, error) {
      console.log("Error:", error.getJSON);
      $error.text("An error occurred. Please try again.").removeClass("error--hidden");
    }
  });
}


// var strip = document.getElementById("strip");
// // var transfer_from_wallet = document.getElementById("transferBtn");
// // var topup = document.getElementById("topupBtn");
// var transfer_money = document.getElementById("transfer_money");
// var card_payment = document.getElementById("card_payment");

// document.getElementById("transferBtn").onclick = function() {
//   console.log("inside fn");
//   strip.style.display = "none";
//   transfer_money.style.display = "flex";
// };

// document.getElementById("topupBtn").onclick = function() {
//   strip.style.display = "none";
//   card_payment.style.display = "flex";
// };
/*
var strip = document.getElementById("strip");

strip.addEventListener("click", function(event) {
  if (event.target.tagName === "BUTTON") {
    var targetId = event.target.getAttribute("data-target");
    if (targetId) {
      var targetElement = document.getElementById(targetId);
      if (targetElement) {
        // Hide all target elements initially
        var targetElements = document.querySelectorAll(".target-element");
        targetElements.forEach(function(element) {
          element.style.display = "none";
        });

        // Show the selected target element
        targetElement.style.display = "flex";
      }
    }
  }
});*/


function show_transfer_money(){
  document.getElementById("card_payment").style.display="none";
  var myelem=document.getElementById("transfer_money");
  myelem.style.display="flex";


}


function show_add_money(){
  document.getElementById("transfer_money").style.display="none";
  var myelem=document.getElementById("card_payment");
  myelem.style.display="flex";

}
