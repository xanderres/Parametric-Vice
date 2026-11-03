// Rendering Quality
$fn = 60;

// Vice Parameter
hight = 20;
length = 60;
width = 15;
jaw_hight = 10;

fixed_jaw_length = 10;
sliding_jaw_length = 15;

opening = 1;


translate([0, 0, 0]) base_fixed_jaw();
translate([0, fixed_jaw_length + opening, 0]) sliding_jaw();

module base_fixed_jaw(){
    color("darkgray"){
        translate([-width/2,0,0])cube([width, length, hight - jaw_hight]);
        translate([-width/2,0,0])cube([width, fixed_jaw_length, hight]);
        }
    }

module sliding_jaw() {
    color("lightcyan"){
        translate([-width/2,0,hight - jaw_hight]) cube([width, sliding_jaw_length, hight - jaw_hight]);
        }
    }