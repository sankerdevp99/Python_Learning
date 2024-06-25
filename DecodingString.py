st = "SANKERDEVPPOOVATHINGALXII2567KRISHNANBLESSY"

#slicing the string with given positions
decoded_st=[st[:10],st[10:22],st[22:24],st[25:29],st[29:37],st[37:43]]

#attributes
attributes = ['name','address','class','ID','Guardian','Teacher']

#Displaying the data with atttributes
for i in range(len(attributes)):
    print(attributes[i],decoded_st[i],end = '\n' )
