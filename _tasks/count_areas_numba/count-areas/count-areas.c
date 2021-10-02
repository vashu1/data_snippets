#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <map>

/*
2 seconds per run? WTF?

g++ count-areas.c 
./a.out

./a.out | grep -v ^0$
./a.out
*/

int replace_component_if_merged(int component_id, std::map<int,int> merge_components) {
    while ( merge_components.find(component_id) != merge_components.end() ) {
        component_id = merge_components[component_id];
    }
    return component_id;
}

int main() {
    //TODO read params
    int bitmap_height = 256;
    int bitmap_width = 256;

    // read file
    FILE * fp = fopen("count-areas/images/resources/sample.bin","rb");
    fseek(fp, 0L, SEEK_END);
    int sz = ftell(fp);
    unsigned char *bitmap = (unsigned char *)malloc(sz);
    rewind(fp);
    fread(bitmap, sz, 1, fp);
    fclose(fp);

    // process
    unsigned char *components = (unsigned char *)malloc(bitmap_width*2);
    int current_component_id = 0;
    int upper_component, left_component;
    bool upper_same_color, left_same_color;
    std::map<int, unsigned char> component_colours;
    std::map<int, int> merge_components;
    for (int current_point = 0; current_point < sz  ; current_point++) {
        upper_same_color = left_same_color = false;
        if (current_point >= bitmap_width) {
            int upper_point = current_point - bitmap_width;
            upper_same_color = bitmap[upper_point] == bitmap[current_point];
            if (upper_same_color) { 
                upper_component = components[upper_point % (2*bitmap_width)];
                upper_component = replace_component_if_merged(upper_component, merge_components);
            }
        }
        if (current_point % bitmap_width) {
            int left_point = current_point - 1;
            left_same_color = bitmap[left_point] == bitmap[current_point];
            if (left_same_color) {
                left_component = components[left_point % (2*bitmap_width)];
                left_component = replace_component_if_merged(left_component, merge_components);
            }
        }
        // set current cell component
        if (upper_same_color && left_same_color && upper_component != left_component) { // merge 2 same coloured components
            int max_component = (upper_component < left_component) ? left_component  : upper_component;
            int min_component = (upper_component < left_component) ? upper_component : left_component;
            components[current_point % (2*bitmap_width)] = min_component;
            merge_components[max_component] = min_component; // remember merge to repeat it on following row
            if (component_colours.find(max_component) != component_colours.end()) {
                component_colours.erase(max_component);
            }
        } else if (upper_same_color || left_same_color) { // extend neighbouring component to current cell
            components[current_point % (2*bitmap_width)] = upper_same_color ? upper_component : left_component;
        } else { // new component starts here
            components[current_point % (2*bitmap_width)] = current_component_id;
            component_colours[current_component_id] = bitmap[current_point];
            current_component_id += 1;
        }
    }

    // count colours
    int counts[256];
    memset(counts, 0, sizeof(counts));
    std::map<int, unsigned char>::iterator it;
    for ( it = component_colours.begin(); it != component_colours.end(); it++ )
        counts[it->second]++;
    // print result
    for (int i = 0; i < 256 ; i++) 
        printf("%d\n", counts[i]);

    free(components);
    free(bitmap);
    return 0;
 }

/* // run 10 times
 int main() {
 	for (int i =0; i < 10; i++)main2();
}
*/