#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is a program done by Claudia Millan

# Import libraries
#future imports
from __future__ import print_function
#from __future__ import division

# Python Modules
import ConfigParser
from collections import Counter
import cPickle
import copy
import math
import itertools
import operator
import os
import shutil
import psutil
import sys
import time
import traceback
import subprocess
from termcolor import colored
from multiprocessing import Pool
# Our own modules
import ALIXE
import alixe_library as al
import Bioinformatics3
import Bio.PDB
import SELSLIB2


def link_file(folder_for_link,path_orifile,name_link):
    path_destination=os.path.join(folder_for_link, name_link)
    if not os.path.exists(path_destination):
        try:
            os.link(path_orifile, path_destination)
        except:
            print('Some error occured during linking')



# Reading input from command line
if len(sys.argv) == 1:
    print("\nUsage for ARCIMBOLDO runs: autoalixe.py name.bor -mode [additional arguments]")
    print("\nUsage for general solutions: autoalixe.py folder_path -mode [additional arguments]")
    print("\n-mode=fish one_step one_step_parallel two_steps combi ens1_fragN cc_analysis")
    print("\n\nAdditional arguments:")
    print("\n-path_combi=path Use this in combi mode to perform clustering between this run and the one given in name.bor")
    print("\n-path=path to the CHESCAT executable")
    print("\n-ref=path_reference_solution or folder_path Use this solution or solutions as references")
    print("\n-tols=integer,integer From 0 to 90 phase difference tolerance in degrees.")
    print("                        First is used for one_step, one_step_parallel, ens1_fragN or fish, second, for combi or two_steps")
    print("\n-res=float Resolution to use in the phase comparison and merging")
    print("\n-res_comp=float Resolution to use in the phase comparison")
    print("\n-res_merge=float Resolution to use in the phase merging")
    print("\n-ncores=n Number of cores to use in parallel modes, by default nCPUs-1")
    print("\n-fom_sorting=CC Figure of merit to sort the references in first steps. Can be CC, LLG or ZSCORE")
    print("\n-lim=integer Hard limit on the number of solutions to be processed. Default is 1000")
    print("\n-exp=boolean If True, expansions of the clusters will be performed sequentially. Default is False")
    print("\n-orisub=sxos Subroutine to compute shifts for polar space groups. Can be sxos or sxosfft")
    print("\n-weight=e Weight to apply to compare the phases. Can be e (e-value) or f (amplitudes)")
    print("\n-fragment=1 Folder to check for ARCIMBOLDO_LITE runs (e.g. ens1_frag1). Can be any integer in the range of the number of fragments")
    print("\n-filtersingle=boolean Filter from the output the clusters coming from a single phase set. Default is False")
    print("\n-mapcc Flag to activate the computation of the map correlation coefficient")
    print("\n-no_oricheck Flag to deactivate the check of the origin shift at cycles > 1")
    print("\n-minchunk=size Number to use as minimum size to move from parallel to sequential algorithm")
    print("\n-shelxe_line='-m5 -a0' SHELXE arguments string to produce the phs files")
    print("\n-seed=0 or 1 seed argument to use in chescat")
    print("\n-postmortem=True or False Perform a wMPE assesment of the solutions")
    print("\n-fusedcoord=False or True Generates in real space the equivalent merging of solutions")
    print("\n-ccfromphi=False or True Computes the initial CC of the combined phases with SHELXE ")
    sys.exit()

# Variables initialization
now = time.time()
type_run = ' '  # To know if clustering is to be applied to an ARCIMBOLDO,BORGES or SHREDDER run
cycles = 3  # cycles for chescat clustering
resolution = 2.0  # resolution for chescat clustering
resolution_comp = 2.0  # resolution for chescat comparing in the parallel algorithm
resolution_merge = 2.0  # resolution for chescat clustering in the parallel algorithm
tolerance_first_round = 60  # First clustering attempt tolerance in degrees
tolerance_second_round = 88  # Second clustering attempt tolerance in degrees
global_tolerance = 75  # Only if we fish with a single or a set of references against the pool
ent_present = False
seed = 0  # Default
seed_parallel = 0
wd = os.getcwd()
fom_sorting = 'CC'  # can be CC, LLG or ZSCORE
folder_mode = False
path_sol= sys.argv[1]
if os.path.isdir(path_sol):
    folder_mode = True
mode = None
path_phstat = None
phstat_version = 'fortran' #placeholder till I remove completely the python part
reference_to_fish = None
ent_filename = None
hkl_filename = None
expansions = False
path_combi = None
orisub = 'sxos'
weight = 'e'
hard_limit_phs = 1000
shelxe_line_alixe = "-m5 -a0 "
shelxe_path = 'shelxe'
n_cores = (psutil.cpu_count(logical=False)-1) # default is the number of cores -1
min_size_list = 20
fragment = 1
filtersingle = False
cc_calc = False
oricheck = True
pm = False
fuscoord = False
phifromfus = False

if len(sys.argv) > 2:
    # Read the options
    for i in range(2, len(sys.argv)):
        option = sys.argv[i]
        if option.startswith("-mode"):
            mode = option[6:]
            if mode not in ('fish','cc_analysis','one_step','one_step_parallel','two_steps','combi') and not mode.startswith('ens1_frag'):
                print('Sorry, you need to provide a valid mode for autoalixe')
                sys.exit(1)
        if option.startswith("-ref"):
            reference_to_fish = option[5:]
            if not os.path.exists(reference_to_fish):
                print("Sorry, you need to provide a valid path for the reference or references")
                sys.exit(1)
            else:
                if os.path.isfile(reference_to_fish):
                    print("\nFile ", reference_to_fish, "is going to be used for fishing")
                    list_references_fish=[reference_to_fish]
                    if reference_to_fish.endswith('.phs'):
                        phs_ref=True
                    else:
                        phs_ref=False
                elif os.path.isdir(reference_to_fish):
                    print('\n Checking the files to use as references ')
                    # NOTE: check whether we have the phase files or just coordinates
                    list_references_fish=al.list_files_by_extension(reference_to_fish, 'phs')
                    phs_ref=True
                    if list_references_fish==None:
                        list_references_fish=al.list_files_by_extension(reference_to_fish, 'pdb')
                        if list_references_fish==None:
                            list_references_fish=al.list_files_by_extension(reference_to_fish, 'pda')
                            if list_references_fish==None:
                                print("Sorry, you need to provide a folder with either phs, pda or pdb references")
                                sys.exit(1)
                        phs_ref=False
        if option.startswith("-path_combi"):
            path_combi = option[12:]
            # TODO: the path to combine should be a pkl file and we should check we can load it
        if option.startswith("-path") and not (option.startswith("-path_combi")):
            path_phstat = option[6:] # path to chescat
            if not al.check_path_phstat(path_phstat):
                sys.exit(1)
        if option.startswith("-lim"):
            hard_limit_phs = int(option[5:])
            print("Hard limit set to ", hard_limit_phs)
        if option.startswith("-exp"):
            expansions = bool(option[5:])
            print("Expansions set to ", expansions)
        if option.startswith("-res="):
            resolution = float(option[5:])
            print("\nResolution for phase comparison and merging set to ", resolution)
        if option.startswith("-res_comp"):
            resolution_comp = float(option[10:])
            print("\nResolution for phase comparison set to ",resolution_comp)
        if option.startswith("-res_merge"):
            resolution_merge = float(option[11:])
            print("\nResolution for phase merging set to ",resolution_merge)
        if option.startswith('-fom'):
            selection=option[13:]
            if selection not in ('CC','LLG','ZSCORE'):
                print('\nSorry, only CC, LLG or ZSCORE can be used for sorting')
                sys.exit(1)
            else:
                fom_sorting=selection
        if option.startswith("-tols"):
            tolerances = option[6:].split(',')
            tolerance_first_round = int(tolerances[0])
            tolerance_second_round = int(tolerances[1])
            global_tolerance = tolerance_first_round
        if option.startswith('-orisub'):
            orisub=option[8:]
        if option.startswith('-weight'):
            weight = option[8:]
        if option.startswith('-ncores'):
            n_cores_read = int(option[8:])
            if n_cores_read > n_cores:
                print('\n Warning: This run is not going to be executed'
                      ' because you set a larger number of cores ',n_cores_read,
                      ' than physical cores in the machine, ',n_cores)
                quit()
            else:
                n_cores = n_cores_read
                print('\n Warning: This run is going to be executed on ',n_cores,' CPUs')
        if option.startswith('-minchunk'):
            min_size_list = int(option[10:])
            print('\n Warning: Using a minimum size list for parallelization of  ',min_size_list)
        if option.startswith('-shelxe_line'):
            shelxe_line_alixe=option[13:]
        if option.startswith('-fragment'):
            fragment=int(option[10:])
        if option.startswith('-mapcc'):
            cc_calc=True
        if option.startswith('-no_oricheck'):
            oricheck=False
        if option.startswith('-seed'):
            seed=int(option[6:])
        if option.startswith('-filtersingle'):
            filtersingle = True if option[14:] in ['True','TRUE','true'] else False 
        if option.startswith('-postmortem'):
            pm = True if option[12:] in ['True','TRUE','true'] else False
        if option.startswith('-fusedcoord'):
            fuscoord = True if option[12:] in ['True','TRUE','true'] else False
        if option.startswith('-ccfromphi'):
            phifromfus = True if option[11:] in ['True','TRUE','true'] else False
            if pm==True and phifromfus==False:
                print('Automatically switching on the SHELXE computation for postmortem even if ccfromphi was set to False')
                phifromfus = True

if path_phstat == None:
    print(colored("\nPlease give the path to the fortran PHSTAT in the option -path", 'red'))
    sys.exit(1)
if mode == None:
    print(colored("\nThe mode keyword is mandatory. ",
                  "Please provide one of the following modes: ",
                  "fish one_step one_step_parallel two_steps combi cc_analysis",'red'))
    sys.exit(1)
