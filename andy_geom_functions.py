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

