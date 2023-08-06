# This source code file is a part of SigProfilerTopography
# SigProfilerTopography is a tool included as part of the SigProfiler
# computational framework for comprehensive analysis of mutational
# signatures from next-generation sequencing of cancer genomes.
# SigProfilerTopography provides the downstream data analysis of
# mutations and extracted mutational signatures w.r.t.
# nucleosome occupancy, replication time, strand bias and processivity.
# Copyright (C) 2018 Burcak Otlu

###############################################################################################################
# In this python code, nucleosome occupancy analysis is carried out
#   for subs, indels and dinucs sample based and all samples pooled
#   for all subs signatures with all single point mutations with a certain probability for that signature
#   for all indels signatures with all indels with a certain probability for that signature
#   for all dinucs signatures with all dinucs with a certain probability for that signature
###############################################################################################################

# #############################################################
# current_abs_path = os.path.abspath(os.path.dirname(__file__))
# commonsPath = os.path.join(current_abs_path, '..','commons')
# sys.path.append(commonsPath)
# #############################################################

from SigProfilerTopography.source.commons.TopographyCommons import *
# import pyBigWig
import time
import pyBigWig

##############################################################################################################
#main function
def occupancyAnalysis(computationType,occupancy_type,using_pyBigWig,using_chrBasedArray,sample_based,plusorMinus,chromSizesDict,chromNamesList,outputDir,jobname,numofSimulations,library_file_with_path,library_file_memo,subsSignature2PropertiesListDict,indelsSignature2PropertiesListDict,dinucsSignature2PropertiesListDict):

    print('\n#################################################################################')
    print('--- %s Analysis starts' %(occupancy_type))
    print('--- Computation Type:%s' % (computationType))
    print('--- Occupancy Type:%s' % (occupancy_type))
    print('--- Library file with path: %s\n' %library_file_with_path)

    #Using pyBigWig for BigWig and BigBed files
    #Using Bed files preparing chr based signal array online
    occupancy_analysis(computationType,occupancy_type,using_pyBigWig,using_chrBasedArray,sample_based,plusorMinus,chromSizesDict,chromNamesList,outputDir,jobname,numofSimulations,library_file_with_path,library_file_memo,subsSignature2PropertiesListDict,indelsSignature2PropertiesListDict,dinucsSignature2PropertiesListDict)
    print('--- %s Analysis ends' %(occupancy_type))
    print('#################################################################################\n')
##############################################################################################################



########################################################################################
# November 1, 2019
# Just fill the list
def fillInputList(using_pyBigWig,using_chrBasedArray,outputDir,jobname,chrLong,simNum,chromSizesDict,library_file_with_path,library_file_type,library_file_df,library_file_df_grouped,sample2NumberofSubsDict,sample2NumberofIndelsDict,sample2NumberofDinucsDict,
                      sample2SubsSignature2NumberofMutationsDict,sample2IndelsSignature2NumberofMutationsDict,sample2DinucsSignature2NumberofMutationsDict,
                      subsSignature2PropertiesListDict,indelsSignature2PropertiesListDict,dinucsSignature2PropertiesListDict,plusorMinus,sample_based):


    print('FillInputList: Worker pid %s current_mem_usage %.2f (mb) chrLong:%s simNum:%d' % (str(os.getpid()), memory_usage(),chrLong,simNum))
    inputList=[]

    inputList.append(using_pyBigWig)
    inputList.append(using_chrBasedArray)
    inputList.append(outputDir)
    inputList.append(jobname)
    inputList.append(chrLong)
    inputList.append(simNum)
    inputList.append(chromSizesDict)
    inputList.append(library_file_with_path)
    inputList.append(library_file_type)
    inputList.append(library_file_df)
    inputList.append(library_file_df_grouped)
    inputList.append(sample2NumberofSubsDict)
    inputList.append(sample2NumberofIndelsDict)
    inputList.append(sample2NumberofDinucsDict)
    inputList.append(sample2SubsSignature2NumberofMutationsDict)
    inputList.append(sample2IndelsSignature2NumberofMutationsDict)
    inputList.append(sample2DinucsSignature2NumberofMutationsDict)
    inputList.append(subsSignature2PropertiesListDict)
    inputList.append(indelsSignature2PropertiesListDict)
    inputList.append(dinucsSignature2PropertiesListDict)
    inputList.append(plusorMinus)
    inputList.append(sample_based)
    # print('FillInputList: Worker pid %s maximum memory usage %.2f (mb)' % (str(os.getpid()), current_mem_usage()))
    return inputList
########################################################################################


