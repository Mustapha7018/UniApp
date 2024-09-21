  // Accordion
  var acc = document.getElementsByClassName("accordion");
  var i;
  
  for (i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function() {
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
document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('hamburger').addEventListener('click', function () {
    const rightSide = document.getElementById('right-side');
    rightSide.classList.toggle('active'); 
  });
});


  // Dropdown
  document.addEventListener('DOMContentLoaded', function() {
    const dropbtn = document.querySelector('.dropbtn');
    const dropdownItems = document.querySelectorAll('.dropdown-content a');
    let currentSelection = 'Public'; 
  
    dropbtn.textContent = currentSelection; 
  
    dropdownItems.forEach(item => {
        item.addEventListener('click', function(e) {
  
            const selectedText = e.target.textContent;
            dropbtn.textContent = selectedText;
            currentSelection = selectedText;
  
            updateDropdownList(selectedText);
        });
    });
  
    function updateDropdownList(selectedText) {
        const dropdownContent = document.querySelector('.dropdown-content');
        while (dropdownContent.firstChild) {
            dropdownContent.removeChild(dropdownContent.firstChild);
        }
  
        const options = ['Public', 'Private', 'Online'];
  
        const updatedOptions = options.filter(option => option !== selectedText);
  
        updatedOptions.forEach(option => {
            const link = document.createElement('a');
            link.href = '#';
            link.textContent = option;
            dropdownContent.appendChild(link);
  
            link.addEventListener('click', function(e) {
                const selectedText = e.target.textContent;
                dropbtn.textContent = selectedText;
                currentSelection = selectedText;
  
                updateDropdownList(selectedText);
            });
        });
    }
  });
