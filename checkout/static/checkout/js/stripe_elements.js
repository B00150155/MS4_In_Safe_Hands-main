var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
// Style of card input
var style = {
  base: {
    color: '#212529',
    fontFamily: '"Josefin Sans", sans-serif',
    fontSmoothing: 'antialiased',
    fontSize: '16px',
    '::placeholder': {
      color: '#c3c1c1'
    }
  },
  invalid: {
    color: '#dc3545',
    iconColor: '#dc3545'
  }
};
// Create the stripe card 
var card = elements.create('card', {
  // Have set stripe so zip/post/eircode is required. Stripe will automatically detect the users country and adjust the form accordingly for zip/post/eircodes. 
  hidePostalCode: false,
  style: style,
});
card.mount('#card-element');

// This code validates any errors on the card input if user enters incorrect card details
card.addEventListener('change', function (event) {
  var errorDiv = document.getElementById('card-errors');
  if (event.error) {
    var html = `
          <span>
              <i class="fas fa-exclamation-circle"></i>
          </span>
          <span>${event.error.message}</span>
      `;
    $(errorDiv).html(html);
  } else {
    errorDiv.textContent = '';
  }
});

// Handle form submit
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
  ev.preventDefault();
  card.update({
    'disabled': true
  });
  $('#submit-button').attr('disabled', true);
  // Payment processing Overlay
  $('#payment-form').fadeToggle(100);
  $('#processing-overlay').fadeToggle(100);

  var saveInfo = Boolean($('#id-save-info').attr('checked'));
  // From using the {% csrf_token %} in the form
  var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
  var postData = {
    'csrfmiddlewaretoken': csrfToken,
    'client_secret': clientSecret,
    'save_info': saveInfo,
  };
  // Added below to test if postData is working
  // console.log(postData); 
  var url = '/checkout/cache_checkout_data/';

  $.post(url, postData).done(function() {
    stripe.confirmCardPayment(clientSecret, {
      payment_method: {
        card: card,
        billing_details: {
          name: $.trim(form.first_name.value) + " " + (form.last_name.value),
          email: $.trim(form.email.value),
          phone: $.trim(form.phone_number.value),
          address: {
            line1: $.trim(form.street_address1.value),
            line2: $.trim(form.street_address2.value),
            city: $.trim(form.town_or_city.value),
            state: $.trim(form.county.value),
            // Removed postcode as stripe will override this as part of the payment form
            country: $.trim(form.country.value),
          }
        }
      },
      shipping: {
        name: (form.first_name.value) + " " + (form.last_name.value),
        phone: $.trim(form.phone_number.value),
        address: {
          line1: $.trim(form.street_address1.value),
          line2: $.trim(form.street_address2.value),
          city: $.trim(form.town_or_city.value),
          state: $.trim(form.county.value),
          postal_code: $.trim(form.eircode.value),
          country: $.trim(form.country.value),
        }
      },
    }).then(function (result) {
      if (result.error) {
        // Error message to user about their card
        var errorDiv = document.getElementById('card-errors');
        var html = `
                  <span class="icon" role="alert">
                  <i class="fas fa-times"></i>
                  </span>
                  <span>${result.error.message}</span>`;
        $(errorDiv).html(html);
        // Payment Processing Overlay
        $('#payment-form').fadeToggle(100);
        $('#processing-overlay').fadeToggle(100);
        card.update({
          'disabled': false
        });
        $('#submit-button').attr('disabled', false);
      } else {
        if (result.paymentIntent.status === 'succeeded') {
          form.submit();
        }
      }
    });
  }).fail(function(){
    // Just reload the page, the error will be in Django messages 
    location.reload();
  });
});