// Get the form element

const submitBtn = document.querySelector('.btn-submit');
submitBtn.addEventListener('click', function(event) {
    event.preventDefault(); // prevent the default form submission
    // your Ajax code goes here
});


const form = document.querySelector('customer_form');
const formData = new FormData(form); // gather form data
fetch('/submit-form', {
  method: 'POST',
  body: formData
})
.then(response => {
  if (response.ok) {
    console.log('Form submitted successfully');
    // do something after successful submission
  } else {
    console.error('Error submitting form');
    // handle error
  }
})
.catch(error => {
  console.error('Error submitting form', error);
  // handle error
});
