# Final-design source audit: Ponte ROL process

**31 October physical-review correction.** The later review in `final-physical-review.md` supersedes the demand-based oxygen-capacity and reserve calculations below. Current calculations integrate transfer self-consistently, giving required kLa about 909 per hour, a Monod feasible grid limit of 1.0 g/L, and proposed tank diameter 0.13 m. Earlier arithmetic is retained as audit history, not the current design basis.

Audit date: 30 October 2026. This is bounded preparation for design decisions, not a completed design. **Reported** values below come from primary sources. **Calculated** values use the stated equations. **Proposed** bounds are engineering assumptions for a feasibility screen. No simulation was run or changed.

## Sources and access limits

- **[T] Ponte Font, X. (2017), _Bioprocess efficiency as a roadmap to establish Pichia pastoris as a reliable cell factory_.** [UAB thesis PDF](https://ddd.uab.cat/pub/tesis/2017/hdl_10803_457712/xpf1de1.pdf). This is the thesis title; the feeding-paper title belongs to Chapter 5. Page references below give printed page, followed by PDF page. Chapter 5 is a manuscript precursor, not proof that every value is unchanged in the final publication.
- **[P] Ponte et al. (2018), JCTB 93, 3208–3218, DOI 10.1002/jctb.5677.** [Publisher abstract and supporting-information listing](https://scijournals.onlinelibrary.wiley.com/doi/abs/10.1002/jctb.5677). The abstract verifies the ROL/Mut+/PAOX1 system and reported relative improvements. The final article's parameter table was not readable in this audit. **Neither qmax,P = 2200 nor YO2/X = 0.206 was independently verified against the final 2018 table.** Both are verified in the thesis.
- **[S1] Authors' File S1**, listed by [P] as `jctb5677-sup-0001-FileS1.docx`, 421.2 KB. The publisher explicitly says it contains predictive-adaptive PI derivation, process-model details, standard-strategy simulations, and algorithm comparison. [Official download](https://scijournals.onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1002%2Fjctb.5677&file=jctb5677-sup-0001-FileS1.docx) returned HTTP 403. Its contents and any numerical controller settings remain unchecked. Do not claim that controller details are absent from the publication.
- **[R19] López-Fernández et al. (2019), _Truncated Prosequence of Rhizopus oryzae Lipase: Key Factor for Production Improvement and Biocatalyst Stability_, Catalysts 9, 961.** [Primary full text](https://ddd.uab.cat/pub/artpub/2019/216725/catalysts_a2019v9p961.pdf), DOI 10.3390/catal9110961. Used for product-form distinctions and a compatible downstream sequence, not replacement titers or kinetics.
- **[R21] López-Fernández et al. (2021), Catalysts 11, 1192.** [Primary full text](https://ddd.uab.cat/pub/artpub/2021/254945/catalysts_a2021v11n10p1192.pdf), DOI 10.3390/catal11101192. Its PGAP/proROL system is a different process.
- **[B18] Barrero et al. (2018), Microbial Cell Factories 17, 161.** [Primary full text](https://ddd.uab.cat/pub/artpub/2018/200901/Articulo_final_MCF_Juanjo_2018.pdf), DOI 10.1186/s12934-018-1009-5. Used only to explain the Roche assay chemistry and unit convention; its BTL2 assay is not the Ponte ROL assay.

## Exact host, product, and activity basis

**Reported:** Pichia pastoris X-33 carrying pPICZαROL, PAOX1, Mut+; the thesis introduction describes a single ROL gene copy. Product activity is extracellular and is measured after removal of cells. [T, p. 11/PDF 18; §§5.2.1 and 5.2.4.3, pp. 94–96/PDF 101–103.] Keep this identifier rather than substituting GS115, KM71, a Mut-slow clone, a multicopy clone, or a constitutive promoter.

**Product interpretation:** this is the established mature recombinant ROL lineage, not an engineered proROL process. R19 explicitly distinguishes mature rROL from a new construct with 28 prosequence amino acids attached to its N-terminus, and reports approximately 29 versus 33 kDa respectively. Its §3.1 starts from the group's existing PAOX1 rROL plasmid. This supports the mature-product interpretation; an exact sequence and processing map for the particular Ponte clone was not independently checked. The α-vector name supports an α-factor secretion construct, but does not establish cleavage efficiency or the exact secreted N-terminus. [R19, pp. 2, 4–5, 10, §§2.2 and 3.1.]

**Verified Ponte assay:** Roche lipase colorimetric kit; clarified supernatant; 30 °C; pH 7.25; stated buffer 400 mM Tris-HCl plus 10 mM CaCl2; 580 nm for 4 min. Chapter 5 refers back to this method. [T, §4.2.4.4, p. 65/PDF 72; §5.2.4.3, p. 96/PDF 103.] These are assay conditions, distinct from cultivation pH 5.5.

**Unit gap:** the readable Ponte methods do not explicitly define the chemical amount per U or give its full calibration. B18, p. 3, defines one unit in a related Roche **BTL2** assay as hydrolysis of 1 µmol ester bond/min and names the methylresorufin-linked dilauryl substrate. That assay uses 50 °C and a different read interval. It supports the assay family's meaning, but cannot certify Ponte's exact calibration. Label results as **Ponte/Roche-assay U**, pending the original assay protocol. Do not identify these units as p-nitrophenyl-palmitate, olive-oil, or triolein units.

**No activity-to-mass conversion is established.** Do not divide Ponte U by proROL specific activity, by total Bradford protein, or by a specific activity measured with another substrate. R19 itself reports different product forms, assay-buffer dependence, and only a fraction of total extracellular protein as ROL. Its activity or powder data cannot supply the missing conversion for this batch. [R19, §§2.2–2.3, Table 3, pp. 4–6; §3.7, p. 12.] Use U/batch and cost per recovered activity until a matching purified-rROL calibration is available.

## Operating basis and oxygen-transfer bounds

| Item | Verified basis and recommended use |
| --- | --- |
| Vessel and start | 5 L Biostat B; initial culture volume 2 L. These are different quantities. [T, p. 94/PDF 101.] |
| Temperature and pH | 30 °C and pH 5.5 throughout the three phases. [T, p. 95/PDF 102.] |
| Glycerol batch | DO above 25% air saturation; 600–1000 rpm; 1 vvm air. [T, p. 94/PDF 101.] |
| Transition | 5 h, glycerol plus stepwise methanol adaptation; DO 25%. [T, pp. 94–95/PDF 101–102.] |
| Methanol induction | DO 25% air saturation; 800–1000 rpm; **total air plus added pure oxygen** 1–2 vvm. This is not an air-only recipe. [T, p. 95/PDF 102.] |
| Pressure | No operating backpressure value was found in the Chapter 5 methods. Use 1 bar absolute only as an explicit screening assumption. Elevated pressure is not a verified Ponte condition. |
| Methanol | CS comparator 2 g/L; model growth and product critical concentrations about 1.9 and 3.5 g/L; model upper constraint 10 g/L. A 2–3.5 g/L range is a defensible initial comparison range, not an optimized profile. [T, Tables 5.1–5.2, pp. 103–104/PDF 110–111.] |
| Biomass and volume | Model limits X ≤ 55 g DCW/L and V ≤ 5 L. They are optimization constraints, not proof that a nominal 5 L vessel has adequate headspace at 5 L working volume. [T, p. 101/PDF 108.] |

The related **same-strain oxygen study**, reproduced in Chapter 4, used S = 3 g/L and nominal DO setpoints 5, 10, 25, and 50%; actual means were approximately 7, 10, 25, and 45%. At 25%, mean qO2 was 7.35 mmol/g/h and maximum OTR approximately 265 mmol/L/h. The best titer and volumetric productivity occurred at 25%; the highest product/biomass yield occurred at 10%. Therefore a lower DO setpoint cannot be assumed to preserve the Chapter 5 growth and production laws. Chapter 4's gas range is printed as 0–1 vvm; do not substitute it for Chapter 5's 1–2 vvm. [T, pp. 64, 77–80/PDF 71, 84–87; Table 4.1.]

**DO normalization:** the stated air-saturation concentration is about 2.3 × 10^-4 mol/L. At 25% air saturation, CL is approximately **5.75 × 10^-5 mol/L**, not 2.3 × 10^-4. With oxygen enrichment, keep CL tied to the air-calibrated setpoint; calculate a different C* from gas oxygen partial pressure. Neither total vvm nor rpm alone determines kLa. [T, p. 95/PDF 102; oxygen-transfer discussion pp. 156–159/PDF 163–166.]

**Calculated screening case, not a simulation:** with S = 2 g/L, the thesis model gives µ = 0.04549 h^-1 and qO2 = 0.009982 mol/g/h. Thus OUR = qO2 X rises from approximately **0.270 to 0.549 mol/L/h** as X rises from 27 to 55 g/L. Using OTR = kLa(C* − CL), the following are idealized requirements at X = 55 g/L:

| Inlet O2 mole fraction | Estimated C*, mol/L | Required kLa, h^-1 |
| ---: | ---: | ---: |
| 0.21 | 0.000230 | 3183 |
| 0.40 | 0.000438 | 1442 |
| 0.60 | 0.000657 | 916 |
| 1.00 | 0.001095 | 529 |

Assumptions: atmospheric screening pressure, C* proportional to oxygen partial pressure, fixed CL, and inlet gas composition used at the interface. These omit oxygen depletion through the vessel, broth salting effects, and spatial gradients. They can overstate available driving force; they are not measured kLa values. At an assumed kLa of 500 h^-1, air-only OTR is just 0.086 mol/L/h, below even the initial CS demand.

**Proposed bounds for the next feasibility screen:** retain DO 25%, the source agitation/gas ranges, and oxygen enrichment as an available control action. Test OTR capability across 0.27–0.55 mol/L/h; a provisional 20% capacity allowance gives 0.32–0.66 mol/L/h. The allowance is a design assumption. Do not approve 55 g/L from kinetics alone. If verified OTR is lower, constrain biomass or feed rather than claiming the present model predicts oxygen-limited behavior. Measure kLa in the actual broth and record gas composition, working volume, and pressure before equipment sizing. No numerical measured kLa for Chapter 5 was established here.

## Parameter and unit audit

The rendered thesis Table 5.1 confirms the repository's numerical transcription:

| Coefficient | Printed thesis value and unit |
| --- | --- |
| µmax; KS,X; KI,X | 0.069 h^-1; 0.50 g/L; 7.5 g/L |
| qmax,P; KS,P; KI,P | 2200 U/g/h; 10.0 g/L; 1.2 g/L |
| YS/X; mS/X | 5.14 g methanol/g biomass; 0.013 g/g/h |
| YO2/X; mO2/X | **0.206 mol O2/g biomass; 6.1 × 10^-4 mol O2/g/h** |

[T, Table 5.1, p. 103/PDF 110; oxygen coefficients also Table 4.2, p. 80/PDF 87.]

- **The mol/g oxygen unit is real in the source.** It is not 0.206 mmol/g or 0.206 g/g. At µ = 0.034 h^-1, the fitted law predicts 7.61 mmol/g/h, close to Table 4.1's measured 7.35 mmol/g/h. The growth-associated oxygen/methanol ratio is 0.206/5.14 = 0.0401 mol O2/g methanol, below complete methanol oxidation's approximately 0.0469 mol/g. This check does not indicate a factor-of-1000 error.
- **The growth/substrate model is not on a mol/g basis throughout.** S, KS and KI use g methanol/L, biomass uses g DCW, µ uses h^-1, and product rate uses U/g/h. C-molar stoichiometric discussions elsewhere do not change Table 5.1's units. YS/X means substrate consumed per biomass formed, not the reciprocal biomass yield.
- **Nominal maxima are not achieved maxima.** The inhibition denominator reduces the actual peak: µ peaks near 0.04550 h^-1 and qP near 324.8 U/g/h, not 0.069 h^-1 and 2200 U/g/h. Table 5.1 reports CV above 100% for all three product-curve parameters, so their fitted combination is better supported than each coefficient individually.
- At S = 2 g/L, calculated apparent yields are **µ/qS = 0.1843 g/g** and **qP/qS = 1162.5 U/g**. These describe the induction-model consumption basis. They exclude seed/glycerol costs, downstream loss, and any conversion of activity to protein mass.
- The existing code calculates oxygen demand but has no DO or OTR constraint. The thesis also accounts for additional liquid and gas-related volume terms. Agreement with its kinetic table alone does not establish a full process replication. [T, §§4.2.5 and 5.3.1, pp. 66–68 and 96–98/PDF 73–75 and 103–105.] This audit requests no code change.

## Compatible downstream route and lab-batch cost basis

**Recommended starting route:** harvest broth, remove cells by centrifugation and microfiltration, then ultrafilter to concentrate extracellular ROL. Consider diafiltration for salt/methanol removal; treat it as a proposed addition requiring retention and activity checks. Keep concentrated liquid as the simplest product option. Add lyophilization only if a powder is required. Centrifugation → microfiltration → ultrafiltration → lyophilization is directly reported for both rROL and proROL in R19, §3.4, p. 11. This is compatible adjacent evidence, not a downstream recovery measured for Ponte's 2018 batch. Do not use cell disruption or assume affinity purification without a demonstrated tag. Chromatography requires a product-purity justification; no Ponte-specific column recovery was established.

**Cost quantities for a 2 L initial batch:** the thesis recipe gives 80 g glycerol, 53.4 mL 85% phosphoric acid, 1.86 g CaSO4, 36.4 g K2SO4, 29.8 g MgSO4·7H2O, 8.26 g KOH, 10 mL trace stock, 4 mL biotin stock, and 1 mL initial antifoam. Cost the trace stock from its component recipe, not as a bulk volume of pure salts. Add seed medium, the 5 h transition feeds, pH-control additions, and subsequent antifoam separately. The seed recipe prints **500 µg zeocin/L**; preserve that value as printed and verify before purchase rather than silently changing it to a customary selection concentration. [T, pp. 94–95/PDF 101–102.]

During induction, each **100 g methanol** requires **12 g NH4Cl**, hence **60 mL of the reported 200 g/L NH4Cl feed**. Methanol and NH4Cl feeds each also contain 5 mL trace stock and 2 mL biotin stock per litre of their respective solution. This nitrogen-feed volume is material to final broth and downstream capacity; the simplified simulation's methanol-volume increase alone is not the complete volume basis. [T, p. 95/PDF 102.]

Use a quantity-times-rate budget with no claimed current prices:

`batch cost = media + all feeds + air/O2 + utilities + consumables + downstream + labor + equipment-use allocation + waste treatment`.

For gas costs, integrate measured air and supplemental-O2 flows separately; 1–2 vvm corresponds to 2–4 L/min total inlet gas at 2 L culture. Declare the gas reference temperature and pressure. Cost agitation, cooling, sterilization, centrifugation, and drying from equipment time and measured/rated consumption, with assumptions visible. Show shared-equipment use separately from new equipment purchase. For downstream costing, provision membrane/filter use, buffer/water, and optional dryer or column time.

Report cost/batch and cost per million **recovered assay U**. Use `recovered U = harvest U × activity recovery`. As an explicit sensitivity assumption, compare 50%, 70%, and 90% total recovery; these are not literature recoveries. Count all upstream phases in the cost even if the performance denominator uses newly formed induction activity. No current supplier prices, product selling price, purified-product mass, or profit claim is established.

## Scientific gaps to carry into design work

1. **Final publication versus precursor:** final 2018 parameter-table identity and File S1's detailed model/controller settings remain unverified because of access limits. The defensible label is “thesis-based parameter set associated with the Ponte process.”
2. **Oxygen capacity:** the required enriched-gas fraction, actual broth kLa, off-gas depletion, pressure, and mixing at the intended final volume remain unknown. These determine feasible biomass/feed bounds. Chapter 7's unsuccessful transfer to 50 L cautions against using a matching DO probe reading as proof of equivalent performance. [T, pp. 157–159 and 168/PDF 164–166 and 175.]
3. **Assay and mass:** establish the original Roche calibration and a same-form, same-assay ROL-specific activity before any U-to-gram conversion. Total extracellular protein is not purified ROL mass.
4. **Downstream specification:** retention, fouling, activity recovery, residual methanol/salts, purity, and storage stability need confirmation for the selected liquid or powder product. Until then, use the explicit recovery sensitivities above.
5. **Keep evidence separate:** R19's truncated-prosequence PAOX1 constructs, R21's PGAP/proROL constructs, B18's altered secretion signals/BTL2 assay, and other Mut-slow, mixed-substrate, native-fungus or E. coli studies cannot supply interchangeable titers, oxygen coefficients, secretion performance, or assay conversions.

## Addendum: scale-up, equipment screen, prices, and pre-induction time

Added 30 October 2026 for Group 21. This addendum supplies research inputs to the report implementation. It does not change the simulation or authorize presentation generation before report approval.

### Same-process pilot evidence and the industrial-scale paragraph

The thesis Chapter 7 is the most directly relevant primary scale-up source. It transferred the same PAOX1 ROL process to a **50 L Biostat UD with 20 L initial culture**, using methanol non-limited feeding at S = 3 g/L and DO near 25% air saturation. The cascade used 300–600 rpm, then pure O2 mixed with air, at 1–2 vvm total gas. The suggested approximately 500 rpm equivalent to the bench's 1000 rpm came from the equipment kLa curves in Figure 7.2, not a new measurement of oxygen transfer in the production broth. [T, §§7.2–7.3.1, pp. 158–160/PDF 165–167; Fig. 7.2.]

The transfer did **not** preserve production:

| Quantity | Pilot | Lab comparator |
| --- | ---: | ---: |
| Mean growth rate, h^-1 | 0.013 ± 0.002 | 0.034 ± 0.001 |
| Mean qP, U/g/h | 48 ± 6 | 256 ± 22 |
| Final activity, U/mL | 59.8 | 368 |
| Volumetric productivity, U/L/h | 585 | 5490 |
| Estimated mean qO2, mmol/g/h | 4.13 | 7.35 |
| Listed maximum OTR, mmol/L/h | 157 | 430 |

[T, Table 7.1, p. 166/PDF 173, visually checked.] Productivity was approximately **9.4 times lower** at pilot scale, calculated from this table. Pilot qO2 was estimated from carbon/electron balances because the pilot lacked off-gas O2/CO2 analyzers. Matching bulk DO therefore did not establish matching physiology or oxygen-transfer conditions. Oxygen gradients are a proposed explanation, not a measured or isolated cause. [T, pp. 166–168/PDF 173–175.]

**Source inconsistency:** Chapter 4 Table 4.1 lists 265 mmol/L/h for the 25% DO run, whereas Chapter 7 Table 7.1 lists 430 for its lab comparator. Both have the same listed mean qO2 of 7.35 mmol/g/h and activity of 368 U/mL. Preserve each table's provenance; do not present either maximum as a uniquely reconciled measured capacity of the chosen bench reactor. The discrepancy was not resolved in this bounded audit. Also, this Chapter 7 test used constant S = 3 g/L, not the Chapter 5 optimized OP1/OP2 profiles. [T, Tables 4.1 and 7.1, pp. 77 and 166/PDF 84 and 173.]

**Suitable report paragraph:** “The design is evaluated at bench scale. Direct transfer of this ROL process to a 50 L vessel was attempted by Ponte, but volumetric productivity fell from 5490 to 585 U/L/h despite nominally similar methanol and dissolved-oxygen settings. Industrial development therefore requires broth-specific oxygen-transfer and mixing tests, heat-removal assessment, gas-use evaluation, and validation of feeding and secretion performance. Bench activity and productivity are not multiplied by industrial volume as predictions.” [T, Chapter 7, especially Table 7.1 and pp. 167–171/PDF 174–178.]

**Transferable engineering evidence from a different product:** Liu et al., *Scientific Reports* **6**, 18439 (**2016**, not 2015; 2015 was submission/acceptance), [primary PDF](https://www.nature.com/articles/srep18439.pdf), DOI 10.1038/srep18439, pp. 1–2, demonstrated Pichia fermentation up to a nominal 1000 L scale for an **intracellular Lentinula edodes glycoside hydrolase in GS115-3.5K-P1-2**. The study substituted higher pressure for pure-O2 supplementation, increasing the stated super-atmospheric pressure from 0.05 to 0.10 ± 0.05 MPa. These are **gauge**, not absolute, pressures: the latter condition is roughly 2 bar absolute at the central value. This supports pressure as an industrial engineering option for a suitable vessel. It supplies no ROL titer, secretion recovery, transferable DO optimum, or guarantee of ROL productivity. Retain atmospheric pressure as the explicit bench screening assumption unless a pressure rating and operating basis are available.

### Primary kLa correlations: equations, units, and limits

**[K79]** van't Riet (1979), *Review of Measuring Methods and Results in Nonviscous Gas-Liquid Mass Transfer in Stirred Vessels*, *Industrial & Engineering Chemistry Process Design and Development* **18**, 357–364, [DOI 10.1021/i260071a001](https://pubs.acs.org/doi/10.1021/i260071a001). The original PDF was blocked. The equations were independently checked in these primary research papers:

- **[K02]** Yawalkar et al. (2002), *Gas–Liquid Mass Transfer Coefficient in Stirred Tank Reactors*, *Canadian Journal of Chemical Engineering* **80**, 840–848, [author-institution publisher PDF](https://pure.rug.nl/ws/portalfiles/portal/14527504/2002CanJChemEngYawalkar2.pdf). Table 2, p. 842/PDF 4, reproduces the water correlation; nomenclature, p. 847/PDF 9, gives the SI units. Table 1, p. 841/PDF 3, describes the underlying coalescing-system datasets and equipment conditions. Its power-number definitions support the power calculation below.
- **[K17]** Labík et al. (2017), *Volumetric mass transfer coefficient in viscous liquid in mechanically agitated fermenters. Measurement and correlation*, *Chemical Engineering Science* **170**, 451–463, [primary publisher text](https://www.sciencedirect.com/science/article/pii/S0009250917302488), [DOI 10.1016/j.ces.2017.04.006](https://doi.org/10.1016/j.ces.2017.04.006). The indexed Introduction explicitly reproduces both equations and their water/electrolyte assignments. The full PDF was inaccessible; its equation numbers and exact page within the Introduction were not verified. Do not invent those locators.

```text
Water / coalescing:       kLa = 0.026 (Pg/VL)^0.4 us^0.5
Electrolyte / generally
non-coalescing:           kLa = 0.002 (Pg/VL)^0.7 us^0.2

kLa: s^-1; Pg: gassed power delivered to liquid, W;
VL: liquid volume, m^3; us = Qgas / vessel cross-sectional area, m/s.
Multiply the calculated kLa by 3600 to obtain h^-1.
```

The numerical prefactors carry units: neither W/L nor rpm can be inserted directly. Use gas flow at the stated vessel temperature and pressure for us; convert standard litres if needed. Gassed power is not motor nameplate power. The relations concern gas dispersion in agitated liquids; they are not universal culture-broth laws. Use the water equation as a **lower screening scenario**, not a guaranteed lower bound under antifoam, viscosity, high biomass, or poor dispersion. Use the electrolyte equation as an optimistic scenario, not proof that basal salts make its prediction correct. K17 explicitly treats viscous liquids as a separate category. K02 also discusses incomplete dispersion below the complete-dispersion speed. No exact, universally applicable validity envelope for the original K79 equations was verified; do not borrow the validity limits of a different correlation or of K02's own fitted equation.

### Bench hardware and oxygen-enrichment calculation

The following is an **illustrative equipment snapshot**, not the measured geometry or performance of Ponte's Biostat B. Assumptions: baffled tank diameter 0.13 m; liquid volume 2 L; two 0.060 m six-blade disc turbines; N = 1000 rpm = 16.67 s^-1; liquid density 1000 kg/m^3; power number 5 per turbine; independent turbine powers; Pg/P0 = 0.50; total gas 4 L/min at 30 °C and 1 bar absolute, equivalent to 2 vvm at this volume. Geometry, power number and the gassing factor are proposed values requiring hardware confirmation.

Using `P0 = sum(Np rho N^3 D^5)` gives **36 W ungassed**, **18 W gassed**, `Pg/VL = 9000 W/m^3`, and `us = 0.00502 m/s`. The correlations give:

| Scenario | Estimated kLa, h^-1 | Interpretation |
| --- | ---: | --- |
| Water/coalescing | 253 | Conservative screening scenario; even pure O2 gives only about 0.263 mol/L/h at the stated CL, below the 55 g/L demand. |
| Electrolyte/non-coalescing | 1464 | Optimistic estimate; must not be selected as measured broth performance. |
| Conditional working case | 800 | Explicit assumption between the two estimates, requiring measurement before acceptance. |

The final values above use Pg/P0 = 0.50. A preliminary 0.60 assumption would give the approximately 270–1660 h^-1 range; it is not an additional measurement.

**A conditional feasible gas case:** retain S = 2 g/L, X = 55 g/L, DO = 25% air saturation, so OUR = 0.549 mol/L/h. If actual broth kLa is **800 h^-1**, a **90% O2 inlet blend** at 4 L/min gives inlet-basis OTR = 0.743 mol/L/h, above the demand. Mixing air and pure O2 requires **3.49 L/min pure O2 plus 0.51 L/min air** at the same flow reference. This fits the reported total 2 vvm at the illustrative 2 L snapshot; it does not verify the installed gas controller's range.

A simple dry off-gas check strengthens this screen. At 30 °C and 1 bar, 4 L/min is 9.52 mol gas/h. At 2 L culture and the above X, total OUR is 1.098 mol/h; the thesis CO2 law gives CER about 0.680 mol/h. A steady dry gas balance gives outlet O2 fraction approximately **0.821**. Even using that outlet fraction for C*, OTR at kLa = 800 h^-1 is approximately **0.673 mol/L/h**, about 23% above demand. This omits water/methanol vapor, salting effects, gas holdup and spatial gradients; it remains an estimate, not validation. Demand reduction or stronger transfer is required if measured broth kLa is closer to the water estimate.

Recompute power/volume, us, gas depletion and transfer at **each actual culture volume**. The 2 L snapshot is not the final volume of a complete trajectory. Hardware evidence still needed includes impeller geometry and spacing, delivered torque/power, gas-controller capacities and calibration, sparger/dispersion, oxygen-compatible supply, condenser/exhaust basis, and measured broth kLa with the actual antifoam. The thesis demonstrates oxygen-enriched operation, not that every bench setup supports this proposed blend.

### Prices: explicit budget assumptions, not current supplier quotations

No reliable current manufacturer quote in public INR was verified within this bounded search. A manufacturer's **historical 2019–21** [Loba price-list page 56](https://www.lobachemie.com/flipbooks/lobachemie-pricelist/files/assets/basic-html/page56.html) was accessible in indexed text: NH4Cl 99.5% AR/ACS, code 01140, 500 g at INR 350. A subsequent live request returned a not-found page. Treat this only as an archival manufacturer listing, not a current quote. Its age and unstable availability make it unsuitable for a current-price claim. The manufacturer's product list also identifies methanol grades and packs but does not establish a usable current price.

For a transparent provisional lab budget, the report can adopt these **analyst-selected rates**, with 0.5× and 2× sensitivity cases:

| Reagent | Assumed budget rate | Cost basis |
| --- | ---: | --- |
| Methanol | INR 800/L | Per litre of purchased neat reagent; convert mass using the declared density. |
| Glycerol | INR 1000/kg | Per kilogram of neat glycerol; not per kilogram of 50% feed solution. |
| NH4Cl | INR 1000/kg | Per kilogram of dry salt; not per litre of 200 g/L solution. |

These are **not supplier quotations, verified market prices, or industrial bulk rates**. For illustration, 100 g methanol at 0.792 kg/L costs INR 101 at the assumed rate; its linked 12 g NH4Cl costs INR 12; the initial 80 g glycerol in 2 L BSM costs INR 80. Add transition glycerol/methanol, seed media, salts, base, antifoam, gases, utilities and downstream separately. Distinguish consumption cost from full-pack purchase cost. Tax, delivery, grade and pack size remain unpriced.

### Seed, glycerol, and whole-batch time

| Stage | Verified duration or defensible boundary |
| --- | --- |
| Bench seed flask | **24 h**, 30 °C, 150 rpm, 1 L baffled flask, YPD; the flask size is not the liquid fill volume. [T, §5.2.2, p. 94/PDF 101.] |
| Bench glycerol batch | 40 g glycerol/L initially; the Chapter 5 methods give no exact fixed duration. End this phase by verified glycerol depletion, not an invented published time. [T, §5.2.3, p. 94/PDF 101.] |
| Transition/adaptation | **5 h** with glycerol feed and stepwise methanol feed. [T, pp. 94–95/PDF 101–102.] |
| Pilot inoculum train | 24 h flask seed, then a 2 L seed-reactor glycerol batch with **20 g glycerol/L** before inoculating the pilot. The seed-reactor duration is not specified in this passage. Do not transplant its lower glycerol charge to the production reactor. [T, §7.3.1.2, p. 161/PDF 168.] |

If a single planning time is needed before experimental data exist, use **18 h glycerol batch with a 12–30 h sensitivity range**, explicitly as a scheduling assumption, not a source result or physiological bound. Then production-reactor occupancy is `t_induction + 18 + 5 h`, before sterilization/harvest/cleaning. A strictly sequential seed-to-harvest calendar adds the 24 h seed; parallel seed preparation can reduce calendar delay but does not remove its cost. Report induction productivity and whole-process productivity separately. No source-backed exact glycerol-batch duration, seed fill volume, or turnaround duration was established here.

### OS-temp source files available to the main implementation

- `C:\Users\Mridul Sharma\AppData\Local\Temp\cl420-ponte-source-audit\ponte-thesis.pdf`
- `C:\Users\Mridul Sharma\AppData\Local\Temp\cl420-ponte-source-audit\scale-pressure.pdf` — Liu et al. 2016, 12 pages; `scale-pressure.txt` is its extracted text.
- `C:\Users\Mridul Sharma\AppData\Local\Temp\cl420-ponte-source-audit\yawalkar2002-kla.pdf` — publisher PDF with repository cover; add one to printed-article page offsets as specified above.
- `thesis-p173.png` and `yawalkar-p4.png` in the same temp directory are checked table renders. K79 and K17 full-text downloads were blocked; no valid local PDFs for those articles were obtained.

### Follow-up: correlation validity and the revised final-code equipment basis

The main implementation reports a revised CS result of V = 3.285 L and peak total OUR = 1.8035 mol/h, using two 0.065 m Rushton turbines in a 0.16 m tank at 1000 rpm, Np = 5, and Pg/P0 = 0.70. These are inputs supplied by the main implementation; this sidecar did not run or modify that simulation.

**What the primary sources establish:** K02, Table 2, p. 842/PDF 4, confirms the 0.026 water equation; its nomenclature, p. 847/PDF 9, confirms the SI units. K17's indexed Introduction confirms both the water and electrolyte equations. K79's publisher record identifies the original as a review of **nonviscous** gas–liquid systems. The original full text remains inaccessible. Thus, an exact original power/volume, gas-velocity and volume validity envelope is **not primary-verified in this audit**. Do not state that the chosen equipment lies within a validated universal van't Riet range. [K79, [publisher record](https://pubs.acs.org/iepdaw/article/18/3/357/1748244/Review-of-Measuring-Methods-and-Results-in); K02 and K17 links above.]

K02 Table 1, p. 841/PDF 3, records the coalescing-system datasets it analyzes, including Smith et al.'s 20–5000 W/m^3 and 0.004–0.046 m/s data. These are **that dataset's conditions**, not the full original K79 envelope. The proposed harvest Pg/V of approximately **11,447 W/m^3** is above that dataset's power range, and the 0.16 m tank is smaller than the listed experimental tank diameters. This directly supports an extrapolation warning; it does not establish a sharp failure boundary. Neither the electrolyte equation nor interpolation between the two equations proves that the culture broth achieves kLa = 1000 h^-1. Also, the proposed Pg/P0 = 0.70 and independent addition of two impeller powers are hardware assumptions, not validated by quoting K02's separate gassed-power datasets.

**Independent arithmetic screen at the supplied peak point:** interpreting 2 vvm as actual gas volume at 30 °C and 1 bar absolute gives Qgas = 6.57 L/min, us = 0.005446 m/s, Pg = 37.60 W, and Pg/V = 11,447 W/m^3. The two correlations then give approximately **290 h^-1 water** and **1760 h^-1 electrolyte**. A reported water estimate near 284 h^-1 differs by about 2%; identify the gas-volume reference, volume, and rounding used before presenting a precise value. A standard-litre flow and an actual-litre flow are not interchangeable in us or the molar gas balance.

For the **qualification assumption** kLa = 1000 h^-1, inlet O2 = 0.75, and respiratory quotient RQ = CER/OUR = 1, the dry total gas molar flow remains constant. At this point it is approximately 15.64 mol/h. Hence:

```text
yO2,out = 0.75 - 1.8035/15.64 = 0.6347
CL = 0.25 × 2.3e-4 = 5.75e-5 mol/L
C*in  = 2.3e-4 × 0.75/0.21
C*out = 2.3e-4 × 0.6347/0.21
log-mean driving force = (dCin - dCout)/ln(dCin/dCout)
                       = 6.989e-4 mol/L
OTR capacity = 1000 × 6.989e-4 × 3.285 = 2.296 mol/h
capacity / demand = 1.273
```

This passes `capacity >= 1.20 × demand`, requiring approximately 943 h^-1. It also passes the stricter convention `demand <= 0.80 × capacity`, requiring approximately 982 h^-1. State which definition is used: a 20% allowance on demand and a 20% unused-capacity reserve are different. At the water estimate of 290 h^-1, the same nominal gas-driving-force calculation supplies only about 0.666 mol/h, far below demand; therefore the water scenario does not establish feasibility.

The appropriate report wording is: **“Oxygen supply is conditionally feasible if the actual broth is qualified at kLa ≥ 1000 h^-1 under the specified volume, gas blend, agitation, sparging and antifoam conditions. The van't Riet calculations are screening estimates and do not establish that qualification.”** Apply the screen over every trajectory and to the selected S = 3.4 g/L case, not just this CS2 peak point. RQ = 1 is a gas-balance assumption rather than a result of the thesis's separately fitted CO2 law. Gas moisture, methanol stripping, broth oxygen solubility and pressure must remain explicit limitations of the screen.

### Final bibliography handoff: demonstration-scale paper

**Liu, Wan-Cang; Gong, Ting; Wang, Qing-Hua; Liang, Xiao; Chen, Jing-Jing; and Zhu, Ping. (2016).** “Scaling-up Fermentation of Pichia pastoris to demonstration-scale using new methanol-feeding strategy and increased air pressure instead of pure oxygen supplement.” *Scientific Reports*, **6**, article **18439**. DOI: [10.1038/srep18439](https://doi.org/10.1038/srep18439). [Primary PDF](https://www.nature.com/articles/srep18439.pdf).

Author order, title, article number and dates are verified on PDF p. 1: received **3 September 2015**, accepted **17 November 2015**, published **21 January 2016**. Cite as **Liu et al. (2016)**, not “Scale2015” or a 2015 publication. Its scale-up and pressure findings concern an intracellular glycoside hydrolase, not secreted ROL. Use it only for transferable engineering context, as bounded above. All proposed INR rates remain budget assumptions; no current supplier quotations were established.
