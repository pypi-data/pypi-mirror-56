#!/usr/bin/env python

#************************************************************************
#
#   Copyright (C) 2019  M. Joyce, L. Lairmore, D. J. Price
#
#   See MESA2HYDRO/LICENSE
#
#************************************************************************

'''

Contains: functions for manipulating and
           formatting MESA data
           
'''

import numpy as np
import codecs, re
import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter 

#########################################################################
#
# MESA output functions
#
# User warning: these functions expect MESA data in its unmodified format,
# including a 6 line header
#
#########################################################################
def strip_MESA_header(in_filename, out_filename, *args, **kwargs):

    n = int(kwargs.get('n', 5))
    num_delete=int(n) #the number of line to be read and deleted
    outfn=out_filename

    with open(in_filename) as f:
        mylist = f.read().splitlines()
    newlist = mylist[:]

    thefile = open(outfn, 'w')
    del mylist[:num_delete]
    for item in mylist:
        thefile.write("%s\n" % item)
    return  thefile, outfn



def get_MESA_output_fields(filename):
    inf=open(filename,'r')
    line = inf.readlines()[5:6] 
    p=line[0].split()
    phys_dict={}            
    for i,v in enumerate(p):
        phys_dict[str(v).strip()]=i
    return phys_dict


def get_column(filename,keyname):
    inf=open(filename,'r')
    inf.seek(0)
    phys_dict=get_MESA_output_fields(filename)
    indx=phys_dict.get(str(keyname))
    column=[] 
    data = inf.readlines()[6:]
    for line in data:
        try:
            p=line.split()
            column.append(p[indx])
        except IndexError:
            pass
    inf.close()
    return np.array(column), type(column)



def get_columns(filename,keyname_list):
    phys_dict=get_MESA_output_fields(filename)
    column_dict={}
    for i in range(len(keyname_list)):
        keyname=str(list(keyname_list)[i])
        column_dict[ keyname ]=(get_column(filename, keyname)[0])
    return column_dict



def get_quantity(readfile,keyname):
    keyname=str(keyname)
    keyname_list=get_MESA_output_fields(readfile).keys()
    column_dict=get_columns(readfile,keyname_list)
    quantity=np.array(column_dict.get(keyname)) 
    try:
        if (quantity==None):
            print("Error: MESA keyword '"+keyname+"' not found!")
            sys.exit()
    except ValueError:
        pass 

    only_numbers=[]
    for q in quantity:
        try:
            only_numbers.append(float(q))
        except ValueError:
            pass
    return np.array(only_numbers).astype(float)



def show_allowed_MESA_keywords(readfile):
    fstr=""
    for i in get_MESA_output_fields(readfile).keys():
        fstr=fstr+str(i) +'\n'
    print(fstr)
    return fstr


#######################################################
#
# Plot makers
#
########################################################
def plotter(xmaj,xmin,ymaj,ymin, xf, yf, *args, **kwargs):
    figsize=kwargs.get("figsize", (15,15))
    #h=10

    fig = plt.figure(figsize=figsize)#(2.5*h,h)) #plt.subplots()#(figsize=figsize)
    ax = fig.add_subplot(1, 1, 1)

    majorLocator_x  = MultipleLocator(xmaj)     # I want a major tick every "x"
    majorFormatter_x = FormatStrFormatter(xf)   # label major ticks with a 1.2f format string
    minorLocator_x  = MultipleLocator(xmin)     # I want a minor tick every "x"

    majorLocator_y  = MultipleLocator(ymaj)     # y axis...
    majorFormatter_y = FormatStrFormatter(yf)    
    minorLocator_y  = MultipleLocator(ymin)     


    ax.xaxis.set_major_locator(majorLocator_x)
    ax.xaxis.set_major_formatter(majorFormatter_x)
    ax.xaxis.set_minor_locator(minorLocator_x)

    ax.yaxis.set_major_locator(majorLocator_y)
    ax.yaxis.set_major_formatter(majorFormatter_y)
    ax.yaxis.set_minor_locator(minorLocator_y)

    return fig, ax