########################################################################################
#November 26 2019
#Will be used for testing purposes
def test_combined_prepare_chrbased_data_fill_signal_count_arrays(
        using_pyBigWig,using_chrBasedArray,
        outputDir, jobname, chrLong, simNum, chromSizesDict, library_file_with_path,
        library_file_type, library_file_df, library_file_df_grouped,
        sample2NumberofSubsDict, sample2NumberofIndelsDict, sample2NumberofDinucsDict,
        sample2SubsSignature2NumberofMutationsDict, sample2IndelsSignature2NumberofMutationsDict,
        sample2DinucsSignature2NumberofMutationsDict,
        subsSignature2PropertiesListDict, indelsSignature2PropertiesListDict, dinucsSignature2PropertiesListDict,
        plusorMinus, sample_based):

    print('\tWorker pid %s memory_usage in %.2f MB START TEST chrLong:%s simNum:%d' %(str(os.getpid()), memory_usage(), chrLong, simNum))
    # 1st part  Prepare chr based mutations dataframes
    maximum_chrom_size = chromSizesDict[chrLong]

    ##############################################################
    simNum2Type2SignalArrayDict = {}
    simNum2Type2CountArrayDict = {}
    simNum2Sample2Type2SignalArrayDict = {}
    simNum2Sample2Type2CountArrayDict = {}
    ##############################################################

    ##############################################################
    chrBasedSignalArray = None #Will be filled from already existing chrom based files or bed files
    library_file = None #Will be filled by pyBigWig from bigWig or bigBed
    my_upperBound = None
    signal_index = None
    ##############################################################

    #################################################################################################################
    # If library file does not exists there is no library file to use and fill the signal and count arrays
    # Nucleosomes have chrM
    # SinglePointMutations and Indels have chrMT
    chrLong_for_mutations_data = chrLong
    if (chrLong == 'chrM'):
        chrLong_for_mutations_data = 'chrMT'

    chrBased_subs_df = readChrBasedMutationsDF(outputDir, jobname, chrLong_for_mutations_data, SUBS, simNum)
    chrBased_indels_df = readChrBasedMutationsDF(outputDir, jobname, chrLong_for_mutations_data, INDELS, simNum)
    chrBased_dinucs_df = readChrBasedMutationsDF(outputDir, jobname, chrLong_for_mutations_data, DINUCS, simNum)
    print('\tWorker pid %s memory_usage in %.2f MB Check1 TEST Read Signal Array and Dataframes chrLong:%s simNum:%d' % (str(os.getpid()), memory_usage(), chrLong, simNum))
    print('\tWorker pid %s -- signal_array_npy: %f in GB -- subs_df: %f in GB -- indels_df: %f in GB -- dinucs_df: %f in GB -- chrLong:%s simNum:%d' % (
            str(os.getpid()),
            sys.getsizeof(chrBasedSignalArray) / GIGABYTE_IN_BYTES,
            sys.getsizeof(chrBased_subs_df) / GIGABYTE_IN_BYTES,
            sys.getsizeof(chrBased_indels_df) / GIGABYTE_IN_BYTES,
            sys.getsizeof(chrBased_dinucs_df) / GIGABYTE_IN_BYTES,
            chrLong, simNum))
    #################################################################################################################

    #################################################################################################################
    nucleosomeFilenameWoExtension = os.path.splitext(os.path.basename(library_file_with_path))[0]
    signalArrayFilename = '%s_signal_%s.npy' % (chrLong, nucleosomeFilenameWoExtension)
    chrBasedSignalFile = os.path.join(current_abs_path, ONE_DIRECTORY_UP, ONE_DIRECTORY_UP, LIB, NUCLEOSOME, CHRBASED,signalArrayFilename)

    if (using_chrBasedArray and os.path.exists(chrBasedSignalFile)):
        chrBasedSignalArray = np.load(chrBasedSignalFile, mmap_mode='r')
        # For testing purposes
        # chrBasedSignalArray = np.load(chrBasedSignalFile,mmap_mode=None)
        # chrBasedSignalArray = np.random.uniform(low=0.0, high=13.3, size=(maximum_chrom_size,))

    elif (((library_file_type == BED) or (library_file_type == NARROWPEAK)) and (library_file_df is not None) and (os.path.exists(library_file_with_path))):
        chrom_based_library_df = library_file_df_grouped.get_group(chrLong)
        # chrBasedSignalArray and library_file_df  signal column is of type np.float32
        chrBasedSignalArray = np.zeros(maximum_chrom_size, dtype=np.float32)
        # TODO Can we fill chrBasedSignalArray faster?
        # chrom_based_library_df.apply(updateChrBasedSignalArray, chrBasedSignalArray=chrBasedSignalArray, axis=1)
        [fillNumpyArray(start, end, signal, chrBasedSignalArray) for start, end, signal in
         zip(chrom_based_library_df['start'], chrom_based_library_df['end'], chrom_based_library_df['signal'])]

    # Comment below to make it run in windows
    elif (using_pyBigWig):
        if (library_file_type == BIGWIG):
            try:
                library_file = pyBigWig.open(library_file_with_path)
                if chrLong in library_file.chroms():
                    maximum_chrom_size = library_file.chroms()[chrLong]
                # For BigWig Files information in header is correct
                if ('sumData' in library_file.header()) and ('nBasesCovered' in library_file.header()):
                    my_mean = library_file.header()['sumData'] / library_file.header()['nBasesCovered']
                    std_dev = (library_file.header()['sumSquared'] - 2 * my_mean * library_file.header()['sumData'] +
                               library_file.header()['nBasesCovered'] * my_mean * my_mean) ** (0.5) / (
                                          library_file.header()['nBasesCovered'] ** (0.5))
                    # Scientific definition of outlier
                    my_upperBound = std_dev * 3
                else:
                    # Undefined
                    my_upperBound = np.iinfo(np.int16).max
            except:
                print('Exception %s' %library_file_with_path)

        elif (library_file_type == BIGBED):
            try:
                library_file = pyBigWig.open(library_file_with_path)
                if BED_6PLUS4 in str(library_file.SQL()):
                    signal_index = 3
                elif BED_9PLUS2 in str(library_file.SQL()):
                    signal_index = 7
                if chrLong in library_file.chroms():
                    # For BigBed Files information in header is not meaningful
                    maximum_chrom_size = library_file.chroms()[chrLong]
                    my_mean = np.mean([float(entry[2].split('\t')[signal_index]) for entry in
                                       library_file.entries(chrLong, 0, maximum_chrom_size)])
                    # Not scientific definition of outlier
                    my_upperBound = my_mean * 10
                else:
                    # Undefined
                    my_upperBound = np.iinfo(np.int16).max
            except:
                print('Exception %s' %library_file_with_path)

    #################################################################################################################

    #################################################################################################################
    if ((((library_file_type == BIGWIG) or (library_file_type == BIGBED)) and (library_file is not None) and (chrLong in library_file.chroms()))
            or (chrBasedSignalArray is not None)):
        ######################################################## #######################
        ################### Fill signal and count array starts ########################
        ###############################################################################

        print('\tWorker pid %s memory_usage in %.2f MB Check2_1 TEST Dinucs Start chrLong:%s simNum:%d' % (str(os.getpid()), memory_usage(), chrLong, simNum))
        # Fill for dinucs
        if ((chrBased_dinucs_df is not None) and (not chrBased_dinucs_df.empty)):
            df_columns = list(chrBased_dinucs_df.columns.values)
            [fillSignalArrayAndCountArrayForMutationsSimulationsIntegrated_using_pyBigWig_using_list_comp(
                row,
                chrLong,
                library_file,
                chrBasedSignalArray,
                library_file_type,
                signal_index,
                my_upperBound,
                maximum_chrom_size,
                sample2NumberofDinucsDict,
                sample2DinucsSignature2NumberofMutationsDict,
                simNum2Type2SignalArrayDict,
                simNum2Type2CountArrayDict,
                simNum2Sample2Type2SignalArrayDict,
                simNum2Sample2Type2CountArrayDict,
                dinucsSignature2PropertiesListDict,
                AGGREGATEDDINUCS,
                plusorMinus,
                sample_based,
                df_columns) for row in chrBased_dinucs_df[df_columns].values]
        print('\tWorker pid %s memory_usage in %.2f MB Check2_2 TEST Dinucs End chrLong:%s simNum:%d' % (str(os.getpid()), memory_usage(), chrLong, simNum))

        print('\tWorker pid %s memory_usage in %.2f MB Check3_1 TEST Indels Start chrLong:%s simNum:%d' % (str(os.getpid()), memory_usage(), chrLong, simNum))
        # Fill for indels
        if ((chrBased_indels_df is not None) and (not chrBased_indels_df.empty)):
            df_columns = list(chrBased_indels_df.columns.values)
            [fillSignalArrayAndCountArrayForMutationsSimulationsIntegrated_using_pyBigWig_using_list_comp(
                row,
                chrLong,
                library_file,
                chrBasedSignalArray,
                library_file_type,
                signal_index,
                my_upperBound,
                maximum_chrom_size,
                sample2NumberofIndelsDict,
                sample2IndelsSignature2NumberofMutationsDict,
                simNum2Type2SignalArrayDict,
                simNum2Type2CountArrayDict,
                simNum2Sample2Type2SignalArrayDict,
                simNum2Sample2Type2CountArrayDict,
                indelsSignature2PropertiesListDict,
                AGGREGATEDINDELS,
                plusorMinus,
                sample_based,
                df_columns) for row in chrBased_indels_df[df_columns].values]
        print('\tWorker pid %s memory_usage in %.2f MB Check3_2 TEST Indels End chrLong:%s simNum:%d' % (str(os.getpid()), memory_usage(), chrLong, simNum))

        print('\tWorker pid %s memory_usage in %.2f MB Check4_1 TEST Subs Start chrLong:%s simNum:%d' % (str(os.getpid()), memory_usage(), chrLong, simNum))
        # Fill for single point mutations
        if ((chrBased_subs_df is not None) and (not chrBased_subs_df.empty)):
            list_of_dfs = None
            df_columns = list(chrBased_subs_df.columns.values)

            # 1 MB 1024*1024= 1048576 B
            size_in_mbs = sys.getsizeof(chrBased_subs_df) / 1048576
            print('\tWorker pid %s ##################### subs_df: %f in MB chrLong:%s simNum:%d' % (str(os.getpid()),size_in_mbs, chrLong, simNum))
            max_size_in_mbs = 50
            if (size_in_mbs > max_size_in_mbs):
                numberofSplits = math.ceil(size_in_mbs / max_size_in_mbs)
                print('\tWorker pid %s numberofSplits: %d chrLong:%s simNum:%d' % (str(os.getpid()),numberofSplits, chrLong, simNum))
                list_of_dfs = np.array_split(chrBased_subs_df, numberofSplits)

            # This is 3X-4X faster with almost same memory usage
            start_time = time.time()

            if list_of_dfs is not None:
                for part_index, part_df in enumerate(list_of_dfs, 1):
                    [fillSignalArrayAndCountArrayForMutationsSimulationsIntegrated_using_pyBigWig_using_list_comp(
                        row,
                        chrLong,
                        library_file,
                        chrBasedSignalArray,
                        library_file_type,
                        signal_index,
                        my_upperBound,
                        maximum_chrom_size,
                        sample2NumberofSubsDict,
                        sample2SubsSignature2NumberofMutationsDict,
                        simNum2Type2SignalArrayDict,
                        simNum2Type2CountArrayDict,
                        simNum2Sample2Type2SignalArrayDict,
                        simNum2Sample2Type2CountArrayDict,
                        subsSignature2PropertiesListDict,
                        AGGREGATEDSUBSTITUTIONS,
                        plusorMinus,
                        sample_based,
                        df_columns) for row in part_df[df_columns].values]
            else:
                [fillSignalArrayAndCountArrayForMutationsSimulationsIntegrated_using_pyBigWig_using_list_comp(
                    row,
                    chrLong,
                    library_file,
                    chrBasedSignalArray,
                    library_file_type,
                    signal_index,
                    my_upperBound,
                    maximum_chrom_size,
                    sample2NumberofSubsDict,
                    sample2SubsSignature2NumberofMutationsDict,
                    simNum2Type2SignalArrayDict,
                    simNum2Type2CountArrayDict,
                    simNum2Sample2Type2SignalArrayDict,
                    simNum2Sample2Type2CountArrayDict,
                    subsSignature2PropertiesListDict,
                    AGGREGATEDSUBSTITUTIONS,
                    plusorMinus,
                    sample_based,
                    df_columns) for row in chrBased_subs_df[df_columns].values]

        print('\tWorker pid %s memory_usage in %.2f MB Check4_2 TEST Subs End chrLong:%s simNum:%d' % (str(os.getpid()), memory_usage(), chrLong, simNum))
        ###############################################################################
        ################### Fill signal and count array ends ##########################
        ###############################################################################

    if (library_file is not None):
        library_file.close()

    print('\tWorker pid %s memory_usage in %.2f MB END TEST  chrLong:%s simNum:%d' % (str(os.getpid()), memory_usage(), chrLong, simNum))
    print('----->\tWorker pid %s took %f seconds chrLong:%s simNum:%d' % (str(os.getpid()), (time.time() - start_time), chrLong, simNum))
    ###############################################################################
    ################### Return  starts ############################################
    ###############################################################################
    # Initialzie the list, you will return this list
    SignalArrayAndCountArrayList = []
    SignalArrayAndCountArrayList.append(simNum2Type2SignalArrayDict)
    SignalArrayAndCountArrayList.append(simNum2Type2CountArrayDict)
    SignalArrayAndCountArrayList.append(simNum2Sample2Type2SignalArrayDict)
    SignalArrayAndCountArrayList.append(simNum2Sample2Type2CountArrayDict)

    return SignalArrayAndCountArrayList
