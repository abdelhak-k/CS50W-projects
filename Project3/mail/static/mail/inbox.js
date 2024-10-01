document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document
    .querySelector("#inbox")
    .addEventListener("click", () => load_mailbox("inbox"));
  document
    .querySelector("#sent")
    .addEventListener("click", () => load_mailbox("sent"));
  document
    .querySelector("#archived")
    .addEventListener("click", () => load_mailbox("archive"));

  document.querySelector("#compose").addEventListener("click", compose_email);
  
  document.querySelector('#compose-form').addEventListener('submit', form_submit);
  
  // By default, load the inbox
  load_mailbox("inbox");

});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#email-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";
}

function form_submit(event) {
  event.preventDefault(); //this is crucial so that the eventListner do not load the inbox page again
  recipients = document.querySelector("#compose-recipients").value;
  subject = document.querySelector("#compose-subject").value;
  mailbody = document.querySelector("#compose-body").value;

  // Send a POST request to the server with the email data
  fetch("/emails", {
    method: "POST",
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: mailbody,
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      load_mailbox("sent");
      alert(result.message);
    });
    // load the sent mailbox

}

function load_mailbox(mailbox) {
  console.log(mailbox);
  // Show the mailbox and hide other views
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#email-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "none";

  // Show the mailbox name
  let email_view = document.querySelector("#emails-view");
  email_view.innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;

  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      if (emails.length == 0) {
        email_view.innerHTML = "There is nothing to see here.";
      } else {
        for (let email of emails) {
          //we check if there are emails or not

          /*
          "id","sender","recipients","subject","body","timestamp","read","archived"
          */
          let mail = document.createElement("div"); // The email container
          mail.classList.add("row", "mb-3", "email");

          if (email.read) {
            mail.classList.add("read");
          } else {
            mail.classList.add("unread");
          }

          let sender = document.createElement("div");
          sender.classList.add("col-md-3");
          sender.innerHTML = email.sender;

          let subject = document.createElement("div");
          subject.classList.add("col-md-7");
          subject.innerHTML = email.subject;

          let time = document.createElement("div");
          time.classList.add("time");
          time.innerHTML = email.timestamp;

          mail.appendChild(sender);
          mail.appendChild(subject);
          mail.appendChild(time);

          if (mailbox != "sent") {
            let archive = document.createElement("button");
            archive.style.marginLeft = "10px";
            if (email.archived) {
              archive.classList.add("btn", "btn-secondary", "archive");
              archive.innerHTML = "unarchive";
            } else {
              archive.classList.add("btn", "btn-danger", "archive");
              archive.innerHTML = "archive";
            }

            archive.addEventListener("click", (event) => {
              event.stopPropagation(); // When we click on the child element, we don't mean the parent mail
              //mark archived as true
              let isArchived = email.archived;
              fetch(`/emails/${email.id}`, {
                method: "PUT",
                body: JSON.stringify({
                  archived: !isArchived,
                }),
              }).then((response) => {
                if (response.ok) {
                  //if there is no problem then load the mail box and to make sure that the fetch was completed
                  load_mailbox("inbox");
                }
              });
            });
            mail.appendChild(archive);
          }

          mail.addEventListener("click", function () {
            //mark email as read
            fetch(`/emails/${email.id}`, {
              method: "PUT",
              body: JSON.stringify({
                read: true,
              }),
            });
            view_email(email.id, mailbox);
          });
          email_view.appendChild(mail);
        }
      }
    });
}

function view_email(email_id, mailbox) {
  // Show the email info and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "none";
  document.querySelector("#email-view").style.display = "block";

  // Display email contents
  fetch(`/emails/${email_id}`)
    .then((response) => response.json())
    .then((email) => {

      let email_view = document.querySelector("#email-view");
      email_view.innerHTML = "";
      let mail = document.createElement("div");

      let subject = document.createElement("h4");
      subject.innerHTML = email.subject;

      let body = document.createElement("div");
      body.classList.add("body");
      body.innerHTML = `<p>${email.body}</p>`;

      let header = document.createElement("div");
      header.classList.add("row", "mb-3");

      let sender = document.createElement("div");
      sender.classList.add("col-md-8");
      sender.innerHTML = `from: <b>${email.sender}</b>`;
      let time = document.createElement("div");
      time.classList.add("time");
      time.innerHTML = email.timestamp;

      let reply = document.createElement("button");

      reply.classList.add("btn", "btn-outline-primary");
      reply.innerHTML = "reply";
      reply.addEventListener("click", () => {
        reply_to_email(email);
      });

      if (mailbox != "sent") {
        let archive = document.createElement("button");
        archive.style.marginBottom = "10px";
        if (email.archived) {
          archive.classList.add("btn", "btn-secondary", "archive");
          archive.innerHTML = "unarchive";
        } else {
          archive.classList.add("btn", "btn-danger", "archive");
          archive.innerHTML = "archive";
        }

        archive.addEventListener("click", (event) => {
          event.stopPropagation(); // When we click on the child element, we don't mean the parent mail
          //mark archived as true
          let isArchived = email.archived;
          fetch(`/emails/${email.id}`, {
            method: "PUT",
            body: JSON.stringify({
              archived: !isArchived,
            }),
          }).then((response) => {
            if (response.ok) {
              //if there is no problem then load the mail box and to make sure that the fetch was completed
              isArchived ? load_mailbox("archive") : load_mailbox("inbox");
            }
          });
        });
        mail.appendChild(archive);
      }
      header.appendChild(sender);
      header.appendChild(time);

      mail.appendChild(subject);
      mail.appendChild(header);
      mail.appendChild(body);
      mail.appendChild(document.createElement("br"));
      mail.appendChild(reply);

      email_view.appendChild(mail);
    });
}

function reply_to_email(email) {
  compose_email();
  document.querySelector("#compose-recipients").value = email.sender;
  if (email.subject.slice(0, 3) != "Re:") {
    document.querySelector("#compose-subject").value = `Re: ${email.subject}`;
  } else {
    document.querySelector("#compose-subject").value = email.subject;
  }
  document.querySelector("#compose-subject").disabled = true;

  document.querySelector(
    "#compose-body"
  ).value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}\n---\nreply:`;
  document.querySelector("#compose-recipients").disabled = true;
}