if mode == 'fish' and reference_to_fish == None:
    # TODO: if we start from an arcimboldo run we can directly use as references the solutions that were going to be expanded
    # for example EXP_PREPARE/ in ARCIMBOLDO_LITE
    print(colored("\nIf you use fish mode, you need to provide an external reference in the -ref keyword",'red'))
    sys.exit(1)
if mode == 'combi' and path_combi == None:
    print(colored("\nIf you use combi mode, you need to provide another bor path in the -path_combi keyword",'red'))
    sys.exit(1)

clust_fold = os.path.join(wd, 'CLUSTERING/')
al.check_dir_or_make_it(clust_fold,remove=True)

log_file = open(os.path.join(clust_fold, 'autoalixe.log'), 'w')
initial_string = '\n Command line used for autoalixe was ' + " ".join(sys.argv)
log_file.write(initial_string)

if not folder_mode:
    config_obj=ConfigParser.ConfigParser()
    config_obj.read(path_sol)
    multiproc, shelxe_path = al.get_computing_info_for_alixe(config_obj)
    wd_run, hkl_filename, ent_filename, ent_present = al.get_general_info_for_alixe(config_obj)
    link_file(folder_for_link=clust_fold, path_orifile=hkl_filename, name_link='reflection.hkl')
    if ent_present and pm:
        print("\nYou have an ent file, a post-mortem analysis of MPE will be performed")
        link_file(folder_for_link=clust_fold, path_orifile=ent_filename, name_link="final_solution.ent")

    shelxe_line_alixe, type_run, topexp, wd_run, fragment_search = al.get_arcirun_info_for_alixe(config_obj,wd_run,ent_present,pm)
else:
    list_pdbs=[]
    list_input_files = os.listdir(path_sol)
    dict_sorted_input={'0':[]}
    list_phs_full=[]
    list_phs=[]
    list_pdb_ori=[]
    list_pda=[]
    for inp in list_input_files:
        fullpathinp = os.path.join(path_sol,inp)
        fullpathclu = os.path.join(clust_fold,inp)
        if inp.endswith('.phs') or inp.endswith('.phi'):
            #dict_sorted_input['0'].append(inp)
            shutil.copy(fullpathinp,fullpathclu)
            list_phs.append(fullpathclu)
        elif inp.endswith('.pdb'):
            shutil.copy(fullpathinp, fullpathclu)
            list_pdb_ori.append(fullpathclu)
        elif inp.endswith('.hkl'):
            hkl_filename = os.path.join(path_sol,inp)
        elif inp.endswith('.pda'):
            shutil.copy(fullpathinp,fullpathclu)
            list_pdbs.append(fullpathclu)
        elif inp.endswith('.ent') and pm==True:
            shelxe_line_alixe = shelxe_line_alixe+' -x'
            ent_present = True
            ent_filename = os.path.join(path_sol,inp)
    if hkl_filename==None:
        print('Sorry, you need to provide the data in SHELX hkl format. Include it in the input folder ')
        sys.exit(0)
    if len(list_phs)==0:
        print('\nYou did not provide phase files, they will be automatically generated using the data ')
        info_frag_txt=open(os.path.join(clust_fold,'info_single_frags'),'w')
        info_frag_txt.write('%-25s %-10s %-15s %-15s %-15s %-10s %-10s %-10s\n' % ('Name','Size','InitCCshelx','wMPE_initial','wMPE_final','ShiftXent','ShiftYent','ShiftZent'))
        for ele in list_pdb_ori:
            print('Linking ',ele)
            list_pda.append(ele)
            try:
                os.link(ele,ele[:-4]+'.pda')
            except:
                print("Error")
                print(sys.exc_info())
            print('\nNow we will run SHELXE ')
            name_shelxe = os.path.basename(ele[:-4])
            try:
                shutil.copy(hkl_filename,os.path.join(clust_fold,name_shelxe+'.hkl'))
            except:
                print("Error")
                print(sys.exc_info())
            if ent_present:
                try:
                    shutil.copy(ent_filename, os.path.join(clust_fold,name_shelxe + '.ent'))
                except:
                    print("Error")
                    print(sys.exc_info())
            output=al.phase_fragment_with_shelxe(shelxe_line_alixe, name_shelxe, clust_fold, shelxe_path)
            print(output)
            list_phs_full.append(ele[:-4]+'.phs')
            # TODO: we want to check some things about our fragments so that we can use this info later
            initcc_frag=al.extract_INITCC_shelxe(output)
            shift_shelx = al.extract_shift_from_shelxe(output)
            wmpe_list = al.extract_wMPE_shelxe(os.path.join(clust_fold,name_shelxe + '.lst'))
            wmpe_bef_demod = wmpe_list[0]
            wmpe_after_demod = wmpe_list[2]
            # check also the size of the fragment
            oristru = Bioinformatics3.get_structure(os.path.basename(ele)[:-4], ele[:-4]+'.pda')
            list_atoms = Bio.PDB.Selection.unfold_entities(oristru, 'A')
            list_ca = [atom for atom in list_atoms if atom.id == 'CA']
            size = len(list_ca)
            info_frag_txt.write(
                '%-25s %-10s %-15s %-15s %-15s %-10s %-10s %-10s\n' % (name_shelxe, size, initcc_frag,
                                                                       wmpe_bef_demod, wmpe_after_demod,shift_shelx[0],
                                                                       shift_shelx[1],shift_shelx[2]))

        list_pdbs=list_pda
        del info_frag_txt
    else:
        print('\nYou did provide phase files, those will be used for the phase clustering')
        list_phs_full=copy.deepcopy(list_phs)

if not folder_mode:
    # Now, depending on the type of run in the case of ARCIMBOLDOs:
    # get the files
    # change their names
    # and link them to the cluster folder
    if type_run == 'ARCIMBOLDO' and mode.startswith('ens1_frag'):
        fragment = mode[9:]
        print('Getting the files from an ARCIMBOLDO_LITE run, from the folder of frag ', fragment)
        dict_sorted_input = al.get_files_from_ARCIMBOLDO_for_ALIXE(wd=wd_run, clust_fold=clust_fold, fragment=fragment,
                                                                   hard_limit_phs=hard_limit_phs)
    elif type_run == 'ARCIMBOLDO' and (mode=='two_steps' or mode=='one_step' or mode=='one_step_parallel'):
        print('Getting the files from the first fragment of an ARCIMBOLDO_LITE run')
        #fragment = 1 I can Use either 1st fragment as it is the default, or the one set by the user
        dict_sorted_input = al.get_files_from_ARCIMBOLDO_for_ALIXE(wd=wd_run, clust_fold=clust_fold, fragment=fragment,
                                                                   hard_limit_phs=hard_limit_phs)
    elif type_run == 'ARCIMBOLDO' and mode=='cc_analysis':
        print('Getting the files from an ARCIMBOLDO_LITE run, fragment number ',fragment)
        dict_sorted_input = al.get_files_from_ARCIMBOLDO_for_ALIXE(wd=wd_run, clust_fold=clust_fold, fragment=fragment,
                                                                   hard_limit_phs=hard_limit_phs)
    elif type_run == 'ARCIMBOLDO' and mode=='fish':
        # NOTE CM then this is performed for all fragments to get all solutions
        dict_all_frags = {}
        for fichiens in range(1,int(fragment_search)+1): 
            dict_sorted_input = al.get_files_from_ARCIMBOLDO_for_ALIXE(wd=wd_run, clust_fold=clust_fold, fragment=str(fichiens),
                                                                       hard_limit_phs=hard_limit_phs)
            dict_all_frags = al.merge_dicts(dict_all_frags,dict_sorted_input)
    elif type_run == "BORGES":
        print('Getting the files from a BORGES run')
        fragment = 1
        dict_sorted_input = {}
        for id_clu in os.listdir(os.path.join(wd_run, '9_EXP')):
            print("Getting files from cluster ", id_clu)
            dict_sorted_input[id_clu] = al.get_files_from_9_EXP_BORGES(wd_run, clust_fold, cluster_id=id_clu, mode=9,
                                                                       hard_limit_phs=hard_limit_phs)  # Only the refined solutions
    print("\nCompleted linking of files in CLUSTERING folder")


####################################################################
# Getting the symmetry information and setting up the files needed #
####################################################################
if not folder_mode:
    path_sym=os.path.join(wd_run, 'best.pda')
    if not os.path.exists(path_sym):
        path_sym = os.path.join(wd_run, 'best.pdb')
else:
    path_sym=os.path.join(clust_fold,list_pdbs[0]) # Just the first file
try:
    print('\nExtracting symmetry information from ',path_sym)
    file_pda = open(path_sym, 'r')
except:
    print('\nSorry, no pdb or pda file was found and this is required to get the symmetry information')
    print('\nExiting now')
    quit()
cryst_card = al.extract_cryst_card_pdb(file_pda.read())
cell, sg_symbol = al.read_cell_and_sg_from_pdb(path_sym)  # Cell is a list of floats
sg_number = al.get_space_group_number_from_symbol(sg_symbol)
polar, origins = al.get_origins_from_sg_dictionary(sg_number)
path_ins = os.path.join(clust_fold, 'symmetry.ins')
al.generate_fake_ins_for_shelxe(path_ins, cell, sg_number)

#########################################################
# Checking the figures of merit of the single solutions #
#########################################################
dictio_fragments = {}
if not folder_mode:
    list_pdbs = al.list_files_by_extension(clust_fold, 'pda')
else:
    list_pdbs = list_phs_full
n_single_solutions=len(list_pdbs)

for pdb in list_pdbs:
        dictio_fragments[pdb[:-4]] = {'rot_cluster': None, 'llg': None, 'zscore': None, 'initcc': None, 'efom': None,
                                      'pseudocc': None, 'list_MPE': None}

