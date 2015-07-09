'''
Created on 2012-08-23; updated on 2014-5-25

@author: skardan & lalles
'''
from BasicParticipant import *
from Participant import export_features_all, write_features_tsv
from ValidityProcessing import output_Validity_info_Segments, output_percent_discarded, output_Validity_info_Participants
from EMDAT_multipleAOIs_wrapper import *

ul =        [61, 62]    # list of user recordings (files extracted for one participant from Tobii studio)
uids =      [61, 62]    # User ID that is used in the external logs (can be different from above but there should be a 1-1 mapping)

alogoffset =[ 3,  2]    # the time sifference between the eye tracker logs and the external log

####### Testing error handling
#ul =        [61, 62, 63]    # list of user recordings (files extracted for one participant from Tobii studio)
#uids =      [61, 62, 63]    # User ID that is used in the external logs (can be different from above but there should be a 1-1 mapping)
#
#alogoffset =[ 3,  2, 2]    # the time sifference between the eye tracker logs and the external log


###### Composite AOIs
sample_aoi_file="./sampledata/Simple composite aois.aoi"
composite_aoi_file="./sampledata/out_test.aoi"
params.aoinames=init_composite_AOIs(sample_aoi_file, composite_aoi_file)
print params.aoinames

###### Read participants
ps = read_participants_Basic(user_list = ul,pids = uids, log_time_offsets = alogoffset, datadir=params.EYELOGDATAFOLDER, 
                           prune_length = None, 
                           aoifile = composite_aoi_file,
#                           aoifile = "./sampledata/Dynamic_1.aoi",
                           require_valid_segs = False, auto_partition_low_quality_segments = True,
                           rpsfile = "./sampledata/all_rest_pupil_sizes.tsv")
print
######

#explore_validation_threshold_segments(ps, auto_partition_low_quality_segments = False)
output_Validity_info_Segments(ps, auto_partition_low_quality_segments_flag = False, validity_method = 3)
output_percent_discarded(ps,'./outputfolder/disc.csv')
output_Validity_info_Segments(ps, auto_partition_low_quality_segments_flag = False, validity_method = 2, threshold_gaps_list = [100, 200, 250, 300],output_file = "./outputfolder/Seg_val.csv")
output_Validity_info_Participants(ps, include_restored_samples =True, auto_partition_low_quality_segments_flag = False)


##### WRITE features to file
print
aoi_feat_names = (map(lambda x:x, params.aoigeneralfeat))
print "exporting:", params.featurelist, "\n", aoi_feat_names
write_features_tsv(ps, './outputfolder/sample_features.tsv',featurelist = params.featurelist, aoifeaturelist=aoi_feat_names, id_prefix = False)

postprocess_composite_AOIs('./outputfolder/sample_features.tsv', params.aoinames, aoi_feat_names)

#print "exporting:", params.featurelist, "\n", aoi_feat_names
#write_features_tsv(ps, './Data/Bar-Radar/outputfolder/sample_features.tsv',featurelist = params.featurelist, aoifeaturelist=aoi_feat_names, id_prefix = False)
#write_features_tsv(ps, './Data/Bar-Radar/outputfolder/sample_sequences.tsv',featurelist = params.aoisequencefeat, aoifeaturelabels=aoi_feat_names, id_prefix = False)
#write_features_tsv(ps, './Data/Bar-Radar/outputfolder/sample_features.tsv',featurelist = params.featurelist, aoifeaturelabels=aoi_feat_lab, id_prefix = False)


#### Export pupil dilations for each scene to a separate file
#print "exporting: pupil dilatoin trends" 
#plot_pupil_dilation_all(ps, './outputfolder\\pupilsizes\\', "problem1")
#plot_pupil_dilation_all(ps, './outputfolder\\pupilsizes\\', "problem2")