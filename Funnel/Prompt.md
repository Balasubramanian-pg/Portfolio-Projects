# Master Prompt Template

### 1. Visual Objective

Describe what the visual represents.

Example fields to provide:

* Type of visualization (funnel, lifecycle, progress tracker, comparison bars, pipeline, journey map)
* Business question being answered
* Intended insight for users

Prompt section:

```
VISUAL OBJECTIVE:
I want to create an SVG-based DAX visual showing:
[Describe the visualization]

Primary purpose:
[What decision or insight should this enable?]
```

### 2. Data Model Definition

Define all metrics involved.

```
DATA INPUTS:
Provide measures or columns involved.

Example format:
Stage1_Total =
Stage2_In =
Stage2_Out =
Stage3_Value =
etc.

Explain what each metric represents.
```

If measures are unknown:

```
Use placeholder variables that I will replace later.
```

### 3. Funnel / Flow Logic (Very Important)

Explain relationships between stages.

```
FLOW LOGIC:
Describe how users/items move.

Example:
Stage A → Stage B → Stage C
Users can either continue or drop off.
Percentages should be calculated relative to:
[previous stage / total / custom base]
```

This determines percentage math inside DAX.

### 4. Visual Layout Specification

Define structure of the SVG canvas.

```
LAYOUT REQUIREMENTS:
Canvas size:
Width =
Height =

Orientation:
Horizontal / Vertical / Centered / Mirrored

Sections required:
Header
Axis line
Stage rows
Connectors
Labels
Annotations
```

Optional:

```
I want symmetry around a center axis: Yes/No
```

### 5. Scaling Rules

Explain how numbers translate into pixels.

```
SCALING RULES:
Maximum bar width =
Scaling base =
(total value / max stage / dynamic)

Bars should scale:
Proportionally / Fixed / Logically grouped
```

Without this, visuals distort.

### 6. Styling and Theme

Define design system.

```
STYLE REQUIREMENTS:
Theme:
Dark / Light / Custom

Primary color =
Secondary color =
Drop-off color =
Background gradient =

Font family =
Font weight style =
Rounded corners: Yes/No
Glow effects: Yes/No
```

If branding exists:

```
Match corporate dashboard styling.
```

### 7. Text and Labels

Specify textual elements.

```
TEXT ELEMENTS:
Show counts: Yes/No
Show percentages: Yes/No
Show averages or annotations: Yes/No

Label positions:
Left / Center / Dynamic

Number formatting:
#,##0
Percentage decimals =
```

### 8. Dynamic Behaviour

Critical for Power BI usage.

```
DYNAMIC BEHAVIOR:
Visual must respond to:
Filters
Slicers
Row context

All calculations should use measures where possible.
```

### 9. Power BI Constraints

Helps prevent production failures.

```
POWER BI REQUIREMENTS:
Output must be:
SVG data URL

Compatible with:
Table visual / Card visual / Matrix

Performance priority:
High / Balanced / Visual richness
```

### 10. Advanced Options (Optional)

```
ADVANCED FEATURES:
Animations required: Yes/No
Tooltips embedded: Yes/No
Conditional coloring: Yes/No
Threshold indicators: Yes/No
Icons or shapes needed:
```

### 11. Output Requirement

Explicitly request final deliverables.

```
OUTPUT EXPECTATION:
Provide:

1. Complete production-ready DAX measure
2. Well-structured variables
3. Optimized SVG layout
4. Commented sections
5. Scalable design usable for other datasets
```

## Example Minimal Filled Prompt

```
VISUAL OBJECTIVE:
Customer onboarding funnel visualization.

DATA INPUTS:
TotalUsers
RegisteredUsers
ActivatedUsers
RetainedUsers

FLOW LOGIC:
Each stage converts from previous stage.

LAYOUT REQUIREMENTS:
Centered funnel layout.
Width 1400 Height 700.

SCALING RULES:
Max width 450px based on TotalUsers.

STYLE REQUIREMENTS:
Dark theme.
Green success, grey drop-off.

TEXT ELEMENTS:
Show counts and percentages.

POWER BI REQUIREMENTS:
Return SVG Image URL.
```

## Why This Structure Works

Short reasoning explanation:

The SVG DAX generation depends on three systems working together:

* Analytical calculations
* Coordinate mathematics
* SVG rendering rules

Most failures happen because prompts miss layout or scaling definitions. This template guarantees all required parameters exist before generation begins.

## Recommended Professional Workflow

For reusable enterprise visuals:

1. Define one master SVG framework.
2. Swap only measures.
3. Parameterize colors and widths.
4. Maintain consistent coordinate systems.

This turns SVG DAX into a reusable visualization framework rather than one-off code.
