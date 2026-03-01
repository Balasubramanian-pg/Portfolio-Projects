# Conversion Funnel SVG

## Detailed Technical Documentation for the DAX Measure

This document explains the **Conversion Funnel SVG** DAX measure in a structured, production-style documentation format. The measure dynamically generates an **SVG image encoded as a data URL**, allowing Power BI to render a fully custom visual without using a standard chart.

The measure transforms numerical funnel data into a **vector-based visualization** directly inside DAX.

## 1. Purpose of the Measure

The objective of this measure is to:

* Model a **multi-step conversion funnel**
* Compare **users progressing forward (In)** versus **users dropping off (Out)**
* Dynamically scale visual elements using measures
* Render the visualization using **SVG markup**
* Display it inside a Power BI visual such as:

  * Table
  * Matrix
  * Card (Image URL category)

Instead of relying on Power BI visuals, the measure builds the graphic manually using SVG geometry.

Conceptually, DAX becomes both:

* a calculation engine
* and a graphics generator.

## 2. High-Level Architecture

The measure follows five logical stages:

1. Input data definition
2. Metric calculations
3. Visual scaling calculations
4. Text formatting
5. SVG construction and return

Execution flow:

Data → Percentages → Layout math → SVG elements → Encoded image output

## 3. Data Section

### Base Funnel Metrics

```dax
VAR signupTotal = 600
VAR paymentIn   = 360
VAR paymentOut  = 240
VAR playIn      = 90
VAR playOut     = 150
VAR shareIn     = 18
VAR shareOut    = 72
```

These variables represent user movement through funnel stages.

Funnel interpretation:

| Stage       | Meaning                     |
| ----------- | --------------------------- |
| Sign up     | Total users entering funnel |
| Payment In  | Users continuing            |
| Payment Out | Users dropping              |
| Play In     | Continued engagement        |
| Play Out    | Exit after payment          |
| Share In    | Final successful conversion |
| Share Out   | Final drop-off              |

In production, these values would typically be replaced by measures such as:

* DISTINCTCOUNT(UserID)
* Event tracking metrics
* Session transitions

## 4. Percentage Calculations

Example:

```dax
VAR pPayIn =
FORMAT(DIVIDE(paymentIn, signupTotal) * 100, "0")
```

### Logic

1. Calculate ratio using `DIVIDE`
2. Convert to percentage
3. Format as display text

Why `DIVIDE` instead of `/`:

* Prevents divide-by-zero errors
* Returns BLANK safely

Derived metrics include:

* Conversion from signup
* Drop-off ratios
* Stage-to-stage efficiency

Example interpretation:

360 / 600 = 0.6
0.6 × 100 = 60%

Displayed inside SVG as:

```
60%
```

## 5. Visual Scaling System

SVG requires pixel dimensions.

The measure converts business metrics into **visual width**.

Example:

```dax
VAR wPayIn =
DIVIDE(paymentIn, signupTotal) * 400
```

### Meaning

400 pixels represents the **maximum funnel width**.

Scaling formula:

Stage Width =
(Stage Value / Total Users) × Max Width

Example calculation:

360 ÷ 600 = 0.6
0.6 × 400 = 240 pixels

This ensures proportional rendering.

## 6. Position Calculations

SVG positioning uses coordinates.

Example:

```dax
VAR xPayIn = 808 - wPayIn
```

### Purpose

The funnel is centered around a vertical divider at:

```
x = 808
```

Left side:

* Successful progression (In)

Right side:

* Drop-offs (Out)

So widths dynamically expand outward from the center.

This produces a mirrored funnel layout.

## 7. Number Formatting Layer

```dax
VAR fPayIn = FORMAT(paymentIn, "#,##0")
```

Purpose:

* Improve readability
* Add thousand separators
* Prepare values for text rendering

Example:

```
3600 → 3,600
```

These values appear beside bars.

## 8. SVG Output Construction

The return statement builds a complete SVG document.

```dax
RETURN
"data:image/svg+xml;utf8,<svg ...>"
```

Power BI interprets this as an **Image URL**.

Result:
The measure outputs an image instead of a number.

## 9. SVG Structural Components

### 9.1 Definitions Section

```xml
<defs>
```

Contains reusable graphical assets:

* Background gradients
* Bar gradients
* Glow filters

Defined once and reused.

Examples:

* bg → dashboard background
* bIn → success bars
* bOut → drop-off bars

## 10. Background and Header

Creates dashboard frame:

* Full background rectangle
* Header banner
* Title text
* Divider line

Example element:

```xml
<rect width='1400' height='780'/>
```

Defines canvas size.

## 11. Funnel Geometry

The funnel shape uses polygons.

Example:

```xml
<polygon points='408,252 808,252 808,358 xPayIn,358'/>
```

Each polygon connects stages visually.

Purpose:

* Show flow between steps
* Create tapered funnel effect
* Emphasize conversion loss

Opacity differences create depth perception.

## 12. Funnel Rows

Each stage consists of:

### Components

* Left bar (In)
* Right bar (Out)
* Labels
* Percentages
* Counts
* Timing annotation
* Connector arrow

Example row:

```
Enter payment
```

Rendering steps:

1. Draw conversion bar
2. Draw drop-off bar
3. Place percentage text
4. Place numeric totals
5. Draw transition indicator

## 13. Dynamic Text Rendering

Text elements embed DAX variables.

Example:

```xml
"text>" & fPayIn & "</text>"
```

At runtime Power BI injects calculated values.

Result:
SVG updates automatically with filters and slicers.

## 14. Center Divider Concept

```xml
<line x1='808' ... />
```

Acts as funnel axis.

Visual meaning:

Left side:
progression

Right side:
attrition

This improves cognitive readability.

## 15. Encoding Requirements

Special characters must be encoded.

Examples:

| Character | SVG Encoding |
| --------- | ------------ |
| #         | %23          |
| %         | %25          |

Without encoding, SVG breaks inside URLs.

## 16. Rendering Behaviour in Power BI

For correct display:

* Data Category must be **Image URL**
* Measure evaluated per context
* SVG re-renders on filter interaction

Advantages:

* Fully dynamic visuals
* No custom visual dependency
* Export-safe vector graphics

## 17. Performance Considerations

Potential production risks:

### String Size

Large SVG strings increase memory usage.

### Recalculation Cost

Runs per evaluation context.

### Table Visual Multiplication

If used in tables with many rows, SVG renders repeatedly.

Recommended usage:
Single KPI visual or controlled context.

## 18. Extending the Measure

Common enhancements:

* Replace hardcoded numbers with measures
* Add tooltips
* Animate transitions
* Theme parameterization
* Responsive width scaling

## 19. Conceptual Model

This measure effectively combines:

* Analytical modeling
* Layout mathematics
* Vector graphics
* DAX string engineering

DAX here behaves like a lightweight rendering engine embedded inside Power BI.

## 20. Reasoning Summary

The measure:

1. Calculates funnel metrics.
2. Converts metrics into proportional pixel widths.
3. Positions graphical elements mathematically.
4. Injects values into SVG markup.
5. Returns a renderable image string.
