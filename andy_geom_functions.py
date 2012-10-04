#!/usr/bin/python
from pydagmc import dagmc

def lost_particle(volumes):
# determines whether or not the particle is defined as lost 

    found_graveyard=0

# loop through the volumes in the problem
    for vol in volumes:
        if dagmc.volume_is_graveyard(vol) == 1:
            # true particle is lost
            found_graveyard = 1

    if found_graveyard == 0:
        return found_graveyard

# take the history data and store it for printing
def add_pos_to_bank(positions,lost_counter):
    global history
    #take position information and add to array
    history[lost_counter]=positions

def dump_2_vtk(origin,positions,lost_counter):
# takes the particle information from positions and writes
# dat to datafile with the suffix lost_$lost_counter.vtk

    # open the data file
    name="lost_"+str(lost_counter)+".vtk"    
    file = open(name,"w")

    file.write("# vtk DataFile Version 2.0\n")
    file.write("Lost particle information\n")
    file.write("ASCII\n")
    file.write("DATASET UNSTRUCTURED_GRID\n")
    string = 'POINTS '+str(len(positions)+1)+' FLOAT\n'
    file.write(string)
    # add the ray origin to file
    string = str(origin)
    string = string.replace("(","")
    string = string.replace(")","")
    string = string.replace(",","")
    string = string+"\n"
    file.write(string)

    # now remove brackets in position data
    for i in positions:
       string = i
       string = string.replace("[","")
       string = string.replace("]","")
       string = string+"\n"
       file.write(string)
    # write blank line
    file.write("\n")

    # write cells line
    string = 'CELLS '+str(len(positions))+' '+str((len(positions)*3))+'\n'
    file.write(string)
     
    for i in range(0,(len(positions))):
        string = '2 '+str(i)+' '+str(i+1)+'\n'
        file.write(string)
    
    # write cell type line
    string = 'CELL_TYPES '+str(len(positions))+'\n'
    file.write(string)
    for i in range(0,(len(positions))):
        file.write("3\n") 

    file.close()

def extrapolate_ray(pos,positions,num_lost,dist):
# the ray is now lost, take its last position and extrapolate some distance
    last_pos=positions[len(positions)-1]
    # get the coordinates of the last sucessful triangle hit
    (x_1,y_1,z_1) = split_string_tuple(last_pos)  
    dif_x = x_1-pos[0]
    dif_y = y_1-pos[1]
    dif_z = z_1-pos[2]
    mod_dir = dif_x*dif_x + dif_y*dif_y + dif_z*dif_z
    mod_dir = math.sqrt(mod_dir)
    u = dif_x/mod_dir
    v = dif_y/mod_dir
    w = dif_z/mod_dir

    x_new = x_1 + (u*dist)
    y_new = y_1 + (v*dist)
    z_new = z_1 + (w*dist)

    print x_new,y_new,z_new
    # open the data file
    name="continue_"+str(num_lost)+".vtk"    
    file = open(name,"w")
    file.write("# vtk DataFile Version 2.0\n")
    file.write("Extrapolated lost particle information\n")
    file.write("ASCII\n")
    file.write("DATASET UNSTRUCTURED_GRID\n")
    string = 'POINTS 2 FLOAT\n'
    file.write(string)
    string = str(last_pos)
    string = string.replace("[","")
    string = string.replace("]","")
    string = string+"\n"
    file.write(string)
#    string = 
    file.write(str(x_new)+' '+str(y_new)+' '+str(z_new)+'\n')
    file.write('\n')
    file.write('CELLS 1 3\n')
    file.write('2 0 1 \n')
    file.write('CELL_TYPES 1\n')
    file.write('3\n')
    file.close()
    return

def split_string_tuple(string_temp):
    string_temp = string_temp.replace("[","")
    string_temp = string_temp.replace("]","")
    while (string_temp.find("   ",) >= 0):
        string_temp = string_temp.replace("   ","  ")
    while (string_temp.find("  ",) >= 0):
        string_temp = string_temp.replace("  "," ")
    print string_temp
    string_temp = str(string_temp)
    (arg1,arg2,arg3) = string_temp.split()
    return float(arg1),float(arg2),float(arg3)
