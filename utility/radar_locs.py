'''
Returns lat, lon of radar for plotting functions
'''

def get_loc(var):

	if var is 'XSCW':
		lon, lat = -122.783451, 38.511884
	if var is 'XEBY':
		lon, lat = -122.062316, 37.815769
	if var is 'XEBY2':
		lon, lat = -122.422901, 37.574263
	if var is 'XSCV':
		lon, lat = -121.833361, 37.398870
	if var is 'XSCR':
		lon, lat = -121.978596, 36.984753

	return lon, lat