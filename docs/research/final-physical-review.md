# Final physical and biological review

31 October 2026. Bounded independent review of `simulation/rol_final_design.py`, its imported rate laws, every final CSV, `design_summary.json`, and the existing source audit. Figure interpretation below follows the plotting code and underlying data; the main reviewer handles image inspection. No model fit, code, report or presentation was changed.

**Decision:** The kinetic comparisons and selected Haldane operating point have a coherent conditional interpretation. Correct the oxygen-capacity calculation and its dependent feasibility labels. Correct blanket claims about positivity or growth association if used. The proposed smaller tank resolves a clear initial impeller-immersion concern, subject to hardware qualification.

## 1. High severity — must correct: oxygen capacity and reserve

`gas_capacity(OUR,V)` calculates the outlet oxygen fraction using nominal OUR, then calls `kLa × log-mean driving force` capacity. That is a transfer-potential check at the specified demand, not a self-consistent maximum transfer rate. Using that same outlet composition to prove a 20% demand allowance overstates the reserve. A biological demand increase also depletes the gas more strongly. The existing source audit's final oxygen-reserve addendum has the same problem and must not be used to validate this step.

The main reviewer's correction is valid for the stated model: plug-flow gas, well-mixed liquid, constant pressure, linear oxygen solubility, constant kLa, and RQ = 1 so dry total gas molar flow is constant. Define:

```text
c = Cair / 0.21                         [mol/L per mole fraction]
g = G/V = 60 vvm p/(RT)                 [mol gas/L/h]
deltaIn = c yin - CL                    [mol/L]
qGas = (g/c) deltaIn                    [mol O2/L/h]
capacityV = qGas [1 - exp(-kLa c/g)]
kLaRequired = -(g/c) ln[1 - 1.20 OURV/qGas]
```

The last expression requires `1.20 OURV < qGas`; otherwise no finite kLa can meet the target at that gas flow. Derivation: `deltaOut = deltaIn - c r/g`; substitution into `r = kLa × (deltaIn-deltaOut)/ln(deltaIn/deltaOut)` gives `ln(deltaIn/deltaOut) = kLa c/g`. This is also the integrated gas-phase balance, so it is not merely an algebraic curve fit.

At the actual repository inputs (30 °C, 1 bar, 2 vvm, 75% inlet oxygen, kLa = 1000 h^-1):

| Quantity | Correct result |
| --- | ---: |
| Selected peak OURV | 0.52204 mol/L/h |
| Self-consistent capacityV | 0.68243 mol/L/h |
| Required kLa for 1.20 × selected OUR | **908.7 h^-1** |
| Capacity/(1.20 × OUR) | 1.0894 |
| Best feasible Haldane grid point | 3.4 g/L, unchanged |
| Best feasible Monod grid point | **1.0 g/L**, 6391.5 U/L/h |

Thus the selected point still passes the assumed qualification target. The exact formula gives 908.7, rather than approximately 930, for these inputs. The current nominal-driving-force calculation gives about 892.2. Monod at 1.1 g/L requires 0.68522 mol/L/h including allowance and fails the corrected capacity of 0.68243.

**Graph correction:** At fixed vvm, gas blend, kLa and CL, volumetric capacity is constant, independent of biomass and time. Air capacity is 0.15410 mol/L/h at the same kLa. Increasing OUR does not itself reduce equipment capacity; it reduces available reserve. Total capacity rises with V because constant vvm makes total gas flow rise with V. Recompute oxygen-design curves, required-kLa curves, feasibility CSV/JSON fields, scan masks, and sensitivity feasibility labels consistently. This is a bounded transfer-screen correction; kinetic trajectories need no refit.

