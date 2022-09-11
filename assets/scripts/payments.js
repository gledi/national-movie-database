console.log("Sanity check");

fetch(PAYMENTS_KEY_URL)
  .then((result) => { return result.json(); })
  .then((data) => {
    // Initialize Stripe.js
    const stripe = Stripe(data.publicKey);
    console.log("stripe initialized:", stripe);

    document.querySelector("#submitBtn").addEventListener("click", () => {
      // Get Checkout Session ID
      fetch(PAYMENS_CHECKOUT_SESSION_URL)
      .then((result) => { return result.json(); })
      .then((data) => {
        console.log(data);
        // Redirect to Stripe Checkout
        return stripe.redirectToCheckout({sessionId: data.sessionId})
      })
      .then((res) => {
        console.log(res);
      });
    });

  });