if not folder_mode:
    # From lst files
    dictio_fragments = al.get_FOMs_from_lst_files_in_folder(dictio_fragments=dictio_fragments, ent_present=ent_present)
    # From SUMs
    gimble=al.check_if_gimble(type_run, wd_run)
    dictio_fragments = al.get_FOMs_from_sum_files_in_folder(wd=wd_run, clust_fold=clust_fold, dictio_fragments=dictio_fragments,
                                                            gimble=gimble, program=type_run,
                                                            fragment=fragment)

    # Generate the list of rotation clusters that are available for clustering
    list_rot_cluster = al.get_list_rotation_clusters_from_dictio_fragments(dictio_fragments)


    # Save information about FOMs of fragments in a file that is readable as a table
    al.write_info_frag_from_dictio_frag(dictio_fragments=dictio_fragments, clust_fold=clust_fold,
                                        ent_present=ent_present)
else:
    list_rot_cluster = ['0'] # just a dummy id, the same for all of them
    # TODO CM: we could also retrieve FOMs from the lst files if we have computed the phs ourselves with SHELXE


######################################
# Modes of autoalixe core algorithms #
######################################
if mode == 'fish':
    dict_clust_by_rotclu = {}
    # NOTE CM: this is a dummy id but will cause problems in the writing of the output, so we have to exit the mode while we do something more standard for the output
    dict_clust_by_rotclu['0']={}
    phs_files = al.list_files_by_extension(path=clust_fold, extension='phs',fullpath=False)
    # preparing the parallel mode using more than one reference
    total_references = len(list_references_fish)
    print('\n*****************************************************************************************')
    print('\n The number of cores available to use in the fishing parallel mode will be ', n_cores)
    print('\n The number of references to attempt will be ', total_references)
    print('\n*****************************************************************************************\n\n')
    # In this case, all attempts are independent, it is totally parallel, I can run all the jobs
    list_references_names = [ os.path.basename(ele)[:-4] for ele in list_references_fish ]
    list_pool_names = [ os.path.basename(ele)[:-4] for ele in phs_files ]
    list_equal_names = [ ele for ele in list_references_names if ele in list_pool_names]
    if len(list_equal_names)==len(list_references_names):
        print('The references are already part of the pool, there is no need to compute anything else')
        list_references_fish = [ ele+'.phs' for ele in list_references_names ]
    else:
        print('The references are not part of the pool')
        if phs_ref:
            for fichito in list_references_fish:
                link_file(clust_fold, fichito, os.path.basename(fichito))
        else:
            print('TODO: phs files should be generated out of the input coordinate files')
            sys.exit(0)
    list_ls_to_process = []
    for i,path_phs1 in enumerate(list_references_fish):
        name_ref=os.path.basename(path_phs1)[:-4]
        path_ls = os.path.join(clust_fold, name_ref+'_ref.ls')
        link_file(clust_fold, path_sym, path_ls[:-3]+".pda")
        lsfile = open(path_ls, 'w')
        lsfile.write(os.path.basename(path_phs1)+'\n')
        for j in range(len(phs_files)):
             phs_namefile = os.path.basename(phs_files[j])
             if phs_namefile!=name_ref+'.phs':
                 lsfile.write(phs_namefile+'\n')
        del lsfile
        list_ls_to_process.append((os.path.basename(path_ls),j-i+1,os.path.basename(path_phs1)))

    # start your parallel workers at the beginning of your script
    total_ref=len(list_references_fish)
    if total_ref < n_cores:
        pool = Pool(total_ref)
        print('\n\n Opening the pool with ',total_ref,' workers')
    else:   
        pool = Pool(n_cores)
        print('\n\n Opening the pool with ',n_cores,' workers')

    # prepare the iterable with the arguments
    list_args = []
    for op,tuplels in enumerate(list_ls_to_process):
        namels = tuplels[0]
        phs_in_ls = tuplels[1]
        phs_ref = tuplels[2]
        list_args.append((namels[:-3],clust_fold,path_phstat,resolution,0,tolerance_first_round,3,
                          orisub,weight,oricheck,cc_calc))

    # execute a computation(s) in parallel
    pool.map(al.call_phstat_for_clustering_in_parallel_pool, list_args)

    # turn off your parallel workers at the end of your script
    print('Closing the pool')
    pool.close()

    for op,tuplels in enumerate(list_ls_to_process):
        namels = tuplels[0]
        phs_in_ls = tuplels[1]
        phs_ref = tuplels[2]
        output_file = open(os.path.join(clust_fold,namels[:-3]+'.out'),'r')
        output_content = output_file.read()
        print('***************************************\n')
        print(output_content)
        print('****************************************\n')

        dictio_result, total_runtime = al.read_phstat_isa_clusterization_output(output_content, 3, phs_in_ls)
        al.write_sum_file_from_dictio_result(os.path.join(clust_fold,namels[:-3]+'.sum'), dictio_result)
        name_phi = namels[:-3]+'.phi'
        path_phi = os.path.join(clust_fold,namels[:-3]+'.phi')
        dict_clust_by_rotclu['0'][name_phi] = {'dictio_result': dictio_result,'n_phs': len(dictio_result.keys()),'dict_FOMs': {}}

    # NOTE: clu is a fake id at this point
    for clufa in dict_clust_by_rotclu.keys():
        for clukey in dict_clust_by_rotclu[clufa]:
            if dict_clust_by_rotclu[clufa][clukey]['n_phs']>1:
                print('This reference ',clukey,' did fish something ')
                print('Check ',clukey[:-4]+'.sum')
            else:
                print('No fish!')
    sys.exit(0)

elif mode == 'one_step':# or mode == 'two_steps' or mode == 'combi':  # In either case we need to perform the first step
    # Prepare the input to perform phase clustering inside each rotation cluster
    dict_clust_by_rotclu = {}
    for rotclu in list_rot_cluster:
        dict_clust_by_rotclu[rotclu] = None
        print("\nWe are performing rotation cluster ", rotclu)
        if not folder_mode:
            list_phs_full = [dict_sorted_input[str(rotclu)][i] for i in range(len(dict_sorted_input[str(rotclu)]))]
            list_phs_rotclu = al.sort_list_phs_rotclu_by_FOM(list_phs_full,fom_sorting,dictio_fragments)
        else:
            list_phs_rotclu = list_phs_full
        # Now we can do the first clustering round inside this rotation
        # 1) Write an ls file with the list of phs
        ref_phs = list_phs_rotclu[0]
        path_ls = os.path.join(clust_fold, "first_round.ls")
        lsrotfile = open(path_ls, 'w')
        for i in range(len(list_phs_rotclu)):
            phs_namefile = (os.path.split(list_phs_rotclu[i]))[1]
            lsrotfile.write(phs_namefile + '\n')
        lsrotfile.close()
        # 2.1) Link the ins file
        link_file(clust_fold, path_ins, "first_round.ins")
        # 2.2) Link the pda file
        link_file(clust_fold, path_sym, "first_round.pda")
        # 3) Launch the sequential clustering function in alixe_library
        dict_clust_by_rotclu[rotclu] = al.clustering_phstat_isa_under_a_tolerance(name_phstat=path_ls[:-3],
                                                                                  wd=clust_fold,
                                                                                  path_phstat=path_phstat,
                                                                                  tolerance=tolerance_first_round,
                                                                                  resolution=resolution, seed=seed,
                                                                                  n_cycles=cycles, orisub=orisub,
                                                                                  weight=weight,idrotclu=rotclu,
                                                                                  oricheck=oricheck, mapcc=cc_calc)

