// Accordion
var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function () {
    this.classList.toggle("active");
    var panel = this.nextElementSibling;
    if (panel.style.maxHeight) {
      panel.style.maxHeight = null;
    } else {
      panel.style.maxHeight = panel.scrollHeight + "px";
    }
  });
}

// Hamburger menu
document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("hamburger").addEventListener("click", function () {
    const rightSide = document.getElementById("right-side");
    rightSide.classList.toggle("active");
  });
});

// Dropdown
document.addEventListener('DOMContentLoaded', function() {
  const dropbtn = document.querySelector('.dropbtn');
  const dropdownItems = document.querySelectorAll('.dropdown-content a');
  const institutionTypeInput = document.getElementById('institution-type');
  const searchForm = document.getElementById('search-form');
  let currentSelection = 'Public'; 

  dropbtn.textContent = currentSelection; 

  dropdownItems.forEach(item => {
    item.addEventListener('click', function(e) {
      e.preventDefault();
      const selectedText = e.target.textContent;
      const selectedValue = e.target.getAttribute('data-value');
      dropbtn.textContent = selectedText;
      currentSelection = selectedText;
      institutionTypeInput.value = selectedValue;

      updateDropdownList(selectedText);
    });
  });

  function updateDropdownList(selectedText) {
    const dropdownContent = document.querySelector(".dropdown-content");
    while (dropdownContent.firstChild) {
      dropdownContent.removeChild(dropdownContent.firstChild);
    }

    const options = ["Public", "Private"];

    const updatedOptions = options.filter((option) => option !== selectedText);

    updatedOptions.forEach((option) => {
      const link = document.createElement("a");
      link.href = "#";
      link.textContent = option;
      dropdownContent.appendChild(link);

      link.addEventListener("click", function (e) {
        const selectedText = e.target.textContent;
        dropbtn.textContent = selectedText;
        currentSelection = selectedText;

        updateDropdownList(selectedText);
      });
    });
  }

  // Handle form submission
  searchForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const searchQuery = document.getElementById('search').value;
    const type = institutionTypeInput.value;
    const url = new URL(searchForm.action);
    url.searchParams.set('search', searchQuery);
    url.searchParams.set('type', type);
    window.location.href = url.toString();
  });
});


document.addEventListener("DOMContentLoaded", function () {
  const locationSelect = document.getElementById("filter-location");
  const institutionTypeSelect = document.getElementById("filter-institution-type");
  const sortOrderSelect = document.getElementById("sort-order");

  function getCurrentQueryParams() {
    const params = new URLSearchParams(window.location.search);
    return params;
  }

  function updateQueryParam(key, value) {
    const params = getCurrentQueryParams();
    if (value) {
      if (key === 'type') {
        // Convert display value to backend value
        if (value === 'Public') {
          params.set(key, 'PUB');
        } else if (value === 'Private') {
          params.set(key, 'PRI');
        }
      } else {
        params.set(key, value);
      }
    } else {
      params.delete(key);
    }
    return params.toString();
  }

  function reloadPageWithParams(newParams) {
    const newURL = `${window.location.pathname}?${newParams}`;
    window.location.href = newURL;
  }

  // Event listener for Location filter
  locationSelect.addEventListener("change", function () {
    const selectedValue = this.value;
    const updatedParams = updateQueryParam("location", selectedValue);
    reloadPageWithParams(updatedParams);
  });

  // Event listener for Institution Type filter
  institutionTypeSelect.addEventListener("change", function () {
    const selectedValue = this.value;
    const updatedParams = updateQueryParam("type", selectedValue);
    reloadPageWithParams(updatedParams);
  });

  // Event listener for Sort Order
  sortOrderSelect.addEventListener("change", function () {
    const selectedValue = this.value;
    const updatedParams = updateQueryParam("sort", selectedValue);
    reloadPageWithParams(updatedParams);
  });
});
