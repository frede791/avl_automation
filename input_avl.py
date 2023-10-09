#!/usr/bin/env
#The idea of this file is to get some user inputs and construct an appropriate AVL file from this.


#Add in support for custom run case naming and case for when a particular file already exists. 

#Prepare liftdrag template here as you will need to set the correct number of control surfaces.

# import argparse
import webbrowser
import avl_out_parse
import os

# parser = argparse.ArgumentParser()


# def parse_args():
#     parser = argparse.ArgumentParser()
    
#     parser.add_argument("file_name")

#     args = parser.parse_args()
#     return args


# This function writes section definition to AVL file
def write_section(plane_name,x,y,z,chord,ainc,nspan,sspace,naca_number,ctrl_surf_type):

    with open(f'{plane_name}.avl','a') as avl_file:
        avl_file.write("SECTION \n")
        avl_file.write("!Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace \n")
        avl_file.write(f'{x}   {y}    {z}    {chord}    {ainc}     {nspan}    {sspace} \n')
        if naca_number != "0000":
            avl_file.write("NACA \n")
            avl_file.write(f'{naca_number} \n')
        avl_file.close()

    match ctrl_surf_type:
        case 'aileron':
            #TODO provide custom options for gain and hinge positions
            with open(f'{plane_name}.avl','a') as avl_file:
                avl_file.write("CONTROL \n")
                avl_file.write("aileron  1.0  0.0  0.0  0.0  0.0  -1 \n")
                avl_file.close()
                        
        case 'elevator':
            with open(f'{plane_name}.avl','a') as avl_file:
                avl_file.write("CONTROL \n")
                avl_file.write("elevator  1.0  0.0  0.0  0.0  0.0  1 \n")
                avl_file.close()
        
        case 'rudder':
            with open(f'{plane_name}.avl','a') as avl_file:
                avl_file.write("CONTROL \n")
                avl_file.write("rudder  1.0  0.0  0.0  0.0  0.0  1 \n")
                avl_file.close()

# This is a helper function to securely split a vector into three elements and retry if it fails
def split_into_three(vector,message):
    while(len(vector)!= 3):
        print("This is not the right number of elements. Try again")
        vector = input(message).split()
        try:
            vector[0] = float(vector[0])
            vector[1] = float(vector[1])
            vector[2] = float(vector[2])
        except:
            print("At least of the coordinates is not a number!")
            vector = []


    return float(vector[0]), float(vector[1]), float(vector[2])


# This function checks provided inputs and ensures that the correct number of values is inputted by the user.
def is_one_num(message):
    prov_input = input(message)
    while len(prov_input.split()) != 1:
        print("Incorrect number of values provided!")
        prov_input = input(message)

    return prov_input
          


