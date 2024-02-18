(function (window, undefined) {
  function setYourRating(container, rating) {
    const starElems = container.querySelectorAll('.star-rate-star');
    starElems.forEach(starElem => {
      const num = parseInt(starElem.dataset.rating, 10);
      if (num <= rating) {
        starElem.classList.remove('bi-star');
        starElem.classList.add('bi-star-fill');
      } else {
        starElem.classList.remove('bi-star-fill');
        starElem.classList.add('bi-star');
      }
    });
  }

  function updateAverageRating(container, rating) {
    container.innerText = rating;
  }

  function showMessage(container, message, options = {}) {
    options.isError = options.isError || false;

    const toastBody = container.querySelector('.toast-body');
    const toastIcon = container.querySelector('.toast-icon');

    const iconClasses = [
      'bi-info-circle-fill',
      'bi-exclamation-triangle-fill',
      'text-primary',
      'text-danger'
    ];

    const funcs = {
      0: options.isError ? 'remove': 'add',
      1: options.isError ? 'add' : 'remove'
    };

    toastBody.innerText = message;

    iconClasses.forEach((className, i) => {
      const funcName = funcs[i % 2];
      toastIcon.classList.__proto__[funcName].bind(toastIcon.classList)(className);
    });

    const toast = new bootstrap.Toast(container);
    toast.show();
  }

  window.addEventListener('load', function (event) {
    const toastContainer = document.querySelector("#ratingToast");

    const avgRatingElem = document.querySelector('#current-movie-rating');
    const starRateElem = document.querySelector('.star-rate');
    const currentUserRating = parseInt(starRateElem.dataset.userRating, 10);

    setYourRating(starRateElem, currentUserRating);

    starRateElem.addEventListener('click', function(event) {
      const container = event.currentTarget;
      const rateUrl = container.dataset.rateurl;

      const csrfInput = document.querySelector('.star-rate > input[type=hidden][name=csrfmiddlewaretoken]');
      const rating = parseInt(event.target.dataset.rating, 10);
      if (isNaN(rating)) {
        return;
      }

      const data = new FormData();
      data.set("csrfmiddlewaretoken", csrfInput.value);
      data.set("rating", rating);

      fetch(rateUrl, { method: 'POST', body: data })
        .then(response => response.json().then(data => ({
          status: response.status,
          statusText: response.statusText,
          data: data
        })))
        .then(json => {
          const {status, data} = json;
          setYourRating(container, rating);
          updateAverageRating(avgRatingElem, data.rating);
          showMessage(toastContainer, data.detail, {
            isError: !(status >= 200 && status <=299)
          });
        })
        .catch(err => {
          showMessage(toastContainer, "Could not update ratings.", {
            isError: true
          });
        });
    }, false);
  });
})(window);
