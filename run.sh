#!/usr/bin/env bash
python eye-detection.py
sleep 2s
python label_image.py --graph retrained_graph.pb --labels retrained_labels.txt --input_layer Placeholder --output_layer final_result --image face.jpg
