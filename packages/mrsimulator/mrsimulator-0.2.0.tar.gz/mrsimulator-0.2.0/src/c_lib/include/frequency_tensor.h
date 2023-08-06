// -*- coding: utf-8 -*-
//
//  frequency_component_function.h
//
//  Created by Deepansh J. Srivastava, Apr 11, 2019
//  Contact email = deepansh2012@gmail.com
//

#include "frequency_component/spatial_orientation_tensor.h"
#include "frequency_component/spin_transition_function.h"

/**
 * The frequency tensors (FT) from the first-order perturbation expansion of
 * the nuclear shielding Hamiltonian, in a given frame, @f$\mathcal{F}@f$,
 * described by the Euler angles @f$\Theta = [\alpha, \beta, \gamma]@f$ are
 * @f[
 *    {\Lambda'}_{0,0}^{(\sigma)}(\Theta, i,j) &=
 *                                    \mathcal{R'}_{0,0}^{(\sigma)}(\Theta)
 *                                    ~~  \mathbb{p}(i, j),~\text{and} \\
 *    {\Lambda'}_{2,n}^{(\sigma)}(\Theta, i,j) &=
 *                                    \mathcal{R'}_{2,n}^{(\sigma)}(\Theta)
 *                                    ~~  \mathbb{p}(i, j),
 * @f]
 * where @f$\mathcal{R'}_{0,0}^{(\sigma)}(\Theta)@f$ and
 * @f$\mathcal{R'}_{2,n}^{(\sigma)}(\Theta)@f$ are the spatial
 * orientation functions in frame @f$\mathcal{F}@f$, and @f$\mathbb{p}(i, j)@f$
 * is the spin transition function for
 * @f$\left|i\right> \rightarrow \left|j\right>@f$ transition.
 *
 * @param Lambda_0 A pointer to an array of length 1 where the frequency
 *      components from @f${\Lambda'}_{0,0}^{(\sigma)}(\Theta, i,j)@f$ will be
 *      stored.
 *
 * @param Lambda_2 A pointer to a complex array of length 5 where the frequency
 *      components from @f${\Lambda'}_{2,n}^{(\sigma)}(\Theta, i,j)@f$ will be
 *      stored ordered according to
 *      @f$\left[{\Lambda'}_{2,n}^{(\sigma)}(\Theta, i,j)\right]_{n=-2}^2@f$.
 *
 * @param omega_0_delta_iso_in_Hz The quantity,
 *      @f$2\pi\omega_0\delta_\text{iso}@f$, given in Hz.
 *
 * @param omega_0_zeta_sigma_in_Hz The quantity, @f$2\pi\omega_0\zeta_sigma@f$,
 *      representing the strength of the nuclear shielding anisotropy, given in
 *      Hz, defined using Haeberlen convention.
 *
 * @param eta The nuclear shielding asymmetry parameter,
 *      @f$\eta_\sigma \in [-1,1]@f$, defined using Haeberlen convention.
 *
 * @param Theta A pointer to an array of length 3 where Euler angles,
 *      ordered as @f$[\alpha, \beta, \gamma]@f$, are stored.
 *
 * @param transition A pointer to an array of length 2 where the quantum
 *      numbers describing the two energy states involved in the transition
 *      @f$\left|i\right> \rightarrow \left|j\right>@f$ are stored ordered as
 *      @f$[i, j]@f$.
 */
static inline void FCF_1st_order_nuclear_shielding_Hamiltonian(
    double *restrict Lambda_0, void *restrict Lambda_2,
    const double omega_0_delta_iso_in_Hz, const double omega_0_zeta_sigma_in_Hz,
    const double eta, const double *Theta, const double *transition) {

  // Spin transition function
  double transition_fn = STF_p(transition[1], transition[0]);

  // Spatial orientation function
  sSOT_1st_order_nuclear_shielding_Hamiltonian(
      Lambda_0, Lambda_2, omega_0_delta_iso_in_Hz, omega_0_zeta_sigma_in_Hz,
      eta, Theta);

  // frequency component function from zeroth-rank irreducible tensor
  *Lambda_0 *= transition_fn;

  // frequency component function from second-rank irreducible tensor
  double *Lambda_2_ = (double *)Lambda_2;
  Lambda_2_[0] *= transition_fn; // Lambda_2-2 real
  Lambda_2_[4] *= transition_fn; // Lambda_2 0 real
  Lambda_2_[8] *= transition_fn; // Lambda_2 2 real
}

