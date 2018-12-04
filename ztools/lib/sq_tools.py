'''	
versions = 
    450:       "1.0.0", -> keygeneration = 0
    65796:     "2.0.0", -> keygeneration = 1
    131162:    "2.1.0", -> keygeneration = 1
    196628:    "2.2.0", -> keygeneration = 1
    262164:    "2.3.0", -> keygeneration = 1
    201327002: "3.0.0", -> keygeneration = 2
    201392178: "3.0.1", -> keygeneration = 3
    201457684: "3.0.2", -> keygeneration = 3
    268435656: "4.0.0", -> keygeneration = 4
    268501002: "4.0.1", -> keygeneration = 4
    269484082: "4.1.0", -> keygeneration = 4
    335544750: "5.0.0", -> keygeneration = 5
    335609886: "5.0.1", -> keygeneration = 5
    335675432: "5.0.2", -> keygeneration = 5
    336592976: "5.1.0", -> keygeneration = 5
    402653494: "6.0.0-4", -> keygeneration = 6 
    402653514: "6.0.0", -> keygeneration = 6
    402653544: "6.0.0", -> keygeneration = 6
    402718730: "6.0.1", -> keygeneration = 6
    403701850: "6.1.0", -> keygeneration = 6
    404750376: "6.2.0" -> keygeneration = 7
'''	

def getTopRSV(keygeneration, RSV):
	if keygeneration == 0:
		return 450	
	if keygeneration == 1:
		return 262164
	if keygeneration == 2:
		return 201327002
	if keygeneration == 3:
		return 201457684
	if keygeneration == 4:
		return 269484082
	if keygeneration == 5:
		return 336592976
	if keygeneration == 6:
		return 403701850
	if keygeneration == 7:
		return 404750376
	else:
		return RSV

def getMinRSV(keygeneration, RSV):
	if keygeneration == 0:
		return 0	
	if keygeneration == 1:
		return 65796
	if keygeneration == 2:
		return 201327002
	if keygeneration == 3:
		return 201392178
	if keygeneration == 4:
		return 268435656
	if keygeneration == 5:
		return 335544750
	if keygeneration == 6:
		return 402653494
	if keygeneration == 7:
		return 404750376
	else:
		return RSV		
		
		
		
		
		