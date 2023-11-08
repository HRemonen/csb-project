### FLAW 1: A01:2021 – Broken Access Control

The developers have created a URL for viewing user information of all the users using the application. This view was solely meant for development admin use only, as the developers did not remember all of the test user information. Somehow, it has made its way into production servers, and anyone could access the user information.

#### LOCATION:

https://github.com/HRemonen/csb-project/blob/0a13853ea4ac085861e3bc147cda9d8858f23eb0/securepolls/views.py#L131

#### FIX:

The developers were on the right track as they have added a *superuser* check in the https://github.com/HRemonen/csb-project/blob/0a13853ea4ac085861e3bc147cda9d8858f23eb0/securepolls/templates/securepolls/index.html#L15. However, the developers have failed to solve the issue where users of any type could simply type in **/users** in the URL and access all of the user information this way.

The solution that would fix the current issue would be to check for *superuser* access in the view as well: https://github.com/HRemonen/csb-project/blob/0a13853ea4ac085861e3bc147cda9d8858f23eb0/securepolls/views.py#L132

An even better solution would be to remove this feature from the application altogether, as the database is accessible through the Django admin panel, providing access to the user information if needed.

### FLAW 2: A04:2021 – Insecure Design

The application was missing a feature to reset user passwords. As the application did not store anything other than *username* and *password* from users, the password reset system did end up rather simple. To reset your password, you just type in your *username* and the *password* will be defaulted back to no other than the good ol' **password**. This allowed resetting any user's password (even the admin password) and gaining access to the user's account.

#### LOCATION:

https://github.com/HRemonen/csb-project/blob/0a13853ea4ac085861e3bc147cda9d8858f23eb0/securepolls/views.py#L67

#### FIX:

The most obvious fix would be to let the user prompt password and also a confirmation to the password. The password and confirm password would then be checked that they match and after that the user's password would be updated to that password avoiding any boilerplate or suggested passwords at all costs.

Also, there is a need to verify the user somehow before setting a new password. This would need an update to the user model information, as something like an email would be needed.

### FLAW 3: A05:2021 – Security Misconfiguration

Once again, the developers have exceeded their intelligence while they configured the superuser account **admin** for the application. As the developers were thinking hard of a good password which every developer on the team would remember and also that was fast to type, no other choice was discussed than the legendary password **admin**.

#### LOCATION:

As the superuser configuration is created on the console the issue does not reside anywhere in the codebase. However the following process is done when creating new superuser to the application [screenshot](admin_conf.png).

#### FIX:

Django includes built-in warnings for insecure configuration, but these warnings can be skipped without any backlashes. The overall fix and recommendation would be to listen to these errors or at least to question yourself before dismissing the errors.

Here the problem would have been avoided if the developers would have listened to Django's recommendations.

### FLAW 4: A09:2021 – Security Logging and Monitoring Failures

The application lacks proper security logging and monitoring, which leaves it vulnerable to undetected security incidents and breaches. In the absence of a robust logging and monitoring system, the application remains blind to potential threats, making it difficult to identify and respond to security issues in a timely manner.

#### LOCATION:

This flaw is not specific to a particular code location, as it pertains to the overall logging and monitoring strategy of the application.

#### FIX:
To address the Security Logging and Monitoring Failures in an application, it is essential to implement a comprehensive logging and monitoring framework. Here are some steps to achieve this:
- Pick any used and well-known 3rd party or built-in logging framework that can be leveraged to log important security-related events. For example in Django project's settings, you can configure the logging settings, including the log file, log level, and log format.
- Identify and log security-related events such as failed login attempts, unauthorized access, and critical system operations. Make sure to include relevant details like timestamps, user IP addresses, and the specific actions taken.
- Set up a monitoring system that continuously monitors the log files for suspicious activities. Tools like Grafana, Gibana or centralized logging services can be used for log analysis and real-time alerting.

### FLAW 5: Cross-Site Request Forgery (CSRF) Vulnerability
As the developers had taken care of disabling CSRF tokens and excepted the middleware the application is susceptible to CSRF attacks, which can allow malicious actors to perform unauthorized actions on behalf of an authenticated user. CSRF vulnerabilities occur when the application fails to validate and verify that requests made to it originate from a legitimate and trusted source, typically a user's browser.

#### LOCATION:
CSRF vulnerabilities exists throughout the application on the https://github.com/HRemonen/csb-project/blob/main/securepolls/views.py file and the https://github.com/HRemonen/csb-project/tree/main/securepolls/templates/securepolls directory.

#### FIX:
Django mitigates CSRF vulnerabilities by default with the use of **csrf_token**s and a **CSRF Middleware**. Most if not all modern trusted browsers and frameworks have also in-built CSRF protection. So the fix would be to remove all of the **@csrf_exempt** from the *views.py* file for example https://github.com/HRemonen/csb-project/blob/1b0b3e58e8fa4bffa4cc82297458dda58d2fb942/securepolls/views.py#L25 and also enable the **{% csrf_token %}** on all of the forms in the *templates* directory for example https://github.com/HRemonen/csb-project/blob/1b0b3e58e8fa4bffa4cc82297458dda58d2fb942/securepolls/templates/securepolls/login.html#L4.


