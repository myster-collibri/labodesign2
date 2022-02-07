/**
* Template Name: Presento - v3.7.0
* Template URL: https://bootstrapmade.com/presento-bootstrap-corporate-template/
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/
(function() {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    let selectEl = select(el, all)
    if (selectEl) {
      if (all) {
        selectEl.forEach(e => e.addEventListener(type, listener))
      } else {
        selectEl.addEventListener(type, listener)
      }
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * Navbar links active state on scroll
   */
  let navbarlinks = select('#navbar .scrollto', true)
  const navbarlinksActive = () => {
    let position = window.scrollY + 200
    navbarlinks.forEach(navbarlink => {
      if (!navbarlink.hash) return
      let section = select(navbarlink.hash)
      if (!section) return
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        navbarlink.classList.add('active')
      } else {
        navbarlink.classList.remove('active')
      }
    })
  }
  window.addEventListener('load', navbarlinksActive)
  onscroll(document, navbarlinksActive)

  /**
   * Scrolls to an element with header offset
   */
  const scrollto = (el) => {
    let header = select('#header')
    let offset = header.offsetHeight

    if (!header.classList.contains('header-scrolled')) {
      offset -= 16
    }

    let elementPos = select(el).offsetTop
    window.scrollTo({
      top: elementPos - offset,
      behavior: 'smooth'
    })
  }

  /**
   * Toggle .header-scrolled class to #header when page is scrolled
   */
  let selectHeader = select('#header')
  if (selectHeader) {
    const headerScrolled = () => {
      if (window.scrollY > 100) {
        selectHeader.classList.add('header-scrolled')
      } else {
        selectHeader.classList.remove('header-scrolled')
      }
    }
    window.addEventListener('load', headerScrolled)
    onscroll(document, headerScrolled)
  }

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

  /**
   * Mobile nav toggle
   */
  on('click', '.mobile-nav-toggle', function(e) {
    select('#navbar').classList.toggle('navbar-mobile')
    this.classList.toggle('bi-list')
    this.classList.toggle('bi-x')
  })

  /**
   * Mobile nav dropdowns activate
   */
  on('click', '.navbar .dropdown > a', function(e) {
    if (select('#navbar').classList.contains('navbar-mobile')) {
      e.preventDefault()
      this.nextElementSibling.classList.toggle('dropdown-active')
    }
  }, true)

  /**
   * Scrool with ofset on links with a class name .scrollto
   */
  on('click', '.scrollto', function(e) {
    if (select(this.hash)) {
      e.preventDefault()

      let navbar = select('#navbar')
      if (navbar.classList.contains('navbar-mobile')) {
        navbar.classList.remove('navbar-mobile')
        let navbarToggle = select('.mobile-nav-toggle')
        navbarToggle.classList.toggle('bi-list')
        navbarToggle.classList.toggle('bi-x')
      }
      scrollto(this.hash)
    }
  }, true)

  /**
   * Scroll with ofset on page load with hash links in the url
   */
  window.addEventListener('load', () => {
    if (window.location.hash) {
      if (select(window.location.hash)) {
        scrollto(window.location.hash)
      }
    }
  });
  /**
   * Clients Slider
   */
  new Swiper('.clients-slider', {
    speed: 400,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    slidesPerView: 'auto',
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    },
    breakpoints: {
      320: {
        slidesPerView: 2,
        spaceBetween: 40
      },
      480: {
        slidesPerView: 3,
        spaceBetween: 60
      },
      640: {
        slidesPerView: 4,
        spaceBetween: 80
      },
      992: {
        slidesPerView: 6,
        spaceBetween: 120
      }
    }
  });

  /**
   * Porfolio isotope and filter
   */
  window.addEventListener('load', () => {
    let portfolioContainer = select('.portfolio-container');
    if (portfolioContainer) {
      let portfolioIsotope = new Isotope(portfolioContainer, {
        itemSelector: '.portfolio-item',
        layoutMode: 'fitRows'
      });

      let portfolioFilters = select('#portfolio-flters li', true);

      on('click', '#portfolio-flters li', function(e) {
        e.preventDefault();
        portfolioFilters.forEach(function(el) {
          el.classList.remove('filter-active');
        });
        this.classList.add('filter-active');

        portfolioIsotope.arrange({
          filter: this.getAttribute('data-filter')
        });
        portfolioIsotope.on('arrangeComplete', function() {
          AOS.refresh()
        });
      }, true);
    }

  });

  /**
   * Initiate portfolio lightbox 
   */
  const portfolioLightbox = GLightbox({
    selector: '.portfolio-lightbox'
  });

  /**
   * Portfolio details slider
   */
  new Swiper('.portfolio-details-slider', {
    speed: 400,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    }
  });

  /**
   * Testimonials slider
   */
  new Swiper('.testimonials-slider', {
    speed: 600,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    slidesPerView: 'auto',
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    },
    breakpoints: {
      320: {
        slidesPerView: 1,
        spaceBetween: 20
      },

      1200: {
        slidesPerView: 3,
        spaceBetween: 20
      }
    }
  });

  /**
   * Animation on scroll
   */
  window.addEventListener('load', () => {
    AOS.init({
      duration: 1000,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    })
  });

})()


