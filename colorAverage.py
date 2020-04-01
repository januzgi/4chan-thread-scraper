import requests, json, grequests
from io import BytesIO
from PIL import Image


# Load the img urls from the imgUrls.json
with open('imgUrls.json') as json_file:
    urls = json.load(json_file)

# Define the url array
sortedUrls = []
# Define the colors array
colors = []
# Count IOErrors in imageAnalyze()
errorCount = 0

dics = len(urls['links']) # urls dictionary
i = 1 # links array (up from 1)
# for the ~150 dics in urls:
while i < 5:
	dicLength = len(urls['links'][i])
	j = 0
	# links[i] contains lists of dictionaries
	while j < dicLength:
		# key 'link' has the value URL 
		# Continue to next when the file is deleted
		if 'deleted' in urls['links'][i][j]['link']:
			j += 1 
			continue 
		# Add each valid URL into an array
		sortedUrls.append(urls['links'][i][j]['link'])
		# Increase j for next iteration
		j += 1
	# Increase i for next iteration
	i += 1

print 'Succesfully read the img urls from imgUrls.json.'


# Calculate HSV color from RGB 
def rgb_to_hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df/mx)*100
    v = mx*100

    # Round numbers
    h = round(h, 0)
    s = round(s, 0)
    v = round(v, 0)

    # Float to int
    hI = int(h)
    sI = int(s)
    vI = int(v)

    hsv = 'invalid'
    #Choose only the green and red / magenta colors from the list
    # Saturation(S) needs to be larger than 50
    if (sI < 50): 
        return hsv

    # Lightness (V) needs to be larger than 30
    if (vI < 30):
        return hsv

    # Add a flag whether r or g hue
    # r = red/pink/magenta, g = green
    # Green Hue (H) from 80 - 160
    if (79 < hI < 161):
        hsv = 'g' + ',' + str(hI) + ',' + str(sI) + ',' + str(vI)
        return hsv

    # Red/Magenta hue (H) from 280 - 360 or 0 - 20
    if ((-1 < hI < 21) or (279 < hI < 361)):
        hsv = 'r' + ',' + str(hI) + ',' + str(sI) + ',' + str(vI)
        return hsv

    # rest of the colors not interesting to us, return 'invalid'
    return hsv



def imageAnalyze(requests):
	# Get the amount of responses
	itemsLength = len(list(requests))

	print 'Begin image analyzing...'
	# Loop through each response content (the img) and analyze the color
	i = 0
	# Reset errors to 0
	errorCount = 0
	while i < itemsLength:
		# Check if the response object exists
		if (list(requests)[i] is None):
			# Next iteration increase
			i += 1
			continue
			
		# Continue only if the request was succesful
		if (list(requests)[i].status_code != 200): 
			# Next iteration increase
			i += 1
			continue
	    
	    # BytesIO may cause error at times, thus with try except
		try:
			# Open the img bytes
			imgBytes = BytesIO(list(requests)[i].content)
			imgBytes.seek(0)
			img = Image.open(imgBytes)
		except IOError as e:
			print 'I/O error: {1}'.format(e)
			# Skip this content
			# If more IOErrors, break and retry from start
			if (errorCount > 5):
				break
			# Next iteration increase
			i += 1
			continue

		# Resize the img to 1x1 pixels
		img2 = img.resize((1, 1))
		# Get the RGB color of the one pixel
		color = img2.getpixel((0, 0))

		# Puts tuple to single string colors rgb
		r, g, b = color
		# Convert the rgb to HSV for determining the color
		# whether it is red/magenta or green
		colorHsv = rgb_to_hsv(r, g, b)

		if (colorHsv == 'invalid'): 
			# Next iteration increase
			i += 1
			continue

		# Save the colors in the correct range
		colors.append(colorHsv)
		
		# Next iteration increase
		i += 1



def run_qrequests():
	print 'Begin grequests to urls...'

	# Get each picture and its average color
	rs = (grequests.get(u) for u in sortedUrls)
	# Send the requests
	requests = grequests.map(rs)

	print 'grequests complete.'

	imageAnalyze(requests)


run_qrequests()


if (errorCount > 5):
	run_qrequests()


print '\nAll valid colors:\n'
print('\n'.join(colors))


# Save the list of colors into a file
with open('colors.json', 'w') as outfile:
    json.dump(colors, outfile)

print 'Succesfully wrote colors.json.'
