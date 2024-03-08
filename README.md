# SVAVOT
1st on VOTS2023 Benchmark (up to march 2024)

IMPORTANT: Read this file in Raw mode, cause you can see the Tab Spaces!! Thanks :)

In order to make the entire pipeline work, you should evaluate DMAOT and HQTrack on VOT Toolkit 4 sequence test (the ones needed for training) and on the 144 Challenge sequences (the ones needed for the test).
Once you have these data, you would store them in this directory structure:
-svavot
  -dmaot_train
    --cat-18
    --ecc.....
  -dmaot_test
    --animal
    --ecc.....
  -hqtrack_train
    --cat-18
    --ecc.....
  -hqtrack_test
    --animal
    --ecc.....
Files inside the sequence folders should be named "nameofthesequence_001" if one target is in, otherwise "nameofthesequence_obj1_001", "nameofthesequence_obj2_001", ecc.. 
Don't forget to store even "_time.value" files. The template is "nameofthesequence_obj1_001_time.value" ecc....

Instead, groundtruth files from VOT Toolkit:
-svavot
  -groundtruth_train
    --color (where all the frames are stored)
    --cat-18
      --cat-18_1_001.txt
      --cat-18_2_001.txt
      --ecc...
  -groundtruth_test
    --sequences
      --color (where all the frames are stored)
      --groundtruth.txt (if 1 target is present)
      --groundtruth_obj1.txt (if more targets are present)
      --groundtruth_obj2.txt.....

Last, create a folder under svavot called "my_groundtruth_hard", for making training labels.

Put all the files in the repo under svavot and then execute in order:
1) label_maker.py
2) make_features_for_svm_train.py
3) make_features_for_svm_test.py
4) svm.py (will create the pkl file already in the repo)
5) create a directory "baseline"
6) make_file_from_svm_results.py
7) results_process_video.py (if you want to create a video of your results, change the name of the sequence where it is required in the file)
8) extract_frames.py (if you need some frames of the output video, just change the name of the sequence where it is required in the file)
9)  

      
