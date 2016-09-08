# Middleware library

For today's project we're going to build a library of useful middlewares to include in our projects. We've thought of 3 examples of useful middlewares to write, but we've written test cases just for one of them `RequestLoggingMiddleware`. We want you to start writing your own test cases using Django's test client, Django RequestFactory and WebTest (used in previous projects). Here's a quick summary of the middlewares we've thought about.

### RequestLoggingMiddleware

This middleware should log every request made to the site. It should log it in a model `RequestLog`. We've included 1 test case for a GET request. Can you come up with a few test cases for `POST`, `PUT` and `DELETE`?

### ExceptionLoggingMiddleware

This is middleware is similar to the previous one, but it should implement the `process_exception` method to log any errors that happened in the application. Are you going to use `RequestLog` or some other model? Up to you, we just want to see tests!

### SSLRedirectMiddleware

This is a simple middleware that should redirect any request coming to `http` to `https`. It might be a good idea to use WebTest to test this middleware.
