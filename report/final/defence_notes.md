# Group 21, report discussion notes

These notes support report review and later Q&A. They are not presentation slides or a speaking script.

## What was done in this study?

A four-state model was implemented in Python to calculate reactor volume, biomass, methanol and extracellular enzyme activity during induction. Monod and substrate inhibition kinetics were compared under defined feeding policies. The study then screened constant methanol setpoints, calculated oxygen transfer requirements, and estimated recovery and batch costs.

The kinetic parameters come from Ponte's thesis. The simulation outputs, comparisons, transfer screen and design calculations were produced for this project. No experimental measurements were made by the team.

## What is the product and why this host?

The product is recombinant Rhizopus oryzae lipase, an enzyme relevant to lipid processing and biodiesel applications. Pichia pastoris X-33 expresses it under the methanol induced AOX1 promoter and secretes it into the broth. Secretion supports a recovery route based on removing cells and concentrating the liquid.

The proposed final product is a concentrated liquid industrial enzyme preparation. It is not assigned pharmaceutical or food certification.

## What does substrate inhibition mean?

At low methanol, adding substrate increases the rate. At higher methanol, inhibition offsets that benefit. The Haldane rate curve therefore has a peak. The Monod curve only approaches saturation. Removing inhibition changes both the growth prediction and the feed needed to maintain a substrate setpoint.

The nominal maximum coefficients are not the achieved peaks of the Haldane curve. The growth coefficient is 0.069 per hour, but the calculated curve peaks near 0.0455 per hour.

## Why track amounts instead of concentrations?

Feed changes the culture volume. A concentration can fall from dilution even while the total amount increases. Balancing biomass amount, methanol amount and total activity makes production, feed and consumption terms explicit. Concentrations are then obtained by dividing by the current volume.

## What are CF, CM, LM and CS?

CF is a constant methanol mass feed of 14 g/h. CM is a prescribed exponential feed based on a target growth rate of 0.03 per hour. LM uses a target growth rate that rises from 0.01 to 0.04 per hour over a specified 60-hour ramp. CS is the ideal mass-balance feed that holds methanol concentration constant.

CM and LM use the same prescribed feed history under both models. CS uses each model's own uptake rate. Thus, the CS comparison uses the same setpoint policy but different actual feed histories.

## Why do the final results differ from the midterm?

The final calculation includes nitrogen feed volume, uses common initial methanol conditions for the reference cases, and defines the growth-based feeds explicitly. The selected setpoint is also different from the 2 g/L reference. The final report is internally consistent with its revised model and should be assessed using its own assumptions and results.

## Is 3.4 g/L the true optimum?

It is the best feasible point on the nominal 0.1 g/L grid under the stated inhibition parameters and oxygen screen. Points from 3.2 to 3.6 g/L differ in productivity by less than 0.3 percent. The biological data do not support a claim that 3.4 is uniquely optimal. The practical proposal is a candidate region for experimental testing.

## Why not simply select the Monod model's highest curve?

Performance and oxygen supply must be checked together. The unfiltered Monod curve rises over the tested interval, but its higher growth rates also require more oxygen. Under the same transfer screen, its best feasible grid point is 1.0 g/L, rather than the highest tested setpoint. This is a design consequence of the kinetic assumption, not proof that either model has been experimentally validated here.

## Is oxygen supply proven sufficient?

No. The selected candidate needs about 909 per hour kLa including the defined 20 percent allowance on demand. The design specifies a qualification target of at least 1000 per hour in the real broth, with the stated gas and agitation conditions. The water and electrolyte correlations predict a wide range and do not prove that this target can be achieved.

If the real reactor cannot meet the target, the proposed high-density operating point must be revised. The current four-state model does not predict the biology after oxygen becomes limiting.

## What is special about the DO percentage?

The target is 25 percent of air saturation. It corresponds to a fixed absolute dissolved oxygen concentration at the chosen temperature. When inlet gas is enriched with oxygen, the saturation concentration rises, but the air-calibrated DO target is retained. Using 25 percent of the enriched saturation concentration would be a different operating condition.

## Is the 20 percent allowance the same as 20 percent spare capacity?

No. The calculation requires capacity to be at least 1.20 times demand. A rule that demand must stay below 80 percent of capacity would require capacity to be at least 1.25 times demand. The report uses the first definition throughout.

## What do the yields mean?

The source coefficient 5.14 is grams of methanol per gram of biomass formed. Its reciprocal is the intrinsic biomass yield before maintenance. The reported batch biomass yield uses the net biomass increase divided by total methanol consumed. Product yield uses net enzyme activity formed per gram of methanol consumed. It therefore has units of U/g, not g/g.

## Why is the cost not given per kilogram of enzyme?

The model predicts enzyme activity, not purified enzyme mass. A conversion would need a matching specific activity measured on the same product form with the same assay. Using a different lipase variant's activity would introduce an unsupported conversion. Cost per batch and per million recovered activity units are appropriate for the available data.

## How reliable is the cost estimate?

It is an illustrative quantity-times-rate budget. Unit rates, equipment occupancy, minor feed allowances and recovery are assumptions. The budget includes seed and basal medium, feeds, gas, utilities, equipment use, recovery, labour and waste treatment. It does not establish a selling price, profit margin or industrial capital cost.

## What does the sensitivity study show?

Product rate uncertainty changes activity and unit cost directly. Increasing the growth coefficient can increase oxygen demand enough to remove the candidate's transfer margin, even when productivity changes little. The chosen 20 percent parameter changes are scenarios, not confidence intervals or a parameter refit.

## How was the code checked?

The time step was halved for all eight reference cases. Integrated material balances were checked against the trajectories. Constant substrate results were checked against an independent analytical solution. These checks support the numerical implementation. They do not replace comparison with experimental data.

## What would industrial scale-up require?

Broth-specific oxygen transfer, mixing, heat removal, gas supply and recovery must be demonstrated at pilot scale. Matching rpm, vvm or a single DO probe reading does not establish identical cell conditions. The source ROL process lost performance at 50 L. Another Pichia process reached 1000 L with pressure and altered feeding, but produced a different intracellular enzyme. Its titer cannot be transferred to this lipase process.

## What are the main limitations?

The model assumes ideal mixing, instantaneous substrate-dependent kinetics and no product degradation. It omits adaptation dynamics, base and antifoam volume, evaporation and spatial gradients. Oxygen transfer is a separate feasibility calculation. The proposed equipment capacity, downstream recovery and budget rates need confirmation before operation.
