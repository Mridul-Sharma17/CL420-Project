# CL 420 three minute video script

## Timing and speaker order

Sneha Shandilya speaks first from 0:00 to 1:00.

Diggaj Maheshwari speaks second from 1:00 to 2:00.

Mridul Sharma speaks third from 2:00 to 3:00.

## Sneha Shandilya, 0:00 to 1:00

### Slide 1 starts, 0:00 to 0:15

Good morning. Our project studies the dynamic comparison of Monod and substrate inhibition models for recombinant lipase production in a methanol fed batch bioreactor. We use a published Pichia pastoris process and simulate its behaviour under different feeding strategies.

### Slide 2 starts, 0:15 to 1:00

The host organism is Pichia pastoris, a yeast used as a cell factory. The product is recombinant Rhizopus oryzae lipase, measured through enzyme activity in units per millilitre.

Methanol has two roles. It is the carbon and energy source, and it induces the AOX1 promoter that supports recombinant product formation.

This creates the main process tradeoff. Too little methanol can limit growth. Too much methanol can inhibit growth and product formation. Our question is whether Monod and substrate inhibition kinetics give different process predictions under the same reactor operation.

Diggaj will now explain the two kinetic assumptions and the mathematical model.

## Diggaj Maheshwari, 1:00 to 2:00

### Slide 3 starts, 1:00 to 1:30

The Monod model assumes that the rate increases with methanol and then reaches saturation. It does not include a high substrate decline.

The substrate inhibition model includes this decline. Its rate rises, reaches a maximum, and falls when methanol becomes excessive. Using the published parameters, the growth rate peaks near 1.9 grams per litre, while product formation peaks near 3.5 grams per litre. Therefore, the best methanol concentration for cell growth is not exactly the best concentration for lipase production.

### Slide 4 starts, 1:30 to 2:00

The mathematical model uses four dynamic states. These are reactor volume, total biomass, total methanol, and total product activity. The balances describe volume increase through feeding, biomass growth, methanol feed minus cellular uptake, and product formation.

We solve the four balances using fourth order Runge Kutta with a time step of 0.01 hours. The feeding strategies are CF, CM, LM, and CS. Their results are compared under both kinetic formulations.

Mridul will now present the numerical results and the oxygen demand.

## Mridul Sharma, 2:00 to 3:00

### Slide 5 starts, 2:00 to 2:40

The four feeding strategies are CF, constant methanol feed at 14 grams per hour, CM, constant target growth rate at 0.03 per hour, LM, a growth target that rises from 0.01 to 0.04 per hour, and CS, constant methanol concentration at 2 grams per litre.

The constant-substrate strategy gives the strongest predicted performance. Under the substrate inhibition model, CS gives a final product activity of 255.01 units per millilitre and a volumetric productivity of about 10,057 units per litre per hour.

The Monod model predicts a higher CS product value of 266.18 units per millilitre because it excludes substrate inhibition. This difference comes from the kinetic assumption. The linearly increasing strategy performs worst in this comparison because it takes the longest time to reach the biomass limit and gives lower productivity.

### Slide 6 starts, 2:40 to 3:00

The best product strategy also gives the highest oxygen requirement. For the substrate inhibition CS case, the maximum total oxygen uptake rate is about 1.437 moles of oxygen per hour. The next design step is to compare this oxygen demand with oxygen transfer rate and kLa.

In conclusion, the kinetic model changes the predicted operating decision. Thank you.

## Recording checklist

1. Start slide 1 when Sneha begins.
2. Start slide 2 at about 15 seconds.
3. Start slide 3 when Diggaj begins at 1 minute.
4. Start slide 4 at about 1 minute 30 seconds.
5. Start slide 5 when Mridul begins at 2 minutes.
6. Start slide 6 at about 2 minutes 40 seconds.
7. Keep the speaking pace steady and end close to three minutes.
