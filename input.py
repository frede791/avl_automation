#!/usr/bin/env
#The idea of this file is to get some user inputs and construct an appropriate AVL file from this.


#Add in support for custom run case naming and case for when a particular file already exists. 

#Prepare liftdrag template here as you will need to set the correct number of control surfaces.

# import argparse

# parser = argparse.ArgumentParser()


# def parse_args():
#     parser = argparse.ArgumentParser()
    
#     parser.add_argument("file_name")

#     args = parser.parse_args()
#     return args



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

    # Set model specific parameters
    # Parameters that need to be provided:
    # General
    # - Reference Area (Sref)
    # - Wing span (Bref) (wing span squared / area = aspect ratio which is a required parameter for the sdf file)
    # - Reference point (X,Y,Zref) point at which moments and forces are calculated
    #Control Surface specific 
    # - type (select from options; aileron,elevon,elevator,rudder)
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
    # - Reference Chord (Cref) (= area/wing span)
    ctrl_surface_types = ['aileron','elevon','elevator','rudder']

    if frame_type == "custom":
        print("First define some model-specific parameters for custom models: \n")
        area = input("Reference area: \n")
        span = input("Wing span: \n")
        ref_pt = input("Reference Point: \n")
        num_ctrl_surfaces = input("Number of control surfaces")
        print("Next define parameter for EACH control surface \n")
        for i in range(0,num_ctrl_surfaces):
            print("Valid control surface types are: ",ctrl_surface_types)
            not_valid_ctrl_surface = True
            
            while(not_valid_ctrl_surface):
                ctrl_surf_type = input(f'Enter type of {i+1}. control surface')
                if ctrl_surf_type not in ctrl_surface_types:
                    print("Not a valid type of control surface!")
                else:
                    not_valid_ctrl_surface = False
            
            nchord = input("Specify number of chordwise horseshoe vortices placed on the surface \n")
            cspace = input("Specify spacing of chordwise vortices \n")
            nspanwise = input("Specify number of spanwise horseshoe vortices placed on the surface \n")
            sspace = input("Specify spacing of spanwise vortex spacing parameter")
            
            angle = input("Specify the angle of incidence across the entire surface.")

            print(f'Define first section of {i}. control surface')
            x1, y1, z1 = input(f'X1 Y1 Z1 for first section of {i}. control surface')
            chord1 = input(f'Chord length for first section of {i}. control surface')
            ainc = input(f'Incidence for first section of {i}. control surface')
            nspan1 = input(f'Number of spanwise vortices for first section of {i}. control surface')
            sspace1 = input(f'Spacing of vortices for first section of {i}. control surface')

            print(f'Define second section of {i}. control surface')
            x2, y2, z2 = input(f'X2 Y2 Z2 for second section of {i}. control surface')
            chord2 = input(f'Chord length for second section of {i}. control surface')
            ainc = input(f'Incidence for second section of {i}. control surface')
            nspan2 = input(f'Number of spanwise vortices for second section of {i}. control surface')
            sspace2 = input(f'Spacing of vortices for second section of {i}. control surface')


            
            

    num_ctrl_surfaces = 0

    match frame_type:
        case "cessna":
            num_ctrl_surfaces = 4
        
        case "standard_vtol":
            num_ctrl_surfaces = 2   


    


if __name__ == '__main__':
    main()