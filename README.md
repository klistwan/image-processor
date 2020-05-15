## Image Processing Libraries
There are many Python libraries that offer image processing functionality:
- [scikit-image](https://github.com/scikit-image/scikit-image) - 3.7k stars, last commit yesterday, 366 contributors
- [Pillow](https://github.com/python-pillow/Pillow) - 7.3k stars, last commit yesterday, 270 contributors
- [OpenCV](https://github.com/skvark/opencv-python)  - 1.3k stars, last commit in April, 20 contributors
- [PIL](http://www.pythonware.com/products/pil/) - discontinued and lacks Python 3 support

In this case, I decided to be pragmatic and choose Pillow. It's received a lot of positive feedback on StackOverflow and resizing an image into a 100x100px can be done in three lines of code:

```python
image = Image.open("mt_fuji.jpg")
image.thumbnail((100,100))
image.save("thumbnail.jpg")
```

When building such a system for production use, much more in-depth research should be done, alongside proper performance testing. For example, just looking at Pillow's [performance testing(https://python-pillow.org/pillow-perf/), there's a highly optimized downstream fork named [Pillow-SIMD](https://github.com/uploadcare/pillow-simd) that is both production-ready and comes with performance improvements.

Resize functionality can also be implemented using [different algorithms](https://uploadcare.com/blog/the-fastest-image-resize/) (e.g. fast nearest neighbour, convolution resampling). As a result, depending on our constraints (e.g. memory, CPU, execution time, photo quality), we'd want to look more in-depth at any library we're considering to understand the details of how it works and why it works the way. 