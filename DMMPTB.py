# API Python module @ https://github.com/meraki/dashboard-api-python/blob/master/meraki.py
# DMMPTB - Don't Make Me Press That Button is a Script that allows the user
# to move a device from one policy to another.  In this case it will move any device
# from a policy that has unrestricted rate and access to the Internet to one that is
# restricted both in rate and access (no you tube!)

#Scripted created by Randy Moore, canemdog@gmail.com

##### DO NOT MODIFY #####
from meraki import meraki
import string
from tkinter import *

################## Meraki API Auth ####################
#Replace these values with those specific to your Environment
#by putting in the requested information between the ''
apikey = '<Insert your API KEY>'
networkid = '<Insert your NetworkID>'
serialnum = '<Insert you MX Serial Number>'
#######################################################

################# Network Policy Info ###############
#Mannually create Policies for Normal Operation and 
#for restricted Operations on your MX. Set your traffic
#fitlering desired in the 'kids' group.
g_policy = 'group'
n_policy = 'normal'
Spolicyid = '102'  #No Internet group Policy
Fpolicyid = '101'  #Kids group Policy
#######################################################

############## Device List ############################
#Dynamically build a list of all devices known by the MX
#and that their description field doesn't have 'none' as a value

ClientList = meraki.getclients(apikey,serialnum, timestamp=86400, suppressprint=False)

N_ClientList = {}

for i in range (len(ClientList)):
	v_description = str(ClientList[i].get('description'))
	v_mac = ClientList[i].get('mac')
	if ((v_description.find('None'))<0):
		d1 = {v_description : v_mac}
		N_ClientList.update(d1)
############### Setup the Gui Window ####################
root = Tk()
root.title("Don't Make Me Press That Button")
frame = Frame(root, bg='white', borderwidth=5, relief="ridge") 

#Construct the window
frame.grid (column=20, row=0, columnspan=1, rowspan=1)
frame.columnconfigure(20, weight = 5)
frame.rowconfigure(0, weight = 5)


###################### Define the Movement of Device to / from a Policy ###################
def M_Disable():
	x = str(tkvar.get())
############################# Display Results of Acations in Display Windows ##############
	t1text = "Device Selected: %s\n" % (x)
	t1.delete(1.0, END)
	t1.insert (END, t1text)
	clientmac = N_ClientList[x]
	output = meraki.updateclientpolicy(apikey, networkid, clientmac, g_policy, Spolicyid, suppressprint=False)
	t1text = "Device Disabled: %s\n" % (output)
	t1.delete(1.0, END)
	t1.insert (END, t1text)
###########################################################################################	
def M_Enable():
	x= str(tkvar.get())
	
	clientmac = N_ClientList[x]
	output = meraki.updateclientpolicy(apikey, networkid, clientmac, n_policy, Fpolicyid, suppressprint=False)
############################# Display Results of Acations in Display Windows ##############
	t1text = "Device Enabled: %s\n" % (output)
	t1.delete(1.0, END)
	t1.insert (END, t1text)

################################### Buttons ############################

b1 = Button(frame, text="Disable", bg='red', command=M_Disable)
b1.grid(row=8, column=2, sticky=E)

b2 = Button(frame, text="Enable", bg='green', command=M_Enable)
b2.grid(row=8, column=0, stick=W)  

b3 = Button (frame, text="Quit", command = quit)
b3.grid(row=8, column=1)

t1 = Text(frame, height=2, width=50)
t1.grid(row=10, column=0, columnspan=3, sticky=E+W)
########################################################################

# Create a Variable for the Drop List to set the original default value
tkvar = StringVar(root)
array = list (N_ClientList.keys())
tkvar.set (array[0])

################# Create the Menu of devices to disable or enable
popupMenu = OptionMenu(frame, tkvar, *N_ClientList)
Label(frame, text="Choose a device", bg='white').grid(row = 1, column = 1)
popupMenu.grid(row = 2, column =1)

# on change dropdown value function
def change_dropdown(*args):
    value = tkvar.get()
 
# link function to change dropdown menu default to last selected value
tkvar.trace('w', change_dropdown)



root.mainloop()
 