########################################################################################




########################################################################################
# November 21, 2019
# Will be used for normal runs
def combined_prepare_chrbased_data_fill_signal_count_arrays(
        using_pyBigWig,using_chrBasedArray,
        outputDir, jobname, chrLong, simNum, chromSizesDict, library_file_with_path,
        library_file_type, library_file_df, library_file_df_grouped,
        sample2NumberofSubsDict, sample2NumberofIndelsDict, sample2NumberofDinucsDict,
        sample2SubsSignature2NumberofMutationsDict, sample2IndelsSignature2NumberofMutationsDict,
        sample2DinucsSignature2NumberofMutationsDict,
        subsSignature2PropertiesListDict, indelsSignature2PropertiesListDict, dinucsSignature2PropertiesListDict,
        plusorMinus, sample_based):

    # print('\tWorker pid %s memory_usage in %.2f MB START TEST chrLong:%s simNum:%d' %(str(os.getpid()), memory_usage(), chrLong, simNum))
    # 1st part  Prepare chr based mutations dataframes
    maximum_chrom_size = chromSizesDict[chrLong]

    ##############################################################
    simNum2Type2SignalArrayDict = {}
    simNum2Type2CountArrayDict = {}
    simNum2Sample2Type2SignalArrayDict = {}
    simNum2Sample2Type2CountArrayDict = {}
    ##############################################################

    ##############################################################
    chrBasedSignalArray = None #Will be filled from already existing chrom based files or bed files
    library_file = None #Will be filled by pyBigWig from bigWig or bigBed
    my_upperBound = None
    signal_index = None
    ##############################################################

    #################################################################################################################
    # If library file does not exists there is no library file to use and fill the signal and count arrays
    # Nucleosomes have chrM
    # SinglePointMutations and Indels have chrMT
    chrLong_for_mutations_data = chrLong
    if (chrLong == 'chrM'):
        chrLong_for_mutations_data = 'chrMT'

    chrBased_subs_df = readChrBasedMutationsDF(outputDir, jobname, chrLong_for_mutations_data, SUBS, simNum)
    chrBased_indels_df = readChrBasedMutationsDF(outputDir, jobname, chrLong_for_mutations_data, INDELS, simNum)
    chrBased_dinucs_df = readChrBasedMutationsDF(outputDir, jobname, chrLong_for_mutations_data, DINUCS, simNum)
    # print('\tWorker pid %s memory_usage in %.2f MB Check1 TEST Read Signal Array and Dataframes chrLong:%s simNum:%d' % (str(os.getpid()), memory_usage(), chrLong, simNum))
    # print('\tWorker pid %s -- signal_array_npy: %f in GB -- subs_df: %f in GB -- indels_df: %f in GB -- dinucs_df: %f in GB -- chrLong:%s simNum:%d' % (
    #         str(os.getpid()),
    #         sys.getsizeof(chrBasedSignalArray) / GIGABYTE_IN_BYTES,
    #         sys.getsizeof(chrBased_subs_df) / GIGABYTE_IN_BYTES,
    #         sys.getsizeof(chrBased_indels_df) / GIGABYTE_IN_BYTES,
    #         sys.getsizeof(chrBased_dinucs_df) / GIGABYTE_IN_BYTES,
    #         chrLong, simNum))
    #################################################################################################################

    #################################################################################################################
    nucleosomeFilenameWoExtension = os.path.splitext(os.path.basename(library_file_with_path))[0]
    signalArrayFilename = '%s_signal_%s.npy' % (chrLong, nucleosomeFilenameWoExtension)
    chrBasedSignalFile = os.path.join(current_abs_path, ONE_DIRECTORY_UP, ONE_DIRECTORY_UP, LIB, NUCLEOSOME, CHRBASED,signalArrayFilename)

    if (using_chrBasedArray and os.path.exists(chrBasedSignalFile)):
        chrBasedSignalArray = np.load(chrBasedSignalFile, mmap_mode='r')
        # For testing purposes
        # chrBasedSignalArray = np.load(chrBasedSignalFile,mmap_mode=None)
        # chrBasedSignalArray = np.random.uniform(low=0.0, high=13.3, size=(maximum_chrom_size,))

    elif (((library_file_type == BED) or (library_file_type == NARROWPEAK)) and (library_file_df is not None) and (os.path.exists(library_file_with_path))):
        chrom_based_library_df = library_file_df_grouped.get_group(chrLong)
        # chrBasedSignalArray and library_file_df  signal column is of type np.float32
        chrBasedSignalArray = np.zeros(maximum_chrom_size, dtype=np.float32)
        # TODO Can we fill chrBasedSignalArray faster?
        # chrom_based_library_df.apply(updateChrBasedSignalArray, chrBasedSignalArray=chrBasedSignalArray, axis=1)
        [fillNumpyArray(start, end, signal, chrBasedSignalArray) for start, end, signal in
         zip(chrom_based_library_df['start'], chrom_based_library_df['end'], chrom_based_library_df['signal'])]

    # Comment below to make it run in windows
    elif (using_pyBigWig):
        if (library_file_type == BIGWIG):
            try:
                library_file = pyBigWig.open(library_file_with_path)
                if chrLong in library_file.chroms():
                    maximum_chrom_size = library_file.chroms()[chrLong]
                # For BigWig Files information in header is correct
                if ('sumData' in library_file.header()) and ('nBasesCovered' in library_file.header()):
                    my_mean = library_file.header()['sumData'] / library_file.header()['nBasesCovered']
                    std_dev = (library_file.header()['sumSquared'] - 2 * my_mean * library_file.header()['sumData'] +
                               library_file.header()['nBasesCovered'] * my_mean * my_mean) ** (0.5) / (
                                          library_file.header()['nBasesCovered'] ** (0.5))
                    # Scientific definition of outlier
                    my_upperBound = std_dev * 3
                else:
                    # Undefined
                    my_upperBound = np.iinfo(np.int16).max
            except:
                print('Exception %s' %library_file_with_path)

        elif (library_file_type == BIGBED):
            try:
                library_file = pyBigWig.open(library_file_with_path)
                if BED_6PLUS4 in str(library_file.SQL()):
                    signal_index = 3
                elif BED_9PLUS2 in str(library_file.SQL()):
                    signal_index = 7
                if chrLong in library_file.chroms():
                    # For BigBed Files information in header is not meaningful
                    maximum_chrom_size = library_file.chroms()[chrLong]
                    my_mean = np.mean([float(entry[2].split('\t')[signal_index]) for entry in
                                       library_file.entries(chrLong, 0, maximum_chrom_size)])
                    # Not scientific definition of outlier
                    my_upperBound = my_mean * 10
                else:
                    # Undefined
                    my_upperBound = np.iinfo(np.int16).max
            except:
                print('Exception %s' %library_file_with_path)

    #################################################################################################################

    #################################################################################################################
    if ((((library_file_type == BIGWIG) or (library_file_type == BIGBED)) and (library_file is not None) and (chrLong in library_file.chroms()))
            or (chrBasedSignalArray is not None)):
        ######################################################## #######################
        ################### Fill signal and count array starts ########################
        ###############################################################################

        # print('\tWorker pid %s memory_usage in %.2f MB Check2_1 TEST Dinucs Start chrLong:%s simNum:%d' % (str(os.getpid()), memory_usage(), chrLong, simNum))
        # Fill for dinucs
        if ((chrBased_dinucs_df is not None) and (not chrBased_dinucs_df.empty)):
            df_columns = list(chrBased_dinucs_df.columns.values)
            [fillSignalArrayAndCountArrayForMutationsSimulationsIntegrated_using_pyBigWig_using_list_comp(
                row,
                chrLong,
                library_file,
                chrBasedSignalArray,
                library_file_type,
                signal_index,
                my_upperBound,
                maximum_chrom_size,
                sample2NumberofDinucsDict,
                sample2DinucsSignature2NumberofMutationsDict,
                simNum2Type2SignalArrayDict,
                simNum2Type2CountArrayDict,
                simNum2Sample2Type2SignalArrayDict,
                simNum2Sample2Type2CountArrayDict,
                dinucsSignature2PropertiesListDict,
                AGGREGATEDDINUCS,
                plusorMinus,
                sample_based,
                df_columns) for row in chrBased_dinucs_df[df_columns].values]
        # print('\tWorker pid %s memory_usage in %.2f MB Check2_2 TEST Dinucs End chrLong:%s simNum:%d' % (str(os.getpid()), memory_usage(), chrLong, simNum))

        # print('\tWorker pid %s memory_usage in %.2f MB Check3_1 TEST Indels Start chrLong:%s simNum:%d' % (str(os.getpid()), memory_usage(), chrLong, simNum))
        # Fill for indels
        if ((chrBased_indels_df is not None) and (not chrBased_indels_df.empty)):
            df_columns = list(chrBased_indels_df.columns.values)
            [fillSignalArrayAndCountArrayForMutationsSimulationsIntegrated_using_pyBigWig_using_list_comp(
                row,
                chrLong,
                library_file,
                chrBasedSignalArray,
                library_file_type,
                signal_index,
                my_upperBound,
                maximum_chrom_size,
                sample2NumberofIndelsDict,
                sample2IndelsSignature2NumberofMutationsDict,
                simNum2Type2SignalArrayDict,
                simNum2Type2CountArrayDict,
                simNum2Sample2Type2SignalArrayDict,
                simNum2Sample2Type2CountArrayDict,
                indelsSignature2PropertiesListDict,
                AGGREGATEDINDELS,
                plusorMinus,
                sample_based,
                df_columns) for row in chrBased_indels_df[df_columns].values]
        # print('\tWorker pid %s memory_usage in %.2f MB Check3_2 TEST Indels End chrLong:%s simNum:%d' % (str(os.getpid()), memory_usage(), chrLong, simNum))

        # print('\tWorker pid %s memory_usage in %.2f MB Check4_1 TEST Subs Start chrLong:%s simNum:%d' % (str(os.getpid()), memory_usage(), chrLong, simNum))
        # Fill for single point mutations
        if ((chrBased_subs_df is not None) and (not chrBased_subs_df.empty)):
            list_of_dfs = None
            df_columns = list(chrBased_subs_df.columns.values)

            # 1 MB 1024*1024= 1048576 B
            size_in_mbs = sys.getsizeof(chrBased_subs_df) / 1048576
            # print('\tWorker pid %s ##################### subs_df: %f in MB chrLong:%s simNum:%d' % (str(os.getpid()),size_in_mbs, chrLong, simNum))
            max_size_in_mbs = 50
            if (size_in_mbs > max_size_in_mbs):
                numberofSplits = math.ceil(size_in_mbs / max_size_in_mbs)
                # print('\tWorker pid %s numberofSplits: %d chrLong:%s simNum:%d' % (str(os.getpid()),numberofSplits, chrLong, simNum))
                list_of_dfs = np.array_split(chrBased_subs_df, numberofSplits)

            # This is 3X-4X faster with almost same memory usage
            start_time = time.time()

            if list_of_dfs is not None:
                for part_index, part_df in enumerate(list_of_dfs, 1):
                    [fillSignalArrayAndCountArrayForMutationsSimulationsIntegrated_using_pyBigWig_using_list_comp(
                        row,
                        chrLong,
                        library_file,
                        chrBasedSignalArray,
                        library_file_type,
                        signal_index,
                        my_upperBound,
                        maximum_chrom_size,
                        sample2NumberofSubsDict,
                        sample2SubsSignature2NumberofMutationsDict,
                        simNum2Type2SignalArrayDict,
                        simNum2Type2CountArrayDict,
                        simNum2Sample2Type2SignalArrayDict,
                        simNum2Sample2Type2CountArrayDict,
                        subsSignature2PropertiesListDict,
                        AGGREGATEDSUBSTITUTIONS,
                        plusorMinus,
                        sample_based,
                        df_columns) for row in part_df[df_columns].values]
            else:
                [fillSignalArrayAndCountArrayForMutationsSimulationsIntegrated_using_pyBigWig_using_list_comp(
                    row,
                    chrLong,
                    library_file,
                    chrBasedSignalArray,
                    library_file_type,
                    signal_index,
                    my_upperBound,
                    maximum_chrom_size,
                    sample2NumberofSubsDict,
                    sample2SubsSignature2NumberofMutationsDict,
                    simNum2Type2SignalArrayDict,
                    simNum2Type2CountArrayDict,
                    simNum2Sample2Type2SignalArrayDict,
                    simNum2Sample2Type2CountArrayDict,
                    subsSignature2PropertiesListDict,
                    AGGREGATEDSUBSTITUTIONS,
                    plusorMinus,
                    sample_based,
                    df_columns) for row in chrBased_subs_df[df_columns].values]

        # print('\tWorker pid %s memory_usage in %.2f MB Check4_2 TEST Subs End chrLong:%s simNum:%d' % (str(os.getpid()), memory_usage(), chrLong, simNum))
        ###############################################################################
        ################### Fill signal and count array ends ##########################
        ###############################################################################

    if (library_file is not None):
        library_file.close()

    # print('\tWorker pid %s memory_usage in %.2f MB END TEST  chrLong:%s simNum:%d' % (str(os.getpid()), memory_usage(), chrLong, simNum))
    # print('----->\tWorker pid %s took %f seconds chrLong:%s simNum:%d' % (str(os.getpid()), (time.time() - start_time), chrLong, simNum))
    ###############################################################################
    ################### Return  starts ############################################
    ###############################################################################
    # Initialzie the list, you will return this list
    SignalArrayAndCountArrayList = []
    SignalArrayAndCountArrayList.append(simNum2Type2SignalArrayDict)
    SignalArrayAndCountArrayList.append(simNum2Type2CountArrayDict)
    SignalArrayAndCountArrayList.append(simNum2Sample2Type2SignalArrayDict)
    SignalArrayAndCountArrayList.append(simNum2Sample2Type2CountArrayDict)

    return SignalArrayAndCountArrayList
