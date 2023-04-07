$fn = 90;

/* https://www.youtube.com/watch?v=e9wGPh-iiRw&list=PLvKkSzWgY7KUUSYDqHVdv0mst4nBnLe64&index=1
  https://en.wikipedia.org/wiki/Tennis_racket_theorem
  
  
  PRINT https://en.wikipedia.org/wiki/Tippe_top
  https://www.youtube.com/watch?v=V7hGcLU_wlY
  https://www.thingiverse.com/search?q=Tippe+top&type=things&sort=relevant
*/
rind_width = 8;
ring_d = 60;
ring_scale = 0.1;
hole_d = 2;

module angle() { 
    translate([-ring_d*(1+ring_scale)/2+rind_width/2,-7/2-hole_d/2,rind_width/2]) difference() {
        cube([7,7,1.2], center = true);
        translate([10,0,0])rotate([0,0,-30]) cube([20,20,2], center = true);
        translate([0,-10,0]) cube([20,20,2], center = true);
    }
}
//cube([10,10,10]); // scale cube

*union() { // spin top'
  translate([0,-ring_d*0.6,rind_width/2]) rotate([90,0,0]) cylinder(h = 20, d = 7, center = true); // axis
    difference() {
        union() {
            scale([1 + ring_scale,1 - ring_scale, 1]) difference() {
                cylinder(d = ring_d + rind_width, h = rind_width);
                cylinder(d = ring_d, h = rind_width);
            }
            //translate([0,-20,rind_width/2]) rotate([-90,0,0]) cylinder(d1 = 0, d2 = 16, h = 8); // bottom cone
        }
        translate([0,53,0]) cube([100,100,100], center = true);
        translate([0,0,rind_width/2]) rotate([0,90,0]) cylinder(d = hole_d, h = 100, center = true);
        translate([0,-7,rind_width/2]) cube([1.6,14,8], center = true);
    }
    //angle();
    //translate([0,0,+rind_width/2]) rotate([0,180,0]) translate([0,0,-rind_width/2]) angle();
}



// round moving part
*union() {
    difference() {
        translate([0,0,rind_width/2]) rotate([0,90,0]) cylinder(d = 6, h = 30, center = true);
        translate([0,0,rind_width/2]) rotate([0,90,0]) cylinder(d = hole_d, h = 100, center = true); // hole
    }
    translate([0,-5,rind_width/2]) rotate([90,0,0]) cylinder(d = 6, h = 10, center = true);
    translate([0,5.5,rind_width/2]) cube([1.2,11,6], center = true);
}

d = 6*1.8;
h = 4*1.8;
rotate([-90,0,180]) translate([0,1.4614-0.03,-d/2])
difference() {
  union() {
    difference() {
        translate([0,0,d/2]) rotate([0,90,0]) cube([d,d,d*5], center = true);
        translate([0,-1.4614+0.03,d/2]) rotate([0,90,0]) cylinder(d = hole_d, h = 100, center = true); // hole
    }
    translate([0,-d/2-h/2,d/2]) rotate([90,0,0]) cylinder(d = d, h = h*2, center = true);
    //translate([0,-d/2-h/2,rind_width/2]) rotate([90,0,0]) cylinder(d = d, h = h, center = true);
    //translate([0,+d/2+h,rind_width/2]) rotate([90,0,0]) cylinder(d = d/1.4142, h = h*2, center = true);
  }
  translate([0,0,d/2]) rotate([90,0,0]) cylinder(d = hole_d, h = 100, center = true); // hole
}

/*
from stl import mesh
your_mesh = mesh.Mesh.from_file('dzhanibekov2.stl')
volume, cog, inertia = your_mesh.get_mass_properties()
print("Volume                                  = {0}".format(volume))
print("Position of the center of gravity (COG) = {0}".format(cog))
*/

