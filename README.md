# MandelbrotSet

## Detailed description

### Mandelbrot set

According to the [Wikipedia](https://en.wikipedia.org/wiki/Mandelbrot_set) article about Mandelbrot set :

> The Mandelbrot set is the set of values of c in the complex plane for which the orbit of 0 under iteration of the complex quadratic polynomial
> ![alt text](https://upload.wikimedia.org/math/5/a/d/5adf5f6cc8f7e30a1fdb1c37bbb785c3.png "Mandelbrot sequence")
> remains bounded.
> For our purpose, to compute the Mandelbrot set :

- the complex plan <==> the image
- for each pixel of coordinate (i, j) in the image, using the previous recurrence relation test if it is bounded

To implement this condition for our computers (quote from [Introduction to Programming in Java book](http://introcs.cs.princeton.edu/java/32class/)) :

> Given a complex point, we can compute the terms at the beginning of its sequence, but may not be able to know for sure that the sequence remains bounded.
> Remarkably, there is a test that tells us for sure that a point is not in the set: if the magnitude of any number in the sequence ever gets to be greater than 2 (like 3 + 0i), then the sequence will surely diverge.
