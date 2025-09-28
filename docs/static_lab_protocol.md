# Electrostatic Measurement Protocol

## Purpose
Provide a reproducible field procedure for measuring electrostatic charge on lottery balls or analogous play objects so the readings can feed the WAMECU electrostatic diagnostics.

## Equipment
- **Faraday cup + electrometer** (preferred) or calibrated fieldmeter for net charge measurement.
- **Reference grounding strap** for the operator.
- **Non-conductive tweezers** to handle balls without imparting additional charge.
- **Digital hygrometer / thermometer** for ambient humidity and temperature.
- **Ionizing blower or anti-static wipes** when mitigation is tested.
- **Logging sheet or digital form** capturing schema fields (run ID, timestamps, charge readings, humidity, anti-static usage, operator).

## Preparation
1. Calibrate the electrometer or fieldmeter per manufacturer guidance; zero the Faraday cup with no ball inserted.
2. Verify grounding: operator connects the grounding strap and confirms minimal static on reference objects.
3. Record baseline ambient measurements (temperature, relative humidity, airflow if notable).
4. If testing anti-static mitigation, document the method (ionizer model, wipe type) before application.

## Measurement Steps
1. **Isolate** one ball at a time using non-conductive tweezers; avoid brushing against clothing or charged surfaces.
2. **Measure charge**:
   - Insert the ball into the Faraday cup, wait for the reading to stabilise (<5 s), and log the net charge in coulombs.
   - If using a fieldmeter, position the probe at the standardised distance (e.g., 2 cm), note the electric field, and convert to charge using the device’s calibration curve.
3. **Record metadata** in the observation log:
   - Timestamp (`electrostatic_measured_at` in ISO8601).
   - Net charge (`electrostatic_charge_C`).
   - Instrument and method (`electrostatic_test_method`, e.g., `faraday`, `fieldmeter`, `qualitative_stick`).
   - Ambient relative humidity (`relative_humidity_pct`).
   - Whether anti-static treatment was applied (`anti_static_used`).
   - Operator identifier and any anomalies (sparks, adhesion, instrument drift).
4. **Reset the setup** by discharging the cup (ground briefly) between measurements.
5. Repeat for each ball, ensuring at least two measurements per ball when time allows to detect drift.

## Calibration and Quality Checks
- Perform a control measurement every 10 balls using a known neutral object; readings should be near zero. Investigate deviations before proceeding.
- Log equipment calibration certificates and dates; note any firmware or configuration changes.
- If multiple devices are used, cross-measure a subset of balls to quantify inter-device variance.

## Safety and Ethics
- Avoid encouraging any procedure that biases live regulated draws. Report anomalous charge buildups or fairness concerns to the appropriate oversight and compliance teams immediately.
- Use anti-static tools responsibly; ensure that mitigation trials are documented as experiments, not operational practices, unless approved by regulators.
- Share findings, scripts, and raw logs with collaborators so simulations (like the electrostatic notebook) remain transparent and auditable.
