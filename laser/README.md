
Connect laser module to FAN output - between bed heat and nozzle heat outputs. Fasten with zip tie.

Distance to wood ~20 mm. Move head with "disable steppers"

Calibrate distance with focus.gcode

Check time and dot size with test_dot_size.py

-

Get black and white pic. GIMP - Image-Mode-Greyscale   then  Colors-BrigghtnessContrast   File-Export as...

Top will be at Y0, right at X0.

	python3 _generate_straight.py woman_welder_small.png > woman.gcode

Change pic size according to script output
; Dot count 73296
; Width 112.6 mm
; Height 168.0 mm

Calibrate position with highlight.gcode - fix with tape!
