This is the testing file for our project

CRSF
There is no check for a POST request for deletion of product. 
This can result in a CSRF attack where the admin could be phished to visit a malicious website that uses a GET request to alter the database and delete products.

SECURE CART
Attackers could modify the values in the cart such as price or quantity before sending it to the server. 
This allowed unrealistic quantities and negative numbers to be added leading to performance issues including denial-of-service attacks.


DEBUG MODE
Debug mode can be tested by pasting into the url any random value and then trying to navigate to that page.
This will reveal the debug page error revealing information that normal users shouldn't see and can lead attackers to 
see critical system infrastructure that can be used for malicous purposes.


ORDER HISTORY
The order history page was discovered to be open to anyone who had the correct order number and any user could get to the page using the url even if they were unlogged in showing broken access control.

localhost:8000/profile/order_history/{ORDER NUMBER}

This can be done from any user or any un-logged in user 
