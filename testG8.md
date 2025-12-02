This is the testing file for our project

CRSF


SECURE CART



DEBUG MODE
Debug mode can be tested by pasting into the url any random thing and then trying to navigate to that page
this will reveal the debug page error revealing information that normal users shouldnt see and can lead attackers to 
see critical system infrastructure that can be used for malicous purposes.


ORDER HISTORY

To test the order history on the original code version you have the system must first have an order be placed within the system
Once an order exists if any user acquires the order number they can then paste it into the url with the following path 

localhost:8000/profile/order_history/{ORDER NUMBER}

This can be done from any user or any un logged in user 