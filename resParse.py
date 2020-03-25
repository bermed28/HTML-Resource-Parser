"""Parse the contents of an HTML file and output the internal resources used.

We are looking for tags of interest: a, script, link, and img.
Within each tag of interest we're looking for a particular attribute of
interest (href for a & link, src for script & img).
A list is created for each type of tag, storing all of the internal 
resources referenced by tags of that type.
Finally, the results are stored in an output file.

Input:  The file index.html will be used as an input file
Output: The results will be stored in a file named index_resources.txt
"""

def load_data():
	"""Returns the contents of index.html in a list, or None if an error occurs."""
	try:
		fh = open('index.html')
	except:
		lstOfLines = None
	else: # Only gets executed if no exception was raised
		lstOfLines = fh.readlines()
		fh.close()
	return lstOfLines


def get_tag_of_interest(line):

	"""Return a tag of interest if one is found in the line, or None otherwise."""

	# Look for any of the tags of interest within this line.
	# If one is found, return that tag (from '<' to '>' of the opening tag only)
	# For example:
	#    If line is "Here is a <a href='sample.html' target='_blank'>sample</a> link",
	#    then we would return "<a href='sample.html' target='_blank'>".

	startTag = line.find("<")
	endTag = line.find(">")
	tag = line[startTag: endTag + 1]
	if ("<a" in tag) or ("<script" in tag) or ("<link" in tag) or ("<img" in tag):
		print(tag)
		return tag
	else:
		return ""

def get_attr_of_interest(openingTag):
	"""Return value of attribute of interest if one is in the tag, or None otherwise."""
	# Look for the attribute of interest for the tag specified.
	# If it is found, return that attribute's value (should be between quotes).
	# For example:
	#    If openingTag is "<a href='sample.html' target='_blank'>",
	#    then we would return "sample.html".
	# Remember to avoid external resources and mailing hyperlinks.
	# Note: It's possible that a tag of interest has no attribute of interest.
	html = ".html"
	css = ".css"
	js = ".js"

	# href for css and hyperlinks, src for js ang img
	attribute = ["href=", "src="]

	#Accepted image file types in html
	imageFileExtensions = [".apng", ".bmp", ".gif", ".ico", ".cur", ".jpg", ".jpeg", ".jfif", ".pjpeg", ".pjp", ".png", ".svg", ".tiff", ".tif", ".wepb"]

	if len(openingTag) > 0:
		openingTag.strip()
		if(attribute[0] in openingTag) and (css in openingTag): # css files
			start = openingTag.find(attribute[0]) + (len(attribute[0]) + 1)
			end = openingTag.find(css) + len(css)
			return openingTag[start:end]

		if (attribute[1] in openingTag) and (js in openingTag):  #js files
			start = openingTag.find(attribute[1]) + (len(attribute[1]) + 1)
			end = openingTag.find(js) + len(js)
			return openingTag[start:end]

		if (attribute[1] in openingTag):  # image files
			for extension in imageFileExtensions:
				if extension in openingTag:
					start = openingTag.find(attribute[1]) + (len(attribute[1]) + 1)
					end = openingTag.find(extension) + len(extension)
					return openingTag[start:end]
		if (attribute[1] in openingTag):  #hyperlinks
			if(html in openingTag):
				start = openingTag.find(attribute[1]) + (len(attribute[1]) + 1)
				end = openingTag.find(html) + len(html)
				return openingTag[start:end]

	else:
		return ""

def write_results(outFH, sectionName, listOfResources): #f(x) = y
	"""Write the resources of a particular section to an already opened file."""
	# outFH should be the file handle of an output file
	# Remember that the section name must be followed by a colon,
	# and the list of resources must be in alphabetical order.
	# If there are no resources for a section, nothing should be outputted.
	if len(listOfResources) != 0:
		if len(listOfResources) > 1:
			listOfResources.sort()
		outFH.write(sectionName + ":" + '\n')
		for resource in listOfResources:
			outFH.write(resource + '\n')
	else:
		return

def main():
	css = []
	js = []
	imgs = []
	hyper = []

	OUTPUT_FILENAME = "index_resources.txt"

	linesInFile = load_data()
	handler = open(OUTPUT_FILENAME, "w")
	if linesInFile is None:
		print('ERROR: Could not open index.html!')
		exit()
	else:
		for line in linesInFile:
			if len(line) > 0:
				tag = get_tag_of_interest(line)
				if len(tag) > 0:
					attribute = get_attr_of_interest(tag)
					if tag.startswith("<a"):
						if not (attribute.startsWith("http:") or attribute.startsWith("https:") or (".com" in attribute)):
							hyper.append(attribute)
					elif tag.startswith("<script"):
						js.append(attribute)
					elif tag.startswith("<link"):
						css.append(attribute)
					elif tag.startswith("<img"):
						imgs.append(attribute)

	write_results(handler, "CSS", css)
	write_results(handler, "JavaScript", js)
	write_results(handler, "Images", imgs)
	write_results(handler, "HyperLinks", hyper)

	handler.close()

	# Loop through linesInFile and process each line
	# In each line look for a tag of interest.
	# If such a tag is found, within that tag look for an attribute of interest
	# If such an attribute is found, store its value in a list, depending
	#    on what type of tag it was.
	# Once you loop through all of the lines, write the results.
	# For each section of output, call write results with the "title" of that 
	#     section and the list of resources for that section.
	#     To minimize I/O, open the output file once, before your calls to
	#     write_result, and then close it after all calls to write_results.


# This line makes python start the program from the main function
# unless our code is being imported
if __name__ == '__main__':
    main()
