// Hamburger menu
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('hamburger').addEventListener('click', function () {
      const rightSide = document.getElementById('right-side');
      rightSide.classList.toggle('active'); 
    });
  });
  
  
  
  // Social Proof counter and animation
  document.addEventListener('DOMContentLoaded', () => {
    const counters = document.querySelectorAll('.counter');
  
    const formatNumber = (num) => {
      if (num >= 1000) {
        return num % 1000 === 0 ? (num / 1000) + 'K' : (num / 1000).toFixed(1) + 'K';
      } else {
        return num;
      }
    };
     
  
    const animateCounter = (counter) => {
      const target = +counter.getAttribute('data-target');
      const increment = target / 200;
  
      const updateCount = () => {
        let count = counter.innerText.replace('K+', '').trim();
        count = count.includes('.') ? parseFloat(count) * 1000 : parseInt(count);
  
        if (count < target) {
          counter.innerText = formatNumber(Math.ceil(count + increment));
          setTimeout(updateCount, 1);
        } else {
          counter.innerText = formatNumber(target);
        }
      };
  
      updateCount();
    };
  
    const observer = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });
  
    counters.forEach(counter => {
      observer.observe(counter);
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
  
  
  // Scroll to top
  var mybutton = document.getElementById("scrollToTop");
  
  window.onscroll = function() {scrollFunction()};
  
  function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
      mybutton.style.display = "block";
    } else {
      mybutton.style.display = "none";
    }
  }
  
  function scrollToTop() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE, and Opera
  }
  
  // Year copyright
  document.addEventListener('DOMContentLoaded', () => {
    const currentYear = new Date().getFullYear();
    document.getElementById('currentYear').textContent = currentYear;
  });
  
  
  // Function to remove messages after 5 seconds
  setTimeout(function () {
    var alertMessages = document.querySelectorAll(".alert");
    alertMessages.forEach(function (alert) {
      alert.remove();
    });
  }, 5000);


  // Profile Tab
  function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
  }
  