import platform

#the first entry is 64bit / 32bit entry
architecture = "Architecture : "+platform.architecture()[0]

#get the distro and version
distro = []
#Contains all the distro related details
distro.append("Distro Name : "+platform.linux_distribution()[0])
distro.append("Distro Version : "+platform.linux_distribution()[1])

#get python details
python_details = []
#Contains all the python related details
python_details.append("Python Branch : "+platform.python_branch())
python_details.append("Python Revision : "+platform.python_revision())
python_details.append("Python Compiled Using : "+ platform.python_compiler())
python_details.append("Python Implementation : "+platform.python_implementation())
python_details.append("Python Version : "+platform.python_version())

print "Please submit the following Feedback !"

print architecture

for i in distro:
    print i
for i in python_details:
    print i