**Conditional:** RQ = 1 is an assumption, not the thesis physiology. The thesis reports RQ about 0.61–0.65 in its DO5 example (Chapter 4, discussion of Figure 4.3B; verified in the local text). At fixed oxygen consumption, RQ below one reduces outlet total molar flow and gives a higher outlet oxygen fraction than RQ = 1. The latter is therefore conservative in this respect, not a universal guarantee. Wet gas, methanol stripping, broth solubility, gradients and real kLa remain outside this screen. [T; code `gas_capacity`, `metrics`, `figures`.]

## 2. Medium severity — geometry correction is physically credible, still conditional

For a cylindrical tank of diameter 0.16 m, 2 L gives only 0.0995 m liquid height. Two 0.065 m turbines with conventional separation cannot be assumed adequately submerged without specified elevations. At the proposed centers of 0.040 and 0.105 m, the upper turbine would not be submerged at this diameter.

The main reviewer's proposed diameter **0.13 m**, with those centers and blade height **0.013 m**, gives initial liquid height **0.15068 m** and selected harvest height **0.24871 m**. The upper blade edge is at 0.1115 m, leaving **39.2 mm** liquid above it initially. The lower blade edge is 33.5 mm above the floor. The center spacing is one impeller diameter. This resolves the static immersion concern under the cylindrical-volume assumption. Check real bottom shape, internals and vessel height against the actual hardware before treating these elevations as installed dimensions.

