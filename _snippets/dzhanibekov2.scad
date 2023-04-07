
SZ = 30;

SHAFT_D = 3;
BEARING_D = 8;
middle_d = (SHAFT_D + BEARING_D) / 2;
BEARING_W = 3;
BEARING_HOLE = SHAFT_D;
WINDADGE = 0.6;

module reel(outer_d, inner_d, h) {
    half_d = (outer_d + inner_d) / 2;
    translate([0,0,h/2]) difference() {
        // main body
        cylinder(d=outer_d, h=h, center=true);
        // center hole
        cylinder(d=inner_d, h=2*h, center=true);
        // torus
        rotate_extrude(angle=360,convexity=2) translate([outer_d*1.15/2,0,0]) circle(d=h);
        // slits for thread
        for(i = [1:6]) rotate([0,0,i*60]) cube([WINDADGE, 1000, 1000], center=true);
        //for(i = [1:6]) rotate([0,0,i*60]) translate([0,500+half_d/2,0]) cube([WINDADGE, 1000, 1000], center=true);
        
    }
}

translate([0,0,SZ*2/3/2]) translate([0, 50, 0]) difference() {
    union() {
        cube([3*SZ,SZ,SZ*2/3], center=true);
        translate([0,0,SZ*2/3/2]) reel(outer_d=SZ/2, inner_d=SZ/4, h=SZ/5);
    }
    //translate([0,0,1000/2-WINDADGE]) 
    cylinder(d=SHAFT_D+WINDADGE, h=1000, center=true, $fn=12);
    // weight holes
    for(i = [-1, +1]) translate([i*SZ/2,0,0]) cylinder(d=SZ/2, h=1000, center=true);
}

translate([0,0,SZ*2/3/2]) translate([0, -50, 0]) difference() {
    // shaft hole
    union() {
        cube([4*SZ,SZ*3/4,SZ*2/3], center=true);
        translate([0,0,SZ*2/3/2]) reel(outer_d=SZ/2, inner_d=SZ/4, h=SZ/5);
    }
    // shaft hole
    //translate([0,0,1000/2-WINDADGE]) 
    cylinder(d=SHAFT_D+WINDADGE, h=1000, center=true, $fn=12);
    // weight holes
    for(i = [-1, +1]) translate([i*SZ/2,0,0]) cylinder(d=SZ/2, h=1000, center=true);
}

th = 0.4;//SZ / 100*2;
ibeam_l = 5.5*SZ; // 5*SZ
ibeam_w = SZ/2; // SZ*2/3
beam_h = SZ/6;
cone_h = SZ/4;

difference() {
    union() {
        // axle support
        translate([0,0,cone_h/2]) cylinder(d1=ibeam_w*1.6, d2=1.6*BEARING_D, h=cone_h, center=true);
        intersection() {
            union() {
                // I-beam vertical
                translate([0,0,th/2]) cube([ibeam_l ,ibeam_w, th], center=true);
                // I-beam sides
                translate([0,-ibeam_w/2,beam_h/2]) cube([ibeam_l ,th, beam_h], center=true);
                translate([0,+ibeam_w/2,beam_h/2]) cube([ibeam_l ,th, beam_h], center=true);
            }
            rotate([0,0,45]) cube([ibeam_l/sqrt(2), ibeam_l/sqrt(2), 1000], center=true);
        }
        // side axles
        for(i =[-1, +1]) difference() {
            translate([i*(ibeam_l/2-BEARING_W),0,0]) rotate([0,90,0]) cylinder(d=BEARING_HOLE, h=ibeam_l/14, center=true, $fn=12);
            translate([0,0,-500]) cube([1000,1000,1000], center=true);
        }
        // side axle support
        translate([0,0,beam_h/2]) difference() {
            cylinder(d=ibeam_l*0.92, h=beam_h, center=true);
            cylinder(d=ibeam_l*0.92-2*th, h=beam_h, center=true);
        }
    }
    // axle hole
    cylinder(d=middle_d, h=1000, center=true, $fn=18);
    // bearing hole
    translate([0,0,1000/2+cone_h-BEARING_W]) cylinder(d=BEARING_D+WINDADGE, h=1000, center=true, $fn=18);
    // cut cone sides
    translate([0,+500+ibeam_w/2+th/2,0]) cube([1000,1000,1000], center=true);
    translate([0,-500-ibeam_w/2-th/2,0]) cube([1000,1000,1000], center=true);
}