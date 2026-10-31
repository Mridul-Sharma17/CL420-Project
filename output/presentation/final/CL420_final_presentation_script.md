# CL 420 final presentation rehearsal script

Group 21. Target duration is six minutes including the short introduction.

Sneha Shandilya presents the introduction and content slides 2 and 3.
Diggaj Maheshwari presents slides 4 and 5.
Mridul Sharma presents slides 6 and 7.

The slide start times are rehearsal targets. Each member should finish within two minutes. Use this script for rehearsal. The course instructions require delivery without reading from notes.

## Sneha Shandilya, 0:00 to 2:00

### Slide 1 starts, 0:00 to 0:12

Good morning. We are Group 21. Our project compares Monod and substrate inhibition models for recombinant lipase production, and connects the simulations to bioreactor design.

### Slide 2 starts, 0:12 to 1:05

The host is Pichia pastoris, a yeast that secretes Rhizopus oryzae lipase into the culture broth. The proposed product is a concentrated liquid enzyme for industrial lipid processing.

Methanol provides carbon and energy. It also induces the AOX1 promoter, which supports lipase production. Too little methanol limits the process. Excess methanol can inhibit growth and production.

The Monod curves rise towards saturation. The inhibition curves reach a peak and then decline. The growth and production peaks occur at different methanol concentrations. This is why the feeding policy matters.

The bench process uses thirty degrees Celsius, pH five point five, and controlled dissolved oxygen.

### Slide 3 starts, 1:05 to 2:00

The mathematical model tracks four quantities. These are liquid volume, biomass amount, methanol amount, and total enzyme activity.

The balances describe liquid addition, cell growth, substrate feed minus consumption, and enzyme formation. The volume calculation includes the linked nutrient solution as well as methanol.

Four feeding methods are compared. CF supplies fourteen grams of methanol per hour. CM uses a prescribed constant growth target. LM gradually raises that target over sixty hours. CS holds methanol concentration constant using the ideal feed balance.

Diggaj will now explain the simulation results and the setpoint selection.

## Diggaj Maheshwari, 2:00 to 4:00

### Slide 4 starts, 2:00 to 3:00

Eight reference cases compare four feeding policies under each model. Each model pair shares its initial conditions and process limits.

The graphs show constant feed and constant substrate operation. Under inhibition kinetics, constant feed gives about one hundred and thirty two units per millilitre. Constant substrate operation at two grams per litre gives about two hundred and seventy four.

Monod predicts a faster constant substrate process. Its final activity is not higher under every feeding policy.

Numerical checks used smaller steps, material balances, and an independent analytical solution.

### Slide 5 starts, 3:00 to 4:00

The next calculation screens constant methanol setpoints together with oxygen capacity.

The inhibition model selects a candidate near three point four grams per litre. It predicts three hundred and twenty one units per millilitre after about twenty eight hours of induction. Net productivity is about ten thousand three hundred and forty nine units per litre per hour. This is almost thirteen percent above the two gram per litre reference.

Nearby setpoints give similar productivity, so three point four is not a uniquely proven biological optimum.

Under the same oxygen screen, Monod selects one gram per litre. Its higher growth predictions use more oxygen. Model choice therefore changes the feasible feeding recommendation.

Mridul will explain the oxygen requirement and practical design.

## Mridul Sharma, 4:00 to 6:00

### Slide 6 starts, 4:00 to 5:02

The selected process needs about one point seven two three moles of oxygen per hour at peak demand.

The oxygen calculation includes depletion between inlet and outlet gas. It uses a seventy five percent inlet oxygen blend, two volumes of gas per volume of broth per minute, and an allowance of twenty percent above demand.

The required kLa is about nine hundred and nine per hour. The proposed qualification target is one thousand per hour in the actual broth.

The word qualification is important. The transfer correlations give a wide range, so the proposed equipment is not proven to achieve this value. Air alone fails the screen. If measured capacity is insufficient, the operating point must change.

### Slide 7 starts, 5:02 to 6:00

The enzyme is recovered from the liquid after removing cells. The proposed sequence uses clarification, ultrafiltration and diafiltration, followed by a concentrated liquid preparation.

Assuming seventy percent activity recovery, the illustrative batch budget is about ten thousand rupees. This corresponds to about thirteen thousand five hundred rupees per million recovered activity units. Recovery and budget rates are assumptions. Reactor occupancy is the largest estimated cost.

Industrial scaling needs pilot oxygen transfer and mixing checks. The same lipase process lost performance at fifty litres, so the bench productivity cannot simply be multiplied by industrial volume.

The main conclusion is that kinetic model selection affects feeding, oxygen supply and useful product output. Thank you.
