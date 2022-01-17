Challenge 2: Django Test
Problem Overview
Write a simple application that allows a user to manage subscriptions using Stripe and Python Django 2.
Problem Details
Upon user signup, we want the user to sign up for a free trial of a Aben Premium membership which includes 7 days of premium service. Afterwards the user will be charged $49.99 per month.
When a user decides to sign up, the Subscription must be activated and we must track trial expiration. After 7 days, the initial charge of $49.99 must be charged on the test credit card.
On the Stripe interface, this must appear as a trial subscription.
The user can cancel their subscription at any time. Upon cancellation, the subscription is marked as cancelled and would also appear on the Stripe interface as a cancelled subscription.
Technical Requirements
Use django registration (https://django-registration.readthedocs.io/en/3.1/) for the user signup.
Databases can be MySQL or PostgreSQL.
Design a Subscription Model with state fields that represent different stages of the subscription process. (You can name the different stages in your own naming convention).
Code must be pep8 compliant.
Code must have comments explaining functionality.
You can use standard bootstrap code for user interface.