elif mode == 'one_step_parallel':
    print('\n*****************************************************************************************')
    print('\n The number of cores to use in the one_step parallel mode will be ', n_cores)
    print('\n*****************************************************************************************\n\n')
    # Prepare the input to perform phase clustering inside each rotation cluster
    dict_clust_by_rotclu = {}
    dict_rotclu = {}
    sizerotclu=len(list_rot_cluster)
    new_list_rot_cluster = []
    for i,ele in enumerate(list_rot_cluster):
        list_clu = ele.split('_')
        list_clu = [ int(ele) for ele in list_clu ]
        list_clu = sorted(list_clu)
        list_clu = [ str(ele) for ele in list_clu ]
        new_list_rot_cluster.append('_'.join(list_clu))
    for indx,rotclu in enumerate(new_list_rot_cluster):
        dict_rotclu[rotclu] = None
        print('\n*****************************************************************************************')
        print("\nWe are performing rotation cluster ", rotclu)
        print('\n*****************************************************************************************\n\n')
        if not folder_mode:
            list_phs_full = [dict_sorted_input[str(rotclu)][i] for i in range(len(dict_sorted_input[str(rotclu)]))]
            list_phs_rotclu = al.sort_list_phs_rotclu_by_FOM(list_phs_full,fom_sorting,dictio_fragments)
        else:
            list_phs_rotclu = list_phs_full
        starting_input_size=len(list_phs_rotclu)
        print('\n*****************************************************************************************')
        print('\n The starting number of phs files to process is  ', starting_input_size)
        print('\n*****************************************************************************************\n\n')
        # Now we can do the first clustering round inside this rotation
        if phstat_version == 'fortran': # NOTE CM: no python version for this
            # All this block is what I will need to iterate over and change every time a round is completed
            # list_phs_rotclu should now be smaller and do not have the things that have clustered already
            dict_global_results = {}
            last_job=False
            single_job=False
            iterations_performed=0
            while len(list_phs_rotclu) > 1:
                iterations_performed=iterations_performed+1
                total_files = len(list_phs_rotclu)
                print('\n*****************************************************************************************')
                print('\n We are processing rotation cluster ',rotclu,' which is the ',indx+1,' out of ',sizerotclu)
                print('\n It remains to process ', total_files ,' phs files out of a total of ',starting_input_size)
                print('\n*****************************************************************************************\n\n')
                list_args = []
                jobs_to_check = []
                start_ref_name=os.path.basename(list_phs_rotclu[0])
                if (total_files-1) <= min_size_list:
                    last_job=True
                    # single_job=True # single job I can remove it I have the iterations
                    break
                size_chunk_float = (total_files - 1) / float(n_cores)  # we do not count the common reference
                size_chunk = int(math.ceil(size_chunk_float))
                list_fish = list_phs_rotclu[1:]
                size_chunk = int(math.ceil((len(list_fish)/float(n_cores))))
                list_to_eval = [list_fish[i:i + size_chunk] for i in xrange(0, len(list_fish), size_chunk)]

                for ind,ele in enumerate(list_to_eval):
                    size_ls = len(ele)+1 # we need to take into account the reference
                    path_ls = os.path.join(clust_fold,'chunk_'+str(ind)+'.ls')
                    lsrotfile = open(path_ls,'w')
                    lsrotfile.write(start_ref_name + '\n')
                    for i in range(len(ele)):
                        phs_namefile = (os.path.split(ele[i]))[1]
                        lsrotfile.write(phs_namefile + '\n')
                    lsrotfile.close()
                    if not os.path.exists(os.path.join(clust_fold, 'chunk_'+str(ind)+".ins")):
                        shutil.copy(path_ins, os.path.join(clust_fold, 'chunk_'+str(ind)+".ins"))
                    if not os.path.exists(os.path.join(clust_fold, 'chunk_'+str(ind)+".pda")):
                        shutil.copy(path_sym, os.path.join(clust_fold, 'chunk_'+str(ind)+".pda"))
                    list_args.append(('chunk_'+str(ind), clust_fold, path_phstat, resolution_comp,
                                      seed_parallel, tolerance_first_round, cycles, orisub, weight,oricheck,cc_calc))
                    jobs_to_check.append((os.path.join(clust_fold,'chunk_'+str(ind)+'.out'),size_ls))

                # Now run all the trials
                for argumlist in list_args:
                    al.call_phstat_for_clustering_in_parallel(argumlist)

                # I need to know when they have finished
                PHSTAT_OUT_END_CONDITION_LOCAL = """cluster phases written to"""
                PHSTAT_OUT_FAILURE_CONDITION_LOCAL = """Bad command line"""
                PHSTAT_OUT_END_TEST = 1
                return_val = False
                while return_val == False:
                    for job,size_ls in jobs_to_check:
                        return_val = SELSLIB2.checkYOURoutput(myfile=job,conditioEND=PHSTAT_OUT_END_CONDITION_LOCAL,
                                                          testEND=PHSTAT_OUT_END_TEST,sleep_ifnot_ready=True,
                                                          failure_test=PHSTAT_OUT_FAILURE_CONDITION_LOCAL)

                # Now I am sure they have finished, I can evaluate them
                list_setsol_remove = []
                for output_filename,size_ls in jobs_to_check:
                    print('Checking ',output_filename)
                    name_chunk=os.path.basename(output_filename)[:-4]
                    output_file=open(output_filename,'r')
                    output_content = output_file.read()
                    dictio_result, total_runtime, seed_tested = al.read_phstat_isa_multiseed_clusterization_output(
                        output_content, cycles, size_ls)
                    if seed_tested:
                        list_dictio_results = al.split_alixe_clusters(dictio_result)
                    else:
                        list_dictio_results = [dictio_result]
                    if seed_parallel == 1:
                        name_superphi = name_chunk + "_" + str(len(list_dictio_results)) + ".phi"
                    elif seed_parallel == 0:
                        name_superphi = name_chunk + "_0.phi"
                    #  Move the file to change its name and make it consistent with the convention
                    os.rename(os.path.join(clust_fold,name_superphi),
                              os.path.join(clust_fold,name_chunk+'.phi'))


                    #log_file.write(str(size_ls) + ' ' + str(total_runtime) + '\n')

                    for iclu, superclu in enumerate(list_dictio_results):
                        dictio_result = superclu
                        phs_in_cluster = len(dictio_result)
                        # Obtain the name of the reference used
                        if phs_in_cluster > 1:  # Then I need to rename the original phi file
                            for fichi in dictio_result.keys():
                                if dictio_result[fichi]['ref_no_cluster'] != 'cluster':
                                    name_phi = fichi[:-4] + '_ref.phi'
                            os.rename(os.path.join(clust_fold,name_chunk+'.phi'), os.path.join(clust_fold, name_phi))
                            name_key=name_phi
                        else:
                            name_key = dictio_result.keys()[0]

                        clustered = True if len(dictio_result.keys())>1 else False
                        keys_global=dict_global_results.keys()
                        if name_key in keys_global: # Add this info
                            if not clustered:
                                dict_global_results[name_key].append((name_chunk,set()))
                            else:
                                dict_global_results[name_key].append((name_chunk,set(dictio_result.keys())))
                        else: # Create the key and add the info then
                            if not clustered:
                                dict_global_results[name_key] = []
                                dict_global_results[name_key].append((name_chunk, set()))
                            else:
                                dict_global_results[name_key] = []
                                dict_global_results[name_key].append((name_chunk, set(dictio_result.keys())))
                        list_setsol_remove.extend([os.path.join(clust_fold,ele) for ele in dictio_result.keys()])
                    ########
                set1 = set(list_phs_rotclu)
                set2 = set(list_setsol_remove)
                new_input = list(set1 - set2)
                list_phs_rotclu = [e for e in new_input]

        if last_job: # We need to perform a last one including all the rest of the files
            list_setsol_remove = []
            while len(list_phs_rotclu)>=1:
                start_ref_name = os.path.basename(list_phs_rotclu[0])
                path_ls = os.path.join(clust_fold, 'last.ls')
                lsrotfile = open(path_ls, 'w')
                for xi in range(len(list_phs_rotclu)):
                    phs_namefile = (os.path.split(list_phs_rotclu[xi]))[1]
                    #phs_relative_path = os.path.join('./CLUSTERING', phs_namefile)
                    #lsrotfile.write(phs_relative_path + '\n')
                    lsrotfile.write(phs_namefile + '\n')
                lsrotfile.close()
                if not os.path.exists(os.path.join(clust_fold, 'last.ins')):
                    shutil.copy(path_ins, os.path.join(clust_fold, 'last.ins'))
                if not os.path.exists(os.path.join(clust_fold, "last.pda")):
                    shutil.copy(path_sym, os.path.join(clust_fold, "last.pda"))
                output,error=al.call_phstat_print_for_clustering_global('last',clust_fold,path_phstat, resolution_comp,
                                          seed, tolerance_first_round, cycles, orisub, weight,oricheck=oricheck,mapcc=cc_calc)
                name_chunk='last'
                dictio_result, total_runtime, seed_tested = al.read_phstat_isa_multiseed_clusterization_output(
                    output, cycles, len(list_phs_rotclu))
                if seed_tested:
                    list_dictio_results = al.split_alixe_clusters(dictio_result)
                else:
                    list_dictio_results = [dictio_result]
                #log_file.write(str(len(list_phs_rotclu))+' '+str(total_runtime)+'\n')

                # Now this is the part that should be done for all the results obtained
                # NOTE CM this is copied from the other part that is not the last, should be merged to function
                for iclu, superclu in enumerate(list_dictio_results):
                    dictio_result = superclu
                    phs_in_cluster = len(dictio_result)
                    # Obtain the name of the reference used
                    if phs_in_cluster > 1:  # Then I need to rename the original phi file
                        for fichi in dictio_result.keys():
                            if dictio_result[fichi]['ref_no_cluster'] != 'cluster':
                                name_phi = fichi[:-4] + '_ref.phi'
                        if len(list_dictio_results)>1:
                            os.rename(os.path.join(clust_fold, name_chunk + '_' +
                                                   str(len(list_dictio_results)) + '.phi'),
                                      os.path.join(clust_fold, name_phi))
                        else:
                            os.rename(os.path.join(clust_fold, name_chunk + '_' + str(seed) + '.phi'),
                                      os.path.join(clust_fold, name_phi))
                        name_key = name_phi
                    else:
                        name_key = dictio_result.keys()[0]

                    clustered = True if len(dictio_result.keys()) > 1 else False
                    keys_global = dict_global_results.keys()
                    if name_key in keys_global:  # Add this info
                        if not clustered:
                            dict_global_results[name_key].append((name_chunk, set()))
                        else:
                            dict_global_results[name_key].append((name_chunk, set(dictio_result.keys())))
                    else:  # Create the key and add the info then
                        if not clustered:
                            dict_global_results[name_key] = []
                            dict_global_results[name_key].append((name_chunk, set()))
                        else:
                            dict_global_results[name_key] = []
                            dict_global_results[name_key].append((name_chunk, set(dictio_result.keys())))
                    list_setsol_remove.extend([os.path.join(clust_fold, ele) for ele in dictio_result.keys()])
                set1 = set(list_phs_rotclu)
                set2 = set(list_setsol_remove)
                new_input = list(set1 - set2)
                list_phs_rotclu=new_input

        # Save the results sorted by rotclu
        dict_rotclu[rotclu] = dict_global_results

    count_single_global=0
    for keyro in dict_rotclu.keys():
        count_single_rot = 0
        list_to_recalculate = []
        for keyclu in dict_rotclu[keyro].keys():
            listsets=dict_rotclu[keyro][keyclu]
            settis=[ele[1] for ele in listsets]
            united=set.union(*settis)
            if len(united) != 0:
                list_to_recalculate.append((keyclu,list(united)))
            else:
                count_single_rot=count_single_rot+1
        count_single_global = count_single_global + count_single_rot


        if len(list_to_recalculate)>0: # NOTE CLAUDIA: I should check whether a single job only
            print('\n\n Now we will perform the reclustering step\n')
            for ref,files in list_to_recalculate:
                name_ref = os.path.basename(ref)[:-8]
                extt_ref = ref[-4:]
                #print('SHERLOCK extt_ref',extt_ref)
                filekeep=os.path.basename(ref)[:-4]#+'_ref'
                path_ls = os.path.join(clust_fold, filekeep+'.ls')
                lsrotfile = open(path_ls, 'w')
                #name_ref_phs=os.path.basename(ref)[:-8]+'.phs'
                name_ref_phs = os.path.basename(ref)[:-8] + extt_ref
                #print('SHERLOCK name_ref_phs',name_ref_phs)
                lsrotfile.write(name_ref_phs+ '\n')
                for xi in range(len(files)):
                    if files[xi]!=name_ref_phs:
                        lsrotfile.write(files[xi] + '\n')
                lsrotfile.close()
                if not os.path.exists(os.path.join(clust_fold, filekeep+'.ins')):
                    shutil.copy(path_ins, os.path.join(clust_fold, filekeep+'.ins'))
                if not os.path.exists(os.path.join(clust_fold, filekeep+".pda")):
                    shutil.copy(path_sym, os.path.join(clust_fold, filekeep+".pda"))
                # NOTE CM changing for the multiseed
                # output,error=al.call_phstat_print_for_clustering(filekeep,"./CLUSTERING/",path_phstat, resolution_merge,
                #                           seed, tolerance_first_round, cycles, orisub, weight,oricheck=oricheck,mapcc=cc_calc)
                # dictio_result, total_runtime = al.read_phstat_isa_clusterization_output(output, cycles, len(files))
                output,error=al.call_phstat_print_for_clustering_global(filekeep,clust_fold,path_phstat, resolution_merge,
                                          seed_parallel, tolerance_first_round, cycles, orisub, weight,oricheck=oricheck,mapcc=cc_calc)

                dictio_result, total_runtime, seed_tested = al.read_phstat_isa_multiseed_clusterization_output(
                    output, cycles, len(files))

                if seed_tested:
                    list_dictio_results = al.split_alixe_clusters(dictio_result)
                else:
                    list_dictio_results = [dictio_result]



                #log_file.write(str(len(files)) + ' ' + str(total_runtime) + '\n')
                namecluphi=os.path.join(clust_fold,filekeep+".phi")
                os.rename(os.path.join(clust_fold,filekeep+"_"+str(seed_parallel)+".phi"),namecluphi)

                if keyro in dict_clust_by_rotclu.keys():
                    dict_clust_by_rotclu[keyro][namecluphi]={'dictio_result': dictio_result,
                                                             'n_phs': len(dictio_result.keys()),
                                                             'dict_FOMs': {}}
                else:
                    dict_clust_by_rotclu[keyro] = {}
                    dict_clust_by_rotclu[keyro][namecluphi]={'dictio_result': dictio_result,
                                                             'n_phs': len(dictio_result.keys()),
                                                             'dict_FOMs': {}}
    # for keyro in dict_clust_by_rotclu.keys():
    #     for key1 in dict_clust_by_rotclu[keyro].keys():
    #         new_key1 = os.path.join(clust_fold, os.path.split(key1)[1])
    #         dict_clust_by_rotclu[keyro][new_key1] = copy.deepcopy(dict_clust_by_rotclu[keyro][key1])
    #         del dict_clust_by_rotclu[keyro][key1]
    #         for key2 in dict_clust_by_rotclu[keyro][new_key1]['dictio_result'].keys():
    #             new_key2 = os.path.join(clust_fold, os.path.split(key2)[1])
    #             dict_clust_by_rotclu[keyro][new_key1]['dictio_result'][new_key2] = copy.deepcopy(
    #                 dict_clust_by_rotclu[keyro][new_key1]['dictio_result'][key2])
    #             del dict_clust_by_rotclu[keyro][new_key1]['dictio_result'][key2]



