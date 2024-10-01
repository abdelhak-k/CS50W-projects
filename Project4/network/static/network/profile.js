document.addEventListener("DOMContentLoaded", () => {
  let follow_count = document.querySelector("#follow-count");
  const user_id = follow_count.getAttribute("data-user-id");
  
  let followed;

  // Load the initial follow count and state
  load_follow_count(user_id).then(followedState => {
      followed = followedState;
  });

  let followButton = document.getElementById('follow-button');
  if (followButton) {
    followButton.addEventListener('click', (event) => {
        event.preventDefault();
        
        fetch(`/toggle_follow/${user_id}`, {
            method: "PUT",
            body: JSON.stringify({
                action: followed ? 'unfollow' : 'follow'
            })
        })
        .then(response => response.json()) // Parse the JSON body
        .then(data => {
            console.log(data.message);
            // Reload follow count and update followed state
            load_follow_count(user_id).then(followedState => {
                followed = followedState;
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
  }
});

function load_follow_count(user_id) {
  return fetch(`/follows_count/${user_id}`)
      .then(response => response.json())
      .then(data => {
          document.getElementById('followers-count').innerHTML = `<b>${data.followers_count}</b> Followers`;
          document.getElementById('followings-count').innerHTML = `<b>${data.followings_count}</b> Followings`;

          let followButton = document.getElementById('follow-button');
          if (followButton) {
            if (data.followed) {
                followButton.innerHTML = "Unfollow";
                followButton.classList.remove("btn-outline-primary");
                followButton.classList.add("btn-outline-danger");
            } else {
                followButton.innerHTML = "Follow";
                followButton.classList.remove("btn-outline-danger");
                followButton.classList.add("btn-outline-primary");
            }
          }

          return data.followed;
      })
      .catch(error => {
          console.error('There has been a problem with your fetch operation:', error);
      });
}
