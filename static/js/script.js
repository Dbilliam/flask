let navbar = document.querySelector('.header .navbar');

document.querySelector('#menu-btn').onclick = () =>{
    navbar.classList.add('active');
}

document.querySelector('#nav-close').onclick = () =>{
    navbar.classList.remove('active');
}

let searchForm = document.querySelector('.search-form');

document.querySelector('#search-btn').onclick = () =>{
    searchForm.classList.add('active');
}

document.querySelector('#close-search').onclick = () =>{
    searchForm.classList.remove('active');
}

window.onscroll = () =>{
    navbar.classList.remove('active');

    if(window.scrollY > 0){
        document.querySelector('.header').classList.add('active');
    }else{
        document.querySelector('.header').classList.remove('active');
    }
};

window.onload = () =>{
    if(window.scrollY > 0){
        document.querySelector('.header').classList.add('active');
    }else{
        document.querySelector('.header').classList.remove('active');
    }
};


var swiper = new Swiper(".home-slider", {
    loop:true, 
    grabCursor:true,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
});

var swiper = new Swiper(".product-slider", {
    loop:true, 
    grabCursor:true,
    spaceBetween: 20,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    breakpoints: {
        0: {
          slidesPerView: 1,
        },
        640: {
          slidesPerView: 2,
        },
        768: {
          slidesPerView: 3,
        },
        1024: {
          slidesPerView: 4,
        },
    },
});

var swiper = new Swiper(".review-slider", {
    loop:true, 
    grabCursor:true,
    spaceBetween: 20,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    breakpoints: {
        0: {
          slidesPerView: 1,
        },
        640: {
          slidesPerView: 2,
        },
        768: {
          slidesPerView: 3,
        },
    },
});

var swiper = new Swiper(".blogs-slider", {
    loop:true, 
    grabCursor:true,
    spaceBetween: 10,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    breakpoints: {
        0: {
          slidesPerView: 1,
        },
        768: {
          slidesPerView: 2,
        },
        991: {
          slidesPerView: 3,
        },
    },
});

var swiper = new Swiper(".clients-slider", {
    loop:true, 
    grabCursor:true,
    spaceBetween: 20,
    breakpoints: {
        0: {
          slidesPerView: 1,
        },
        640: {
          slidesPerView: 2,
        },
        768: {
          slidesPerView: 3,
        },
        1024: {
          slidesPerView: 4,
        },
    },
});



function like(postId) {
  const likeButton = document.getElementById(`like-button-${postId}`);
  const likeCount = document.getElementById(`like-count-${postId}`);

  fetch(`/like-post/${postId}`, {method:'POST'}).then((res) => res.json()).then((data) => {
      likeCount.innerHTML = data['likes'];
      
      if (data['liked'] == true) {
          likeButton.class = "fa-thumbs-up  fa-2x";
      }
      else {
          likeButton.class  = "fa-thumbs-up fa-2x";
      }
  })
  .catch((e) => alert('Sorry post can\'t be liked'));
  
}

// function heart(postId) {
//   const heartButtton = document.getElementById(`heart-button-${postId}`);
//   const heartCount = document.getElementById(`heart-count-${postId}`);
//   fetch(`/heart-post/${postId}`, {method: 'POST'}).then((res) = res.json()).then((date) => {
//     heartCount.innerHTML = data['heart'];
//     if (data['heart'] == true) {
//       heartButtton.className = "fa fa-heart fa-2x";
//     }
//     else {
//       heartButtton.class = "fa fa-heart fa-2x";
//     }
//   })
//   .catch((e) => alert('Sorry Post can\'t be heart'));
// }


function deleteComment(commentId) {
  const deleteItem = document.getElementById(`comment-text-${commentId}`);

  fetch(`/delete-comment/${commentId}`, {method: 'POST'})
  .then((res) => res.json())
  .then((data) => { console.log(data)
      
      if (data['commentLen'] == 0) {
          const options = document.getElementById(`options-${data['postId']}`);
          $(options).load(document.URL + ' ' + `#options-${data['postId']}`);
      }

      else if (data['success']) {
          const parentBox = document.getElementById(`comment-section-${data['postId']}`);
          $(deleteItem).remove();
          $(parentBox).load(document.URL+' '+ `#comment-section-${data['postId']}`);

      }
             
  }).catch((e) => alert('Sorry, can\'t delete this comment'));
 

}


function addComment(postId) {

  let searchData = new URLSearchParams()
  searchData.append('comment', document.getElementById(`comment-${postId}`).value); 
  console.log(document.getElementById(`comment-${postId}`).value);

  fetch(`/add-comment/${postId}`, {method: 'POST',
   body: searchData}).then((res) => res.json())
  .then((data) => { console.log(data)
      if (data['success']) {
          const commentDiv = document.getElementById(`form-reload-${data['postId']}`);
          
          $(commentDiv).load(document.URL + ' '+ `#form-reload-${data['postId']}`);
          
      }

  }).catch((e) => alert('Sorry, can\'t post this comment'));
  return false;
}



function deletePost(postId) {
  
  fetch(`/delete-post/${postId}`, {method: 'POST'}).then((res) => res.json())
  .then((data) => {
      console.log(data);
      if (data['success']) {
          const page = document.getElementById('posts-reload');
          $(page).load(document.URL + ' ' + '#posts-reload')
      }

  }).catch((e) => alert('Sorry, can\'t delete this post'));

}