elif mode.startswith('ens1_frag'):
    dict_clust_by_rotclu = {}
    rotclu = 'arci' # In this case we consider all clusters together
    list_phs_full = [ dict_sorted_input[key][i] for key in dict_sorted_input.keys() for i in range(len(dict_sorted_input[key]))]
    list_tuple_sort = []
    for phs in list_phs_full:
        phs_key=phs[:-4]
        list_tuple_sort.append((phs,dictio_fragments[phs_key]['zscore'],dictio_fragments[phs_key]['llg'],dictio_fragments[phs_key]['initcc']))
    if fom_sorting=='CC':
        list_tuple_sort.sort(key=lambda x: x[3],reverse=True)
    elif fom_sorting=='LLG':
        list_tuple_sort.sort(key=lambda x: x[2],reverse=True)
    elif fom_sorting=='ZSCORE':
        list_tuple_sort.sort(key=lambda x: x[1],reverse=True)
    list_phs_full = [ list_tuple_sort[i][0] for i in range(len(list_tuple_sort)) ]
    if phstat_version == 'fortran':
        # 1) Write an ls file with the list of phs
        ref_phs = list_phs_full[0]
        path_ls = os.path.join(clust_fold, "first_round.ls")
        lsrotfile = open(path_ls, 'w')
        # NOTE: I need to use a relative path because fortran does not accept such long paths
        for i in range(len(list_phs_full)):
            phs_namefile = (os.path.split(list_phs_full[i]))[1]
            #phs_relative_path = os.path.join('./CLUSTERING', phs_namefile)
            #lsrotfile.write(phs_relative_path + '\n')
            lsrotfile.write(phs_namefile + '\n')
        lsrotfile.close()
        # 2) Link the ins file
        if not os.path.exists(os.path.join(clust_fold, "first_round.ins")):
            os.link(path_ins, os.path.join(clust_fold, "first_round.ins"))
        # 2) Link the pda file
        if not os.path.exists(os.path.join(clust_fold, "first_round.pda")):
            os.link(path_sym, os.path.join(clust_fold, "first_round.pda"))
        # 3) Launch the function in alixe_library
        dict_clust_by_rotclu[rotclu] = al.clustering_phstat_isa_under_a_tolerance(name_phstat='first_round',
                                                                                  wd=clust_fold,
                                                                                  path_phstat=path_phstat,
                                                                                  tolerance=tolerance_first_round,
                                                                                  resolution=resolution, seed=seed,
                                                                                  n_cycles=cycles,orisub=orisub,
                                                                                  weight=weight,idrotclu=rotclu)




elif mode == ('cc_analysis'):
    # We need to prepare all the ls files
    phs_files = al.list_files_by_extension(clust_fold, 'phs')
    if not phs_files:
        print('\n There were not phs files found, trying to get phi files')
        phs_files = al.list_files_by_extension(clust_fold, 'phi')
    table_cc_names = open(os.path.join(clust_fold,'corresp_names_ccfiles.txt'),'w')
    dict_cc_names = {}
    list_ls_to_process = []
    for i,phs1 in enumerate(phs_files):
        table_cc_names.write(str(i + 1) + '\t' + os.path.basename(phs1) + '\n')
        dict_cc_names[os.path.basename(phs1)] = str(i + 1)
        if i < len(phs_files)-1:
            path_ls = os.path.join(clust_fold, "ref"+str(i+1)+'.ls')
            #print 'Using reference phs ', phs1
            # We also need to have linked a pda file for each of the ls files
            if not os.path.exists(os.path.join(clust_fold, path_ls[:-3]+".pda")):
                os.link(path_sym, os.path.join(clust_fold, path_ls[:-3]+".pda"))
            lsfile = open(path_ls, 'w')
            for j in range(i,len(phs_files)):
                #print '   And including ',phs_files[j]
                phs_namefile = os.path.basename(phs_files[j])
                lsfile.write(phs_namefile+'\n')
            del lsfile
            list_ls_to_process.append((os.path.basename(path_ls),j-i+1,os.path.basename(phs1)))
    del table_cc_names

    # start your parallel workers at the beginning of your script
    pool = Pool(n_cores)
    print('\n\n Opening the pool with ',n_cores,' workers')

    # prepare the iterable with the arguments
    list_args = []
    for op,tuplels in enumerate(list_ls_to_process):
        namels = tuplels[0]
        phs_in_ls = tuplels[1]
        phs_ref = tuplels[2]
        list_args.append((namels[:-3],clust_fold,path_phstat,resolution,0,100,1,orisub,weight,oricheck,cc_calc))

    # execute a computation(s) in parallel
    pool.map(al.call_phstat_for_clustering_in_parallel_pool, list_args)

    # turn off your parallel workers at the end of your script
    print('Closing the pool')
    pool.close()

    input_for_ccanalysis = open(os.path.join(clust_fold,'alixecc.dat'),'w')
    info_relations = open(os.path.join(clust_fold,'global_table.dat'),'w')
    info_relations.write('%-35s %-35s %-12s %-12s %-12s %-12s %-12s %-12s \n' % ('File1', 'File2', 'mapCC', 'wMPD','diffwMPD', 'shiftX', 'shiftY', 'shiftZ'))

    for op,tuplels in enumerate(list_ls_to_process):
        namels = tuplels[0]
        phs_in_ls = tuplels[1]
        phs_ref = tuplels[2]
        output_file = open(os.path.join(clust_fold,namels[:-3]+'.out'),'r')
        output_content = output_file.read()
        print(output_content)
        dictio_result, total_runtime = al.read_phstat_isa_clusterization_output(output_content, 1, phs_in_ls)
        # Note: in this case, there is only one cycle so dictio_result first and last entries are the same
        ref_id = dict_cc_names[phs_ref]
        for keyphs in dictio_result.keys():
            comp_id = dict_cc_names[os.path.basename(keyphs)]
            comp_name = os.path.basename(keyphs)
            if ref_id == comp_id:
                continue
            mapcc_scaled1 = (dictio_result[keyphs]['mapcc_first'])/100
            wmpd = dictio_result[keyphs]['wMPE_first']
            diffwmpd = dictio_result[keyphs]['diff_wMPE_first']
            shiftx = dictio_result[keyphs]['shift_first'][0]
            shifty = dictio_result[keyphs]['shift_first'][1]
            shiftz = dictio_result[keyphs]['shift_first'][2]
            input_for_ccanalysis.write('\t'+str(ref_id)+'\t'+str(comp_id)+'\t'+str(mapcc_scaled1)+'\n')
            info_relations.write('%-35s %-35s %-12s %-12s %-12s %-12s %-12s %-12s \n' % (phs_ref, comp_name, mapcc_scaled1, wmpd, diffwmpd, shiftx, shifty, shiftz))
    del input_for_ccanalysis
    del info_relations
    # Remove the phi files resulting from this mode
    phi_to_remove=al.list_files_by_extension(clust_fold, 'phi')
    phi_to_remove=[ele for ele in phi_to_remove if (os.path.basename(ele)).startswith('ref')]
    for phi in phi_to_remove: # Remove all the files with ref, not only the phi
        try:
            os.remove(phi)
            os.remove(phi[:-4]+'.ls')
            os.remove(phi[:-4]+'.pda')
            # At the moment I keep them just to be able to check if everything is OK.
            #os.remove(phi[:-4]+'.out')
        except:
            pass

    #TODO with ANTONIA: write some kind of pickle file with
    # the dictio_result or something that allows to rerun just including some files in the folder
    new_now = time.time()
    final_string = '\nTotal time spent in running autoalixe in cc_analysis mode is ' + str((new_now - now)) + ' seconds , or ' + str(
        (new_now - now) / 60) + ' minutes \n'
    log_file.write(final_string)
    print(final_string)
    del log_file
    sys.exit(0)  # Finishing normally the cc_analysis mode



