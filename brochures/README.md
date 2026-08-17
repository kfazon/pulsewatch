# PulseWatch client brochure

Client-facing Croatian sales brochure for PulseWatch Managed Intelligence.

## Generate

```bash
python -m brochures.render \
  brochures/pulsewatch_client_brochure_hr.json \
  PulseWatch-ponude-i-paketi-INMAR.pdf
```

The JSON file is the editable content source. `render.py` owns the A4 layout and visual system.

Before external distribution, confirm the validity date, package prices, contact information, public company identifiers, and any client-specific scope.
