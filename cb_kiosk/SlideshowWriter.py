import os

""" https://www.w3schools.com/howto/tryit.asp?filename=tryhow_js_slideshow_auto """

"""
	Writes an html file that can display a slideshow
"""
class SlideshowWriter:

	def __init__(self, images: [str], timings_s: [int]):
		self.slides = [os.path.basename(i) for i in images]
		self.timings_s = timings_s

		nb_slides = len(self.timings_s)
		nb_timings = len(self.timings_s)
		if nb_slides != nb_timings:
			msg=f"Incompatible number of slides and timings: {nb_slides} slides and {nb_timings} timings"
			raise ValueError(f)

	def write(self, outfile):
		'''
		Write a webpage using JS to display the slideshow
		Each slide is defined as a div element
		The page will display each div (slide) at a time
		'''
		with open(outfile, 'w') as f:
			f.write(self.bulk_start)

			for idx, _ in enumerate(self.slides):
				div_slide=f"""
<div class="mySlides fade" time="{self.timings_s[idx]}">
  <img src="{self.slides[idx]}" style="width:100%">
</div>

"""
				f.write(div_slide)

			f.write(self.bulk_end)

	bulk_start="""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* {box-sizing: border-box;}
body {font-family: Verdana, sans-serif;}
.mySlides {display: none;}
img {vertical-align: middle;}

/* Slideshow container */
.slideshow-container {
#  max-width: 1000px;
#  position: relative;
  margin: auto;
}

.active {
  background-color: #717171;
}

/* Fading animation */
.fade {
  animation-name: fade;
  animation-duration: 1.5s;
}

@keyframes fade {
  from {opacity: .4} 
  to {opacity: 1}
}

/* On smaller screens, decrease text size */
@media only screen and (max-width: 300px) {
  .text {font-size: 11px}
}
</style>
</head>
<body>

<div class="slideshow-container">

"""
# <div class="mySlides fade" time="2000">
#   <img src="img_nature_wide.jpg" style="width:100%">
# </div>

# <div class="mySlides fade" time="5000">
#   <img src="img_snow_wide.jpg" style="width:100%">
# </div>

# <div class="mySlides fade" time="2000">
#   <img src="img_mountains_wide.jpg" style="width:100%">
# </div>

	bulk_end="""
</div>
<br>

<script>
// Global variable indicating which slides is currently shown
let slideIndex = 0;

// Call the function
showSlides();

// It works by hiding all slides and showing only the one we want
function showSlides() {
  let i;
  
  // Default configuration
  let slides = document.getElementsByClassName("mySlides"); // Get all the slides
  for (i = 0; i < slides.length; i++) { // Hide all the slide
	slides[i].style.display = "none";  
  }
  
  // Pass to the next slide
  slideIndex++;
  // Handle looping around
  if (slideIndex > slides.length) {slideIndex = 1}
  
  // Display the slide and leave it for some time
  let cur_slide = slides[slideIndex-1]
  cur_slide.style.display = "block"; // Show the silde
  let display_time = parseInt(cur_slide.getAttribute("time")) // get the time the slide should be displayed from the text attribute "time"
  setTimeout(showSlides, display_time); // Change image
}
</script>

</body>
</html>
"""