# Nice table from first round
table_clust_first_round = open(clust_fold + "info_clust_table", 'w')
if ent_present and pm:
    if fuscoord:
        if phifromfus:
            table_clust_first_round.write(
            '%-40s %-5s %-10s %-10s %-10s %-10s %-10s %-10s\n' %
            ('Cluster', 'n_phs', 'topzscore', 'topllg', 'fused_cc', 'fused_wmpe', 'phi_cc','phi_wmpe'))
        else:
            table_clust_first_round.write(
            '%-40s %-5s %-10s %-10s %-10s %-10s \n' % 
            ('Cluster', 'n_phs', 'topzscore', 'topllg', 'fused_cc', 'fused_wmpe'))
    else:
        if phifromfus:
            table_clust_first_round.write(
            '%-40s %-5s %-10s %-10s %-10s %-10s\n' % 
            ('Cluster', 'n_phs', 'topzscore', 'topllg', 'phi_cc','phi_wmpe'))
        else:
            table_clust_first_round.write(
            '%-40s %-5s %-10s %-10s \n' % 
            ('Cluster', 'n_phs', 'topzscore', 'topllg'))
    del table_clust_first_round
else:
    if fuscoord:
        if phifromfus:
            table_clust_first_round.write(
            '%-40s %-5s %-10s %-10s %-10s %-10s\n' %
            ('Cluster', 'n_phs', 'topzscore', 'topllg', 'fused_cc', 'phi_cc'))
        else:
            table_clust_first_round.write(
            '%-40s %-5s %-10s %-10s %-10s\n' % 
            ('Cluster', 'n_phs', 'topzscore', 'topllg', 'fused_cc'))
    else:
        if phifromfus:
            table_clust_first_round.write(
            '%-40s %-5s %-10s %-10s %-10s\n' %
            ('Cluster', 'n_phs', 'topzscore', 'topllg', 'phi_cc'))
        else:
            table_clust_first_round.write(
            '%-40s %-5s %-10s %-10s\n' % 
            ('Cluster', 'n_phs', 'topzscore', 'topllg'))
    del table_clust_first_round
# Raw output from first run
raw_clust_first_round = open(clust_fold + "info_clust_raw", 'w')
del raw_clust_first_round