/**
 * The frequency component function (FCF) from the first-order electric
 * quadrupole Hamiltonian, in a given frame, @f$\mathcal{F}@f$, described
 * by the Euler angles @f$\Theta = [\alpha, \beta, \gamma]@f$, is
 * @f[
 *    {\Lambda'}_{2,n}^{(q)}(\Theta,i,j) =
 *                \mathcal{R'}_{2,n}^{(q)}(\Theta) ~~ \mathbb{d}(i, j),
 * @f]
 * where @f$\mathcal{R}_{2,n}^{(q)}(\Theta)@f$ are the spatial orientation
 * functions in frame @f$\mathcal{F}@f$, and @f$\mathbb{d}(i, j)@f$ is the
 * spin transition function for @f$\left|i\right> \rightarrow \left|j\right>@f$
 * transition.
 *
 * @param Lambda_2 A pointer to a complex array of length 5 where the frequency
 *      components from @f${\Lambda'}_{2,n}^{(q)}(\Theta,i,j)@f$ will be stored
 *      ordered according to
 *      @f$\left[{\Lambda'}_{2,n}^{(q)}(\Theta,i,j)\right]_{n=-2}^2@f$.
 *
 * @param spin The spin quantum number, @f$I@f$.
 *
 * @param Cq_in_Hz The quadrupole coupling constant, @f$C_q@f$, in Hz.
 *
 * @param eta The quadrupole asymmetry parameter, @f$\eta_q \in [0, 1]@f$.
 *
 * @param Theta A pointer to an array of length 3 where Euler angles,
 *      ordered as @f$[\alpha, \beta, \gamma]@f$, are stored.
 *
 * @param transition A pointer to an array of length 2 where the quantum
 *      numbers describing the two energy states involved in the transition
 *      @f$\left|i\right> \rightarrow \left|j\right>@f$ are stored ordered as
 *      @f$[i, j]@f$.
 */
static inline void FCF_1st_order_electric_quadrupole_Hamiltonian(
    void *restrict Lambda_2, const double spin, const double Cq_in_Hz,
    const double eta, const double *Theta, const double *transition) {

  // Spin transition function
  double transition_fn = STF_d(transition[1], transition[0]);

  // Spatial orientation function
  sSOT_1st_order_electric_quadrupole_Hamiltonian(Lambda_2, spin, Cq_in_Hz, eta,
                                                 Theta);

  // frequency component function from second-rank irreducible tensor
  double *Lambda_2_ = (double *)Lambda_2;
  Lambda_2_[0] *= transition_fn; // Lambda_2-2 real
  Lambda_2_[4] *= transition_fn; // Lambda_2 0 real
  Lambda_2_[8] *= transition_fn; // Lambda_2 2 real
}

