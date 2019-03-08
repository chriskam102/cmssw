import os
import copy
import collections

import six
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

from Validation.RecoTrack.plotting.plotting import Plot, PlotGroup, PlotFolder, Plotter, PlotOnSideGroup
from Validation.RecoTrack.plotting.html import PlotPurpose
import Validation.RecoTrack.plotting.plotting as plotting
import Validation.RecoTrack.plotting.validation as validation
import Validation.RecoTrack.plotting.html as html
from Validation.HGCalValidation.makeHGCalValidationPlots import layerscheme

lastLayerEEzm = layerscheme.lastLayerEEzm  # last layer of EE -z
lastLayerFHzm = layerscheme.lastLayerFHzm  # last layer of FH -z
maxlayerzm = layerscheme.maxlayerzm # last layer of BH -z
lastLayerEEzp = layerscheme.lastLayerEEzp  # last layer of EE +z
lastLayerFHzp = layerscheme.lastLayerFHzp  # last layer of FH +z
maxlayerzp = layerscheme.maxlayerzp # last layer of BH +z

_common = {"stat": True, "drawStyle": "hist", "staty": 0.65 }
_legend_common = {"legendDx": -0.3,
                  "legendDy": -0.05,
                  "legendDw": 0.1}

_SelectedCaloParticles = PlotGroup("SelectedCaloParticles", [
        Plot("num_caloparticle_eta", xtitle="", **_common),
        Plot("caloparticle_energy", xtitle="", **_common),
        Plot("caloparticle_pt", xtitle="", **_common),
        Plot("caloparticle_phi", xtitle="", **_common),
        Plot("Eta vs Zorigin", xtitle="", **_common),
       ])

#Need to adjust the statbox to see better the plot
_common = {"stat": True, "drawStyle": "hist", "statx": 0.38, "staty": 0.68 }
_num_reco_cluster_eta = PlotGroup("num_reco_cluster_eta", [
  Plot("num_reco_cluster_eta", xtitle="", **_common),
],ncols=1)
#Back to normal
_common = {"stat": True, "drawStyle": "hist", "staty": 0.65 }

_mixedhitsclusters = PlotGroup("mixedhitsclusters", [
  Plot("mixedhitscluster_zminus", xtitle="", **_common),
  Plot("mixedhitscluster_zplus", xtitle="", **_common),
],ncols=2)

#Just to prevent the stabox covering the plot
_common = {"stat": True, "drawStyle": "hist", "statx": 0.45, "staty": 0.65 }

_energyclustered = PlotGroup("energyclustered", [
  Plot("energyclustered_zminus", xtitle="", **_common),
  Plot("energyclustered_zplus", xtitle="", **_common),
],ncols=2)

#Coming back to the usual box definition
_common = {"stat": True, "drawStyle": "hist", "staty": 0.65 }

_longdepthbarycentre = PlotGroup("longdepthbarycentre", [
  Plot("longdepthbarycentre_zminus", xtitle="", **_common),
  Plot("longdepthbarycentre_zplus", xtitle="", **_common),
],ncols=2)

_common_layerperthickness = {}
_common_layerperthickness.update(_common)
_common_layerperthickness['xmin'] = 0.
_common_layerperthickness['xmax'] = 100

_totclusternum_thick = PlotGroup("totclusternum_thick", [
  Plot("totclusternum_thick_120", xtitle="", **_common_layerperthickness),
  Plot("totclusternum_thick_200", xtitle="", **_common_layerperthickness),
  Plot("totclusternum_thick_300", xtitle="", **_common_layerperthickness),
  Plot("totclusternum_thick_-1", xtitle="", **_common_layerperthickness),
  Plot("mixedhitscluster", xtitle="", **_common_layerperthickness),    
])

#We will plot the density in logy scale. 
_common = {"stat": True, "drawStyle": "hist", "staty": 0.65}

_cellsenedens_thick =  PlotGroup("cellsenedens_thick", [
  Plot("cellsenedens_thick_120", xtitle="", **_common),
  Plot("cellsenedens_thick_200", xtitle="", **_common),
  Plot("cellsenedens_thick_300", xtitle="", **_common),
  Plot("cellsenedens_thick_-1", xtitle="", **_common),
])

#Coming back to the usual box definition
_common = {"stat": True, "drawStyle": "hist", "staty": 0.65 }