# Read clusters from results and process them
list_to_expand_first_round = []
count_cluster = 0
for rotclu in dict_clust_by_rotclu.keys():
    print('We are evaluating rotation cluster',rotclu)
    for cluster in (dict_clust_by_rotclu[rotclu]).keys():
        print("\n\tEvaluating cluster ", cluster)
        n_phs = dict_clust_by_rotclu[rotclu][cluster]['n_phs']
        count_cluster = count_cluster+1
        if dict_clust_by_rotclu[rotclu][cluster]['n_phs'] > 1:
            print("\t This cluster contains more than one phs")
            list_llg = []
            list_zscore = []
            list_of_filepaths = []  # list of files to join
            dict_clust_by_rotclu[rotclu][cluster][
                'rot_clust_list'] = []  # Generate new key to save original rotation_cluster
            for phs in dict_clust_by_rotclu[rotclu][cluster]['dictio_result'].keys():  # For each phs in the cluster
                print("\t Processing file ", phs)
                keydictiofrag=os.path.join(clust_fold,phs[:-4])
                print('SHERLOCK keydictiofrag',keydictiofrag)
                print('SHERLOCK dictio_fragments.keys()',dictio_fragments.keys())
                list_llg.append(dictio_fragments[keydictiofrag]['llg'])
                list_zscore.append(dictio_fragments[keydictiofrag]['zscore'])
                if dictio_fragments[keydictiofrag]['rot_cluster'] not in dict_clust_by_rotclu[rotclu][cluster][
                    'rot_clust_list']:
                    # If more than 1 rot cluster elongated together you will have a list with len >1
                    dict_clust_by_rotclu[rotclu][cluster]['rot_clust_list'].append(
                        dictio_fragments[keydictiofrag]['rot_cluster'])
                shift = dict_clust_by_rotclu[rotclu][cluster]['dictio_result'][phs]['shift_first']
                if shift == [-1,-1,-1]: # Then this phs entered in the third cycle and I need to catch that
                    shift = dict_clust_by_rotclu[rotclu][cluster]['dictio_result'][phs]['shift_last']
                if polar:  # Check if the shift is too small to be considered
                    for i in range(len(shift)):
                        if abs(shift[i]) < 0.0001 and shift[i] != 0.0:  # NOTE: What will be a sensible number?
                            shift[i] = 0.0
                if fuscoord:
                    if not (shift == [0.0, 0.0, 0.0]):  # Make sure it is not the reference
                        al.shifting_coordinates(dict_clust_by_rotclu[rotclu][cluster]['dictio_result'][phs]['shift_first'],
                                                keydictiofrag + '.pda')
                        list_of_filepaths.append(keydictiofrag + '_shifted.pda')  # Write pda with its shift
                    else:
                        list_of_filepaths.append(keydictiofrag + '.pda')

            if fuscoord:
                # Fuse the files in a single pdb
                al.fuse_pdbs(list_of_filepaths, cluster[:-4] + "_fused.pda")
                al.add_cryst_card(cryst_card, cluster[:-4] + "_fused.pda")

                # Check FOMs Starting from from the fused pda
                name_shelxe = ((os.path.split(cluster))[1])[:-4] + "_fused"
                #path_name_shelxe = os.path.join(clust_fold, name_shelxe)
                if ent_present and pm:
                    link_file(clust_fold,ent_filename,name_shelxe+'.ent')
                link_file(clust_fold,hkl_filename,name_shelxe + ".hkl")
                output = al.phase_fragment_with_shelxe(shelxe_line_alixe, name_shelxe, clust_fold, shelxe_path)
                lst_file = open(os.path.join(clust_fold,name_shelxe + '.lst'), 'r')
                lst_content = lst_file.read()
                list_fom = al.extract_EFOM_and_pseudoCC_shelxe(lst_content)
                initcc = al.extract_INITCC_shelxe(lst_content)
                try:
                    dict_clust_by_rotclu[rotclu][cluster]['dict_FOMs']['efom_fused'] = list_fom[0]
                    dict_clust_by_rotclu[rotclu][cluster]['dict_FOMs']['pseudocc_fused'] = list_fom[1]
                    dict_clust_by_rotclu[rotclu][cluster]['dict_FOMs']['CC_fused'] = initcc
                except:
                    dict_clust_by_rotclu[rotclu][cluster]['dict_FOMs']['efom_fused'] = -1
                    dict_clust_by_rotclu[rotclu][cluster]['dict_FOMs']['pseudocc_fused'] = -1
                    dict_clust_by_rotclu[rotclu][cluster]['dict_FOMs']['CC_fused'] = -1
                if ent_present and pm:  # Retrieve final MPE and save them too
                    try:
                        list_mpe = al.extract_wMPE_shelxe(clust_fold + name_shelxe + '.lst')
                        dict_clust_by_rotclu[rotclu][cluster]['dict_FOMs']['final_MPEs_fused'] = list_mpe
                        # Get the shift to final and apply it to better see in Coot to what solutions they correspond
                        lst_file = open(clust_fold + name_shelxe + '.lst')
                        lst_content = lst_file.read()
                        shift_to_apply = al.extract_shift_from_shelxe(lst_content)
                        if not shift_to_apply == [0.0, 0.0, 0.0]:
                            print("Moving pda ", name_shelxe, ".pda with this shift respect to the ent "
                                  , shift_to_apply)
                            al.shifting_coordinates_inverse(shift_to_apply, clust_fold + name_shelxe + '.pda')
                            al.add_cryst_card(cryst_card,
                                              clust_fold + name_shelxe + "_shifted.pda")  # Add cryst card to this pdb
                            os.rename(clust_fold + name_shelxe + "_shifted.pda",
                                      clust_fold + name_shelxe + "_shifted_to_final.pda")
                    except:
                        dict_clust_by_rotclu[rotclu][cluster]['dict_FOMs']['final_MPEs_fused'] = [-1,-1,-1,-1]
                fusedcc = dict_clust_by_rotclu[rotclu][cluster]['dict_FOMs']['CC_fused']
            if phifromfus:
                # 2) Starting from from the phi file
                name_shelxe = ((os.path.split(cluster))[1])[:-4]
                path_name_shelxe = os.path.join(clust_fold, name_shelxe)
                if ent_present and pm:
                    shutil.copy(ent_filename, path_name_shelxe + ".ent")
                shutil.copy(hkl_filename, path_name_shelxe + ".hkl")
                shutil.copy(path_ins, path_name_shelxe + ".ins")
                output = al.phase_with_shelxe_from_phi(shelxe_line_alixe, name_shelxe, clust_fold, shelxe_path)
                lst_file = open(path_name_shelxe + '.lst', 'r')
                lst_content = lst_file.read()
                list_fom = al.extract_EFOM_and_pseudoCC_shelxe(lst_content)
                if ent_present and pm:  # Retrieve final MPE and save them too
                    list_mpe = al.extract_wMPE_shelxe(clust_fold + name_shelxe + '.lst')
                    dict_clust_by_rotclu[rotclu][cluster]['dict_FOMs']['final_MPEs_phi'] = list_mpe
                phicc = al.extract_INITCC_shelxe(lst_content,map=True)
                dict_clust_by_rotclu[rotclu][cluster]['dict_FOMs']['efom_phi'] = list_fom[0]
                dict_clust_by_rotclu[rotclu][cluster]['dict_FOMs']['pseudocc_phi'] = list_fom[1]
                dict_clust_by_rotclu[rotclu][cluster]['dict_FOMs']['CC_phi'] = phicc

            # We add the top LLG or ZSCORE as representative of the cluster
            dict_clust_by_rotclu[rotclu][cluster]['dict_FOMs']['llg'] = (sorted(list_llg, reverse=True))[0]
            dict_clust_by_rotclu[rotclu][cluster]['dict_FOMs']['zscore'] = (sorted(list_zscore, reverse=True))[0]

            # Prepare to save info from clusters in this file
            name_cluster = os.path.split(cluster)[1]
            if not folder_mode:
                topzscore = dict_clust_by_rotclu[rotclu][cluster]['dict_FOMs']['zscore']
                topllg = dict_clust_by_rotclu[rotclu][cluster]['dict_FOMs']['llg']
            else:
                topzscore = -1.0
                topllg = -1.0
            
            # TODO claudia add this only if we are going to do expansions
            #list_to_expand_first_round.append((name_cluster, n_phs, topzscore, topllg, phicc))

            if ent_present and pm:
                if fuscoord:
                    wmpefinal_fused = dict_clust_by_rotclu[rotclu][cluster]['dict_FOMs']['final_MPEs_fused'][2]
                if phifromfus: 
                    wmpefinal_phi = dict_clust_by_rotclu[rotclu][cluster]['dict_FOMs']['final_MPEs_phi'][2]
                table_clust_first_round = open(clust_fold + "info_clust_table", 'a')
                if fuscoord:
                    if phifromfus:
                        table_clust_first_round.write('%-40s %-5i %-10.2f %-10.2f %-10.2f %-10.2f %-10.2f %-10.2f\n' % (
                        name_cluster, n_phs, topzscore, topllg, fusedcc, wmpefinal_fused, phicc, wmpefinal_phi))
                    else:
                        table_clust_first_round.write('%-40s %-5i %-10.2f %-10.2f %-10.2f %-10.2f \n' % (
                        name_cluster, n_phs, topzscore, topllg, fusedcc, wmpefinal_fused))
                else:
                    if phifromfus:
                        table_clust_first_round.write('%-40s %-5i %-10.2f %-10.2f %-10.2f %-10.2f \n' % (
                        name_cluster, n_phs, topzscore, topllg, phicc, wmpefinal_phi))
                    else:
                        table_clust_first_round.write('%-40s %-5i %-10.2f %-10.2f \n' % (
                        name_cluster, n_phs, topzscore, topllg))
                del table_clust_first_round
            else:
                table_clust_first_round = open(clust_fold + "info_clust_table", 'a')
                if fuscoord:
                    if phifromfus:
                        table_clust_first_round.write(
                            '%-40s %-5i %-10.2f %-10.2f %-10.2f %-10.2f \n' %
                            (name_cluster, n_phs, topzscore, topllg, fusedcc, phicc))
                    else:
                        table_clust_first_round.write(
                            '%-40s %-5i %-10.2f %-10.2f %-10.2f \n' %
                            (name_cluster, n_phs, topzscore, topllg, fusedcc))
                else:
                    if phifromfus:
                        table_clust_first_round.write(
                            '%-40s %-5i %-10.2f %-10.2f %-10.2f \n' % (name_cluster, n_phs, topzscore, topllg, phicc))
                    else:
                        table_clust_first_round.write(
                            '%-40s %-5i %-10.2f %-10.2f \n' % (name_cluster, n_phs, topzscore, topllg))

                del table_clust_first_round
        else:
            name_file = ((dict_clust_by_rotclu[rotclu][cluster]['dictio_result'].keys())[0])[:-4]
            name_file = os.path.join(clust_fold, os.path.split(name_file)[1])
            if not folder_mode:
                dict_clust_by_rotclu[rotclu][cluster]['dict_FOMs']['CC'] = dictio_fragments[name_file]['initcc']
                dict_clust_by_rotclu[rotclu][cluster]['dict_FOMs']['pseudocc'] = dictio_fragments[name_file]['pseudocc']
                dict_clust_by_rotclu[rotclu][cluster]['dict_FOMs']['efom'] = dictio_fragments[name_file]['efom']
                # Save also the phaser FOMs
                dict_clust_by_rotclu[rotclu][cluster]['dict_FOMs']['llg'] = dictio_fragments[name_file]['llg']
                dict_clust_by_rotclu[rotclu][cluster]['dict_FOMs']['zscore'] = dictio_fragments[name_file]['zscore']
                list_rot = []
                list_rot.append(dictio_fragments[name_file]['rot_cluster'])
                dict_clust_by_rotclu[rotclu][cluster]['rot_clust_list'] = list_rot
            else:
                print('SHERLOCK we will have to do something')
            if ent_present and not folder_mode and pm: # NOTE CM: unless we generated the phs in the folder
                dict_clust_by_rotclu[rotclu][cluster]['dict_FOMs']['final_MPEs'] = dictio_fragments[name_file][
                    'list_MPE']
                # Get the shift and apply it to better see in Coot to what solutions they correspond
                lst_file = open(name_file + '.lst')
                lst_content = lst_file.read()
                shift_to_apply = al.extract_shift_from_shelxe(lst_content)
                if not shift_to_apply == [0.0, 0.0, 0.0]:
                    print("Moving pda ", name_file + ".pda",
                          ".pda with this shift respect to the ent ", shift_to_apply)
                    al.shifting_coordinates_inverse(shift_to_apply, name_file + '.pda')
                    al.add_cryst_card(cryst_card, name_file + "_shifted.pda")  # Add cryst card to this pdb
                    os.rename(name_file + "_shifted.pda", name_file + "_shifted_to_final.pda")
            # Write the information about the cluster in the files
            raw_clust_first_round = open(clust_fold + "info_clust_raw",
                                         'a')  # Prepare to save info from clusters in this file
            raw_clust_first_round.write(
                "**********************************************************************************\n")
            raw_clust_first_round.write(str(cluster) + str(dict_clust_by_rotclu[rotclu][cluster]) + "\n")
            del raw_clust_first_round
            name_cluster = os.path.split(cluster)[1]
            if not folder_mode:
                topzscore = dict_clust_by_rotclu[rotclu][cluster]['dict_FOMs']['zscore']
                topllg = dict_clust_by_rotclu[rotclu][cluster]['dict_FOMs']['llg']
                fusedcc = dict_clust_by_rotclu[rotclu][cluster]['dict_FOMs']['CC']
            else: # TODO: This is quick and dirty to get the mode to work
                topzscore = -1.0
                topllg = -1.0
                fusedcc = -1.0
            if mode == 'two_steps' or filtersingle==False:
                if ent_present and pm:
                    if not folder_mode:
                        wmpefinal = dict_clust_by_rotclu[rotclu][cluster]['dict_FOMs']['final_MPEs'][2]
                    else:
                        wmpefinal = -1.0 # again, this we would have if we have or produce the lst ourselves
                    table_clust_first_round = open(clust_fold + "info_clust_table",
                                                   'a')  # Prepare to save info from clusters in this file
                    if phifromfus or fuscoord:
                        table_clust_first_round.write('%-40s %-5i %-10.2f %-10.2f %-10.2f %-10.2f\n' % (
                        name_cluster, n_phs, topzscore, topllg, fusedcc, wmpefinal))
                    else:
                        table_clust_first_round.write('%-40s %-5i %-10.2f %-10.2f %-10.2f\n' % (
                        name_cluster, n_phs, topzscore, topllg, wmpefinal))
                    del table_clust_first_round
                else:
                    table_clust_first_round = open(clust_fold + "info_clust_table",
                                                   'a')
                    if phifromfus or fuscoord:
                        table_clust_first_round.write(
                            '%-40s %-5i %-10.2f %-10.2f %-10.2f\n' % (name_cluster, n_phs, topzscore, topllg, fusedcc))
                    else:
                        table_clust_first_round.write(
                            '%-40s %-5i %-10.2f %-10.2f\n' % (name_cluster, n_phs, topzscore, topllg))
                    del table_clust_first_round

    # For each cluster write a summary table file with the information of its contents
    for cluster in dict_clust_by_rotclu[rotclu].keys():
        path_clu = os.path.join(clust_fold, os.path.basename(cluster)[:-4] + '.sum')
        fileforclu = open(path_clu, 'w')
        fileforclu.write(
            '%-40s %-10s %-10s %-10s %-10s %-10s %-10s %-10s %-10s %-10s %-10s %-10s\n' % ('Name','wMPD_first','wMPD_last', 'diff_wMPD','mapcc_first',
                                                 'mapcc_last','shift_first_x','shift_first_y','shift_first_z','shift_last_x','shift_last_y','shift_last_z'))
        for phaseset in dict_clust_by_rotclu[rotclu][cluster]['dictio_result'].keys():
            name = os.path.basename(phaseset)
            wmpe_first = round(dict_clust_by_rotclu[rotclu][cluster]['dictio_result'][phaseset]['wMPE_first'], 2)
            wmpe_last = round(dict_clust_by_rotclu[rotclu][cluster]['dictio_result'][phaseset]['wMPE_last'], 2)
            if phstat_version != 'fortran':
                if dict_clust_by_rotclu[rotclu][cluster]['n_phs']>1 and \
                        isinstance(dict_clust_by_rotclu[rotclu][cluster]['dictio_result'][phaseset]['diff_wMPE'],float):
                    diffwmpe = round(dict_clust_by_rotclu[rotclu][cluster]['dictio_result'][phaseset]['diff_wMPE'], 2)
                else:
                    diffwmpe = -1
            else:
                diffwmpe = -1
            if dict_clust_by_rotclu[rotclu][cluster]['dictio_result'][phaseset]['mapcc_first'] != None:
                mapcc_first = round(dict_clust_by_rotclu[rotclu][cluster]['dictio_result'][phaseset]['mapcc_first'], 2)
            else:
                mapcc_first = -1
            if dict_clust_by_rotclu[rotclu][cluster]['dictio_result'][phaseset]['mapcc_last'] != None:
                mapcc_last = round(dict_clust_by_rotclu[rotclu][cluster]['dictio_result'][phaseset]['mapcc_last'], 2)
            else:
                mapcc_last = -1
            shift_first = dict_clust_by_rotclu[rotclu][cluster]['dictio_result'][phaseset]['shift_first']
            shift_last = dict_clust_by_rotclu[rotclu][cluster]['dictio_result'][phaseset]['shift_last']
            fileforclu.write(
                '%-40s %-10s %-10s %-10s %-10s %-10s %-10s %-10s %-10s %-10s %-10s %-10s\n' % (name, wmpe_first,wmpe_last,
                                                                                           diffwmpe,mapcc_first,
                                                                                           mapcc_last,
                                                                                           shift_first[0],
                                                                                           shift_first[1],
                                                                                           shift_first[2],
                                                                                           shift_last[0],
                                                                                           shift_last[1],
                                                                                           shift_last[2]))
        del (fileforclu)


