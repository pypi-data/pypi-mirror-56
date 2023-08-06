#! /usr/bin/python
# -*- coding: utf-8 -*-

# import logging
# logger = logging.getLogger(__name__)
from loguru import logger
import unittest
import io3d

# import openslide
import scaffan
import scaffan.algorithm
import numpy as np
import os.path as op
import os
import shutil
from pathlib import Path


class LobulusTest(unittest.TestCase):
    def test_run_lobuluses(self):
        output_dir = Path("test_lobulus_output_dir").absolute()
        if output_dir.exists():
            shutil.rmtree(output_dir)
            # os.remove(output_dir)
        # fn = io3d.datasets.join_path("medical", "orig", "CMU-1.ndpi", get_root=True)
        fn = io3d.datasets.join_path(
            "medical", "orig", "sample_data", "SCP003", "SCP003.ndpi", get_root=True
        )
        # fn = io3d.datasets.join_path("scaffold", "Hamamatsu", "PIG-003_J-18-0165_HE.ndpi", get_root=True)
        # imsl = openslide.OpenSlide(fn)
        # annotations = scan.read_annotations(fn)
        # scan.annotations_to_px(imsl, annotations)
        mainapp = scaffan.algorithm.Scaffan()
        mainapp.set_input_file(fn)
        mainapp.set_output_dir(str(output_dir))
        mainapp.init_run()
        mainapp.set_report_level(10)
        # Yellow
        mainapp.set_annotation_color_selection("#FFFF00")
        # mainapp.parameters.param("Processing", "Show").setValue(True)
        mainapp.run_lobuluses()
        logger.debug("imgs: ", mainapp.report.imgs)

        img = mainapp.report.load_array("lobulus_central_thr_skeleton_7.png")
        imsz = np.prod(img.shape)
        lobulus_size = np.sum(img == 1) / imsz
        central_vein_size = np.sum(img == 2) / imsz
        thr_size = np.sum(img == 3) / imsz
        skeleton_size = np.sum(img == 4) / imsz
        self.assertGreater(lobulus_size, 0.10, "Lobulus size 10%")
        self.assertGreater(central_vein_size, 0.001, "Central vein size 0.1%")
        self.assertGreater(thr_size, 0.001, "Threshold size 0.1%")
        self.assertGreater(skeleton_size, 0.001, "Skeleton size 0.1%")
        self.assertGreater(thr_size, skeleton_size, "More threshold than Skeleton")

        self.assertTrue((output_dir/"lobulus_central_thr_skeleton_7.png").exists())
        self.assertTrue((output_dir/"lobulus_central_thr_skeleton_7_skimage.png").exists())
        self.assertTrue((output_dir/"data.xlsx").exists())

        self.assertLess(0.6, mainapp.evaluation.evaluation_history[0]["Lobulus Border Dice"],
                        "Lobulus segmentation should have Dice coefficient above some low level")
        # self.assertLess(0.6, mainapp.evaluation.evaluation_history[1]["Lobulus Border Dice"],
        #                 "Lobulus segmentation should have Dice coefficient above some low level")
        self.assertLess(0.2, mainapp.evaluation.evaluation_history[0]["Central Vein Dice"],
                        "Central Vein segmentation should have Dice coefficient above some low level")
        # mainapp.start_gui()