#--------------------------------------------------------------------------------------------
# z-
#--------------------------------------------------------------------------------------------
_totclusternum_layer_EE_zminus = PlotGroup("totclusternum_layer_EE_zminus", [ 
  Plot("totclusternum_layer_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm) 
], ncols=4)

_totclusternum_layer_FH_zminus = PlotGroup("totclusternum_layer_FH_zminus", [ 
  Plot("totclusternum_layer_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_totclusternum_layer_BH_zminus = PlotGroup("totclusternum_layer_BH_zminus", [ 
  Plot("totclusternum_layer_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)

_energyclustered_perlayer_EE_zminus = PlotGroup("energyclustered_perlayer_EE_zminus", [ 
  Plot("energyclustered_perlayer{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm) 
], ncols=4)

_energyclustered_perlayer_FH_zminus = PlotGroup("energyclustered_perlayer_FH_zminus", [ 
  Plot("energyclustered_perlayer{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_energyclustered_perlayer_BH_zminus = PlotGroup("energyclustered_perlayer_BH_zminus", [ 
  Plot("energyclustered_perlayer{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)

#----------------------------------------------------------------------------------------------------------------
#120 um 
_common_cells = {}
_common_cells.update(_common)
_common_cells["xmin"] = 0
_common_cells["xmax"] = 50
_common_cells["ymin"] = 0.1
_common_cells["ymax"] = 10000
_common_cells["ylog"] = True
_cellsnum_perthick_perlayer_120_EE_zminus = PlotGroup("cellsnum_perthick_perlayer_120_EE_zminus", [ 
  Plot("cellsnum_perthick_perlayer_120_{:02d}".format(i), xtitle="", **_common_cells) for i in range(lastLayerEEzm) 
], ncols=4)

_cellsnum_perthick_perlayer_120_FH_zminus = PlotGroup("cellsnum_perthick_perlayer_120_FH_zminus", [ 
  Plot("cellsnum_perthick_perlayer_120_{:02d}".format(i), xtitle="", **_common_cells) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_cellsnum_perthick_perlayer_120_BH_zminus = PlotGroup("cellsnum_perthick_perlayer_120_BH_zminus", [ 
  Plot("cellsnum_perthick_perlayer_120_{:02d}".format(i), xtitle="", **_common_cells) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)

#200 um 
_cellsnum_perthick_perlayer_200_EE_zminus = PlotGroup("cellsnum_perthick_perlayer_200_EE_zminus", [ 
  Plot("cellsnum_perthick_perlayer_200_{:02d}".format(i), xtitle="", **_common_cells) for i in range(lastLayerEEzm) 
], ncols=4)

_cellsnum_perthick_perlayer_200_FH_zminus = PlotGroup("cellsnum_perthick_perlayer_200_FH_zminus", [ 
  Plot("cellsnum_perthick_perlayer_200_{:02d}".format(i), xtitle="", **_common_cells) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_cellsnum_perthick_perlayer_200_BH_zminus = PlotGroup("cellsnum_perthick_perlayer_200_BH_zminus", [ 
  Plot("cellsnum_perthick_perlayer_200_{:02d}".format(i), xtitle="", **_common_cells) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)

#300 um 
_cellsnum_perthick_perlayer_300_EE_zminus = PlotGroup("cellsnum_perthick_perlayer_300_EE_zminus", [ 
  Plot("cellsnum_perthick_perlayer_300_{:02d}".format(i), xtitle="", **_common_cells) for i in range(lastLayerEEzm) 
], ncols=4)

_cellsnum_perthick_perlayer_300_FH_zminus = PlotGroup("cellsnum_perthick_perlayer_300_FH_zminus", [ 
  Plot("cellsnum_perthick_perlayer_300_{:02d}".format(i), xtitle="", **_common_cells) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_cellsnum_perthick_perlayer_300_BH_zminus = PlotGroup("cellsnum_perthick_perlayer_300_BH_zminus", [ 
  Plot("cellsnum_perthick_perlayer_300_{:02d}".format(i), xtitle="", **_common_cells) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)

#scint um 
_cellsnum_perthick_perlayer_scint_EE_zminus = PlotGroup("cellsnum_perthick_perlayer_-1_EE_zminus", [ 
  Plot("cellsnum_perthick_perlayer_-1_{:02d}".format(i), xtitle="", **_common_cells) for i in range(lastLayerEEzm) 
], ncols=4)

_cellsnum_perthick_perlayer_scint_FH_zminus = PlotGroup("cellsnum_perthick_perlayer_-1_FH_zminus", [ 
  Plot("cellsnum_perthick_perlayer_-1_{:02d}".format(i), xtitle="", **_common_cells) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_cellsnum_perthick_perlayer_scint_BH_zminus = PlotGroup("cellsnum_perthick_perlayer_-1_BH_zminus", [ 
  Plot("cellsnum_perthick_perlayer_-1_{:02d}".format(i), xtitle="", **_common_cells) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)

#----------------------------------------------------------------------------------------------------------------
#120 um 
_common_distance = {}
_common_distance.update(_common)
_common_distance.update(_legend_common)
_common_distance["xmax"] = 150
_common_distance["stat"] = False
_common_distance["ymin"] = 1e-3
_common_distance["ymax"] = 10000
_common_distance["ylog"] = True

_distancetomaxcell_perthickperlayer_120_EE_zminus = PlotGroup("distancetomaxcell_perthickperlayer_120_EE_zminus", [ 
  Plot("distancetomaxcell_perthickperlayer_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm) 
], ncols=4)

_distancetomaxcell_perthickperlayer_120_FH_zminus = PlotGroup("distancetomaxcell_perthickperlayer_120_FH_zminus", [ 
  Plot("distancetomaxcell_perthickperlayer_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_distancetomaxcell_perthickperlayer_120_BH_zminus = PlotGroup("distancetomaxcell_perthickperlayer_120_BH_zminus", [ 
  Plot("distancetomaxcell_perthickperlayer_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)

#200 um 
_distancetomaxcell_perthickperlayer_200_EE_zminus = PlotGroup("distancetomaxcell_perthickperlayer_200_EE_zminus", [ 
  Plot("distancetomaxcell_perthickperlayer_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm) 
], ncols=4)

_distancetomaxcell_perthickperlayer_200_FH_zminus = PlotGroup("distancetomaxcell_perthickperlayer_200_FH_zminus", [ 
  Plot("distancetomaxcell_perthickperlayer_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_distancetomaxcell_perthickperlayer_200_BH_zminus = PlotGroup("distancetomaxcell_perthickperlayer_200_BH_zminus", [ 
  Plot("distancetomaxcell_perthickperlayer_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)

#300 um 
_distancetomaxcell_perthickperlayer_300_EE_zminus = PlotGroup("distancetomaxcell_perthickperlayer_300_EE_zminus", [ 
  Plot("distancetomaxcell_perthickperlayer_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm) 
], ncols=4)

_distancetomaxcell_perthickperlayer_300_FH_zminus = PlotGroup("distancetomaxcell_perthickperlayer_300_FH_zminus", [ 
  Plot("distancetomaxcell_perthickperlayer_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_distancetomaxcell_perthickperlayer_300_BH_zminus = PlotGroup("distancetomaxcell_perthickperlayer_300_BH_zminus", [ 
  Plot("distancetomaxcell_perthickperlayer_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)

#scint um 
_distancetomaxcell_perthickperlayer_scint_EE_zminus = PlotGroup("distancetomaxcell_perthickperlayer_-1_EE_zminus", [ 
  Plot("distancetomaxcell_perthickperlayer_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm) 
], ncols=4)

_distancetomaxcell_perthickperlayer_scint_FH_zminus = PlotGroup("distancetomaxcell_perthickperlayer_-1_FH_zminus", [ 
  Plot("distancetomaxcell_perthickperlayer_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_distancetomaxcell_perthickperlayer_scint_BH_zminus = PlotGroup("distancetomaxcell_perthickperlayer_-1_BH_zminus", [ 
  Plot("distancetomaxcell_perthickperlayer_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)

#----------------------------------------------------------------------------------------------------------------
#120 um 
_distancebetseedandmaxcell_perthickperlayer_120_EE_zminus = PlotGroup("distancebetseedandmaxcell_perthickperlayer_120_EE_zminus", [ 
  Plot("distancebetseedandmaxcell_perthickperlayer_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm) 
], ncols=4)

_distancebetseedandmaxcell_perthickperlayer_120_FH_zminus = PlotGroup("distancebetseedandmaxcell_perthickperlayer_120_FH_zminus", [ 
  Plot("distancebetseedandmaxcell_perthickperlayer_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_distancebetseedandmaxcell_perthickperlayer_120_BH_zminus = PlotGroup("distancebetseedandmaxcell_perthickperlayer_120_BH_zminus", [ 
  Plot("distancebetseedandmaxcell_perthickperlayer_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)

#200 um 
_distancebetseedandmaxcell_perthickperlayer_200_EE_zminus = PlotGroup("distancebetseedandmaxcell_perthickperlayer_200_EE_zminus", [ 
  Plot("distancebetseedandmaxcell_perthickperlayer_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm) 
], ncols=4)

_distancebetseedandmaxcell_perthickperlayer_200_FH_zminus = PlotGroup("distancebetseedandmaxcell_perthickperlayer_200_FH_zminus", [ 
  Plot("distancebetseedandmaxcell_perthickperlayer_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_distancebetseedandmaxcell_perthickperlayer_200_BH_zminus = PlotGroup("distancebetseedandmaxcell_perthickperlayer_200_BH_zminus", [ 
  Plot("distancebetseedandmaxcell_perthickperlayer_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)

#300 um 
_distancebetseedandmaxcell_perthickperlayer_300_EE_zminus = PlotGroup("distancebetseedandmaxcell_perthickperlayer_300_EE_zminus", [ 
  Plot("distancebetseedandmaxcell_perthickperlayer_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm) 
], ncols=4)

_distancebetseedandmaxcell_perthickperlayer_300_FH_zminus = PlotGroup("distancebetseedandmaxcell_perthickperlayer_300_FH_zminus", [ 
  Plot("distancebetseedandmaxcell_perthickperlayer_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_distancebetseedandmaxcell_perthickperlayer_300_BH_zminus = PlotGroup("distancebetseedandmaxcell_perthickperlayer_300_BH_zminus", [ 
  Plot("distancebetseedandmaxcell_perthickperlayer_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)

#scint um 
_distancebetseedandmaxcell_perthickperlayer_scint_EE_zminus = PlotGroup("distancebetseedandmaxcell_perthickperlayer_-1_EE_zminus", [ 
  Plot("distancebetseedandmaxcell_perthickperlayer_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm) 
], ncols=4)

_distancebetseedandmaxcell_perthickperlayer_scint_FH_zminus = PlotGroup("distancebetseedandmaxcell_perthickperlayer_-1_FH_zminus", [ 
  Plot("distancebetseedandmaxcell_perthickperlayer_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_distancebetseedandmaxcell_perthickperlayer_scint_BH_zminus = PlotGroup("distancebetseedandmaxcell_perthickperlayer_-1_BH_zminus", [ 
  Plot("distancebetseedandmaxcell_perthickperlayer_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)

#----------------------------------------------------------------------------------------------------------------
#120 um 
_distancebetseedandmaxcellvsclusterenergy_perthickperlayer_120_EE_zminus = PlotGroup("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_120_EE_zminus", [ 
  Plot("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm) 
], ncols=4)

_distancebetseedandmaxcellvsclusterenergy_perthickperlayer_120_FH_zminus = PlotGroup("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_120_FH_zminus", [ 
  Plot("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_distancebetseedandmaxcellvsclusterenergy_perthickperlayer_120_BH_zminus = PlotGroup("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_120_BH_zminus", [ 
  Plot("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)

#200 um 
_distancebetseedandmaxcellvsclusterenergy_perthickperlayer_200_EE_zminus = PlotGroup("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_200_EE_zminus", [ 
  Plot("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm) 
], ncols=4)

_distancebetseedandmaxcellvsclusterenergy_perthickperlayer_200_FH_zminus = PlotGroup("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_200_FH_zminus", [ 
  Plot("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_distancebetseedandmaxcellvsclusterenergy_perthickperlayer_200_BH_zminus = PlotGroup("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_200_BH_zminus", [ 
  Plot("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)

#300 um 
_distancebetseedandmaxcellvsclusterenergy_perthickperlayer_300_EE_zminus = PlotGroup("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_300_EE_zminus", [ 
  Plot("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm) 
], ncols=4)

_distancebetseedandmaxcellvsclusterenergy_perthickperlayer_300_FH_zminus = PlotGroup("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_300_FH_zminus", [ 
  Plot("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_distancebetseedandmaxcellvsclusterenergy_perthickperlayer_300_BH_zminus = PlotGroup("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_300_BH_zminus", [ 
  Plot("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)

#scint um 
_distancebetseedandmaxcellvsclusterenergy_perthickperlayer_scint_EE_zminus = PlotGroup("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_-1_EE_zminus", [ 
  Plot("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm) 
], ncols=4)

_distancebetseedandmaxcellvsclusterenergy_perthickperlayer_scint_FH_zminus = PlotGroup("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_-1_FH_zminus", [ 
  Plot("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_distancebetseedandmaxcellvsclusterenergy_perthickperlayer_scint_BH_zminus = PlotGroup("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_-1_BH_zminus", [ 
  Plot("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)

#----------------------------------------------------------------------------------------------------------------
#120 um 
_distancetoseedcell_perthickperlayer_120_EE_zminus = PlotGroup("distancetoseedcell_perthickperlayer_120_EE_zminus", [ 
  Plot("distancetoseedcell_perthickperlayer_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm) 
], ncols=4)

_distancetoseedcell_perthickperlayer_120_FH_zminus = PlotGroup("distancetoseedcell_perthickperlayer_120_FH_zminus", [ 
  Plot("distancetoseedcell_perthickperlayer_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_distancetoseedcell_perthickperlayer_120_BH_zminus = PlotGroup("distancetoseedcell_perthickperlayer_120_BH_zminus", [ 
  Plot("distancetoseedcell_perthickperlayer_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)

#200 um 
_distancetoseedcell_perthickperlayer_200_EE_zminus = PlotGroup("distancetoseedcell_perthickperlayer_200_EE_zminus", [ 
  Plot("distancetoseedcell_perthickperlayer_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm) 
], ncols=4)

_distancetoseedcell_perthickperlayer_200_FH_zminus = PlotGroup("distancetoseedcell_perthickperlayer_200_FH_zminus", [ 
  Plot("distancetoseedcell_perthickperlayer_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_distancetoseedcell_perthickperlayer_200_BH_zminus = PlotGroup("distancetoseedcell_perthickperlayer_200_BH_zminus", [ 
  Plot("distancetoseedcell_perthickperlayer_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)

#300 um 
_distancetoseedcell_perthickperlayer_300_EE_zminus = PlotGroup("distancetoseedcell_perthickperlayer_300_EE_zminus", [ 
  Plot("distancetoseedcell_perthickperlayer_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm) 
], ncols=4)

_distancetoseedcell_perthickperlayer_300_FH_zminus = PlotGroup("distancetoseedcell_perthickperlayer_300_FH_zminus", [ 
  Plot("distancetoseedcell_perthickperlayer_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_distancetoseedcell_perthickperlayer_300_BH_zminus = PlotGroup("distancetoseedcell_perthickperlayer_300_BH_zminus", [ 
  Plot("distancetoseedcell_perthickperlayer_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)

#scint um 
_distancetoseedcell_perthickperlayer_scint_EE_zminus = PlotGroup("distancetoseedcell_perthickperlayer_-1_EE_zminus", [ 
  Plot("distancetoseedcell_perthickperlayer_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm) 
], ncols=4)

_distancetoseedcell_perthickperlayer_scint_FH_zminus = PlotGroup("distancetoseedcell_perthickperlayer_-1_FH_zminus", [ 
  Plot("distancetoseedcell_perthickperlayer_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_distancetoseedcell_perthickperlayer_scint_BH_zminus = PlotGroup("distancetoseedcell_perthickperlayer_-1_BH_zminus", [ 
  Plot("distancetoseedcell_perthickperlayer_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)

#=====================================================================================================================
#----------------------------------------------------------------------------------------------------------------
#We need points for the weighted plots
_common = {"stat": True, "drawStyle": "EP", "staty": 0.65 }
#120 um 
_distancetomaxcell_perthickperlayer_eneweighted_120_EE_zminus = PlotGroup("distancetomaxcell_perthickperlayer_eneweighted_120_EE_zminus", [ 
  Plot("distancetomaxcell_perthickperlayer_eneweighted_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm) 
], ncols=4)

_distancetomaxcell_perthickperlayer_eneweighted_120_FH_zminus = PlotGroup("distancetomaxcell_perthickperlayer_eneweighted_120_FH_zminus", [ 
  Plot("distancetomaxcell_perthickperlayer_eneweighted_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_distancetomaxcell_perthickperlayer_eneweighted_120_BH_zminus = PlotGroup("distancetomaxcell_perthickperlayer_eneweighted_120_BH_zminus", [ 
  Plot("distancetomaxcell_perthickperlayer_eneweighted_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)

#200 um 
_distancetomaxcell_perthickperlayer_eneweighted_200_EE_zminus = PlotGroup("distancetomaxcell_perthickperlayer_eneweighted_200_EE_zminus", [ 
  Plot("distancetomaxcell_perthickperlayer_eneweighted_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm) 
], ncols=4)

_distancetomaxcell_perthickperlayer_eneweighted_200_FH_zminus = PlotGroup("distancetomaxcell_perthickperlayer_eneweighted_200_FH_zminus", [ 
  Plot("distancetomaxcell_perthickperlayer_eneweighted_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_distancetomaxcell_perthickperlayer_eneweighted_200_BH_zminus = PlotGroup("distancetomaxcell_perthickperlayer_eneweighted_200_BH_zminus", [ 
  Plot("distancetomaxcell_perthickperlayer_eneweighted_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)

#300 um 
_distancetomaxcell_perthickperlayer_eneweighted_300_EE_zminus = PlotGroup("distancetomaxcell_perthickperlayer_eneweighted_300_EE_zminus", [ 
  Plot("distancetomaxcell_perthickperlayer_eneweighted_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm) 
], ncols=4)

_distancetomaxcell_perthickperlayer_eneweighted_300_FH_zminus = PlotGroup("distancetomaxcell_perthickperlayer_eneweighted_300_FH_zminus", [ 
  Plot("distancetomaxcell_perthickperlayer_eneweighted_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_distancetomaxcell_perthickperlayer_eneweighted_300_BH_zminus = PlotGroup("distancetomaxcell_perthickperlayer_eneweighted_300_BH_zminus", [ 
  Plot("distancetomaxcell_perthickperlayer_eneweighted_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)
#scint um 
_distancetomaxcell_perthickperlayer_eneweighted_scint_EE_zminus = PlotGroup("distancetomaxcell_perthickperlayer_eneweighted_-1_EE_zminus", [ 
  Plot("distancetomaxcell_perthickperlayer_eneweighted_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm) 
], ncols=4)

_distancetomaxcell_perthickperlayer_eneweighted_scint_FH_zminus = PlotGroup("distancetomaxcell_perthickperlayer_eneweighted_-1_FH_zminus", [ 
  Plot("distancetomaxcell_perthickperlayer_eneweighted_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_distancetomaxcell_perthickperlayer_eneweighted_scint_BH_zminus = PlotGroup("distancetomaxcell_perthickperlayer_eneweighted_-1_BH_zminus", [ 
  Plot("distancetomaxcell_perthickperlayer_eneweighted_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)


#----------------------------------------------------------------------------------------------------------------
#120 um 
_distancetoseedcell_perthickperlayer_eneweighted_120_EE_zminus = PlotGroup("distancetoseedcell_perthickperlayer_eneweighted_120_EE_zminus", [ 
  Plot("distancetoseedcell_perthickperlayer_eneweighted_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm) 
], ncols=4)

_distancetoseedcell_perthickperlayer_eneweighted_120_FH_zminus = PlotGroup("distancetoseedcell_perthickperlayer_eneweighted_120_FH_zminus", [ 
  Plot("distancetoseedcell_perthickperlayer_eneweighted_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_distancetoseedcell_perthickperlayer_eneweighted_120_BH_zminus = PlotGroup("distancetoseedcell_perthickperlayer_eneweighted_120_BH_zminus", [ 
  Plot("distancetoseedcell_perthickperlayer_eneweighted_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)

#200 um 
_distancetoseedcell_perthickperlayer_eneweighted_200_EE_zminus = PlotGroup("distancetoseedcell_perthickperlayer_eneweighted_200_EE_zminus", [ 
  Plot("distancetoseedcell_perthickperlayer_eneweighted_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm) 
], ncols=4)

_distancetoseedcell_perthickperlayer_eneweighted_200_FH_zminus = PlotGroup("distancetoseedcell_perthickperlayer_eneweighted_200_FH_zminus", [ 
  Plot("distancetoseedcell_perthickperlayer_eneweighted_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_distancetoseedcell_perthickperlayer_eneweighted_200_BH_zminus = PlotGroup("distancetoseedcell_perthickperlayer_eneweighted_200_BH_zminus", [ 
  Plot("distancetoseedcell_perthickperlayer_eneweighted_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)

#300 um 
_distancetoseedcell_perthickperlayer_eneweighted_300_EE_zminus = PlotGroup("distancetoseedcell_perthickperlayer_eneweighted_300_EE_zminus", [ 
  Plot("distancetoseedcell_perthickperlayer_eneweighted_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm) 
], ncols=4)

_distancetoseedcell_perthickperlayer_eneweighted_300_FH_zminus = PlotGroup("distancetoseedcell_perthickperlayer_eneweighted_300_FH_zminus", [ 
  Plot("distancetoseedcell_perthickperlayer_eneweighted_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_distancetoseedcell_perthickperlayer_eneweighted_300_BH_zminus = PlotGroup("distancetoseedcell_perthickperlayer_eneweighted_300_BH_zminus", [ 
  Plot("distancetoseedcell_perthickperlayer_eneweighted_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)

#scint um 
_distancetoseedcell_perthickperlayer_eneweighted_scint_EE_zminus = PlotGroup("distancetoseedcell_perthickperlayer_eneweighted_-1_EE_zminus", [ 
  Plot("distancetoseedcell_perthickperlayer_eneweighted_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm) 
], ncols=4)

_distancetoseedcell_perthickperlayer_eneweighted_scint_FH_zminus = PlotGroup("distancetoseedcell_perthickperlayer_eneweighted_-1_FH_zminus", [ 
  Plot("distancetoseedcell_perthickperlayer_eneweighted_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzm,lastLayerFHzm) 
], ncols=4)

_distancetoseedcell_perthickperlayer_eneweighted_scint_BH_zminus = PlotGroup("distancetoseedcell_perthickperlayer_eneweighted_-1_BH_zminus", [ 
  Plot("distancetoseedcell_perthickperlayer_eneweighted_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzm,maxlayerzm) 
], ncols=4)

#Coming back to the usual definition 
_common = {"stat": True, "drawStyle": "hist", "staty": 0.65 }

#--------------------------------------------------------------------------------------------
# z+
#--------------------------------------------------------------------------------------------
_totclusternum_layer_EE_zplus = PlotGroup("totclusternum_layer_EE_zplus", [ 
  Plot("totclusternum_layer_{:02d}".format(i), xtitle="", **_common) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)

_totclusternum_layer_FH_zplus = PlotGroup("totclusternum_layer_FH_zplus", [ 
  Plot("totclusternum_layer_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)

_totclusternum_layer_BH_zplus = PlotGroup("totclusternum_layer_BH_zplus", [ 
  Plot("totclusternum_layer_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)

_energyclustered_perlayer_EE_zplus = PlotGroup("energyclustered_perlayer_EE_zplus", [ 
  Plot("energyclustered_perlayer{:02d}".format(i), xtitle="", **_common) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)

_energyclustered_perlayer_FH_zplus = PlotGroup("energyclustered_perlayer_FH_zplus", [ 
  Plot("energyclustered_perlayer{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)

_energyclustered_perlayer_BH_zplus = PlotGroup("energyclustered_perlayer_BH_zplus", [ 
  Plot("energyclustered_perlayer{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)

#----------------------------------------------------------------------------------------------------------------
#120 um 
_cellsnum_perthick_perlayer_120_EE_zplus = PlotGroup("cellsnum_perthick_perlayer_120_EE_zplus", [ 
  Plot("cellsnum_perthick_perlayer_120_{:02d}".format(i), xtitle="", **_common_cells) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)

_cellsnum_perthick_perlayer_120_FH_zplus = PlotGroup("cellsnum_perthick_perlayer_120_FH_zplus", [ 
  Plot("cellsnum_perthick_perlayer_120_{:02d}".format(i), xtitle="", **_common_cells) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)
_cellsnum_perthick_perlayer_120_BH_zplus = PlotGroup("cellsnum_perthick_perlayer_120_BH_zplus", [ 
  Plot("cellsnum_perthick_perlayer_120_{:02d}".format(i), xtitle="", **_common_cells) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)

#200 um 
_cellsnum_perthick_perlayer_200_EE_zplus = PlotGroup("cellsnum_perthick_perlayer_200_EE_zplus", [ 
  Plot("cellsnum_perthick_perlayer_200_{:02d}".format(i), xtitle="", **_common_cells) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)

_cellsnum_perthick_perlayer_200_FH_zplus = PlotGroup("cellsnum_perthick_perlayer_200_FH_zplus", [ 
  Plot("cellsnum_perthick_perlayer_200_{:02d}".format(i), xtitle="", **_common_cells) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)

_cellsnum_perthick_perlayer_200_BH_zplus = PlotGroup("cellsnum_perthick_perlayer_200_BH_zplus", [ 
  Plot("cellsnum_perthick_perlayer_200_{:02d}".format(i), xtitle="", **_common_cells) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)
#300 um 
_cellsnum_perthick_perlayer_300_EE_zplus = PlotGroup("cellsnum_perthick_perlayer_300_EE_zplus", [ 
  Plot("cellsnum_perthick_perlayer_300_{:02d}".format(i), xtitle="", **_common_cells) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)

_cellsnum_perthick_perlayer_300_FH_zplus = PlotGroup("cellsnum_perthick_perlayer_300_FH_zplus", [ 
  Plot("cellsnum_perthick_perlayer_300_{:02d}".format(i), xtitle="", **_common_cells) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)
_cellsnum_perthick_perlayer_300_BH_zplus = PlotGroup("cellsnum_perthick_perlayer_300_BH_zplus", [ 
  Plot("cellsnum_perthick_perlayer_300_{:02d}".format(i), xtitle="", **_common_cells) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)

#scint um 
_cellsnum_perthick_perlayer_scint_EE_zplus = PlotGroup("cellsnum_perthick_perlayer_-1_EE_zplus", [ 
  Plot("cellsnum_perthick_perlayer_-1_{:02d}".format(i), xtitle="", **_common_cells) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)

_cellsnum_perthick_perlayer_scint_FH_zplus = PlotGroup("cellsnum_perthick_perlayer_-1_FH_zplus", [ 
  Plot("cellsnum_perthick_perlayer_-1_{:02d}".format(i), xtitle="", **_common_cells) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)

_cellsnum_perthick_perlayer_scint_BH_zplus = PlotGroup("cellsnum_perthick_perlayer_-1_BH_zplus", [ 
  Plot("cellsnum_perthick_perlayer_-1_{:02d}".format(i), xtitle="", **_common_cells) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)

#----------------------------------------------------------------------------------------------------------------
#120 um 
_common_distance = {}
_common_distance.update(_common)
_common_distance.update(_legend_common)
_common_distance["xmax"] = 150
_common_distance["stat"] = False
_common_distance["ymin"] = 1e-3
_common_distance["ymax"] = 10000
_common_distance["ylog"] = True

_distancetomaxcell_perthickperlayer_120_EE_zplus = PlotGroup("distancetomaxcell_perthickperlayer_120_EE_zplus", [ 
  Plot("distancetomaxcell_perthickperlayer_120_{:02d}".format(i), xtitle="", **_common) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)

_distancetomaxcell_perthickperlayer_120_FH_zplus = PlotGroup("distancetomaxcell_perthickperlayer_120_FH_zplus", [ 
  Plot("distancetomaxcell_perthickperlayer_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)

_distancetomaxcell_perthickperlayer_120_BH_zplus = PlotGroup("distancetomaxcell_perthickperlayer_120_BH_zplus", [ 
  Plot("distancetomaxcell_perthickperlayer_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)

#200 um 
_distancetomaxcell_perthickperlayer_200_EE_zplus = PlotGroup("distancetomaxcell_perthickperlayer_200_EE_zplus", [ 
  Plot("distancetomaxcell_perthickperlayer_200_{:02d}".format(i), xtitle="", **_common) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)

_distancetomaxcell_perthickperlayer_200_FH_zplus = PlotGroup("distancetomaxcell_perthickperlayer_200_FH_zplus", [ 
  Plot("distancetomaxcell_perthickperlayer_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)

_distancetomaxcell_perthickperlayer_200_BH_zplus = PlotGroup("distancetomaxcell_perthickperlayer_200_BH_zplus", [ 
  Plot("distancetomaxcell_perthickperlayer_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)

#300 um 
_distancetomaxcell_perthickperlayer_300_EE_zplus = PlotGroup("distancetomaxcell_perthickperlayer_300_EE_zplus", [ 
  Plot("distancetomaxcell_perthickperlayer_300_{:02d}".format(i), xtitle="", **_common) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)

_distancetomaxcell_perthickperlayer_300_FH_zplus = PlotGroup("distancetomaxcell_perthickperlayer_300_FH_zplus", [ 
  Plot("distancetomaxcell_perthickperlayer_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)

_distancetomaxcell_perthickperlayer_300_BH_zplus = PlotGroup("distancetomaxcell_perthickperlayer_300_BH_zplus", [ 
  Plot("distancetomaxcell_perthickperlayer_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)

#scint um 
_distancetomaxcell_perthickperlayer_scint_EE_zplus = PlotGroup("distancetomaxcell_perthickperlayer_-1_EE_zplus", [ 
  Plot("distancetomaxcell_perthickperlayer_-1_{:02d}".format(i), xtitle="", **_common) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)

_distancetomaxcell_perthickperlayer_scint_FH_zplus = PlotGroup("distancetomaxcell_perthickperlayer_-1_FH_zplus", [ 
  Plot("distancetomaxcell_perthickperlayer_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)

_distancetomaxcell_perthickperlayer_scint_BH_zplus = PlotGroup("distancetomaxcell_perthickperlayer_-1_BH_zplus", [ 
  Plot("distancetomaxcell_perthickperlayer_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)

#----------------------------------------------------------------------------------------------------------------
#120 um 
_distancebetseedandmaxcell_perthickperlayer_120_EE_zplus = PlotGroup("distancebetseedandmaxcell_perthickperlayer_120_EE_zplus", [ 
  Plot("distancebetseedandmaxcell_perthickperlayer_120_{:02d}".format(i), xtitle="", **_common) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)

_distancebetseedandmaxcell_perthickperlayer_120_FH_zplus = PlotGroup("distancebetseedandmaxcell_perthickperlayer_120_FH_zplus", [ 
  Plot("distancebetseedandmaxcell_perthickperlayer_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)

_distancebetseedandmaxcell_perthickperlayer_120_BH_zplus = PlotGroup("distancebetseedandmaxcell_perthickperlayer_120_BH_zplus", [ 
  Plot("distancebetseedandmaxcell_perthickperlayer_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)

#200 um 
_distancebetseedandmaxcell_perthickperlayer_200_EE_zplus = PlotGroup("distancebetseedandmaxcell_perthickperlayer_200_EE_zplus", [ 
  Plot("distancebetseedandmaxcell_perthickperlayer_200_{:02d}".format(i), xtitle="", **_common) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)

_distancebetseedandmaxcell_perthickperlayer_200_FH_zplus = PlotGroup("distancebetseedandmaxcell_perthickperlayer_200_FH_zplus", [ 
  Plot("distancebetseedandmaxcell_perthickperlayer_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)

_distancebetseedandmaxcell_perthickperlayer_200_BH_zplus = PlotGroup("distancebetseedandmaxcell_perthickperlayer_200_BH_zplus", [ 
  Plot("distancebetseedandmaxcell_perthickperlayer_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)

#300 um 
_distancebetseedandmaxcell_perthickperlayer_300_EE_zplus = PlotGroup("distancebetseedandmaxcell_perthickperlayer_300_EE_zplus", [ 
  Plot("distancebetseedandmaxcell_perthickperlayer_300_{:02d}".format(i), xtitle="", **_common) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)

_distancebetseedandmaxcell_perthickperlayer_300_FH_zplus = PlotGroup("distancebetseedandmaxcell_perthickperlayer_300_FH_zplus", [ 
  Plot("distancebetseedandmaxcell_perthickperlayer_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)

_distancebetseedandmaxcell_perthickperlayer_300_BH_zplus = PlotGroup("distancebetseedandmaxcell_perthickperlayer_300_BH_zplus", [ 
  Plot("distancebetseedandmaxcell_perthickperlayer_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)

#scint um 
_distancebetseedandmaxcell_perthickperlayer_scint_EE_zplus = PlotGroup("distancebetseedandmaxcell_perthickperlayer_-1_EE_zplus", [ 
  Plot("distancebetseedandmaxcell_perthickperlayer_-1_{:02d}".format(i), xtitle="", **_common) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)

_distancebetseedandmaxcell_perthickperlayer_scint_FH_zplus = PlotGroup("distancebetseedandmaxcell_perthickperlayer_-1_FH_zplus", [ 
  Plot("distancebetseedandmaxcell_perthickperlayer_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)

_distancebetseedandmaxcell_perthickperlayer_scint_BH_zplus = PlotGroup("distancebetseedandmaxcell_perthickperlayer_-1_BH_zplus", [ 
  Plot("distancebetseedandmaxcell_perthickperlayer_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)

#----------------------------------------------------------------------------------------------------------------
#120 um 
_distancebetseedandmaxcellvsclusterenergy_perthickperlayer_120_EE_zplus = PlotGroup("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_120_EE_zplus", [ 
  Plot("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_120_{:02d}".format(i), xtitle="", **_common) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)

_distancebetseedandmaxcellvsclusterenergy_perthickperlayer_120_FH_zplus = PlotGroup("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_120_FH_zplus", [ 
  Plot("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)

_distancebetseedandmaxcellvsclusterenergy_perthickperlayer_120_BH_zplus = PlotGroup("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_120_BH_zplus", [ 
  Plot("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)

#200 um 
_distancebetseedandmaxcellvsclusterenergy_perthickperlayer_200_EE_zplus = PlotGroup("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_200_EE_zplus", [ 
  Plot("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_200_{:02d}".format(i), xtitle="", **_common) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)

_distancebetseedandmaxcellvsclusterenergy_perthickperlayer_200_FH_zplus = PlotGroup("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_200_FH_zplus", [ 
  Plot("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)

_distancebetseedandmaxcellvsclusterenergy_perthickperlayer_200_BH_zplus = PlotGroup("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_200_BH_zplus", [ 
  Plot("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)

#300 um 
_distancebetseedandmaxcellvsclusterenergy_perthickperlayer_300_EE_zplus = PlotGroup("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_300_EE_zplus", [ 
  Plot("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_300_{:02d}".format(i), xtitle="", **_common) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)

_distancebetseedandmaxcellvsclusterenergy_perthickperlayer_300_FH_zplus = PlotGroup("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_300_FH_zplus", [ 
  Plot("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)

_distancebetseedandmaxcellvsclusterenergy_perthickperlayer_300_BH_zplus = PlotGroup("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_300_BH_zplus", [ 
  Plot("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)

#scint um 
_distancebetseedandmaxcellvsclusterenergy_perthickperlayer_scint_EE_zplus = PlotGroup("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_-1_EE_zplus", [ 
  Plot("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_-1_{:02d}".format(i), xtitle="", **_common) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)

_distancebetseedandmaxcellvsclusterenergy_perthickperlayer_scint_FH_zplus = PlotGroup("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_-1_FH_zplus", [ 
  Plot("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)

_distancebetseedandmaxcellvsclusterenergy_perthickperlayer_scint_BH_zplus = PlotGroup("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_-1_BH_zplus", [ 
  Plot("distancebetseedandmaxcellvsclusterenergy_perthickperlayer_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)


#----------------------------------------------------------------------------------------------------------------
#120 um 
_distancetoseedcell_perthickperlayer_120_EE_zplus = PlotGroup("distancetoseedcell_perthickperlayer_120_EE_zplus", [ 
  Plot("distancetoseedcell_perthickperlayer_120_{:02d}".format(i), xtitle="", **_common) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)

_distancetoseedcell_perthickperlayer_120_FH_zplus = PlotGroup("distancetoseedcell_perthickperlayer_120_FH_zplus", [ 
  Plot("distancetoseedcell_perthickperlayer_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)

_distancetoseedcell_perthickperlayer_120_BH_zplus = PlotGroup("distancetoseedcell_perthickperlayer_120_BH_zplus", [ 
  Plot("distancetoseedcell_perthickperlayer_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)

#200 um 
_distancetoseedcell_perthickperlayer_200_EE_zplus = PlotGroup("distancetoseedcell_perthickperlayer_200_EE_zplus", [ 
  Plot("distancetoseedcell_perthickperlayer_200_{:02d}".format(i), xtitle="", **_common) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)

_distancetoseedcell_perthickperlayer_200_FH_zplus = PlotGroup("distancetoseedcell_perthickperlayer_200_FH_zplus", [ 
  Plot("distancetoseedcell_perthickperlayer_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)

_distancetoseedcell_perthickperlayer_200_BH_zplus = PlotGroup("distancetoseedcell_perthickperlayer_200_BH_zplus", [ 
  Plot("distancetoseedcell_perthickperlayer_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)

#300 um 
_distancetoseedcell_perthickperlayer_300_EE_zplus = PlotGroup("distancetoseedcell_perthickperlayer_300_EE_zplus", [ 
  Plot("distancetoseedcell_perthickperlayer_300_{:02d}".format(i), xtitle="", **_common) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)

_distancetoseedcell_perthickperlayer_300_FH_zplus = PlotGroup("distancetoseedcell_perthickperlayer_300_FH_zplus", [ 
  Plot("distancetoseedcell_perthickperlayer_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)

_distancetoseedcell_perthickperlayer_300_BH_zplus = PlotGroup("distancetoseedcell_perthickperlayer_300_BH_zplus", [ 
  Plot("distancetoseedcell_perthickperlayer_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)

#scint um 
_distancetoseedcell_perthickperlayer_scint_EE_zplus = PlotGroup("distancetoseedcell_perthickperlayer_-1_EE_zplus", [ 
  Plot("distancetoseedcell_perthickperlayer_-1_{:02d}".format(i), xtitle="", **_common) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)

_distancetoseedcell_perthickperlayer_scint_FH_zplus = PlotGroup("distancetoseedcell_perthickperlayer_-1_FH_zplus", [ 
  Plot("distancetoseedcell_perthickperlayer_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)

_distancetoseedcell_perthickperlayer_scint_BH_zplus = PlotGroup("distancetoseedcell_perthickperlayer_-1_BH_zplus", [ 
  Plot("distancetoseedcell_perthickperlayer_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)

#=====================================================================================================================
#----------------------------------------------------------------------------------------------------------------
#We need points for the weighted plots
_common = {"stat": True, "drawStyle": "EP", "staty": 0.65 }

#120 um 
_distancetomaxcell_perthickperlayer_eneweighted_120_EE_zplus = PlotGroup("distancetomaxcell_perthickperlayer_eneweighted_120_EE_zplus", [ 
  Plot("distancetomaxcell_perthickperlayer_eneweighted_120_{:02d}".format(i), xtitle="", **_common) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)

_distancetomaxcell_perthickperlayer_eneweighted_120_FH_zplus = PlotGroup("distancetomaxcell_perthickperlayer_eneweighted_120_FH_zplus", [ 
  Plot("distancetomaxcell_perthickperlayer_eneweighted_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)

_distancetomaxcell_perthickperlayer_eneweighted_120_BH_zplus = PlotGroup("distancetomaxcell_perthickperlayer_eneweighted_120_BH_zplus", [ 
  Plot("distancetomaxcell_perthickperlayer_eneweighted_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)

#200 um 
_distancetomaxcell_perthickperlayer_eneweighted_200_EE_zplus = PlotGroup("distancetomaxcell_perthickperlayer_eneweighted_200_EE_zplus", [ 
  Plot("distancetomaxcell_perthickperlayer_eneweighted_200_{:02d}".format(i), xtitle="", **_common) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)
_distancetomaxcell_perthickperlayer_eneweighted_200_FH_zplus = PlotGroup("distancetomaxcell_perthickperlayer_eneweighted_200_FH_zplus", [ 
  Plot("distancetomaxcell_perthickperlayer_eneweighted_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)

_distancetomaxcell_perthickperlayer_eneweighted_200_BH_zplus = PlotGroup("distancetomaxcell_perthickperlayer_eneweighted_200_BH_zplus", [ 
  Plot("distancetomaxcell_perthickperlayer_eneweighted_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)

#300 um 
_distancetomaxcell_perthickperlayer_eneweighted_300_EE_zplus = PlotGroup("distancetomaxcell_perthickperlayer_eneweighted_300_EE_zplus", [ 
  Plot("distancetomaxcell_perthickperlayer_eneweighted_300_{:02d}".format(i), xtitle="", **_common) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)

_distancetomaxcell_perthickperlayer_eneweighted_300_FH_zplus = PlotGroup("distancetomaxcell_perthickperlayer_eneweighted_300_FH_zplus", [ 
  Plot("distancetomaxcell_perthickperlayer_eneweighted_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)

_distancetomaxcell_perthickperlayer_eneweighted_300_BH_zplus = PlotGroup("distancetomaxcell_perthickperlayer_eneweighted_300_BH_zplus", [ 
  Plot("distancetomaxcell_perthickperlayer_eneweighted_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)

#scint um 
_distancetomaxcell_perthickperlayer_eneweighted_scint_EE_zplus = PlotGroup("distancetomaxcell_perthickperlayer_eneweighted_-1_EE_zplus", [ 
  Plot("distancetomaxcell_perthickperlayer_eneweighted_-1_{:02d}".format(i), xtitle="", **_common) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)

_distancetomaxcell_perthickperlayer_eneweighted_scint_FH_zplus = PlotGroup("distancetomaxcell_perthickperlayer_eneweighted_-1_FH_zplus", [ 
  Plot("distancetomaxcell_perthickperlayer_eneweighted_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)

_distancetomaxcell_perthickperlayer_eneweighted_scint_BH_zplus = PlotGroup("distancetomaxcell_perthickperlayer_eneweighted_-1_BH_zplus", [ 
  Plot("distancetomaxcell_perthickperlayer_eneweighted_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)

#----------------------------------------------------------------------------------------------------------------
#120 um 
_distancetoseedcell_perthickperlayer_eneweighted_120_EE_zplus = PlotGroup("distancetoseedcell_perthickperlayer_eneweighted_120_EE_zplus", [ 
  Plot("distancetoseedcell_perthickperlayer_eneweighted_120_{:02d}".format(i), xtitle="", **_common) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)

_distancetoseedcell_perthickperlayer_eneweighted_120_FH_zplus = PlotGroup("distancetoseedcell_perthickperlayer_eneweighted_120_FH_zplus", [ 
  Plot("distancetoseedcell_perthickperlayer_eneweighted_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)

_distancetoseedcell_perthickperlayer_eneweighted_120_BH_zplus = PlotGroup("distancetoseedcell_perthickperlayer_eneweighted_120_BH_zplus", [ 
  Plot("distancetoseedcell_perthickperlayer_eneweighted_120_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)

#200 um 
_distancetoseedcell_perthickperlayer_eneweighted_200_EE_zplus = PlotGroup("distancetoseedcell_perthickperlayer_eneweighted_200_EE_zplus", [ 
  Plot("distancetoseedcell_perthickperlayer_eneweighted_200_{:02d}".format(i), xtitle="", **_common) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)

_distancetoseedcell_perthickperlayer_eneweighted_200_FH_zplus = PlotGroup("distancetoseedcell_perthickperlayer_eneweighted_200_FH_zplus", [ 
  Plot("distancetoseedcell_perthickperlayer_eneweighted_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)

_distancetoseedcell_perthickperlayer_eneweighted_200_BH_zplus = PlotGroup("distancetoseedcell_perthickperlayer_eneweighted_200_BH_zplus", [ 
  Plot("distancetoseedcell_perthickperlayer_eneweighted_200_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)

#300 um 
_distancetoseedcell_perthickperlayer_eneweighted_300_EE_zplus = PlotGroup("distancetoseedcell_perthickperlayer_eneweighted_300_EE_zplus", [ 
  Plot("distancetoseedcell_perthickperlayer_eneweighted_300_{:02d}".format(i), xtitle="", **_common) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)

_distancetoseedcell_perthickperlayer_eneweighted_300_FH_zplus = PlotGroup("distancetoseedcell_perthickperlayer_eneweighted_300_FH_zplus", [ 
  Plot("distancetoseedcell_perthickperlayer_eneweighted_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)

_distancetoseedcell_perthickperlayer_eneweighted_300_BH_zplus = PlotGroup("distancetoseedcell_perthickperlayer_eneweighted_300_BH_zplus", [ 
  Plot("distancetoseedcell_perthickperlayer_eneweighted_300_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)

#scint um 
_distancetoseedcell_perthickperlayer_eneweighted_scint_EE_zplus = PlotGroup("distancetoseedcell_perthickperlayer_eneweighted_-1_EE_zplus", [ 
  Plot("distancetoseedcell_perthickperlayer_eneweighted_-1_{:02d}".format(i), xtitle="", **_common) for i in range(maxlayerzm,lastLayerEEzp) 
], ncols=4)

_distancetoseedcell_perthickperlayer_eneweighted_scint_FH_zplus = PlotGroup("distancetoseedcell_perthickperlayer_eneweighted_-1_FH_zplus", [ 
  Plot("distancetoseedcell_perthickperlayer_eneweighted_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerEEzp,lastLayerFHzp) 
], ncols=4)

_distancetoseedcell_perthickperlayer_eneweighted_scint_BH_zplus = PlotGroup("distancetoseedcell_perthickperlayer_eneweighted_-1_BH_zplus", [ 
  Plot("distancetoseedcell_perthickperlayer_eneweighted_-1_{:02d}".format(i), xtitle="", **_common) for i in range(lastLayerFHzp,maxlayerzp) 
], ncols=4)
#Just in case we add some plots below to be on the safe side. 
_common = {"stat": True, "drawStyle": "hist", "staty": 0.65 }

#--------------------------------------------------------------------------------------------
# z-
#--------------------------------------------------------------------------------------------

_common_score = {"title": "Score CaloParticle to LayerClusters in z-",
                 "stat": False,
                 "ymin": 0.1,
                 "ymax": 1000,
                 "xmin": 0,
                 "xmax": 1,
                 "drawStyle": "hist",
                 "lineWidth": 1,
                 "ylog": True
                }
_common_score.update(_legend_common)
_score_caloparticle_to_layerclusters_zminus = PlotGroup("score_caloparticle_to_layercluster_zminus", [
        Plot("Score_caloparticle2layercl_perlayer{:02d}".format(i), xtitle="Layer {:02d} in z-".format(i%maxlayerzm+1) if (i<maxlayerzm) else "Layer {:02d} in z+".format(i%maxlayerzm+1), **_common_score) for i in range(0,maxlayerzm)
        ], ncols=8 )

_common_score = {"title": "Score LayerCluster to CaloParticles in z-",
                 "stat": False,
                 "ymin": 0.1,
                 "ymax": 1000,
                 "xmin": 0,
                 "xmax": 1,
                 "drawStyle": "hist",
                 "lineWidth": 1,
                 "ylog": True
                }
_common_score.update(_legend_common)
_score_layercluster_to_caloparticles_zminus = PlotGroup("score_layercluster_to_caloparticle_zminus", [
        Plot("Score_layercl2caloparticle_perlayer{:02d}".format(i), xtitle="Layer {:02d} in z-".format(i%maxlayerzm+1) if (i<maxlayerzm) else "Layer {:02d} in z+".format(i%maxlayerzm+1), **_common_score) for i in range(0,maxlayerzm)
        ], ncols=8 )

_common_shared= {"title": "Shared Energy CaloParticle To Layer Cluster in z-",
                 "stat": False,
                 "legend": False,
                }
_common_shared.update(_legend_common)
_shared_plots_zminus = [Plot("SharedEnergy_caloparticle2layercl_perlayer{:02d}".format(i), xtitle="Layer {:02d} in z-".format(i%maxlayerzm+1) if (i<maxlayerzm) else "Layer {:02d} in z+".format(i%maxlayerzm+1), **_common_shared) for i in range(0,maxlayerzm)]
_shared_plots_zminus.extend([Plot("SharedEnergy_caloparticle2layercl_vs_eta_perlayer{:02d}".format(i), xtitle="Layer {:02d} in z-".format(i%maxlayerzm+1) if (i<maxlayerzm) else "Layer {:02d} in z+".format(i%maxlayerzm+1), **_common_shared) for i in range(0,maxlayerzm)])
_shared_plots_zminus.extend([Plot("SharedEnergy_caloparticle2layercl_vs_phi_perlayer{:02d}".format(i), xtitle="Layer {:02d} in z-".format(i%maxlayerzm+1) if (i<maxlayerzm) else "Layer {:02d} in z+".format(i%maxlayerzm+1), **_common_shared) for i in range(0,maxlayerzm)])
_sharedEnergy_caloparticle_to_layercluster_zminus = PlotGroup("sharedEnergy_caloparticle_to_layercluster_zminus", _shared_plots_zminus, ncols=8)

_common_shared= {"title": "Shared Energy Layer Cluster To CaloParticle in z-",
                 "stat": False,
                 "legend": False,
                }
_common_shared.update(_legend_common)
_shared_plots2_zminus = [Plot("SharedEnergy_layercluster2caloparticle_perlayer{:02d}".format(i), xtitle="Layer {:02d} in z-".format(i%maxlayerzm+1) if (i<maxlayerzm) else "Layer {:02d} in z+".format(i%maxlayerzm+1), **_common_shared) for i in range(0,maxlayerzm)]
_shared_plots2_zminus.extend([Plot("SharedEnergy_layercl2caloparticle_vs_eta_perlayer{:02d}".format(i), xtitle="Layer {:02d} in z-".format(i%maxlayerzm+1) if (i<maxlayerzm) else "Layer {:02d} in z+".format(i%maxlayerzm+1), **_common_shared) for i in range(0,maxlayerzm)])
_shared_plots2_zminus.extend([Plot("SharedEnergy_layercl2caloparticle_vs_phi_perlayer{:02d}".format(i), xtitle="Layer {:02d} in z-".format(i%maxlayerzm+1) if (i<maxlayerzm) else "Layer {:02d} in z+".format(i%maxlayerzm+1), **_common_shared) for i in range(0,maxlayerzm)])
_sharedEnergy_layercluster_to_caloparticle_zminus = PlotGroup("sharedEnergy_layercluster_to_caloparticle_zminus", _shared_plots2_zminus, ncols=8)


_common_assoc = {#"title": "Cell Association Table in z-",
                 "stat": False,
                 "legend": False,
                 "xbinlabels": ["", "TN(pur)", "FN(ineff.)", "FP(fake)", "TP(eff)"],
                 "xbinlabeloption": "h",
                 "drawStyle": "hist",
                 "ymin": 0.1,
                 "ymax": 10000,
                 "ylog": True}
_common_assoc.update(_legend_common)
_cell_association_table_zminus = PlotGroup("cellAssociation_table_zminus", [
        Plot("cellAssociation_perlayer{:02d}".format(i), xtitle="Layer {:02d} in z-".format(i%maxlayerzm+1) if (i<maxlayerzm) else "Layer {:02d} in z+".format(i%maxlayerzm+1), **_common_assoc) for i in range(0,maxlayerzm)
        ], ncols=8 )

_bin_count = 0
_xbinlabels = [ "Layer {:02d}".format(i+1) for i in range(0,maxlayerzm) ]
_common_eff = {"stat": False, "legend": False, "xbinlabels": _xbinlabels, "xbinlabelsize": 12, "xbinlabeloptions": "v"}
_effplots_zminus = [Plot("effic_eta_layer{:02d}".format(i), xtitle="", **_common_eff) for i in range(0,maxlayerzm)]
_effplots_zminus.extend([Plot("effic_phi_layer{:02d}".format(i), xtitle="", **_common_eff) for i in range(0,maxlayerzm)])
_common_eff["xmin"] = 0.
_bin_count += maxlayerzm
_common_eff["xmax"] =_bin_count
_effplots_zminus.extend([Plot("globalEfficiencies", xtitle="Global Efficiencies in z-", **_common_eff)])
_efficiencies_zminus = PlotGroup("Efficiencies_zminus", _effplots_zminus, ncols=8)


_common_dup = {"stat": False, "legend": False, "title": "Global Duplicates in z-", "xbinlabels": _xbinlabels, "xbinlabelsize": 12, "xbinlabeloptions": "v"}
_dupplots_zminus = [Plot("duplicate_eta_layer{:02d}".format(i), xtitle="", **_common_dup) for i in range(0,maxlayerzm)]
_dupplots_zminus.extend([Plot("duplicate_phi_layer{:02d}".format(i), xtitle="", **_common_dup) for i in range(0,maxlayerzm)])
_common_dup["xmin"] = _bin_count+maxlayerzm+1
_bin_count += maxlayerzp
_common_dup["xmax"] = _bin_count
_dupplots_zminus.extend([Plot("globalEfficiencies", xtitle="Global Duplicates in z-", **_common_dup)])
_duplicates_zminus = PlotGroup("Duplicates_zminus", _dupplots_zminus, ncols=8)

_common_fake = {"stat": False, "legend": False, "title": "Global Fake Rates in z-", "xbinlabels": _xbinlabels, "xbinlabelsize": 12, "xbinlabeloptions": "v"}
_fakeplots_zminus = [Plot("fake_eta_layer{:02d}".format(i), xtitle="", **_common_fake) for i in range(0,maxlayerzm)]
_fakeplots_zminus.extend([Plot("fake_phi_layer{:02d}".format(i), xtitle="", **_common_fake) for i in range(0,maxlayerzm)])
_common_fake["xmin"] = _bin_count+maxlayerzm+1
_bin_count += maxlayerzp
_common_fake["xmax"] = _bin_count
_common_fake["xbinlabels"] = [ "Layer {:02d}".format(i+1) for i in range(0,maxlayerzm) ]
_common_fake["xbinlabelsize"] = 10.
_fakeplots_zminus.extend([Plot("globalEfficiencies", xtitle="Global Fake Rate in z-", **_common_fake)])
_fakes_zminus = PlotGroup("FakeRate_zminus", _fakeplots_zminus, ncols=8)

_common_merge = {"stat": False, "legend": False, "title": "Global Merge Rates in z-", "xbinlabels": _xbinlabels, "xbinlabelsize": 12, "xbinlabeloptions": "v"}
_mergeplots_zminus = [Plot("merge_eta_layer{:02d}".format(i), xtitle="", **_common_merge) for i in range(0,maxlayerzm)]
_mergeplots_zminus.extend([Plot("merge_phi_layer{:02d}".format(i), xtitle="", **_common_merge) for i in range(0,maxlayerzm)])
_common_merge["xmin"] = _bin_count+maxlayerzm+1
_bin_count += maxlayerzp
_common_merge["xmax"] = _bin_count
_common_merge["xbinlabels"] = [ "Layer {:02d}".format(i+1) for i in range(0,maxlayerzm) ]
_common_merge["xbinlabelsize"] = 10.
_mergeplots_zminus.extend([Plot("globalEfficiencies", xtitle="Global merge Rate in z-", **_common_merge)])
_merges_zminus = PlotGroup("MergeRate_zminus", _mergeplots_zminus, ncols=8)


_common_energy_score = dict(removeEmptyBins=True, xbinlabelsize=10, xbinlabeloption="d", ncols=4)
_energyscore_cp2lc_zminus = []
for i in range(0, maxlayerzm):
  _energyscore_cp2lc_zminus.append(PlotOnSideGroup("Energy_vs_Score_Layer{:02d}".format(i), Plot("Energy_vs_Score_caloparticle2layer_perlayer{:02d}".format(i), drawStyle="COLZ", adjustMarginLeft=0.1, adjustMarginRight=0.1, **_common_energy_score)))

_energyscore_lc2cp_zminus = []
for i in range(0, maxlayerzm):
  _energyscore_lc2cp_zminus.append(PlotOnSideGroup("Energy_vs_Score_Layer{:02d}".format(i), Plot("Energy_vs_Score_layer2caloparticle_perlayer{:02d}".format(i), drawStyle="COLZ", adjustMarginLeft=0.1, adjustMarginRight=0.1, **_common_energy_score)))
#_energyclustered =

#--------------------------------------------------------------------------------------------
# z+
#--------------------------------------------------------------------------------------------
_common_score = {"title": "Score CaloParticle to LayerClusters in z+",
                 "stat": False,
                 "ymin": 0.1,
                 "ymax": 1000,
                 "xmin": 0,
                 "xmax": 1,
                 "drawStyle": "hist",
                 "lineWidth": 1,
                 "ylog": True
                }
_common_score.update(_legend_common)
_score_caloparticle_to_layerclusters_zplus = PlotGroup("score_caloparticle_to_layercluster_zplus", [
        Plot("Score_caloparticle2layercl_perlayer{:02d}".format(i), xtitle="Layer {:02d} in z-".format(i%maxlayerzm+1) if (i<maxlayerzm) else "Layer {:02d} in z+".format(i%maxlayerzm+1), **_common_score) for i in range(maxlayerzm,maxlayerzp)
        ], ncols=8 )

_common_score = {"title": "Score LayerCluster to CaloParticles in z+",
                 "stat": False,
                 "ymin": 0.1,
                 "ymax": 1000,
                 "xmin": 0,
                 "xmax": 1,
                 "drawStyle": "hist",
                 "lineWidth": 1,
                 "ylog": True
                }
_common_score.update(_legend_common)
_score_layercluster_to_caloparticles_zplus = PlotGroup("score_layercluster_to_caloparticle_zplus", [
        Plot("Score_layercl2caloparticle_perlayer{:02d}".format(i), xtitle="Layer {:02d} in z-".format(i%maxlayerzm+1) if (i<maxlayerzm) else "Layer {:02d} in z+".format(i%maxlayerzm+1), **_common_score) for i in range(maxlayerzm,maxlayerzp)
        ], ncols=8 )

_common_shared= {"title": "Shared Energy CaloParticle To Layer Cluster in z+",
                 "stat": False,
                 "legend": False,
                }
_common_shared.update(_legend_common)
_shared_plots_zplus = [Plot("SharedEnergy_caloparticle2layercl_perlayer{:02d}".format(i), xtitle="Layer {:02d} in z-".format(i%maxlayerzm+1) if (i<maxlayerzm) else "Layer {:02d} in z+".format(i%maxlayerzm+1), **_common_shared) for i in range(maxlayerzm,maxlayerzp)]
_shared_plots_zplus.extend([Plot("SharedEnergy_caloparticle2layercl_vs_eta_perlayer{:02d}".format(i), xtitle="Layer {:02d} in z-".format(i%maxlayerzm+1) if (i<maxlayerzm) else "Layer {:02d} in z+".format(i%maxlayerzm+1), **_common_shared) for i in range(maxlayerzm,maxlayerzp)])
_shared_plots_zplus.extend([Plot("SharedEnergy_caloparticle2layercl_vs_phi_perlayer{:02d}".format(i), xtitle="Layer {:02d} in z-".format(i%maxlayerzm+1) if (i<maxlayerzm) else "Layer {:02d} in z+".format(i%maxlayerzm+1), **_common_shared) for i in range(maxlayerzm,maxlayerzp)])
_sharedEnergy_caloparticle_to_layercluster_zplus = PlotGroup("sharedEnergy_caloparticle_to_layercluster_zplus", _shared_plots_zplus, ncols=8)

_common_shared= {"title": "Shared Energy Layer Cluster To CaloParticle in z+",
                 "stat": False,
                 "legend": False,
                }
_common_shared.update(_legend_common)
_shared_plots2_zplus = [Plot("SharedEnergy_layercluster2caloparticle_perlayer{:02d}".format(i), xtitle="Layer {:02d} in z-".format(i%maxlayerzm+1) if (i<maxlayerzm) else "Layer {:02d} in z+".format(i%maxlayerzm+1), **_common_shared) for i in range(maxlayerzm,maxlayerzp)]
_shared_plots2_zplus.extend([Plot("SharedEnergy_layercl2caloparticle_vs_eta_perlayer{:02d}".format(i), xtitle="Layer {:02d} in z-".format(i%maxlayerzm+1) if (i<maxlayerzm) else "Layer {:02d} in z+".format(i%maxlayerzm+1), **_common_shared) for i in range(maxlayerzm,maxlayerzp)])
_shared_plots2_zplus.extend([Plot("SharedEnergy_layercl2caloparticle_vs_phi_perlayer{:02d}".format(i), xtitle="Layer {:02d} in z-".format(i%maxlayerzm+1) if (i<maxlayerzm) else "Layer {:02d} in z+".format(i%maxlayerzm+1), **_common_shared) for i in range(maxlayerzm,maxlayerzp)])
_sharedEnergy_layercluster_to_caloparticle_zplus = PlotGroup("sharedEnergy_layercluster_to_caloparticle_zplus", _shared_plots2_zplus, ncols=8)


_common_assoc = {#"title": "Cell Association Table in z+",
                 "stat": False,
                 "legend": False,
                 "xbinlabels": ["", "TN(pur)", "FN(ineff.)", "FP(fake)", "TP(eff)"],
                 "xbinlabeloption": "h",
                 "drawStyle": "hist",
                 "ymin": 0.1,
                 "ymax": 10000,
                 "ylog": True}
_common_assoc.update(_legend_common)
_cell_association_table_zplus = PlotGroup("cellAssociation_table_zplus", [
        Plot("cellAssociation_perlayer{:02d}".format(i), xtitle="Layer {:02d} in z-".format(i%maxlayerzm+1) if (i<maxlayerzm) else "Layer {:02d} in z+".format(i%maxlayerzm+1), **_common_assoc) for i in range(maxlayerzm,maxlayerzp)
        ], ncols=8 )

_bin_count = 0
_common_eff = {"stat": False, "legend": False, "xbinlabels": _xbinlabels, "xbinlabelsize": 12, "xbinlabeloptions": "v"}
_effplots_zplus = [Plot("effic_eta_layer{:02d}".format(i), xtitle="", **_common_eff) for i in range(maxlayerzm,maxlayerzp)]
_effplots_zplus.extend([Plot("effic_phi_layer{:02d}".format(i), xtitle="", **_common_eff) for i in range(maxlayerzm,maxlayerzp)])
_common_eff["xmin"] = maxlayerzm  
_bin_count += maxlayerzp
_common_eff["xmax"] =_bin_count
_effplots_zplus.extend([Plot("globalEfficiencies", xtitle="Global Efficiencies in z+", **_common_eff)])
_efficiencies_zplus = PlotGroup("Efficiencies_zplus", _effplots_zplus, ncols=8)


_common_dup = {"stat": False, "legend": False, "title": "Global Duplicates in z+", "xbinlabels": _xbinlabels, "xbinlabelsize": 12, "xbinlabeloptions": "v"}
_dupplots_zplus = [Plot("duplicate_eta_layer{:02d}".format(i), xtitle="", **_common_dup) for i in range(maxlayerzm,maxlayerzp)]
_dupplots_zplus.extend([Plot("duplicate_phi_layer{:02d}".format(i), xtitle="", **_common_dup) for i in range(maxlayerzm,maxlayerzp)])
_common_dup["xmin"] = _bin_count+maxlayerzm+1
_bin_count += maxlayerzp
_common_dup["xmax"] = _bin_count
_dupplots_zplus.extend([Plot("globalEfficiencies", xtitle="Global Duplicates in z+", **_common_dup)])
_duplicates_zplus = PlotGroup("Duplicates_zplus", _dupplots_zplus, ncols=8)

_common_fake = {"stat": False, "legend": False, "title": "Global Fake Rates in z+", "xbinlabels": _xbinlabels, "xbinlabelsize": 12, "xbinlabeloptions": "v"}
_fakeplots_zplus = [Plot("fake_eta_layer{:02d}".format(i), xtitle="", **_common_fake) for i in range(maxlayerzm,maxlayerzp)]
_fakeplots_zplus.extend([Plot("fake_phi_layer{:02d}".format(i), xtitle="", **_common_fake) for i in range(maxlayerzm,maxlayerzp)])
_common_fake["xmin"] = _bin_count+maxlayerzm+1
_bin_count += maxlayerzp
_common_fake["xmax"] = _bin_count
_fakeplots_zplus.extend([Plot("globalEfficiencies", xtitle="Global Fake Rate in z+", **_common_fake)])
_fakes_zplus = PlotGroup("FakeRate_zplus", _fakeplots_zplus, ncols=8)

_common_merge = {"stat": False, "legend": False, "title": "Global Merge Rates in z+", "xbinlabels": _xbinlabels, "xbinlabelsize": 12, "xbinlabeloptions": "v"}
_mergeplots_zplus = [Plot("merge_eta_layer{:02d}".format(i), xtitle="", **_common_merge) for i in range(maxlayerzm,maxlayerzp)]
_mergeplots_zplus.extend([Plot("merge_phi_layer{:02d}".format(i), xtitle="", **_common_merge) for i in range(maxlayerzm,maxlayerzp)])
_common_merge["xmin"] = _bin_count+maxlayerzm+1
_bin_count += maxlayerzp
_common_merge["xmax"] = _bin_count
_mergeplots_zplus.extend([Plot("globalEfficiencies", xtitle="Global merge Rate in z+", **_common_merge)])
_merges_zplus = PlotGroup("MergeRate_zplus", _mergeplots_zplus, ncols=8)


_common_energy_score = dict(removeEmptyBins=False, xbinlabelsize=10, xbinlabeloption="d", ncols=4)
_energyscore_cp2lc_zplus = []
for i in range(maxlayerzm,maxlayerzp):
  _energyscore_cp2lc_zplus.append(PlotOnSideGroup("Energy_vs_Score_Layer{:02d}".format(i), Plot("Energy_vs_Score_caloparticle2layer_perlayer{:02d}".format(i), drawStyle="COLZ", adjustMarginLeft=0.1, adjustMarginRight=0.1, **_common_energy_score)))

_energyscore_lc2cp_zplus = []
for i in range(maxlayerzm,maxlayerzp):
  _energyscore_lc2cp_zplus.append(PlotOnSideGroup("Energy_vs_Score_Layer{:02d}".format(i), Plot("Energy_vs_Score_layer2caloparticle_perlayer{:02d}".format(i), drawStyle="COLZ", adjustMarginLeft=0.1, adjustMarginRight=0.1, **_common_energy_score)))
#_energyclustered =

#=================================================================================================
hgcalLayerClustersPlotter = Plotter()
#We follow Chris categories in folders
# [A] calculated "energy density" for cells in a) 120um, b) 200um, c) 300um, d) scint
# (one entry per rechit, in the appropriate histo)
hgcalLayerClustersPlotter.append("CellsEnergyDensityPerThickness", [
        "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
        ], PlotFolder(
        _cellsenedens_thick,
        loopSubFolders=False,
        purpose=PlotPurpose.Timing, page="CellsEnergyDensityPerThickness"
        ))

# [B] number of layer clusters per event in a) 120um, b) 200um, c) 300um, d) scint
# (one entry per event in each of the four histos)
hgcalLayerClustersPlotter.append("TotalNumberofLayerClustersPerThickness", [
        "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
        ], PlotFolder(
        _totclusternum_thick,
        loopSubFolders=False,
        purpose=PlotPurpose.Timing, page="TotalNumberofLayerClustersPerThickness"
        ))

# [C] number of layer clusters per layer (one entry per event in each histo)
# z-
hgcalLayerClustersPlotter.append("NumberofLayerClustersPerLayer_zminus", [
        "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
        ], PlotFolder(
        _totclusternum_layer_EE_zminus,
        _totclusternum_layer_FH_zminus,
        _totclusternum_layer_BH_zminus,
        loopSubFolders=False,
        purpose=PlotPurpose.Timing, page="NumberofLayerClustersPerLayer_zminus"   
        ))

# z+
hgcalLayerClustersPlotter.append("NumberofLayerClustersPerLayer_zplus", [
        "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
        ], PlotFolder(
        _totclusternum_layer_EE_zplus,
        _totclusternum_layer_FH_zplus,
        _totclusternum_layer_BH_zplus,
        loopSubFolders=False,
        purpose=PlotPurpose.Timing, page="NumberofLayerClustersPerLayer_zplus"   
        ))

# [D] For each layer cluster:
# number of cells in layer cluster, by layer - separate histos in each layer for 120um Si, 200/300um Si, Scint
# NB: not all combinations exist; e.g. no 120um Si in layers with scint.
# (One entry in the appropriate histo per layer cluster).
# z-
hgcalLayerClustersPlotter.append("CellsNumberPerLayerPerThickness_zminus", [
        "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
        ], PlotFolder(
        _cellsnum_perthick_perlayer_120_EE_zminus,
        _cellsnum_perthick_perlayer_120_FH_zminus,
        _cellsnum_perthick_perlayer_120_BH_zminus,
        _cellsnum_perthick_perlayer_200_EE_zminus,
        _cellsnum_perthick_perlayer_200_FH_zminus,
        _cellsnum_perthick_perlayer_200_BH_zminus,
        _cellsnum_perthick_perlayer_300_EE_zminus,
        _cellsnum_perthick_perlayer_300_FH_zminus,
        _cellsnum_perthick_perlayer_300_BH_zminus,
        _cellsnum_perthick_perlayer_scint_EE_zminus,
        _cellsnum_perthick_perlayer_scint_FH_zminus,
        _cellsnum_perthick_perlayer_scint_BH_zminus,
        loopSubFolders=False,
        purpose=PlotPurpose.Timing, page="CellsNumberPerLayerPerThickness_zminus"   
        ))

# z+
hgcalLayerClustersPlotter.append("CellsNumberPerLayerPerThickness_zplus", [
        "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
        ], PlotFolder(
        _cellsnum_perthick_perlayer_120_EE_zplus,
        _cellsnum_perthick_perlayer_120_FH_zplus,
        _cellsnum_perthick_perlayer_120_BH_zplus,
        _cellsnum_perthick_perlayer_200_EE_zplus,
        _cellsnum_perthick_perlayer_200_FH_zplus,
        _cellsnum_perthick_perlayer_200_BH_zplus,
        _cellsnum_perthick_perlayer_300_EE_zplus,
        _cellsnum_perthick_perlayer_300_FH_zplus,
        _cellsnum_perthick_perlayer_300_BH_zplus,
        _cellsnum_perthick_perlayer_scint_EE_zplus,
        _cellsnum_perthick_perlayer_scint_FH_zplus,
        _cellsnum_perthick_perlayer_scint_BH_zplus,
        loopSubFolders=False,
        purpose=PlotPurpose.Timing, page="CellsNumberPerLayerPerThickness_zplus"   
        ))

# [E] For each layer cluster:
# distance of cells from a) seed cell, b) max cell; and c), d): same with entries weighted by cell energy
# separate histos in each layer for 120um Si, 200/300um Si, Scint
# NB: not all combinations exist; e.g. no 120um Si in layers with scint.
# (One entry in each of the four appropriate histos per cell in a layer cluster)
# z-
hgcalLayerClustersPlotter.append("CellsDistanceToSeedAndMaxCellPerLayerPerThickness_zminus", [
        "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
        ], PlotFolder(
        _distancetomaxcell_perthickperlayer_120_EE_zminus,
        _distancetomaxcell_perthickperlayer_120_FH_zminus,
        _distancetomaxcell_perthickperlayer_120_BH_zminus,
        _distancetomaxcell_perthickperlayer_200_EE_zminus,
        _distancetomaxcell_perthickperlayer_200_FH_zminus,
        _distancetomaxcell_perthickperlayer_200_BH_zminus,
        _distancetomaxcell_perthickperlayer_300_EE_zminus,
        _distancetomaxcell_perthickperlayer_300_FH_zminus,
        _distancetomaxcell_perthickperlayer_300_BH_zminus,
        _distancetomaxcell_perthickperlayer_scint_EE_zminus,
        _distancetomaxcell_perthickperlayer_scint_FH_zminus,
        _distancetomaxcell_perthickperlayer_scint_BH_zminus,
        _distancetoseedcell_perthickperlayer_120_EE_zminus,
        _distancetoseedcell_perthickperlayer_120_FH_zminus,
        _distancetoseedcell_perthickperlayer_120_BH_zminus,
        _distancetoseedcell_perthickperlayer_200_EE_zminus,
        _distancetoseedcell_perthickperlayer_200_FH_zminus,
        _distancetoseedcell_perthickperlayer_200_BH_zminus,
        _distancetoseedcell_perthickperlayer_300_EE_zminus,
        _distancetoseedcell_perthickperlayer_300_FH_zminus,
        _distancetoseedcell_perthickperlayer_300_BH_zminus,
        _distancetoseedcell_perthickperlayer_scint_EE_zminus,
        _distancetoseedcell_perthickperlayer_scint_FH_zminus,
        _distancetoseedcell_perthickperlayer_scint_BH_zminus,
        _distancetomaxcell_perthickperlayer_eneweighted_120_EE_zminus,
        _distancetomaxcell_perthickperlayer_eneweighted_120_FH_zminus,
        _distancetomaxcell_perthickperlayer_eneweighted_120_BH_zminus,
        _distancetomaxcell_perthickperlayer_eneweighted_200_EE_zminus,
        _distancetomaxcell_perthickperlayer_eneweighted_200_FH_zminus,
        _distancetomaxcell_perthickperlayer_eneweighted_200_BH_zminus,
        _distancetomaxcell_perthickperlayer_eneweighted_300_EE_zminus,
        _distancetomaxcell_perthickperlayer_eneweighted_300_FH_zminus,
        _distancetomaxcell_perthickperlayer_eneweighted_300_BH_zminus,
        _distancetomaxcell_perthickperlayer_eneweighted_scint_EE_zminus,
        _distancetomaxcell_perthickperlayer_eneweighted_scint_FH_zminus,
        _distancetomaxcell_perthickperlayer_eneweighted_scint_BH_zminus,
        _distancetoseedcell_perthickperlayer_eneweighted_120_EE_zminus,
        _distancetoseedcell_perthickperlayer_eneweighted_120_FH_zminus,
        _distancetoseedcell_perthickperlayer_eneweighted_120_BH_zminus,
        _distancetoseedcell_perthickperlayer_eneweighted_200_EE_zminus,
        _distancetoseedcell_perthickperlayer_eneweighted_200_FH_zminus,
        _distancetoseedcell_perthickperlayer_eneweighted_200_BH_zminus,
        _distancetoseedcell_perthickperlayer_eneweighted_300_EE_zminus,
        _distancetoseedcell_perthickperlayer_eneweighted_300_FH_zminus,
        _distancetoseedcell_perthickperlayer_eneweighted_300_BH_zminus,
        _distancetoseedcell_perthickperlayer_eneweighted_scint_EE_zminus,
        _distancetoseedcell_perthickperlayer_eneweighted_scint_FH_zminus,
        _distancetoseedcell_perthickperlayer_eneweighted_scint_BH_zminus,
        _distancebetseedandmaxcell_perthickperlayer_120_EE_zminus,
        _distancebetseedandmaxcell_perthickperlayer_120_FH_zminus,
        _distancebetseedandmaxcell_perthickperlayer_120_BH_zminus,
        _distancebetseedandmaxcell_perthickperlayer_200_EE_zminus,
        _distancebetseedandmaxcell_perthickperlayer_200_FH_zminus,
        _distancebetseedandmaxcell_perthickperlayer_200_BH_zminus,
        _distancebetseedandmaxcell_perthickperlayer_300_EE_zminus,
        _distancebetseedandmaxcell_perthickperlayer_300_FH_zminus,
        _distancebetseedandmaxcell_perthickperlayer_300_BH_zminus,
        _distancebetseedandmaxcell_perthickperlayer_scint_EE_zminus,
        _distancebetseedandmaxcell_perthickperlayer_scint_FH_zminus,
        _distancebetseedandmaxcell_perthickperlayer_scint_BH_zminus,
        _distancebetseedandmaxcellvsclusterenergy_perthickperlayer_120_EE_zminus,
        _distancebetseedandmaxcellvsclusterenergy_perthickperlayer_120_FH_zminus,
        _distancebetseedandmaxcellvsclusterenergy_perthickperlayer_120_BH_zminus,
        _distancebetseedandmaxcellvsclusterenergy_perthickperlayer_200_EE_zminus,
        _distancebetseedandmaxcellvsclusterenergy_perthickperlayer_200_FH_zminus,
        _distancebetseedandmaxcellvsclusterenergy_perthickperlayer_200_BH_zminus,
        _distancebetseedandmaxcellvsclusterenergy_perthickperlayer_300_EE_zminus,
        _distancebetseedandmaxcellvsclusterenergy_perthickperlayer_300_FH_zminus,
        _distancebetseedandmaxcellvsclusterenergy_perthickperlayer_300_BH_zminus,
        _distancebetseedandmaxcellvsclusterenergy_perthickperlayer_scint_EE_zminus,
        _distancebetseedandmaxcellvsclusterenergy_perthickperlayer_scint_FH_zminus,
        _distancebetseedandmaxcellvsclusterenergy_perthickperlayer_scint_BH_zminus,
        loopSubFolders=False,
        purpose=PlotPurpose.Timing, page="CellsDistanceToSeedAndMaxCellPerLayerPerThickness_zminus"   
        ))

# z+
hgcalLayerClustersPlotter.append("CellsDistanceToSeedAndMaxCellPerLayerPerThickness_zplus", [
        "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
        ], PlotFolder(
        _distancetomaxcell_perthickperlayer_120_EE_zplus,
        _distancetomaxcell_perthickperlayer_120_FH_zplus,
        _distancetomaxcell_perthickperlayer_120_BH_zplus,
        _distancetomaxcell_perthickperlayer_200_EE_zplus,
        _distancetomaxcell_perthickperlayer_200_FH_zplus,
        _distancetomaxcell_perthickperlayer_200_BH_zplus,
        _distancetomaxcell_perthickperlayer_300_EE_zplus,
        _distancetomaxcell_perthickperlayer_300_FH_zplus,
        _distancetomaxcell_perthickperlayer_300_BH_zplus,
        _distancetomaxcell_perthickperlayer_scint_EE_zplus,
        _distancetomaxcell_perthickperlayer_scint_FH_zplus,
        _distancetomaxcell_perthickperlayer_scint_BH_zplus,
        _distancetoseedcell_perthickperlayer_120_EE_zplus,
        _distancetoseedcell_perthickperlayer_120_FH_zplus,
        _distancetoseedcell_perthickperlayer_120_BH_zplus,
        _distancetoseedcell_perthickperlayer_200_EE_zplus,
        _distancetoseedcell_perthickperlayer_200_FH_zplus,
        _distancetoseedcell_perthickperlayer_200_BH_zplus,
        _distancetoseedcell_perthickperlayer_300_EE_zplus,
        _distancetoseedcell_perthickperlayer_300_FH_zplus,
        _distancetoseedcell_perthickperlayer_300_BH_zplus,
        _distancetoseedcell_perthickperlayer_scint_EE_zplus,
        _distancetoseedcell_perthickperlayer_scint_FH_zplus,
        _distancetoseedcell_perthickperlayer_scint_BH_zplus,
        _distancetomaxcell_perthickperlayer_eneweighted_120_EE_zplus,
        _distancetomaxcell_perthickperlayer_eneweighted_120_FH_zplus,
        _distancetomaxcell_perthickperlayer_eneweighted_120_BH_zplus,
        _distancetomaxcell_perthickperlayer_eneweighted_200_EE_zplus,
        _distancetomaxcell_perthickperlayer_eneweighted_200_FH_zplus,
        _distancetomaxcell_perthickperlayer_eneweighted_200_BH_zplus,
        _distancetomaxcell_perthickperlayer_eneweighted_300_EE_zplus,
        _distancetomaxcell_perthickperlayer_eneweighted_300_FH_zplus,
        _distancetomaxcell_perthickperlayer_eneweighted_300_BH_zplus,
        _distancetomaxcell_perthickperlayer_eneweighted_scint_EE_zplus,
        _distancetomaxcell_perthickperlayer_eneweighted_scint_FH_zplus,
        _distancetomaxcell_perthickperlayer_eneweighted_scint_BH_zplus,
        _distancetoseedcell_perthickperlayer_eneweighted_120_EE_zplus,
        _distancetoseedcell_perthickperlayer_eneweighted_120_FH_zplus,
        _distancetoseedcell_perthickperlayer_eneweighted_120_BH_zplus,
        _distancetoseedcell_perthickperlayer_eneweighted_200_EE_zplus,
        _distancetoseedcell_perthickperlayer_eneweighted_200_FH_zplus,
        _distancetoseedcell_perthickperlayer_eneweighted_200_BH_zplus,
        _distancetoseedcell_perthickperlayer_eneweighted_300_EE_zplus,
        _distancetoseedcell_perthickperlayer_eneweighted_300_FH_zplus,
        _distancetoseedcell_perthickperlayer_eneweighted_300_BH_zplus,
        _distancetoseedcell_perthickperlayer_eneweighted_scint_EE_zplus,
        _distancetoseedcell_perthickperlayer_eneweighted_scint_FH_zplus,
        _distancetoseedcell_perthickperlayer_eneweighted_scint_BH_zplus,
        _distancebetseedandmaxcell_perthickperlayer_120_EE_zplus,
        _distancebetseedandmaxcell_perthickperlayer_120_FH_zplus,
        _distancebetseedandmaxcell_perthickperlayer_120_BH_zplus,
        _distancebetseedandmaxcell_perthickperlayer_200_EE_zplus,
        _distancebetseedandmaxcell_perthickperlayer_200_FH_zplus,
        _distancebetseedandmaxcell_perthickperlayer_200_BH_zplus,
        _distancebetseedandmaxcell_perthickperlayer_300_EE_zplus,
        _distancebetseedandmaxcell_perthickperlayer_300_FH_zplus,
        _distancebetseedandmaxcell_perthickperlayer_300_BH_zplus,
        _distancebetseedandmaxcell_perthickperlayer_scint_EE_zplus,
        _distancebetseedandmaxcell_perthickperlayer_scint_FH_zplus,
        _distancebetseedandmaxcell_perthickperlayer_scint_BH_zplus,
        _distancebetseedandmaxcellvsclusterenergy_perthickperlayer_120_EE_zplus,
        _distancebetseedandmaxcellvsclusterenergy_perthickperlayer_120_FH_zplus,
        _distancebetseedandmaxcellvsclusterenergy_perthickperlayer_120_BH_zplus,
        _distancebetseedandmaxcellvsclusterenergy_perthickperlayer_200_EE_zplus,
        _distancebetseedandmaxcellvsclusterenergy_perthickperlayer_200_FH_zplus,
        _distancebetseedandmaxcellvsclusterenergy_perthickperlayer_200_BH_zplus,
        _distancebetseedandmaxcellvsclusterenergy_perthickperlayer_300_EE_zplus,
        _distancebetseedandmaxcellvsclusterenergy_perthickperlayer_300_FH_zplus,
        _distancebetseedandmaxcellvsclusterenergy_perthickperlayer_300_BH_zplus,
        _distancebetseedandmaxcellvsclusterenergy_perthickperlayer_scint_EE_zplus,
        _distancebetseedandmaxcellvsclusterenergy_perthickperlayer_scint_FH_zplus,
        _distancebetseedandmaxcellvsclusterenergy_perthickperlayer_scint_BH_zplus,
        loopSubFolders=False,
        purpose=PlotPurpose.Timing, page="CellsDistanceToSeedAndMaxCellPerLayerPerThickness_zplus"   
        ))

# [F] Looking at the fraction of true energy that has been clustered; by layer and overall
# z-
hgcalLayerClustersPlotter.append("EnergyClusteredByLayerAndOverall_zminus", [
        "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
        ], PlotFolder(
        _energyclustered_perlayer_EE_zminus,
        _energyclustered_perlayer_FH_zminus,
        _energyclustered_perlayer_BH_zminus,
        loopSubFolders=False,
        purpose=PlotPurpose.Timing, page="EnergyClusteredByLayerAndOverall_zminus"   
        ))
# z+
hgcalLayerClustersPlotter.append("EnergyClusteredByLayerAndOverall_zplus", [
        "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
        ], PlotFolder(
        _energyclustered_perlayer_EE_zplus,
        _energyclustered_perlayer_FH_zplus,
        _energyclustered_perlayer_BH_zplus,
        loopSubFolders=False,
        purpose=PlotPurpose.Timing, page="EnergyClusteredByLayerAndOverall_zplus"   
        ))

# [G] Miscellaneous plots:
# longdepthbarycentre: The longitudinal depth barycentre. One entry per event.
# mixedhitscluster: Number of clusters per event with hits in different thicknesses.
# num_reco_cluster_eta: Number of reco clusters vs eta

hgcalLayerClustersPlotter.append("Miscellaneous", [
            "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
            ], PlotFolder(
            _num_reco_cluster_eta,
            _energyclustered,
            _mixedhitsclusters,
            _longdepthbarycentre,
            loopSubFolders=False,
            purpose=PlotPurpose.Timing, page="Miscellaneous"
            ))

# [H] SelectedCaloParticles plots
hgcalLayerClustersPlotter.append("SelectedCaloParticles_Photons", [
            "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/SelectedCaloParticles/22",
            ], PlotFolder(
            _SelectedCaloParticles,
            loopSubFolders=False,
            purpose=PlotPurpose.Timing, page="SelectedCaloParticles_Photons"
            ))

# [I] Score of CaloParticles wrt Layer Clusters
# z-
hgcalLayerClustersPlotter.append("ScoreCaloParticlesToLayerClusters_zminus", [
            "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
            ], PlotFolder(
            _score_caloparticle_to_layerclusters_zminus,
            loopSubFolders=False,
            purpose=PlotPurpose.Timing, page="ScoreCaloParticlesToLayerClusters_zminus"))

# z+
hgcalLayerClustersPlotter.append("ScoreCaloParticlesToLayerClusters_zplus", [
            "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
            ], PlotFolder(
            _score_caloparticle_to_layerclusters_zplus,
            loopSubFolders=False,
            purpose=PlotPurpose.Timing, page="ScoreCaloParticlesToLayerClusters_zplus"))

# [J] Score of LayerClusters wrt CaloParticles
# z-
hgcalLayerClustersPlotter.append("ScoreLayerClustersToCaloParticles_zminus", [
            "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
            ], PlotFolder(
            _score_layercluster_to_caloparticles_zminus,
            loopSubFolders=False,
            purpose=PlotPurpose.Timing, page="ScoreLayerClustersToCaloParticles_zminus"))

# z+
hgcalLayerClustersPlotter.append("ScoreLayerClustersToCaloParticles_zplus", [
            "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
            ], PlotFolder(
            _score_layercluster_to_caloparticles_zplus,
            loopSubFolders=False,
            purpose=PlotPurpose.Timing, page="ScoreLayerClustersToCaloParticles_zplus"))

# [K] Shared Energy between CaloParticle and LayerClusters
# z-
hgcalLayerClustersPlotter.append("SharedEnergy_zminus", [
            "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
            ], PlotFolder(
            _sharedEnergy_caloparticle_to_layercluster_zminus,
            loopSubFolders=False,
            purpose=PlotPurpose.Timing, page="SharedEnergyCaloParticleToLayerCluster_zminus"))

# z+
hgcalLayerClustersPlotter.append("SharedEnergy_zplus", [
            "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
            ], PlotFolder(
            _sharedEnergy_caloparticle_to_layercluster_zplus,
            loopSubFolders=False,
            purpose=PlotPurpose.Timing, page="SharedEnergyCaloParticleToLayerCluster_zplus"))

# [K2] Shared Energy between LayerClusters and CaloParticle
# z-
hgcalLayerClustersPlotter.append("SharedEnergy_zminus", [
            "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
            ], PlotFolder(
            _sharedEnergy_layercluster_to_caloparticle_zminus,
            loopSubFolders=False,
            purpose=PlotPurpose.Timing, page="SharedEnergyLayerClusterToCaloParticle_zminus"))

# z+
hgcalLayerClustersPlotter.append("SharedEnergy_zplus", [
            "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
            ], PlotFolder(
            _sharedEnergy_layercluster_to_caloparticle_zplus,
            loopSubFolders=False,
            purpose=PlotPurpose.Timing, page="SharedEnergyLayerClusterToCaloParticle_zplus"))

# [L] Cell Association per Layer
# z-
hgcalLayerClustersPlotter.append("CellAssociation_zminus", [
            "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
            ], PlotFolder(
            _cell_association_table_zminus,
            loopSubFolders=False,
            purpose=PlotPurpose.Timing, page="CellAssociation_zminus"))

# z+
hgcalLayerClustersPlotter.append("CellAssociation_zplus", [
            "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
            ], PlotFolder(
            _cell_association_table_zplus,
            loopSubFolders=False,
            purpose=PlotPurpose.Timing, page="CellAssociation_zplus"))

# [M] Efficiency Plots
# z-
hgcalLayerClustersPlotter.append("Efficiencies_zminus", [
            "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
            ], PlotFolder(
            _efficiencies_zminus,
            loopSubFolders=False,
            purpose=PlotPurpose.Timing, page="Efficiencies_zminus"))

# z+
hgcalLayerClustersPlotter.append("Efficiencies_zplus", [
            "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
            ], PlotFolder(
            _efficiencies_zplus,
            loopSubFolders=False,
            purpose=PlotPurpose.Timing, page="Efficiencies_zplus"))

# [L] Duplicate Plots
# z-
hgcalLayerClustersPlotter.append("Duplicates_zminus", [
            "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
            ], PlotFolder(
            _duplicates_zminus,
            loopSubFolders=False,
            purpose=PlotPurpose.Timing, page="Duplicates_zminus"))

# z+
hgcalLayerClustersPlotter.append("Duplicates_zplus", [
            "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
            ], PlotFolder(
            _duplicates_zplus,
            loopSubFolders=False,
            purpose=PlotPurpose.Timing, page="Duplicates_zplus"))

# [M] Fake Rate Plots
# z-
hgcalLayerClustersPlotter.append("FakeRate_zminus", [
            "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
            ], PlotFolder(
            _fakes_zminus,
            loopSubFolders=False,
            purpose=PlotPurpose.Timing, page="Fakes_zminus"))

# z+
hgcalLayerClustersPlotter.append("FakeRate_zplus", [
            "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
            ], PlotFolder(
            _fakes_zplus,
            loopSubFolders=False,
            purpose=PlotPurpose.Timing, page="Fakes_zplus"))

# [N] Merge Rate Plots
# z-
hgcalLayerClustersPlotter.append("MergeRate_zminus", [
            "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
            ], PlotFolder(
            _merges_zminus,
            loopSubFolders=False,
            purpose=PlotPurpose.Timing, page="Merges_zminus"))

# z+
hgcalLayerClustersPlotter.append("MergeRate_zplus", [
            "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
            ], PlotFolder(
            _merges_zplus,
            loopSubFolders=False,
            purpose=PlotPurpose.Timing, page="Merges_zplus"))

# [O] Energy vs Score 2D plots CP to LC
# z-
for i,item in enumerate(_energyscore_cp2lc_zminus, start=1):
  hgcalLayerClustersPlotter.append("Energy_vs_Score_CP2LC_zminus", [
              "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
              ], PlotFolder(
              item,
              loopSubFolders=False,
              purpose=PlotPurpose.Timing, page="Energy_vs_Score_CP2LC_zminus"))

# z+
for i,item in enumerate(_energyscore_cp2lc_zplus, start=1):
  hgcalLayerClustersPlotter.append("Energy_vs_Score_CP2LC_zplus", [
              "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
              ], PlotFolder(
              item,
              loopSubFolders=False,
              purpose=PlotPurpose.Timing, page="Energy_vs_Score_CP2LC_zplus"))

# [P] Energy vs Score 2D plots LC to CP
# z-
for i,item in enumerate(_energyscore_lc2cp_zminus, start=1):
  hgcalLayerClustersPlotter.append("Energy_vs_Score_LC2CP_zminus", [
              "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
              ], PlotFolder(
              item,
              loopSubFolders=False,
              purpose=PlotPurpose.Timing, page="Energy_vs_Score_LC2CP_zminus"))

# z+
for i,item in enumerate(_energyscore_lc2cp_zplus, start=1):
  hgcalLayerClustersPlotter.append("Energy_vs_Score_LC2CP_zplus", [
              "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/hgcalLayerClusters",
              ], PlotFolder(
              item,
              loopSubFolders=False,
              purpose=PlotPurpose.Timing, page="Energy_vs_Score_LC2CP_zplus"))