//mes lignes de codes
function display_success(message){
  $('#msg-feed').removeClass("d-none").removeClass("text-danger").addClass("custom_success")
  $('#msg-feed').html(`<i class="fas fa-check-circle"></i> ${message}`)

}
function display_error(message){
  //-------
  $('#msg-feed').removeClass("d-none").removeClass("custom_success").addClass("text-danger")
  $('#msg-feed').html(`<i class="fas fa-times"></i> ${message}`)
}

$('#seepass').change(function() {
    // this will contain a reference to the checkbox   
    if (this.checked) {
        // the checkbox is now checked
        $("#passwordfield").attr('type','text')
    } else {
        // the checkbox is now no longer checked
        $("#passwordfield").attr('type','password')
    }
});

//login ajax request

$("#loginform").on('submit', function(e){
  e.preventDefault();
  var data=new FormData()
  var username=document.querySelector("#usernamefield").value;
  var password=document.querySelector("#passwordfield").value;
  alert(password+"nnn")
  data.append('username', username)
  data.append('password',password)
  data.append("csrfmiddlewaretoken",document.querySelector("input[name=csrfmiddlewaretoken]").value);
  var ajx= new XMLHttpRequest();
  ajx.onreadystatechange=function(){
        if(ajx.readyState == 4 && ajx.status == 200){
          var response=JSON.parse(ajx.responseText);
          if(response['success']){
            display_success(response['success_message'])
            //alert(response['success_message']);
            window.setTimeout(function () {
                   window.location = "../";
                  }, 2000);
          }
          else{
            display_error(response['error_message'])
          }
        }
      }
  //sending requst
  ajx.open("POST","");
  ajx.send(data)

})

const validateEmail = (email) => {
  return email.match(
    /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  );
};
$("#regform").on('submit', function(e){
  e.preventDefault();
  var data=new FormData()
  var username=document.querySelector("#usernamefield").value;
  var password=document.querySelector("#passwordfield").value;
  var repassword=document.querySelector("#repasswordfield").value;
  var mail=document.querySelector("#mail").value;
  if(password != repassword){
    display_error("Les deux mot de passe sont pas les meme! reessayez.")
    return 1
  }
  if(!validateEmail(mail)){
    display_error("L'adresse mail est invalide...'")
    return 1
  }
  data.append('username', username)
  data.append('password',password)
  data.append('mail',mail)
  data.append("csrfmiddlewaretoken",document.querySelector("input[name=csrfmiddlewaretoken]").value);
  var ajx= new XMLHttpRequest();
  ajx.onreadystatechange=function(){
        if(ajx.readyState == 4 && ajx.status == 200){
          var response=JSON.parse(ajx.responseText);
          if(response['success']){
            display_success(response['success_message'])
            //alert(response['success_message']);
            window.setTimeout(function () {
                   window.location = "../login";
                  }, 2000);
          }
          else{
            display_error(response['error_message'])
          }
        }
      }
  //sending requst
  ajx.open("POST","");
  ajx.send(data)

})


try{
$('#closemodal').on('click',function(e){
  e.preventDefault();
  $('#exampleModalCenter').modal("hide");
});
}catch{
  //..........
}


try{
$('#closemodal2').on('click',function(e){
  e.preventDefault();
  $('#exampleModal').modal("hide");
});
}catch{
  //..........
}

try{
$('#retablirBtn').on('click',function(e){
  e.preventDefault();
  $('#exampleModalCenter').modal("hide");
});
}catch{
  //..........
}



