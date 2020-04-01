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

dics = len(urls['links']) # urls dictionary
i = 1 # links array (up from 1)
# for the ~150 dics in urls:
while i < 10:
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
        # print 'saturation invalid (not over 50): ',sI
        return hsv

    # Lightness (V) needs to be larger than 30
    if (vI < 30):
        # print 'lightness invalid (not over 30): ',vI
        return hsv

    # Add a flag whether r or g hue
    # r = red/pink/magenta, g = green
    # Green Hue (H) from 80 - 160
    if (79 < hI < 161):
        # print 'color greenish (H 80 - 160):'
        hsv = 'g' + ',' + str(hI) + ',' + str(sI) + ',' + str(vI)
        print hsv
        return hsv

    # Red/Magenta hue (H) from 280 - 360 or 0 - 20
    if ((-1 < hI < 21) or (279 < hI < 361)):
        # print 'color red/magenta (H 0 - 20 OR 280 - 360):'
        hsv = 'r' + ',' + str(hI) + ',' + str(sI) + ',' + str(vI)
        print hsv
        return hsv

    # rest of the colors not interesting to us, return 'invalid'
    return hsv



# Get each picture and its average color
rs = (grequests.get(u) for u in sortedUrls)
# Send the requests
requests = grequests.map(rs)

# Get the amount of responses
itemsLength = len(list(requests))

# Loop through each response content (the img) and analyze the color
i = 0
while i < itemsLength:
	# Continue only if the request was succesful
	if (list(requests)[i].status_code != 200): 
		# Next iteration increase
		i += 1
		continue

	# Open the img bytes
	imgBytes = BytesIO(list(requests)[i].content)
	imgBytes.seek(0)
	img = Image.open(imgBytes)
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


# Sort the in ascending order
colors.sort();

# Save the list of colors into a file
print('\n'.join(colors))




