/**
 * The frequency component functions (FCF) from the second-order electric
 * quadrupole Hamiltonian, in a given frame, @f$\mathcal{F}@f$, described
 * by the Euler angles @f$\Theta = [\alpha, \beta, \gamma]@f$, are
 * @f[
 *    {\Lambda'}_{0,0}^{(qq)}(\Theta, i,j) &= \mathcal{R'}_{0,0}^{(qq)}(\Theta)
 *                                      ~~ \mathbb{c}_0(i, j), \\
 *    {\Lambda'}_{2,n}^{(qq)}(\Theta, i,j) &= \mathcal{R'}_{2,n}^{(qq)}(\Theta)
 *                                      ~~ \mathbb{c}_2(i, j),~\text{and} \\
 *    {\Lambda'}_{4,n}^{(qq)}(\Theta, i,j) &= \mathcal{R'}_{4,n}^{(qq)}(\Theta)
 *                                      ~~ \mathbb{c}_4(i, j),
 * @f]
 * where @f$\mathcal{R'}_{0,0}^{(qq)}(\Theta)@f$,
 * @f$\mathcal{R'}_{2,n}^{(qq)}(\Theta)@f$, and,
 * @f$\mathcal{R'}_{4,n}^{(qq)}(\Theta)@f$ are the spatial orientation
 * functions in frame @f$\mathcal{F}@f$, and @f$\mathbb{c}_i(i, j)@f$ are the
 * composite spin transition functions for
 * @f$\left|i\right> \rightarrow \left|j\right>@f$ transition.
 *
 * @param Lambda_0 A pointer to an array of length 1 where the frequency
 *      component from @f${\Lambda'}_{0,0}^{(qq)}(\Theta, i,j)@f$ will be
 *      stored.
 *
 * @param Lambda_2 A pointer to a complex array of length 5 where the frequency
 *      components from @f$\Lambda_{2,n}^{(qq)}(\Theta, i,j)@f$ will be stored
 *      ordered according to
 *      @f$\left[{\Lambda'}_{2,n}^{(qq)}(\Theta, i,j)\right]_{n=-2}^2@f$.
 *
 * @param Lambda_4 A pointer to a complex array of length 5 where the frequency
 *      components from @f${\Lambda'}_{4,n}^{(qq)}(\Theta, i,j)@f$ will be
 *      stored ordered according to
 *      @f$\left[{\Lambda'}_{4,n}^{(qq)}(\Theta, i,j)\right]_{n=-4}^4@f$.
 *
 * @param spin The spin quantum number, @f$I@f$.
 *
 * @param Cq_in_Hz The quadrupole coupling constant, @f$C_q@f$, in Hz.
 *
 * @param eta The quadrupole asymmetry parameter, @f$\eta_q \in [0, 1]@f$.
 *
 * @param v0_in_Hz The Larmor frequency, @f$\nu_0@f$, in Hz.
 *
 * @param Theta A pointer to an array of length 3 where Euler angles,
 *      ordered as @f$[\alpha, \beta, \gamma]@f$, are stored.
 *
 * @param transition A pointer to an array of length 2 where the quantum
 *      numbers describing the two energy states involved in the transition
 *      @f$\left|i\right> \rightarrow \left|j\right>@f$ are stored ordered as
 *      @f$[i, j]@f$.
 */
static inline void FCF_2nd_order_electric_quadrupole_Hamiltonian(
    double *restrict Lambda_0, void *restrict Lambda_2, void *restrict Lambda_4,
    const double spin, const double v0_in_Hz, const double Cq_in_Hz,
    const double eta, const double *Theta, const double *transition) {

  // Composite spin transition functions
  double *cl_value = malloc_double(3);
  STF_cL(cl_value, transition[1], transition[0], spin);

  // Spatial orientation function
  sSOT_2nd_order_electric_quadrupole_Hamiltonian(
      Lambda_0, Lambda_2, Lambda_4, spin, v0_in_Hz, Cq_in_Hz, eta, Theta);

  // frequency component function from zeroth-rank irreducible tensor
  *Lambda_0 *= *cl_value++;

  // frequency component function from second-rank irreducible tensor
  double *Lambda_2_ = (double *)Lambda_2;
  Lambda_2_[0] *= *cl_value; // Lambda_2-2 real
  Lambda_2_[4] *= *cl_value; // Lambda_2 0 real
  Lambda_2_[8] *= *cl_value; // Lambda_2 2 real

  cl_value++;
  // frequency component function from fourth-rank irreducible tensor
  double *Lambda_4_ = (double *)Lambda_4;
  Lambda_4_[0] *= *cl_value;  // Lambda_4-4 real
  Lambda_4_[4] *= *cl_value;  // Lambda_4-2 real
  Lambda_4_[8] *= *cl_value;  // Lambda_4 0 real
  Lambda_4_[12] *= *cl_value; // Lambda_4 2 real
  Lambda_4_[16] *= *cl_value; // Lambda_4 4 real
}

/*
===============================================================================
       First order Weakly coupled Magnetic Dipole frequency in the PAS.
-------------------------------------------------------------------------------
The frequency includes the product of second rank tensor and the
spin transition functions in the weak coupling limit.
*/
static inline void weakly_coupled_direct_dipole_frequencies_to_first_order(
    double *restrict Lambda_0, void *restrict Lambda_2, const double D,
    const double *transition) {
  // Spin transition contribution
  double transition_fn = STF_dIS(transition[0], transition[1], 0.5, 0.5);

  // Scaled R00
  *Lambda_0 += 0.0;

  /* Scaled R2m containing the components of the magnetic dipole second rank
  tensor in its principal axis frame. */
  vm_double_zeros(10, (double *)Lambda_2);
  double *Lambda_2_ = (double *)Lambda_2;
  Lambda_2_[4] = 2.0 * D * transition_fn; // Lambda_2 0 real
}