if mode == 'one_step' or mode.startswith('ens1_frag') or mode == 'one_step_parallel':
    print("\nOne step clustering performed, results can be found at the files "
          "info_clust_raw and info_clust_table, found in the CLUSTERING folder")
    if mode == 'one_step_parallel':
            print('\nOut  of ',n_single_solutions, ' single solutions, ', count_single_global,
                    ' did not merge with any phase set')
            print('The rest of solutions were merged and formed ',count_cluster,' phase clusters ')
    # Generating a pkl file out of the results of a single round of clusterization
    pkl_round_one = open(os.path.join(clust_fold, 'first_round.pkl'), 'w')
    cPickle.dump(dict_clust_by_rotclu, pkl_round_one)
    pkl_round_one.close()
    print('\n A pickled file named first_round.pkl has been written with the clustering output')
    if expansions == True:
        print("\n Starting the expansions of the phase clusters of a single round")
        expansions_folder_phi = os.path.join(clust_fold, 'EXPANSIONS_FROM_PHI')
        al.check_dir_or_make_it(expansions_folder_phi, remove=True)
        list_to_expand_first_round_phi = sorted(list_to_expand_first_round, key=operator.itemgetter(1, 2, 3, 4),
                                                reverse=True)
        list_to_expand_first_round_phi = [os.path.join(clust_fold, ele[0][:-4]) for ele in list_to_expand_first_round]
        al.phase_round_with_shelxe(linea_arg=shelxe_line, lista_clusters=list_to_expand_first_round_phi,
                                   wd=expansions_folder_phi, path_shelxe=shelxe_path, hkl_path=hkl_filename,
                                   ins_path=path_ins, ent_path=ent_filename, fragment_type='phi')

elif mode == 'two_steps':
    # TODO: write different functions to test possible ways of combining at the second round
    if folder_mode:
        topexp=len(dict_clust_by_rotclu["0"].keys())
    final_dict = ALIXE.fishing_round_by_prio_list(dict_first_round_by_rotclu=dict_clust_by_rotclu,
                                                  reference_hkl=hkl_filename, sg_symbol=sg_symbol,
                                                  phstat_version=phstat_version, path_phstat=path_phstat, ncores=topexp,
                                                  clust_fold=clust_fold, path_ins=path_ins, path_best=path_sym,
                                                  cell=cell,resolution=resolution, cycles=cycles,
                                                  tolerance=tolerance_second_round, orisub=orisub, weight=weight,
                                                  ent_path=ent_filename,folder_mode=folder_mode,
                                                  shelxe_line=shelxe_line_alixe,shelxe_path=shelxe_path,
                                                  oricheck=oricheck, mapcc=cc_calc)

    print("\nTwo steps clustering performed, "
          "results can be found at the files info_clust_second_round_raw "
          "and info_clust_second_round_table, found in the CLUSTERING folder")
    if expansions == True:
        list_to_expand_second_round = []
        print('\nStarting the expansions of the clusters from the second round')
        expansions_folder = os.path.join(clust_fold, 'EXPANSIONS')
        al.check_dir_or_make_it(expansions_folder,remove=True)
        for ref in final_dict.keys():
            for key in final_dict[ref].keys():
                if len(final_dict[ref][key].keys()) > 1:
                    print("This cluster ", key, "contains more then one file, we will expand it")
                    list_to_expand_second_round.append(key[:-4])
        al.phase_round_with_shelxe(linea_arg=shelxe_line, lista_clusters=list_to_expand_second_round,
                                   wd=expansions_folder, path_shelxe=shelxe_path, hkl_path=hkl_filename,
                                   ins_path=path_ins, ent_path=ent_filename, fragment_type='phi')
elif mode == "combi":
    print("We are going to combine the results of this first round with the one of ", path_combi)
    for fich in os.listdir(path_combi):
        if fich == "CLUSTERING":
            for fich2 in os.listdir(os.path.join(path_combi, fich)):
                if fich2.endswith(".pkl"):
                    print("Found the pkl file of the first round of ", path_combi)
                    path_combi_clustering = os.path.join(path_combi, "CLUSTERING")
                    back_first_round = open(os.path.join(path_combi_clustering, 'first_round.pkl'), 'rb')
                    dict_round_combi = cPickle.load(back_first_round)
                    back_first_round.close()
    # Can we generate a dictionary with a unique rotation cluster and fool the ALIXE.fishing_round_by_prio_list function?
    new_clust_fold = os.path.join(wd, 'COMBI_CLUSTERING')
    al.check_dir_or_make_it(new_clust_fold,remove=True)
    dict_global = {}
    dict_global['0'] = {}
    for rotclu in dict_round_combi.keys():
        for key in dict_round_combi[rotclu].keys():
            name_file = os.path.split(key)[1]
            new_key = os.path.join(new_clust_fold, name_file)
            os.link(key, new_key)
            dict_global['0'][new_key] = copy.deepcopy(dict_round_combi[rotclu][key])
    for rotclu in dict_clust_by_rotclu.keys():
        for key in dict_clust_by_rotclu[rotclu].keys():
            name_file = os.path.split(key)[1]
            new_key = os.path.join(new_clust_fold, name_file)
            os.link(key, new_key)
            dict_global['0'][new_key] = copy.deepcopy(dict_clust_by_rotclu[rotclu][key])
    # dict_first_round_by_rotclu, reference_hkl, sg_symbol
    final_dict = ALIXE.fishing_round_by_prio_list(dict_first_round_by_rotclu=dict_global, reference_hkl=hkl_filename,
                                                  sg_symbol=sg_symbol, weight=weight,
                                                  phstat_version=phstat_version, path_phstat=path_phstat, ncores=topexp,
                                                  clust_fold=new_clust_fold, path_ins=path_ins, path_best=path_best,
                                                  cell=cell,resolution=resolution, cycles=cycles,
                                                  tolerance=tolerance_second_round, orisub=orisub,
                                                  shelxe_line=shelxe_line_alixe,shelxe_path=shelxe_path)
    if expansions == True:
        list_to_expand_combi_round = []
        print('\nStarting the expansions of the clusters from the combination round')
        expansions_folder = os.path.join(new_clust_fold, 'EXPANSIONS')
        al.check_dir_or_make_it(expansions_folder, remove=True)
        for ref in final_dict.keys():
            for key in final_dict[ref].keys():
                if len(final_dict[ref][key].keys()) > 1:
                    print("This cluster ", key, "contains more then one file, we will expand it")
                    list_to_expand_combi_round.append(key[:-4])
        al.phase_round_with_shelxe(linea_arg=shelxe_line, lista_clusters=list_to_expand_combi_round,
                                   wd=expansions_folder, path_shelxe=shelxe_path, hkl_path=hkl_filename,
                                   ins_path=path_ins, ent_path=ent_filename, fragment_type='phi')

# Print final time and close log file before finishing
new_now=time.time()
final_string = '\nTotal time spent in running autoalixe is '+str((new_now-now))+' seconds , or '+str((new_now-now)/60)+' minutes \n Command line used was '+" ".join(sys.argv)
log_file.write(final_string)
print(final_string)
del log_file
