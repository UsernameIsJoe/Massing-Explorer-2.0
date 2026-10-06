# Model input — Underwood v0.1 (Step 02)
Source: original Massing Explorer commit `751ba24b0d2bcaeae5274eaffa589060c95ec0f9`.

## Verbatim brief
3 masses, max 3 floors. length max 60 meters. gym and dining together and double height. art and music prefer on ground floor. media prefer on top floor above admin. admin have to be on ground floor. core academic and special ed width has to be 80 feet. mass ratio have to be between 2:5 and 5:8. prefer 3 floors.

## Program schedule (net square feet)
The full source workbook is `examples/Underwood_Elementary_Space_Summary_GSF_Tweaked.xlsx` in the pinned original repository. Retain room names, quantities and NFA. Zero-quantity line items remain zero. Source department totals:

| Department | NFA (SF) |
|---|---:|
| Core academic | 14,280 |
| Special education | 5,610 |
| Art & music | 3,040 |
| Health & physical education | 6,950 |
| Media center | 2,800 |
| Dining & food service | 6,150 |
| Medical | 730 |
| Administration & guidance | 2,510 |
| Custodial & maintenance | 2,200 |
| **Total** | **44,270** |

The workbook displays a 1.50 grossing factor and 66,405 SF GFA. Its complete room schedule must also be supplied to each model; these subtotals alone are insufficient.

## Numeric planning assumptions
Base dimensions in feet; areas in SF. Double-loaded classroom bar: 30-ft depth, 8-ft corridor. Story extrusion height: 14 ft. Gym clear minimum 60 x 100 ft and double height. Cafeteria clear minimum 40 x 60 ft; the brief additionally calls for gym and dining together and double height. Minimum L-shaped residual arm depth: 20 ft. Daylight preference: 90-ft maximum depth. Configured GSF tolerance: ±3%. Separately, config lists area adjustment 1.15 and grossing factor 1.50: preserve the discrepancy with the workbook rather than resolving it without documentation.

No site footprint, frontage, neighbors, or topography are provided; do not invent site facts. The verbatim brief takes precedence over generic configuration preferences. Generic example program-grouping and floor-allocation hints must not be presented as user design requirements.

## Primary source links
- [Frozen program workbook](https://github.com/UsernameIsJoe/Massing-Explorer/blob/751ba24b0d2bcaeae5274eaffa589060c95ec0f9/examples/Underwood_Elementary_Space_Summary_GSF_Tweaked.xlsx)
- [Frozen brief](https://github.com/UsernameIsJoe/Massing-Explorer/blob/751ba24b0d2bcaeae5274eaffa589060c95ec0f9/examples/underwood_3mass_brief.txt)
- [Frozen config](https://github.com/UsernameIsJoe/Massing-Explorer/blob/751ba24b0d2bcaeae5274eaffa589060c95ec0f9/config/project.example.yaml)
