// -*- coding: utf-8 -*-
//
//  spinning_sidebands.h
//
//  Created by Deepansh J. Srivastava, Apr 11, 2019
//  Contact email = deepansh2012@gmail.com
//

#include "mrsimulator.h"

// headerdoc

extern void spinning_sideband_core(
    // spectrum information and related amplitude
    double *spec,              // The amplitude of the spectrum.
    double spectral_start,     // The start of the frequency spectrum.
    double spectral_increment, // The increment of the frequency spectrum.
    int number_of_points,      // Number of points on the frequency spectrum.

    isotopomer_ravel *ravel_isotopomer, // isotopomer structure

    int quad_second_order,                  // Quad theory for second order,
    int remove_second_order_quad_isotropic, // remove the isotropic contribution
                                            // from the second order quad
                                            // Hamiltonian.

    // spin rate, spin angle and number spinning sidebands
    int number_of_sidebands,                // The number of sidebands
    double sample_rotation_frequency_in_Hz, // The rotor spin frequency
    double rotor_angle_in_rad, // The rotor angle relative to lab-frame z-axis

    // Pointer to the transitions. transition[0] = mi and transition[1] = mf
    double *transition,

    // powder orientation average
    int geodesic_polyhedron_frequency, // The number of triangle along
                                       // the edge of octahedron
    unsigned int integration_volume             // 0-octant, 1-hemisphere, 2-sphere.
);
