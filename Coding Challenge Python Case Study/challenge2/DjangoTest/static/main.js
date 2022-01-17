console.log("Sanity Check!");

// Get Stripe publishable key
fetch("/config/")
  .then((result) => result.json())
  .then((data) => {
    // Initialize Stripe.js
    const stripe = Stripe(data.publicKey);

    // new

    // Event Handler
    let submitBtn = document.querySelector("#submitBtn");
    if (submitBtn != null) {
      submitBtn.addEventListener("click", () => {
        // Get Checkout Session ID
        fetch("/create-checkout-session/")
          .then((result) => {
            return result.json();
          })
          .then((data) => {
            console.log(data);

            // Redirect to Stripe Checkout
            return stripe.redirectToCheckout({ sessionId: data.sessionId });
          })
          .catch((res) => {
            console.log(res);
          });
      });
    }
  });

  function cancelSubscription(id) {
    console.log("clicked");
    try {
      console.log(id);
      let data = JSON.stringify({ subscription_id: id });

      console.log(data);
      $.ajax({
        async: true,
        type: "POST",
        url: "/cancel-subscription/",
        data: data,
        contentType: false,
        processData: false,
        dataType: "json",
        beforeSend: function () {},
        success: function (data) {
          console.log(data);
          if (data["url"] !== undefined) {
            window.location.replace(data["url"]);
          }
        },

        error: function (XMLHttpRequest, textStatus, errorThrown) {
          alert("operation failed");
          console.log("Status: " + textStatus);
          console.log("Error: " + errorThrown);
          flag = True;
        },
        complete: function () {},
      });
      return false;
    } catch (err) {
      console.log("Error", err.stack);
    }
  }