########################################################################################


########################################################################################
# November 1, 2019
def combined_prepare_chrbased_data_fill_signal_count_arrays_using_inputList(inputList):
    using_pyBigWig=inputList[0]
    using_chrBasedArray=inputList[1]
    outputDir=inputList[2]
    jobname=inputList[3]
    chrLong=inputList[4]
    simNum=inputList[5]
    chromSizesDict=inputList[6]
    library_file_with_path=inputList[7]
    library_file_type=inputList[8]
    library_file_df=inputList[9]
    library_file_df_grouped=inputList[10]
    sample2NumberofSubsDict=inputList[11]
    sample2NumberofIndelsDict=inputList[12]
    sample2NumberofDinucsDict=inputList[13]
    sample2SubsSignature2NumberofMutationsDict=inputList[14]
    sample2IndelsSignature2NumberofMutationsDict=inputList[15]
    sample2DinucsSignature2NumberofMutationsDict=inputList[16]
    subsSignature2PropertiesListDict=inputList[17]
    indelsSignature2PropertiesListDict=inputList[18]
    dinucsSignature2PropertiesListDict=inputList[19]
    plusorMinus=inputList[20]
    sample_based=inputList[21]

    return combined_prepare_chrbased_data_fill_signal_count_arrays(using_pyBigWig,using_chrBasedArray,outputDir, jobname, chrLong, simNum, chromSizesDict, library_file_with_path,
                                        library_file_type, library_file_df, library_file_df_grouped,
                                        sample2NumberofSubsDict, sample2NumberofIndelsDict, sample2NumberofDinucsDict,
                                        sample2SubsSignature2NumberofMutationsDict, sample2IndelsSignature2NumberofMutationsDict,sample2DinucsSignature2NumberofMutationsDict,
                                        subsSignature2PropertiesListDict, indelsSignature2PropertiesListDict,dinucsSignature2PropertiesListDict,
                                        plusorMinus, sample_based)
