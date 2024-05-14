'''
Returns lat, lon of radar for plotting functions
'''

def get_loc(var):

	if var is 'XSCW':
		lon, lat = -122.802292, 38.521615
	if var is 'XEBY':
		lon, lat = -122.061983, 37.815557
	# if var is 'XEBY2':
	# 	lon, lat = -122.422901, 37.574263
	if var is 'XSCV':
		lon, lat = -121.833361, 37.398870
	if var is 'XSCR':
		lon, lat = -121.978641, 36.984709

	return lon, lat