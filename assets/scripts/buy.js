fetch(PAYMENTS_KEY_URL)
  .then((result) => { return result.json(); })
  .then((data) => {
    // Initialize Stripe.js
    const stripe = Stripe(data.publicKey);

    document.querySelector("#submitBtn").addEventListener("click", () => {
      const quantityElem = document.querySelector('input[name=quantity]');
      const quantity = parseInt(quantityElem.value, 10);

      // Get Checkout Session ID
      fetch(`${PAYMENTS_CHECKOUT_SESSION_URL}?quantity=${quantity}`)
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