def main():    

    not_valid_a = True
    airframes = ['cessna','standard_vtol','custom']
    plane_name = input("Please enter a name for your vehicle: ")
    print("Choose from predetermined models or define a custom model. Current options for airframes are:",airframes,'\n')
    print("For a custom model, write 'custom'. \n")


    while(not_valid_a):
        frame_type = input("Please enter the type of airframe you would like to use: ")
        if not frame_type in airframes:
            print("\nThis is not a valid airframe, please select a valid airframe. \n")
        else:
            not_valid_a = False

    #Set t

    # Set model specific parameters
    # Parameters that need to be provided:
    # General
    # - Reference Area (Sref)
    # - Wing span (Bref) (wing span squared / area = aspect ratio which is a required parameter for the sdf file)
    # - Reference point (X,Y,Zref) point at which moments and forces are calculated
    #Control Surface specific 
    # - type (select from options; aileron,elevator,rudder)
    # - nchord
    # - cspace
    # - nspanwise
    # - sspace
    # - x,y,z 1. (section)
    # - chord 1. (section)
    # - ainc 1. (section)
    # - Nspan 1. (optional for section)
    # - sspace 1. (optional for section)
    # - x,y,z 2. (section)
    # - chord 2. (section)
    # - ainc 2. (section)
    # - Nspan 2. (optional for section)
    # - sspace 2. (optional for section)


    # TODO: Find out if elevons are defined
    ctrl_surface_types = ['aileron','elevator','rudder'] 
    # - Reference Chord (Cref) (= area/wing span)
    delineation = '!***************************************'
    sec_demark = '#--------------------------------------------------'
    num_ctrl_surfaces = 0
    area = 0
    span = 0
    ref_pts =[]
        
    # TODO: Provide some pre-worked frames for a Cessna and standard VTOL
    match frame_type:
        case "cessna":
            num_ctrl_surfaces = 4
            # TODO: Finish
        
        case "standard_vtol":
            num_ctrl_surfaces = 2
            # TODO: Finish

        case "custom":

            with open(f'{plane_name}.avl','w') as avl_file:
                avl_file.write(f'{delineation} \n')
                avl_file.write(f'!{plane_name} input dataset \n')
                avl_file.write(f'{delineation} \n')
                avl_file.write(f'{plane_name} \n')
                avl_file.write('!Mach \n0.0 \n')
                avl_file.write('!IYsym    IZsym    Zsym \n')
                avl_file.write('0     0     0 \n')
                avl_file.close()

            print("First define some model-specific parameters for custom models: ")
            area = is_one_num("Reference area: ")
            span = is_one_num("Wing span: ")
            ref_pts = input("Reference Point (X Y Z): ").split()
            ref_pt_x, ref_pt_y, ref_pt_z = split_into_three(ref_pts,"Reference Point: X Y Z ")
            
            if(span != 0 and area != 0):
                ref_chord = float(area)/float(span)
            else:
                raise ValueError("Invalid reference chord. Check area and wing span")
            
            with open(f'{plane_name}.avl','a') as avl_file:
                avl_file.write('!Sref    Cref    Bref \n')
                avl_file.write(f'{area}     {str(ref_chord)}     {span} \n')
                avl_file.write('!Xref    Yref    Zref \n')
                avl_file.write(f'{ref_pt_x}     {ref_pt_y}      {ref_pt_z} \n')
                avl_file.close()


            num_ctrl_surfaces = is_one_num("Number of control surfaces: ")
            
            print("\nDefine parameter for EACH control surface \n")
                
            for i in range(0,int(num_ctrl_surfaces)):

                # Wings always need to be defined from left to right
                ctrl_surf_name = is_one_num(f'Provide a name for {i+1}. control surface: ')
                print("Valid control surface types are: ",ctrl_surface_types)
                not_valid_ctrl_surface = True
                
                while(not_valid_ctrl_surface):
                    ctrl_surf_type = is_one_num(f'Enter type of {i+1}. control surface: ')
                    if ctrl_surf_type not in ctrl_surface_types:
                        print("Not a valid type of control surface! \n")
                    else:
                        not_valid_ctrl_surface = False
                
                nchord = is_one_num("Specify number of chordwise horseshoe vortices placed on the surface: ")
                cspace = is_one_num("Specify spacing of chordwise vortices: ")
                nspanwise = is_one_num("Specify number of spanwise horseshoe vortices placed on the surface: ")
                sspace = is_one_num("Specify spacing of spanwise vortex spacing parameter: ")
                
                if ctrl_surf_type.lower() == 'aileron':
                    angle = is_one_num("Specify the angle of incidence across the entire surface.(OPTIONAL): ")

                #Translation of control surface, will move the whole surface to specified position
                trans_vec = input(f'Translation of {i+1}. control surface X Y Z: ').split()
                tx, ty, tz = split_into_three(trans_vec,f'Translation of {i+1}. control surface X Y Z: ')

                # Write common part of this surface to .avl file
                with open(f'{plane_name}.avl','a') as avl_file:
                    avl_file.write(sec_demark)
                    avl_file.write("\nSURFACE \n")
                    avl_file.write(f'{ctrl_surf_name} \n')
                    avl_file.write("!Nchordwise     Cspace      Nspanwise       Sspace \n")
                    avl_file.write(f'{nchord}       {cspace}        {nspanwise}     {sspace} \n')
                    
                    # If we have a rudder, we can duplicate the defined control surface along the y-axis of the model
                    # as both sides are generally modelled and controlled as one in simulation. 
                    if ctrl_surf_type.lower() == 'elevator':
                        avl_file.write("\nYDUPLICATE\n")
                        avl_file.write("0.0\n\n")
                    
                    if ctrl_surf_type.lower() == 'aileron':
                        avl_file.write("ANGLE \n")
                        avl_file.write(f'{angle} \n')

                    avl_file.write("TRANSLATE \n")
                    avl_file.write(f'{tx}    {ty}    {tz} \n')
                    avl_file.close()

                
                # Define NACA airfoil shape. Only used for aileron. 
                if ctrl_surf_type.lower() == "aileron":
                    naca_help = input("Consult NACA airfoil shape guide? (y/n) ")
                    if "y" in naca_help.lower():
                        webbrowser.open_new('http://airfoiltools.com/airfoil/naca4digit')
                    naca_number = '10000'

                    while(int(naca_number) > 9999):
                        naca_number = is_one_num("Enter selected NACA number: ")
                        
                        if int(naca_number) > 9999:
                            print("NOTE: AVL only supports 4-digit NACA numbers! Please try again")

                else:
                    # Provide a default NACA number for unused airfoils
                    naca_number = '0000'

                print(f'Define first section of {i+1}. control surface \n')
                xyz1_vec = input(f'X1 Y1 Z1 for first section of {i+1}. control surface: ').split()
                x1, y1, z1 = split_into_three(xyz1_vec,f'X1 Y1 Z1 for first section of {i+1}. control surface: ')

                chord1 = is_one_num(f'Chord length for first section of {i+1}. control surface: ')
                ainc1 = is_one_num(f'Incidence for first section of {i+1}. control surface: ')
                nspan1 = is_one_num(f'Number of spanwise vortices for first section of {i+1}. control surface: ')
                sspace1 = is_one_num(f'Spacing of vortices for first section of {i+1}. control surface: ') 


                print(f'Define second section of {i+1}. control surface \n')
                xyz2_vec = input(f'X2 Y2 Z2 for second section of {i+1}. control surface: ').split()
                x2, y2, z2 = split_into_three(xyz2_vec,f'X2 Y2 Z2 for second section of {i+1}. control surface: ')

                chord2 = is_one_num(f'Chord length for second section of {i+1}. control surface: ')
                ainc2 = is_one_num(f'Incidence for second section of {i+1}. control surface: ')
                nspan2 = is_one_num(f'Number of spanwise vortices for second section of {i+1}. control surface: ')
                sspace2 = is_one_num(f'Spacing of vortices for second section of {i+1}. control surface: ')

                write_section(plane_name,x1,y1,z1,chord1,ainc1,nspan1,sspace1,naca_number,ctrl_surf_type)
                write_section(plane_name,x2,y2,z2,chord2,ainc2,nspan2,sspace2,naca_number,ctrl_surf_type)

                print(f'\nPARAMETER DEFINITION FOR {i+1}. CONTROL SURFACE COMPLETED \n')


    AR = str((float(span)*float(span))/float(area))
    mac = str((2/3)*(float(area)/float(span)))
    ref_pt_x, ref_pt_y, ref_pt_z = float(ref_pts[0]),float(ref_pts[1]),float(ref_pts[2])


    # Call shell script that will pass the generated .avl file to AVL
    os.system(f'./process.sh {plane_name}')

    # Call main function of avl parse script
    avl_out_parse.main(plane_name,frame_type,AR,mac,ref_pt_x,ref_pt_y,ref_pt_z,num_ctrl_surfaces,area)


if __name__ == '__main__':
    main()