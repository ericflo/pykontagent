This is a very minimal API into Kontagent, written using purely modules from
the Python standard library.

I haven't put it into production yet, but plan to in the near future (at which
point I will change this notice to say that I am using it in production).

Here's how you might use it:

    from kontagent import Kontagent
    
    k = Kontagent('MY_API_KEY', 'MY_SECRET_KEY')
    k.invite_sent(16904779, [542469672], tracking_tag='testtag')


A full list of all of the methods available is:

 * invite_sent
 * invite_click_response
 * notification_sent
 * notification_click_response
 * notification_email_sent
 * notification_email_response
 * post
 * post_response
 * application_added
 * application_removed
 * undirected_communication_click
 * page_request
 * user_information
 * goal_counts
 * revenue_tracking

You should consult with the Kontagent REST Server API to see what each of these
functions does.  You can find that here:

http://support.kontagent.com/reference/api-documentation/facebook-rest-server-api

Unfortunately, for right now you're going to have to UTSL to find out about the
parameters that each method takes.

Hope you find this useful!