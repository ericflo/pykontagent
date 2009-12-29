from setuptools import setup, find_packages
 
version = '0.3'

LONG_DESCRIPTION = """
This is a very minimal API into Kontagent, written using purely modules from
the Python standard library.

Here's how you might use it:

    from kontagent import Kontagent
    
    k = Kontagent('MY_API_KEY', 'MY_SECRET_KEY')
    k.invite_sent(16904779, [542469672], tracking_tag='testtag')

This is now being used in production for http://radiosox.com/

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
 * raw_request

You should consult with the Kontagent REST Server API to see what each of these
functions does.  You can find that here:

http://developers.kontagent.com/reference/api-documentation/facebook-rest-server-api

Unfortunately, for right now you're going to have to UTSL to find out about the
parameters that each method takes.

Hope you find this useful!
"""

setup(
    name='pykontagent',
    version=version,
    description="A simple interface into the Kontagent REST API",
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Web Environment",
    ],
    keywords='kontagent,rest,api,client',
    author='Eric Florenzano',
    author_email='floguy@gmail.com',
    url='http://github.com/ericflo/pykontagent',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools'],
)