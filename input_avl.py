#!/usr/bin/env
#The idea of this file is to get some user inputs and construct an appropriate AVL file from this.


#Add in support for custom run case naming and case for when a particular file already exists. 

#Prepare liftdrag template here as you will need to set the correct number of control surfaces.

# import argparse
import webbrowser
import avl_out_parse

# parser = argparse.ArgumentParser()


# def parse_args():
#     parser = argparse.ArgumentParser()
    
#     parser.add_argument("file_name")

#     args = parser.parse_args()
#     return args


# This function writes section definition to AVL file
def write_section(plane_name,x,y,z,chord,ainc,nspan,sspace,naca_number,ctrl_surf_type):

    with open(f'{plane_name}.avl','a') as avl_file:
        avl_file.write("SECTION")
        avl_file.write("!Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace")
        avl_file.write(f'{x}   {y}    {z}    {chord}    {ainc}     {nspan}    {sspace}')
        avl_file.write("NACA")
        avl_file.write(f'{naca_number} \n')
        avl_file.close()

    match ctrl_surf_type:
        case 'aileron':
            #TODO provide custom options for gain and hinge positions
            with open(f'{plane_name}.avl','a') as avl_file:
                avl_file.write("CONTROL")
                avl_file.write("aileron  1.0  0.0  0.0  0.0  0.0  -1 \n")
                avl_file.close()
                        
        case 'elevator':
            with open(f'{plane_name}.avl','a') as avl_file:
                avl_file.write("CONTROL")
                avl_file.write("elevator  1.0  0.0  0.0  0.0  0.0  1 \n")
                avl_file.close()
        
        case 'rudder':
            with open(f'{plane_name}.avl','a') as avl_file:
                avl_file.write("CONTROL")
                avl_file.write("rudder  1.0  0.0  0.0  0.0  0.0  1 \n")
                avl_file.close()



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


    # Derived parameters, these can be derived from parameters not provided by the user
    # TODO: Find out if elevons are defined
    ctrl_surface_types = ['aileron','elevator','rudder'] 
    # - Reference Chord (Cref) (= area/wing span)
    delineation = '!***************************************'
    sec_demark = '#--------------------------------------------------'
    num_ctrl_surfaces = 0
    area = 0
    span = 0
    ref_pts =[]
        
    # TODO: Provide some preworked frames for a Cessna and standard VTOL
    match frame_type:
        case "cessna":
            num_ctrl_surfaces = 4
        
        case "standard_vtol":
            num_ctrl_surfaces = 2

        case "custom":

            with open(f'{plane_name}.avl','a') as avl_file:
                avl_file.write(delineation)
                avl_file.write(f'!{plane_name} input dataset')
                avl_file.write(delineation)
                avl_file.write('!Mach \n 0.0 \n')
                avl_file.write('!IYsym    IZsym    Zsym')
                avl_file.write('0.0     0.0     0.0 \n')
                avl_file.close()

            print("First define some model-specific parameters for custom models: ")
            area = input("Reference area: ")
            span = input("Wing span: ")
            ref_pts = input("Reference Point: X Y Z ").split()
            ref_pt_x, ref_pt_y, ref_pt_z = float(ref_pts[0]),float(ref_pts[1]),float(ref_pts[2])
            
            if(span != 0 and area != 0):
                ref_chord = float(area)/float(span)
            else:
                raise ValueError("Invalid reference chord. Check area and wing span")
            
            with open(f'{plane_name}.avl','a') as avl_file:
                avl_file.write('!Sref    Cref    Bref')
                avl_file.write(f'{area}     {str(ref_chord)}     {span}')
                avl_file.write('!Xref    Yref    Zref')
                avl_file.write(f'{ref_pt_x}     {ref_pt_y}      {ref_pt_z} \n')
                avl_file.close()


            num_ctrl_surfaces = input("Number of control surfaces")        
            
            print("Define parameter for EACH control surface \n")
                
            for i in range(0,num_ctrl_surfaces):

                # Wings always need to be defined from left to right
                ctrl_surf_name = input("Provide a name for this control surface")
                print("Valid control surface types are: ",ctrl_surface_types)
                not_valid_ctrl_surface = True
                
                while(not_valid_ctrl_surface):
                    ctrl_surf_type = input(f'Enter type of {i+1}. control surface')
                    if ctrl_surf_type not in ctrl_surface_types:
                        print("Not a valid type of control surface! \n")
                    else:
                        not_valid_ctrl_surface = False
                
                nchord = input("Specify number of chordwise horseshoe vortices placed on the surface")
                cspace = input("Specify spacing of chordwise vortices")
                nspanwise = input("Specify number of spanwise horseshoe vortices placed on the surface")
                sspace = input("Specify spacing of spanwise vortex spacing parameter")
                
                angle = input("Specify the angle of incidence across the entire surface.(OPTIONAL)")

                #Translation of control surface, will move the whole surface to specified position
                trans_vec = input(f'Translation of {i}. control surface X Y Z').split()
                tx, ty, tz = float(trans_vec[0]),float(trans_vec[1]),float(trans_vec[2])

                # Write common part of this surface
                with open(f'{plane_name}.avl','a') as avl_file:
                    avl_file.write(sec_demark)
                    avl_file.write("SURFACE")
                    avl_file.write(f'{ctrl_surf_name}')
                    avl_file.write("!Nchordwise     Cspace      Nspanwise       Sspace")
                    avl_file.write(f'{nchord}       {cspace}        {nspanwise}     {sspace} \n')
                    avl_file.write("ANGLE")
                    avl_file.write(f'{angle}')
                    avl_file.write("TRANSLATE")
                    avl_file.write(f'{tx}    {ty}    {tz}')
                    avl_file.close()

                
                #Define NACA airfoil shape
                naca_help = input("Consult NACA airfoil shape guide? (y/n)")
                if "y" in naca_help.lower():
                    webbrowser.open_new('http://airfoiltools.com/airfoil/naca4digit')

                naca_number = input("Enter selected NACA number")

                print(f'Define first section of {i}. control surface \n')
                xyz1_vec = input(f'X1 Y1 Z1 for first section of {i}. control surface').split()
                x1, y1, z1 = float(xyz1_vec[0]),float(xyz1_vec[1]),float(xyz1_vec[2])
                chord1 = input(f'Chord length for first section of {i}. control surface')
                ainc1 = input(f'Incidence for first section of {i}. control surface')
                nspan1 = input(f'Number of spanwise vortices for first section of {i}. control surface')
                sspace1 = input(f'Spacing of vortices for first section of {i}. control surface') 

                print(f'Define second section of {i}. control surface \n')
                xyz2_vec = input(f'X2 Y2 Z2 for second section of {i}. control surface').split()
                x2, y2, z2 = float(xyz2_vec[0]),float(xyz2_vec[1]),float(xyz2_vec[2])
                chord2 = input(f'Chord length for second section of {i}. control surface')
                ainc2 = input(f'Incidence for second section of {i}. control surface')
                nspan2 = input(f'Number of spanwise vortices for second section of {i}. control surface')
                sspace2 = input(f'Spacing of vortices for second section of {i}. control surface')

                write_section(plane_name,x1,y1,z1,chord1,ainc1,nspan1,sspace1,naca_number,ctrl_surf_type)
                write_section(plane_name,x2,y2,z2,chord2,ainc2,nspan2,sspace2,naca_number,ctrl_surf_type)


    AR = (span*span)/area
    mac = (2/3)*(area/span)
    ref_pt_x, ref_pt_y, ref_pt_z = float(ref_pts[0]),float(ref_pts[1]),float(ref_pts[2])




    # Call shell script that will pass the generated .avl file to AVL



    # Call main function of output script
    avl_out_parse.main(plane_name,frame_type,AR,mac,ref_pt_x,ref_pt_y,ref_pt_z,num_ctrl_surfaces)


if __name__ == '__main__':
    main()