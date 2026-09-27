# Ponte model replication notes

## Scope

This note records the source-grounded choices used in the CL 420 mid-term report. The selected process is recombinant Rhizopus oryzae lipase production by *Pichia pastoris* under methanol induction. This host and product are different from the project topics already listed as unavailable by the course team.

## Primary sources

1. Ponte, X., Barrigón, J. M., Maurer, M., Mattanovich, D., Valero, F., and Montesinos-Seguí, J. L. “Towards optimal substrate feeding for heterologous protein production in *Pichia pastoris* fed-batch processes under PAOX1 control: a modeling aided approach.” *Journal of Chemical Technology and Biotechnology*, 93, 3208 to 3218, 2018. DOI: https://doi.org/10.1002/jctb.5677
2. Ponte, X. “Towards optimal substrate feeding for heterologous protein production in *Pichia pastoris* fed batch process under PAOX1 control: a modelling aided approach.” Doctoral thesis, Universitat Autònoma de Barcelona, 2017. The accessible full text is https://ddd.uab.cat/pub/tesis/2017/hdl_10803_457712/xpf1de1.pdf. Chapter 5 contains the model equations, parameters, initial conditions, and standard feeding strategies used here.
3. Indian Institute of Technology Bombay, CL 420 project instructions, local file `moodle-content/CL420 Upstream Bioprocess Project - Student Instructions.pdf`.
4. Indian Institute of Technology Bombay, CL 420 kickoff slides, local file `moodle-content/CL_420_Biochemical_Engineering_Kickoff.pdf`.
5. Indian Institute of Technology Bombay, Structured Model V1, local file `moodle-content/Structured Model V1.pdf`.

## Model extracted from the paper source

The published model uses non-monotonic substrate functions for growth and ROL production:

```text
q_i = qmax_i S / (KS_i + S + S^2/KI_i)
```

The specific uptake relations are:

```text
q_i = Y_i/X mu + m_i/X
```

The report uses the following values from Table 5.1 of the thesis, which reproduces the paper model.

| Quantity | Value | Unit |
| --- | ---: | --- |
| mu_max | 0.069 | h^-1 |
| KS,X | 0.50 | g L^-1 |
| KI,X | 7.5 | g L^-1 |
| qmax,P | 2200 | U g^-1 h^-1 |
| KS,P | 10.0 | g L^-1 |
| KI,P | 1.2 | g L^-1 |
| YS/X | 5.14 | g g^-1 |
| mS/X | 0.013 | g g^-1 h^-1 |
| YO2/X | 0.206 | mol O2 g^-1 |
| mO2/X | 6.1 x 10^-4 | mol O2 g^-1 h^-1 |

The critical substrate concentrations are 1.9 g L^-1 for growth and 3.5 g L^-1 for product formation, obtained from the square root of KS KI and rounded as reported.

The initial conditions for the fed-batch simulations are X0 = 27 g L^-1, P0 = 50 U mL^-1, V0 = 2 L, and S0 = 1 g L^-1 for predefined feed profiles. For the constant-substrate case, the reported target S = 2 g L^-1 is used as the initial setpoint so that the ideal setpoint trajectory starts without an artificial transient.

The standard strategy definitions are constant feed CF with F = 14 g h^-1, constant growth CM with mu = 0.03 h^-1, linearly increasing growth LM from mu = 0.01 to 0.04 h^-1, and constant substrate CS with S = 2 g L^-1. The process limits are Xmax = 55 g L^-1, Vmax = 5 L, and Smax = 10 g L^-1. The simulation stops when a limit is first reached.

## Controlled comparator

The Monod comparator replaces only the non-monotonic function by:

```text
q_i = qmax_i S / (KS_i + S)
```

The qmax and KS values remain unchanged. This isolates the effect of removing substrate inhibition. It is a new comparison added for this project, not a claim that the original paper used a Monod branch.

## Numerical and oxygen-demand choices

The four dynamic states are V, XV, SV, and PV. Amount form is used so that feed and consumption terms are explicit:

```text
dV/dt   = F/rho_methanol
dXV/dt  = mu XV
dSV/dt  = F - qS XV
dPV/dt  = qP XV
```

The reference paper solved the ODE system with MATLAB ode45. The project implementation uses fixed-step classical RK4 with dt = 0.01 h and checks the CS result again at dt = 0.005 h. The reported relative difference is stored in the simulation output.

Oxygen is not added as a fifth dynamic state. It is derived from the published relation:

```text
qO2 = YO2/X mu + mO2/X
OUR = qO2 XV
```

This gives total oxygen demand in mol O2 h^-1 and volumetric oxygen demand in mol O2 L^-1 h^-1.

## Known limitation

The paper describes a predictive adaptive PI controller for the experimental constant-substrate strategy but does not give all tuned controller gains in the model-parameter table. The code therefore reproduces the reported kinetic model and ideal CS setpoint by the algebraic feed balance. It does not claim to reproduce the hidden controller tuning.