def multi_plotter(ax,xmaj, xmin, ymaj, ymin,**kwargs):
    xf = kwargs.get('xf', '%1.1f')
    yf = kwargs.get('yf', '%1.1f')

    majorLocator_x  = MultipleLocator(xmaj)    
    majorFormatter_x = FormatStrFormatter(xf)
    minorLocator_x  = MultipleLocator(xmin)     

    majorLocator_y  = MultipleLocator(ymaj)     
    majorFormatter_y = FormatStrFormatter(yf)
    minorLocator_y  = MultipleLocator(ymin)  


    ax.xaxis.set_major_locator(majorLocator_x)
    ax.xaxis.set_major_formatter(majorFormatter_x)
    ax.xaxis.set_minor_locator(minorLocator_x)

    ax.yaxis.set_major_locator(majorLocator_y)
    ax.yaxis.set_major_formatter(majorFormatter_y)
    ax.yaxis.set_minor_locator(minorLocator_y)

    return 


#######################################################
#
# Non-essential MESA inlist manipulators
#
########################################################
def generate_basic_inlist(mass, age, metallicity, m2h_path, mesa_dir, inlist_path,output_model_name):
    lines = []

    lines.append("&star_job")
    lines.append("")
    lines.append("  mesa_dir = '"+ str(mesa_dir) +"'")
    lines.append("  history_columns_file='"+m2h_path+"/data/history_columns_testsuite.list'")
    lines.append("  profile_columns_file='"+m2h_path+"/data/profile_columns_testsuite.list'")
    lines.append("")
    lines.append("  load_saved_model = .false.")
    lines.append("  !create_pre_main_sequence_model = .false. !!need this to be able to specify y?")
    lines.append("")
    lines.append("  save_model_when_terminate = .false.")
    lines.append("")
    lines.append("  write_profile_when_terminate = .true.")
    lines.append("  filename_for_profile_when_terminate = 'profile_"+str(output_model_name)+".data'")
    lines.append("")
    lines.append("  pgstar_flag = .false.")
    lines.append("  save_pgstar_files_when_terminate = .false.")
    lines.append("")
    lines.append(" / !end of star_job namelist")
    lines.append("")
    lines.append("&controls")
    lines.append("")
    lines.append("  star_history_name = 'history_"+str(output_model_name)+".data'")
    lines.append("" )
    lines.append("  !max_number_backups = 0")
    lines.append("  max_number_retries = 5")
    lines.append("  !max_model_number = 500")
    lines.append("")
    lines.append("  initial_mass ="+str(mass)+"d0")
    lines.append("  !initial_y = 0.27d0 !solar")
    lines.append("  initial_z = "+str(metallicity)+"d0 !solar")
    lines.append("")
    lines.append("  terminal_show_age_in_years = .true.")
    lines.append("  max_age = "+str(age)+"d9 ! age of Sun in Gyr")
    lines.append("")
    lines.append("")
    lines.append("  !photo_interval = 50")
    lines.append("  !profile_interval = 50")
    lines.append("  history_interval = 1")
    lines.append("  !terminal_interval = 100")
    lines.append("  !write_header_frequency = 100")
    lines.append("")
    lines.append("/ ! end of controls namelist")
    lines.append("")

    with open(inlinst_path, "w") as outf:
        outf.write("\n".join(lines))


def update_MESA_inlist_value(MESA_inlist, field, value):
    inlist_dict=grab_fields(MESA_inlist)
    old_value=inlist_dict.get(field)
    new_value=str(value)
    oldstr=r'{}\s*=\s*{}'.format(field, old_value)
    newstr='{} = {}'.format(field, value)

    f = codecs.open(MESA_inlist)
    contents = f.read()
    newcontents=re.sub(oldstr, newstr, contents) 
    f.close()
    with open(MESA_inlist,"w") as outf:
        outf.write(newcontents)

def grab_fields(MESA_inlist):
    inf=open(MESA_inlist,'r')
    inlist_dict={}
    for line in inf:
        if line and "=" in line:
            try:
                p=line.split("=")
                try: 
                    p[1]=p[1].split('\n')[0]
                except:
                    pass
                if "!" in p[0]:
                    del p    
                inlist_dict[str(p[0]).strip()]=str(p[1]).strip()
            except:
                pass 
    return inlist_dict


# end module MESAhandling
