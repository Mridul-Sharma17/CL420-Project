# CL 420 final report, Group 21

The final report is a standalone design study. The accepted midterm files remain separate. Presentation work is deferred until the report is approved.

## Rebuild

From the repository root, regenerate the calculations, figures and numerical TeX inputs.

```powershell
python -B simulation/rol_final_design.py
python -B simulation/draw_recovery_process.py
```

Then compile the report and export identical PDFs with the three required registration numbers.

```powershell
python -B simulation/build_final_report.py
```

Python needs NumPy 2 or later, Matplotlib and pypdf. The tested versions are recorded in `simulation/requirements_final.txt`. Compilation uses XeLaTeX with Times New Roman installed. The build helper compiles twice, checks the page limit, and rejects unresolved references, missing glyphs and overfull boxes. Build files use an operating system temporary directory.

For prose edits, edit `CL420_final_report.tex` and run only the build helper. For model or assumption changes, run both commands. Do not edit generated `numbers.tex` or `result_rows.tex` by hand.

## Calculation files

`simulation/rol_final_design.py` reuses the published rate functions and RK4 step from `simulation/rol_fed_batch_simulation.py`. Running it does not run the midterm generator or overwrite its figures.

`output/data/final` contains the complete trajectories, endpoint table, setpoint scan, parameter scenarios, oxygen capacity scenarios, budget, cost scenarios, and numerical check results. `design_summary.json` holds the exact inputs and selected outputs. `report/final/figures` contains the generated vector PDF and PNG figures.

The four dynamic states are culture volume, biomass amount, methanol amount and product activity. Oxygen supply is a separate quasi steady feasibility screen. It does not simulate oxygen limited cell physiology.

## Important definitions

- Methanol feed is a mass rate in g/h. Total liquid volume includes methanol and the linked 200 g/L NH4Cl solution. Base, antifoam, sampling, evaporation and gas stripping are omitted from the dynamics.
- All eight reference cases start at 2 g/L methanol. CF, CM and LM feeds are identical across the kinetic model pair. CS is an ideal constant substrate policy with model dependent feed. Its setpoint scan starts each case at the corresponding setpoint.
- CM and LM are prescribed feeds. The LM target rises from 0.01 to 0.04 per hour over a study-defined 60 hours. Actual growth rates need not equal target rates during a transient.
- The gas reference is actual volume at 30 C and 1 bar absolute. The DO target is 25 percent of air saturation, including when oxygen enriched gas is used. The RQ equal to one gas balance is integrated to determine transfer capacity self-consistently. The margin is applied before inverting capacity to find required kLa.
- The kLa value of 1000 per hour is an equipment qualification target. It is not a measurement or a claim that the illustrative equipment will achieve it. Capacity must be at least 1.20 times demand. The water and electrolyte correlations are uncertain screening extrapolations.
- All reported performance is calculated, not experimental. All budget unit rates and downstream recoveries are explicit planning assumptions, not supplier quotes or measured recovery.
- Induction productivity subtracts initial activity and divides by harvest volume and induction time. Cycle productivity also includes the stated preinduction and turnaround allowances. Cost per recovered activity uses total harvest activity after the assumed recovery.

## Numerical verification

Each reference case is repeated at time steps of 0.01 and 0.005 hours. Methanol and product integral balances are checked. The constant substrate case is also checked against an independently derived analytical solution. Gas capacity is checked against the independent log mean equation at capacity, and required kLa is substituted back into the capacity equation. Initial upper-impeller immersion is checked. Integration refines stopping events and raises an error on negative states rather than silently clipping them. The tested trajectories remain positive, but the maintenance law is not a general starvation-boundary model.

Source details and access limits are recorded in `docs/research/final-design-source-audit.md`. The thesis parameter table was inspected directly. The final 2018 article table and supplementary controller settings were not independently readable, so the report attributes numerical inputs to the thesis.