########################################################################################


########################################################################################
#Using pyBigWig for bigBed and bigWig files starts
#Using bed files prepared on the fly starts
def occupancy_analysis(computation_type,
                        occupancy_type,
                        using_pyBigWig,
                        using_chrBasedArray,
                        sample_based,
                        plusorMinus,
                        chromSizesDict,
                        chromNamesList,
                        outputDir,
                        jobname,
                        numofSimulations,
                        library_file_with_path,
                        library_file_memo,
                        subsSignature2PropertiesListDict,
                        indelsSignature2PropertiesListDict,
                        dinucsSignature2PropertiesListDict):

    if sample_based:
        ##########################################################################
        sample2NumberofSubsDict = getSample2NumberofSubsDict(outputDir,jobname)
        sample2NumberofIndelsDict = getSample2NumberofIndelsDict(outputDir,jobname)
        sample2NumberofDinucsDict = getDictionary(outputDir,jobname, Sample2NumberofDinucsDictFilename)

        sample2SubsSignature2NumberofMutationsDict = getSample2SubsSignature2NumberofMutationsDict(outputDir,jobname)
        sample2IndelsSignature2NumberofMutationsDict = getSample2IndelsSignature2NumberofMutationsDict(outputDir,jobname)
        sample2DinucsSignature2NumberofMutationsDict = getDictionary(outputDir, jobname,Sample2DinucsSignature2NumberofMutationsDictFilename)
        ##########################################################################
    else:
        ##########################################################################
        sample2NumberofSubsDict = {}
        sample2NumberofIndelsDict = {}
        sample2NumberofDinucsDict = {}

        sample2SubsSignature2NumberofMutationsDict ={}
        sample2IndelsSignature2NumberofMutationsDict = {}
        sample2DinucsSignature2NumberofMutationsDict = {}
        ##########################################################################

    ##########################################################################
    # If chunksize is 1, maxtasksperchild=x will call the function x times in each process,
    # but if chunksize is y, it will call the function x*y times in each process.
    # Setting maxtaskperchild to 1 would restart each process in your pool after it processed a single task, which is the most aggressive setting you could use to free any leaked resources.
    numofProcesses = multiprocessing.cpu_count()
    # pool = multiprocessing.Pool(numofProcesses, maxtasksperchild=1)
    ##########################################################################

    simNum2Type2AccumulatedSignalArrayDict = {}
    simNum2Type2AccumulatedCountArrayDict = {}
    simNum2Sample2Type2AccumulatedSignalArrayDict = {}
    simNum2Sample2Type2AccumulatedCountArrayDict = {}

    ##############################################################
    #What is the type of the signal_file_with_path?
    #If it is a bed file read signal_file_with_path here
    file_extension = os.path.basename(library_file_with_path).split('.')[-1]

    #If file type is bigwig or bigbed set the library_file_type only
    #If file type is bed or narrowpeak read the files and just set library_file_df and library_file_df_grouped
    library_file_df=None
    library_file_df_grouped=None

    if ((file_extension.lower()=='bigwig') or (file_extension.lower()=='bw')):
        library_file_type=BIGWIG
    elif ((file_extension.lower()=='bigbed') or (file_extension.lower()=='bb')):
        library_file_type=BIGBED
    elif (file_extension.lower()=='bed'):
        library_file_type=BED
        library_file_df=readFileInBEDFormat(library_file_with_path)
        library_file_df_grouped=library_file_df.groupby(chrom)
    elif (file_extension.lower()=='wig'):
        library_file_type=WIG
    elif (file_extension.lower()=='narrowpeak'):
        library_file_type = NARROWPEAK
        library_file_df = readFileInNarrowPeakFormat(library_file_with_path)
        library_file_df_grouped = library_file_df.groupby(chrom)
    else:
        library_file_type=LIBRARY_FILE_TYPE_OTHER
    ##############################################################

    ###################################################################################
    ##################  USING IMAP UNORDERED starts ###################################
    ###################################################################################
    if (computation_type==USING_IMAP_UNORDERED):

        #original
        sim_nums = range(0, numofSimulations+1)
        sim_num_chr_tuples=((sim_num,chrLong) for sim_num in sim_nums for chrLong in chromNamesList)

        # test
        # sim_nums = range(0,10)
        # chromNamesList=['chr1']
        # sim_num_chr_tuples=((sim_num,chrLong) for sim_num in sim_nums for chrLong in chromNamesList)

        #on tscc-11-9 all works, on tscc-11-17 it does not work
        pool = multiprocessing.Pool(numofProcesses)

        # works in laptop, works in login node in tscc, submits each task to different process, but not hpc on tscc
        # pool = multiprocessing.Pool(numofProcesses, maxtasksperchild=1000)

        # This worked. Sends each job to a new process. Works for laptop, login node,  tscc hpc
        # pool = multiprocessing.Pool(numofProcesses,maxtasksperchild=1)

        #imap uses iterable as input
        # Note that map may cause high memory usage for very long iterables.
        # Consider using imap() or imap_unordered() with explicit chunksize option for better efficiency.
        # This method chops the iterable into a number of chunks which it submits to the process pool as separate tasks.
        # The (approximate) size of these chunks can be specified by setting chunksize to a positive integer.
        # default chunksize=1

        for simulatonBased_SignalArrayAndCountArrayList in pool.imap_unordered(combined_prepare_chrbased_data_fill_signal_count_arrays_using_inputList, (fillInputList(using_pyBigWig,using_chrBasedArray,outputDir,jobname,chrLong,simNum,chromSizesDict,library_file_with_path,library_file_type,library_file_df,library_file_df_grouped,
                                                            sample2NumberofSubsDict,sample2NumberofIndelsDict,sample2NumberofDinucsDict,sample2SubsSignature2NumberofMutationsDict,sample2IndelsSignature2NumberofMutationsDict,sample2DinucsSignature2NumberofMutationsDict,
                                                            subsSignature2PropertiesListDict,indelsSignature2PropertiesListDict,dinucsSignature2PropertiesListDict,plusorMinus,sample_based) for simNum,chrLong in sim_num_chr_tuples),chunksize=1):

                simNum2Type2SignalArrayDict = simulatonBased_SignalArrayAndCountArrayList[0]
                simNum2Type2CountArrayDict = simulatonBased_SignalArrayAndCountArrayList[1]
                simNum2Sample2Type2SignalArrayDict = simulatonBased_SignalArrayAndCountArrayList[2]
                simNum2Sample2Type2CountArrayDict = simulatonBased_SignalArrayAndCountArrayList[3]

                keys = simNum2Type2SignalArrayDict.keys()
                print('Accumulate: Worker pid %s current_mem_usage %.2f (mb) simNum:%s' % (str(os.getpid()),memory_usage(),keys))

                accumulateSimulationBasedTypeBasedArrays(simNum2Type2AccumulatedSignalArrayDict, simNum2Type2SignalArrayDict)
                accumulateSimulationBasedTypeBasedArrays(simNum2Type2AccumulatedCountArrayDict, simNum2Type2CountArrayDict)
                accumulateSimulationBasedSampleBasedTypeBasedArrays(simNum2Sample2Type2AccumulatedSignalArrayDict,simNum2Sample2Type2SignalArrayDict)
                accumulateSimulationBasedSampleBasedTypeBasedArrays(simNum2Sample2Type2AccumulatedCountArrayDict,simNum2Sample2Type2CountArrayDict)

        ################################
        pool.close()
        pool.join()
        ################################

    ###################################################################################
    ##################  USING IMAP UNORDERED ends #####################################
    ###################################################################################

    ###################################################################################
    ##################  USING APPLY ASYNC starts ######################################
    ###################################################################################
    elif (computation_type == USING_APPLY_ASYNC):

        sim_nums = range(0, numofSimulations+1)
        sim_num_chr_tuples=((sim_num,chrLong) for sim_num in sim_nums for chrLong in chromNamesList)

        pool = multiprocessing.Pool(numofProcesses)

        #########################################################################################
        def accumulate_apply_async_result(simulatonBased_SignalArrayAndCountArrayList):
            simNum2Type2SignalArrayDict = simulatonBased_SignalArrayAndCountArrayList[0]
            simNum2Type2CountArrayDict = simulatonBased_SignalArrayAndCountArrayList[1]
            simNum2Sample2Type2SignalArrayDict = simulatonBased_SignalArrayAndCountArrayList[2]
            simNum2Sample2Type2CountArrayDict = simulatonBased_SignalArrayAndCountArrayList[3]

            accumulateSimulationBasedTypeBasedArrays(simNum2Type2AccumulatedSignalArrayDict,simNum2Type2SignalArrayDict)
            accumulateSimulationBasedTypeBasedArrays(simNum2Type2AccumulatedCountArrayDict, simNum2Type2CountArrayDict)
            accumulateSimulationBasedSampleBasedTypeBasedArrays(simNum2Sample2Type2AccumulatedSignalArrayDict,simNum2Sample2Type2SignalArrayDict)
            accumulateSimulationBasedSampleBasedTypeBasedArrays(simNum2Sample2Type2AccumulatedCountArrayDict,simNum2Sample2Type2CountArrayDict)
        #########################################################################################

        for simNum, chrLong in sim_num_chr_tuples:
            pool.apply_async(combined_prepare_chrbased_data_fill_signal_count_arrays, (using_pyBigWig,using_chrBasedArray,outputDir, jobname, chrLong, simNum, chromSizesDict, library_file_with_path,
                          library_file_type, library_file_df, library_file_df_grouped,
                          sample2NumberofSubsDict, sample2NumberofIndelsDict, sample2NumberofDinucsDict,
                          sample2SubsSignature2NumberofMutationsDict, sample2IndelsSignature2NumberofMutationsDict,
                          sample2DinucsSignature2NumberofMutationsDict,
                          subsSignature2PropertiesListDict, indelsSignature2PropertiesListDict,
                          dinucsSignature2PropertiesListDict, plusorMinus, sample_based,), callback=accumulate_apply_async_result)

        pool.close()
        pool.join()

    ###################################################################################
    ##################  USING APPLY ASYNC ends ########################################
    ###################################################################################

    ###################################################################################
    ##################  USING TEST APPLY ASYNC starts #################################
    ###################################################################################
    elif (computation_type == USING_TEST_APPLY_ASYNC):

        sim_nums = range(0, numofSimulations+1)
        sim_num_chr_tuples=((sim_num,chrLong) for sim_num in sim_nums for chrLong in chromNamesList)

        pool = multiprocessing.Pool(numofProcesses)

        #########################################################################################
        def accumulate_apply_async_result(simulatonBased_SignalArrayAndCountArrayList):
            simNum2Type2SignalArrayDict = simulatonBased_SignalArrayAndCountArrayList[0]
            simNum2Type2CountArrayDict = simulatonBased_SignalArrayAndCountArrayList[1]
            simNum2Sample2Type2SignalArrayDict = simulatonBased_SignalArrayAndCountArrayList[2]
            simNum2Sample2Type2CountArrayDict = simulatonBased_SignalArrayAndCountArrayList[3]

            keys = simNum2Type2SignalArrayDict.keys()
            print('Worker pid %s memory_usage %.2f MB ACCUMULATE simNum:%s' % (str(os.getpid()), memory_usage(), keys))

            accumulateSimulationBasedTypeBasedArrays(simNum2Type2AccumulatedSignalArrayDict,simNum2Type2SignalArrayDict)
            accumulateSimulationBasedTypeBasedArrays(simNum2Type2AccumulatedCountArrayDict, simNum2Type2CountArrayDict)
            accumulateSimulationBasedSampleBasedTypeBasedArrays(simNum2Sample2Type2AccumulatedSignalArrayDict,simNum2Sample2Type2SignalArrayDict)
            accumulateSimulationBasedSampleBasedTypeBasedArrays(simNum2Sample2Type2AccumulatedCountArrayDict,simNum2Sample2Type2CountArrayDict)
        #########################################################################################

        for simNum, chrLong in sim_num_chr_tuples:
            # Accumulation
            pool.apply_async(test_combined_prepare_chrbased_data_fill_signal_count_arrays, (using_pyBigWig,using_chrBasedArray,outputDir, jobname, chrLong, simNum, chromSizesDict, library_file_with_path,
                          library_file_type, library_file_df, library_file_df_grouped,
                          sample2NumberofSubsDict, sample2NumberofIndelsDict, sample2NumberofDinucsDict,
                          sample2SubsSignature2NumberofMutationsDict, sample2IndelsSignature2NumberofMutationsDict,
                          sample2DinucsSignature2NumberofMutationsDict,
                          subsSignature2PropertiesListDict, indelsSignature2PropertiesListDict,
                          dinucsSignature2PropertiesListDict, plusorMinus, sample_based,), callback=accumulate_apply_async_result)


        pool.close()
        pool.join()

    ###################################################################################
    ##################  USING TEST APPLY ASYNC starts #################################
    ###################################################################################

    ###################################################################################
    ##########  USING MAP Simulations Sequential Chromosomes Parallel starts ##########
    ###################################################################################
    elif (computation_type == SIMULATIONS_SEQUENTIAL_CHROMOSOMES_PARALLEL_USING_MAP):
        pool = multiprocessing.Pool(numofProcesses, maxtasksperchild=1000)

        ##############################################################################
        for simNum in range(0, numofSimulations + 1):

            poolInputList=[]
            ##############################################################################
            for chrLong in chromNamesList:
                inputList = fillInputList(outputDir,
                              jobname,
                              chrLong,
                              simNum,
                              chromSizesDict,
                              library_file_with_path,
                              library_file_type,
                              library_file_df,
                              library_file_df_grouped,
                              sample2NumberofSubsDict,
                              sample2NumberofIndelsDict,
                              sample2NumberofDinucsDict,
                              sample2SubsSignature2NumberofMutationsDict,
                              sample2IndelsSignature2NumberofMutationsDict,
                              sample2DinucsSignature2NumberofMutationsDict,
                              subsSignature2PropertiesListDict,
                              indelsSignature2PropertiesListDict,
                              dinucsSignature2PropertiesListDict,
                              plusorMinus,
                              sample_based)

                poolInputList.append(inputList)
            ##############################################################################

            allChromosomes_SignalArrayAndCountArrayList_List=pool.map(combined_prepare_chrbased_data_fill_signal_count_arrays_using_inputList,poolInputList)

            #####################################################################################################
            ######################### Accumulate right in the left starts  ######################################
            #####################################################################################################
            for signalArrayAndCountArrayList in allChromosomes_SignalArrayAndCountArrayList_List:
                simNum2Type2SignalArrayDict = signalArrayAndCountArrayList[0]
                simNum2Type2CountArrayDict = signalArrayAndCountArrayList[1]
                simNum2Sample2Type2SignalArrayDict = signalArrayAndCountArrayList[2]
                simNum2Sample2Type2CountArrayDict = signalArrayAndCountArrayList[3]

                accumulateSimulationBasedTypeBasedArrays(simNum2Type2AccumulatedSignalArrayDict, simNum2Type2SignalArrayDict)
                accumulateSimulationBasedTypeBasedArrays(simNum2Type2AccumulatedCountArrayDict, simNum2Type2CountArrayDict)
                accumulateSimulationBasedSampleBasedTypeBasedArrays(simNum2Sample2Type2AccumulatedSignalArrayDict,simNum2Sample2Type2SignalArrayDict)
                accumulateSimulationBasedSampleBasedTypeBasedArrays(simNum2Sample2Type2AccumulatedCountArrayDict,simNum2Sample2Type2CountArrayDict)
            #####################################################################################################
            ######################### Accumulate right in the left ends  ########################################
            #####################################################################################################
        ##############################################################################

        ################################
        pool.close()
        pool.join()
        ################################

    ###################################################################################
    ##########  USING MAP Simulations Sequential Chromosomes Parallel ends ############
    ###################################################################################

    writeSimulationBasedAverageNucleosomeOccupancy(occupancy_type,
                                                   sample_based,
                                                   plusorMinus,
                                                   simNum2Type2AccumulatedSignalArrayDict,
                                                   simNum2Type2AccumulatedCountArrayDict,
                                                   simNum2Sample2Type2AccumulatedSignalArrayDict,
                                                   simNum2Sample2Type2AccumulatedCountArrayDict,
                                                   outputDir, jobname,library_file_memo)


#Using pyBigWig for bigBed and bigWig files ends
#Using bed files prepared on the fly ends
########################################################################################