$("#caoaddvet").on('click', function(e){
  e.preventDefault()
  var vetement=$("#caovetement").val();
  data= new FormData();
  data.append('is_ceo_get_info',true)
  data.append('vetement', vetement)
  data.append("csrfmiddlewaretoken",document.querySelector("input[name=csrfmiddlewaretoken]").value)
  //getting vetement info
  $.ajax({
          type: "POST",
          url:'',
          data:data,
          cache:false,
          processData:false,
          contentType:false,
      success: function (data) {
            if (data.success_message!= '' && data.success_message!= 'undefined'){
              $("#cao_viewer").empty();
              $("#cao_viewer").append(`
                  <div class="row text-center">\
                    <div class="col-5 bg-light text-dark m-1" style="border-radius:5px/5px">Concevoir un(e): </div>
                    <div class="col-5 bg-warning text-dark m-1" style="border-radius:5px/5px" id="cao_nom_val">${data.vetement.vetement}</div>
                    <div class="col-5 bg-light text-dark m-1" style="border-radius:5px/5px">Pour genre : </div>
                    <div class="col-5 bg-warning text-dark m-1" style="border-radius:5px/5px" id="cao_sex_val">${data.vetement.sex}</div>
                    <div class="col-12" >-------Composants----------<br>
                    <div class="row" id="composantss">
                    </div>
                    </div>
                  </div>
                `)
              if(data.has_composant){
                for(var i=0; i<data.composants.length; i++){
                 $("#composantss").append(` <div class="col-5 bg-light text-dark m-1" style="border-radius:5px/5px">${data.composants[i].nom}</div>
                  `)
                }

                $("#cao_viewer").append(`
                    <div class="row">
                      <a href="#" id="caobtnval" class="btn btn-success btn-sm col-6 m-4">Valider</a>
                      <script>
                      $("#caobtnval").on('click',validate_cao);
                      </script>
                    </div>
                  `)
              }else{
              $("#composantss").append(`
                  <p class="col-12 text-center text-dark" style="font-size:12px">
                  Ce vetement n'a pas encore des composant, donc pas d'image a ajouter a la conception
                  ,Veuillez svp svp <a href="../" class='text-info'>ajouter des composant</a> et des design (modele a ce composant) via l'interface laboratoire et puis revennez
                  continuer la conception</p>
                `)
            }
              //alert(data.vetement.vetement);
              /*window.setTimeout(function () {
                window.location = "../";
              }, 1000);*/
            }
            else{
              /*notify(data.error_message,'error');
              notify("Votre session a expirer, actualiser la page!","error");
              window.setTimeout(function () {
                window.location = "../";
              }, 2000);*/
              alert(data.error_message)
            }
            
          },
          error: function (error) {
            // handle error
            //notify(data.msg,'error');
          },
          async: true,
          timeout: 60000,
        });

})



function validate_cao(e){
  e.preventDefault();
  var vetement=document.querySelector("#cao_nom_val").textContent;
  var sexe=document.querySelector("#cao_sex_val").textContent;

  data= new FormData();
  data.append('is_validate_cao',true)
  data.append('vetement', vetement)
  data.append('sexe', sexe)
  data.append("csrfmiddlewaretoken",document.querySelector("input[name=csrfmiddlewaretoken]").value)
  //getting vetement info
  $.ajax({
          type: "POST",
          url:'',
          data:data,
          cache:false,
          processData:false,
          contentType:false,
      success: function (data) {
            if (data.success_message!= '' && data.success_message!= undefined){
              //alert(data.success_message)
              window.setTimeout(function () {
                window.location = "../scene/"+data.cao_id;
              }, 1000);
            }
            else{
              /*notify(data.error_message,'error');
              notify("Votre session a expirer, actualiser la page!","error");
              window.setTimeout(function () {
                window.location = "../";
              }, 2000);*/
              //alert(data.error_message)
            }
            
          },
          error: function (error) {
            // handle error
            //notify(data.msg,'error');
          },
          async: true,
          timeout: 60000,
        });
}

Array.from(document.querySelectorAll("#compo_js")).forEach(function(element){
  element.addEventListener('change', function(e){
    var valuer=this.value;
    data=valuer.split(":")
    compo=data[0].split(" ")[1]
    document.querySelector("#"+compo).setAttribute("src", data[1]);
    document.querySelector(`#imaggg${compo}`).setAttribute("src", data[1])
  })
})

Array.from(document.querySelectorAll("#closemodal")).forEach(function(closebtn){
  //faut retrouver son modal et la fermer
  closebtn.addEventListener('click', function(e){
    var btn=e.target;
    var header_modal=btn.closest(".modal-header");
    var modal_content=btn.closest(".modal-content");
    var modal_dialog=modal_content.closest(".modal-dialog");
    var modal=modal_dialog.closest(".modal");
    var id_modal=modal.getAttribute('id')
    $(`#${id_modal}`).modal("hide");
  })
})