At unchanged power and 2 vvm, the revised superficial gas velocity is 0.005023 m/s initially and 0.008290 m/s at harvest. The existing correlations give approximately **340/357 h^-1 water** and **2452/1908 h^-1 electrolyte**, initially/at harvest. These are screening extrapolations, not a measured bracket. D/T becomes 0.50; independent addition of turbine powers, Np = 5 and Pg/P0 = 0.70 remain assumptions. Actual torque, dispersion and broth kLa require qualification. This geometry change does not change the kinetic calculation or the specified 1000 h^-1 qualification target. [Calculated from user-proposed geometry; code `hardware`; source audit's K02/K17 evidence.]

## 3. Valid comparisons, with precise physical meanings

| Figure or table | Physical interpretation and limitation |
| --- | --- |
| Kinetic inputs and `kinetic_models` | Haldane growth and activity peaks differ: approximately 1.94 and 3.46 g/L. Nominal rate coefficients are not attained peaks. Monod removes inhibition with other coefficients fixed; it is a controlled comparator, not a separately validated organism model. [T, Table 5.1; imported `specific_rates`.] |
| Feeding-policy table; `dynamic_comparison` | All eight reference cases start at S = 2 g/L, X = 27 g/L, V = 2 L and P = 50 U/mL. CF, CM and LM have identical prescribed feed rates across paired models at common times; independently checked maximum difference is zero. CM/LM prescribe target biomass histories, not actual growth. CS uses model-dependent uptake and therefore different feeds. A flat CS trace is an algebraic invariant, not demonstrated controller performance. [Code `feed`, `simulate`; timeseries.] |
| `feeding_comparison`; endpoint table | Compare each run at its own stopping time, not equal time, equal methanol use or equal biomass amount. Monod CF can finish with lower activity despite its higher rate curve at fixed S: feed-limited uptake causes lower residual S, changing qP along the path. Near substrate limitation both models converge in growth behavior. CS avoids that low-S production penalty but assumes exact uptake compensation. [Timeseries and summary metrics.] |
| `setpoint_scan` | Each scan starts at its own setpoint, including a different initial methanol inventory. This compares ideal operating states, not identical startup charges or transitions. The broad productivity maximum near the product-rate peak is credible; a precise experimental optimum at 3.4 g/L is not established. Correct the Monod feasible segment as above. [Scan CSV; `exact_cs`.] |
| Endpoint and design-summary yields | Net biomass and net activity divided by methanol consumed include fitted maintenance losses. They are induction-model yields, not purified-protein mass yields or whole-process substrate efficiencies. The summary table label “Observed” should be **“Predicted”** for these model-derived yields. [Code `metrics`; report design-summary table.] |
| Numerical-check table | Small residuals establish numerical consistency for these equations and runs. They do not validate biology, transfer, heat removal, controller behavior or general positivity. [Numerical checks CSV.] |
| Monitoring/control table | Sensible proposed measurements and responses. Feed reduction under oxygen shortage changes S and growth and can invalidate ideal CS performance. The model does not simulate that cascade or oxygen-limited physiology. [Report control table; T, Chapters 4–5.] |

## 4. Medium severity — positivity and biological classification need qualified wording

The model is **unstructured and unsegregated**: biomass is a single lumped pool, with no intracellular composition or population distribution. Four reactor states do not make it structured. Biomass growth is substrate dependent; activity formation has its own substrate-dependent qP law. Calling production strictly growth associated suggests `qP = alpha mu`, which is not this model. Prefer “growth-linked during methanol induction, with a substrate-dependent activity/biomass yield.” Both rates vanish at S = 0, but that mathematical property does not establish causal growth dependence or rule out nongrowing production experimentally. [Imported rate laws; report kinetic discussion.]

Amount balances correctly handle dilution. Although B and A are nondecreasing when mu and qP are nonnegative, `dX/dt = (mu - Vdot/V)X` and `dP/dt = qP X/1000 - (Vdot/V)P`; concentrations need not increase. All exported runs have positive states: minimum S is about 0.0872 g/L, and none crosses zero. This is a result for these runs, not a general positivity proof. At M = 0 the maintenance law still gives `Mdot = F - mS B`, which can be negative. A generic starvation simulation would need a boundary-valid uptake law; no expanded implementation is required for this review. [Code `rhs`, imported `q_substrate`; full timeseries minima checked.]

## 5. Valid stop rules and sensitivity, conditional operating feasibility

Every reference case and scanned setpoint stops at **55 g/L biomass**, before 3.5 L, 10 g/L methanol or 120 h. These are design constraints, not predicted death or substrate exhaustion. The selected volume is 3.301 L; adding a 5% volume allowance gives 3.466 L, within 3.5 L. CF finishes near 3.480 L, so the same omitted-liquid allowance would exceed its limit. Do not extend the selected-case headspace claim to all reference cases. Linked nitrogen volume is included; base, antifoam, sampling, stripping and evaporation remain omitted. [All endpoint/scan CSVs; source audit; code `simulate`.]

Small growth-coefficient sensitivity of induction QP is physically explainable **within this metric**. For CS, `Anew = (qP/mu)(Bf-B0)` and `tf = ln(Bf/B0)/mu`, hence:

`QP = qP (Bf-B0) / [Vf ln(Bf/B0)]`.

The explicit mu cancels. Residual dependence comes mainly through maintenance and the final volume/biomass amount. Faster growth shortens residence time and reduces final activity while leaving this time-normalized metric almost unchanged. It can still raise oxygen demand and fail transfer. Growth is therefore not biologically unimportant. qP perturbations directly scale net QP, while total titer changes less because the initial 100,000 U is retained. These one-at-a-time 20% scenarios are not uncertainty intervals, and infeasible cases must remain identified. [Sensitivity CSV; exact CS solution.]

## 6. Oxygen, heat and recovery economics are plausible screens

**Oxygen stoichiometry:** The source really gives 0.206 **mol** O2/g biomass, not mmol. At the selected S, mu = 0.04311 h^-1, qS = 0.23461 g/g/h and qO2 = 0.009492 mol/g/h. Their ratio, 0.04046 mol O2/g methanol, is below complete oxidation (`CH3OH + 1.5 O2 -> CO2 + 2 H2O`, about 0.04682 mol/g). This passes a gross plausibility check, not a full elemental/energy closure: activity has no established protein-mass conversion, and product synthesis is not a separate substrate sink. [T, Tables 4.2/5.1; source audit.]

**Heat:** Mixing electricity is an energy cost, not total cooling duty. As an order-of-magnitude calculation only, the 440 kJ/mol O2 measured in a primary aerobic-fermentation study would imply about **211 W metabolic heat** at the selected peak total OUR of 1.723 mol/h, plus about **38 W gassed shaft dissipation**. This is not a measured methanol-ROL heat balance. The budget's thermal allowance does not establish jacket capacity. No new thermal model is needed; keep this limitation explicit. [Birou et al. (1987), primary experimental abstract](https://pubmed.ncbi.nlm.nih.gov/18581452/).

**Recovery and cost:** The membrane route is compatible with extracellular ROL; diafiltration remains proposed. Seventy percent recovery means retained **assay activity**, not 70% protein purity, broth volume, enzyme mass or recovery of methanol. The budget correctly applies it to total harvest activity: 1.06084 million U × 0.70 = 0.74259 million recovered U, giving about INR 13,487/million recovered U. Using net induction activity for productivity but total harvest activity for a saleable batch denominator is coherent if clearly stated. No selling price or profitability follows. The pre-existing 0.100 million U must be supported by upstream operation; it is an initial-condition assumption, not free newly made induction product. [Budget/cost CSVs; code `budget`; T; R19.]

Gas cost integrates the fixed 75% blend for the full induction, while the narrative also calls it an upper-capacity case and proposes a cascade. Treat that cost as the stated fixed-blend scenario, not metered cascade consumption. Preinduction oxygen, seed timing, thermal utilities and minor feeds use allowances. Cost sensitivity uniformly scales rates and changes recovery at fixed process cost; it does not simulate extra recovery steps or their cost. [Budget CSV/JSON; source audit.]

## Primary-source basis

- **T:** Ponte Font (2017), [UAB thesis](https://ddd.uab.cat/pub/tesis/2017/hdl_10803_457712/xpf1de1.pdf), especially Chapters 4–5, Table 5.1 (printed p. 103/PDF 110), and Chapter 7 pilot evidence. Local extracted evidence: OS temp `cl420-ponte-source-audit/ponte-thesis.txt`. Final 2018 parameter-table identity and inaccessible File S1 remain unverified, as recorded in `final-design-source-audit.md`.
- **R19:** López-Fernández et al. (2019), [primary article](https://ddd.uab.cat/pub/artpub/2019/216725/catalysts_a2019v9p961.pdf), §3.4: compatible recovery sequence, not a measured Ponte-batch recovery.
- **Transfer correlations:** [Yawalkar et al. (2002), primary publisher PDF](https://pure.rug.nl/ws/portalfiles/portal/14527504/2002CanJChemEngYawalkar2.pdf), and [Labík et al. (2017)](https://doi.org/10.1016/j.ces.2017.04.006), with access and validity limits recorded in the existing source audit. Correlation values do not qualify real broth.

The oxygen correction is derived directly from the repository's stated gas/liquid assumptions. No external source is needed to establish that mathematical inconsistency. No code, report, presentation, Git or GitHub state was changed during this review.

## Implementation and visual follow-through

The main implementation subsequently corrected the gas-capacity screen, its inverse, scan feasibility, and proposed tank geometry. Gas capacity is independently checked against the log-mean equation at the calculated capacity. The inverted kLa is substituted back into the capacity equation to verify the 20 percent demand allowance. Kinetic predictions remain unchanged.

All six generated simulation figures were visually inspected individually, including the comparison bar chart outside the submitted report. The report's quality-attribute table and all eight numbered tables were inspected on rendered pages. Reference endpoints are now identified as unconstrained kinetic calculations. Model-derived yields are labelled predicted, and the weak growth-rate sensitivity of QP is explained through time/activity cancellation.

The recovery diagram was rebuilt in Python with equal-sized stages, wash-buffer input and separate cell/solute removal streams. The same PNG is embedded in the presentation. Assay language now defines the activity basis of the published parameter values without implying that the team performed laboratory measurements. Oxygen transfer, recovery and economics remain conditional design calculations rather than experimental validation.
