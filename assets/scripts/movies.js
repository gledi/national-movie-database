function loadMovies() {
  const url = "/api/v1/movies/";

  fetch(url, {
    headers: {
      Accept: "application/json"
    }
  }).then(async (resp) => {
    const body = await resp.json();
    const { results } = body;

    const tbody = document.querySelector("table.table > tbody");

    const rows = results.map(row => {
      const tr = document.createElement("tr");

      const idCell = document.createElement("td");
      idCell.innerText = `${row.id}`;
      tr.appendChild(idCell);

      const titleCell = document.createElement("td");
      titleCell.innerText = row.title;
      tr.appendChild(titleCell);

      const yearCell = document.createElement("td");
      yearCell.innerText = row.year;
      tr.appendChild(yearCell);

      const runtimeCell = document.createElement("td");
      runtimeCell.innerText = row.title;
      tr.appendChild(runtimeCell);

      const ratingCell = document.createElement("td");
      ratingCell.innerText = row.year;
      tr.appendChild(ratingCell);

      return tr;
    });

    rows.forEach(element => {
      tbody.appendChild(element);
    });
  }, (err) => {
    console.error("Could not get movies");
  });
}


window.onload = function(e) {
  loadMovies();
}
