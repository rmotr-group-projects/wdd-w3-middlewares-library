# Middleware library

For today's project we're going to build a library of useful middlewares to include in our projects. We've thought of 4 examples of useful middlewares to write, but we've written test cases just for one of them `RequestLoggingMiddleware`. We want you to start writing your own test cases using Django's test client, Django RequestFactory and WebTest (used in previous projects). Here's a quick summary of the middlewares we've thought about.

### RequestLoggingMiddleware

This middleware should log every request made to the site. It should log it in a model `RequestLog`. We've included 1 test case for a GET request. Can you come up with a few test cases for `POST`, `PUT` and `DELETE`?

### ExceptionLoggingMiddleware

This is middleware is similar to the previous one, but it should implement the `process_exception` method to log any errors that happened in the application. Are you going to use `RequestLog` or some other model? Up to you, we just want to see tests!

### SSLRedirectMiddleware

This is a simple middleware that should redirect any request comming to `http` to `https`. It might be a good idea to use WebTest to test this middleware.

### WWWRedirectMiddleware

This is also another simple middleware. The idea is to have a setting like `USE_WWW` that can be either `True` or `False`. If `USE_WWW` is `True` and the request URL doesn't start with `www.`, it should be redirected.
