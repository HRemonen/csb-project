### FLAW 1: A01:2021 – Broken Access Control
The developers have created an URL for viewing user information of all the users using the application. This view was solely ment for development admin use only as the developers did not remember all of the test user information. Somehow it has made its way into production servers and anyone could access the user information.

#### LOCATION:
https://github.com/HRemonen/csb-project/blob/0a13853ea4ac085861e3bc147cda9d8858f23eb0/securepolls/views.py#L131

#### FIX:
The developers were on the right track as they have made the *superuser* check in the **index.html** file: https://github.com/HRemonen/csb-project/blob/0a13853ea4ac085861e3bc147cda9d8858f23eb0/securepolls/templates/securepolls/index.html#L15. However the developers have failed to solve issue where users of any type could just type in the **/users** in the URL and access all of the user information this way.

Solution that would fix the current solution would be to check for *superuser* access in the view also: https://github.com/HRemonen/csb-project/blob/0a13853ea4ac085861e3bc147cda9d8858f23eb0/securepolls/views.py#L132

Even better solution would be to remove this kind of feature all along from the application, because the database is accessible through the Django admin panel, thus providing access to the user information if needed.

### FLAW 2: A04:2021 – Insecure Design
