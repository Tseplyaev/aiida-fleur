# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c), Forschungszentrum Jülich GmbH, IAS-1/PGI-1, Germany.         #
#                All rights reserved.                                         #
# This file is part of the AiiDA-FLEUR package.                               #
#                                                                             #
# The code is hosted on GitHub at https://github.com/broeder-j/aiida-fleur    #
# For further information on the license, see the LICENSE.txt file            #
# For further information please visit http://www.flapw.de or                 #
# http://aiida-fleur.readthedocs.io/en/develop/                               #
###############################################################################

# Here we test if the interfaces of the workflows are still the same
import pytest

@pytest.mark.usefixtures("aiida_env")
class TestFleur_workflow_interfaces:#TestAiida_fleur_entrypoints
    """
    Test all aiida-fleur workflow interfaces
    """
    # TODO
    # prepare some nodes:
    # structure, option, fleurinp, wfparameters
    # add to builder and see if he takes it
    # ggf if possible run initial step only, that the input is checked...
    
    def test_fleur_scf_wc_init(aiida_env):
        """
        Test the interface of the scf workchain
        """
        from aiida_fleur.workflows.scf import fleur_scf_wc
        
        builder = fleur_scf_wc.get_builder()

        
    def test_fleur_eos_wc_init(aiida_env):
        """
        Test the interface of the eos workchain
        """
        from aiida_fleur.workflows.eos import fleur_eos_wc
        
        builder = fleur_eos_wc.get_builder()


    def test_fleur_dos_wc_init(aiida_env):
        """
        Test the interface of the dos workchain
        """
        from aiida_fleur.workflows.dos import fleur_dos_wc
        
        builder = fleur_dos_wc.get_builder()


    def test_fleur_band_wc_init(aiida_env):
        """
        Test the interface of the band workchain
        """
        from aiida_fleur.workflows.scf import fleur_scf_wc
        
        builder = fleur_scf_wc.get_builder()


    #def test_fleur_band2_wc_init(aiida_env):
    #    """
    #    Test the interface of the band2 workchain
    #    """
    #    from aiida_fleur.workflows.band2 import fleur_band2_wc
    #    
    #    builder = fleur_band2_wc.get_builder()


    def test_fleur_corehole_wc_init(aiida_env):
        """
        Test the interface of the corehole workchain
        """
        from aiida_fleur.workflows.corehole import fleur_corehole_wc
        
        builder = fleur_corehole_wc.get_builder()


    def test_fleur_initial_cls_wc_init(aiida_env):
        """
        Test the interface of the scf workchain
        """
        from aiida_fleur.workflows.initial_cls import fleur_initial_cls_wc
        
        builder = fleur_initial_cls_wc.get_builder()


    def test_fleur_delta_wc_init(aiida_env):
        """
        Test the interface of the delta workchain
        """
        from aiida_fleur.workflows.delta import fleur_delta_wc
        
        builder = fleur_delta_wc.get_builder()


    def test_fleur_relax_wc_init(aiida_env):
        """
        Test the interface of the relax workchain
        """
        from aiida_fleur.workflows.relax import fleur_relax_wc
        
        builder = fleur_relax_wc.get_builder()


    def test_fleur_optimize_para_wc_init(aiida_env):
        """
        Test the interface of the optimize_para_ workchain
        """
        from aiida_fleur.workflows.optimize_para import fleur_optimize_parameters_wc
        
        builder = fleur_optimize_parameters_wc.get_builder()