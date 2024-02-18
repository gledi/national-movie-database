fetch(PAYMENTS_KEY_URL)
  .then((result) => { return result.json(); })
  .then((data) => {
    // Initialize Stripe.js
    const stripe = Stripe(data.publicKey);
    console.log("PAYMENTS_CHECKOUT_SESSION_URL:", PAYMENTS_CHECKOUT_SESSION_URL);

    document.querySelector("#checkout-btn").addEventListener("click", () => {
      // Get Checkout Session ID
      fetch(PAYMENTS_CHECKOUT_SESSION_URL)
      .then((result) => {
          if (result.status >= 200 && result.status <= 299) {
            return Promise.resolve(result.json());
          } else {
            return Promise.reject(result.json());
          }
       })
      .then((data) => {
        console.log(data);
        // Redirect to Stripe Checkout
        return stripe.redirectToCheckout({sessionId: data.sessionId})
      })
      .then((res) => {
        console.log(res);
      }).catch(err => {
        console.error("THERE WAS AN ERROR!");
      });
    });
  });
