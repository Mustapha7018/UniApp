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
