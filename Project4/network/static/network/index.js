document.addEventListener("DOMContentLoaded", () => {

  document.querySelectorAll("#edit").forEach((editElement) => {
    editElement.addEventListener('click', (event) =>{
      editElement.innerHTML="";
      event.preventDefault();
      const postId = editElement.getAttribute('data-post-id');
      let content = document.querySelector(`#content-${postId}`);
      let formGroup= document.createElement("div");
      let text= document.createElement("textarea");
      let save = document.createElement("a");
      save.href="#";
      let cancel = document.createElement("a");
      cancel.href="#";
      let save_cancel= document.createElement("div");

      save.classList.add("no-underline","g-font-size-12","ms-1");
      save.innerHTML="save";
      cancel.classList.add("no-underline","ms-4","g-font-size-12");
      cancel.innerHTML= "cancel";

      save_cancel.appendChild(save);
      save_cancel.appendChild(cancel);
      text.innerHTML = content.innerHTML;
      formGroup.classList.add("form-control");

      formGroup.appendChild(text);
      formGroup.appendChild(save_cancel);

      content.innerHTML="";
      content.appendChild(formGroup);
      
      save.addEventListener('click', (event) => {
        event.preventDefault();
        save.innerHTML=""
        cancel.innerHTML="";
        content.innerHTML= text.value;
        //now I need to fetch method=PUT and change the data of the post with id= post.id
        fetch(`/update_post/${postId}`, {
          method: "PUT",
          body: JSON.stringify({
            content: text.value
          })
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            console.log("Post updated successfully");
          } else {
            console.error("Error updating post:", data.error);
          }
          editElement.innerHTML="Edit";
        })
        .catch(error => {
          console.error('Error:', error);
        });
      })
      cancel.addEventListener('click', (event) => {
        event.preventDefault();
        save.innerHTML=""
        cancel.innerHTML="";
        content.innerHTML= text.innerHTML;
        editElement.innerHTML="Edit";

      })
    })
  });
  // for each like element: 
  document.querySelectorAll("#like").forEach((likeElement) => {
    // add an event listener if the user clicks the like
    likeElement.addEventListener("click", (event) => {
      event.preventDefault(); //so that when we click on the like button we don't go back by default to the top of the page
      const postId = likeElement.getAttribute("data-post-id");

      fetch(`/toggle_like/${postId}`, {
        method: "PUT"
        })
      .then(response => response.json()) // Parse the JSON body
      .then(data => {
        console.log(data.message);
        loadLikesUI(postId, likeElement);
      })
      .catch(error => {
        console.error('Error:', error);
      });
       

    });

    const postId = likeElement.getAttribute("data-post-id");
    loadLikesUI(postId, likeElement);  
  });
});





function loadLikesUI(postId, likeElement) {
  fetch(`/likes/${postId}`)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      let heart = document.createElement("i");
      heart.classList.add("bi");
      data.user_has_liked? heart.classList.add("bi-suit-heart-fill"): heart.classList.add("bi-suit-heart");

      let count = document.createElement("small");
      count.innerHTML = `&nbsp;${data.likes_count}`;

      // clear existing children before appending new ones
      likeElement.innerHTML = '';
      likeElement.appendChild(heart);
      likeElement.appendChild(count);
    })
    .catch((error) => {
      console.error("Error fetching post likes:", error);
    });
}
