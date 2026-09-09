# Design System Contract

> This file is the technical design contract for implementation.
> Use it to implement colors, typography, spacing, radii, shadows, breakpoints, and UI token mapping.
> The creative direction remains in the root `DESIGN.md`.

## 1. Product Intent

- Product / app:
- Primary user:
- Main task:
- Design stage:

## 2. Design Tokens

### Color Tokens

```json
{
  "primary": "",
  "primary-foreground": "",
  "secondary": "",
  "background": "",
  "surface": "",
  "surface-elevated": "",
  "text": "",
  "muted-text": "",
  "border": "",
  "success": "",
  "warning": "",
  "danger": "",
  "focus": ""
}
```

### Typography Tokens

```json
{
  "font-sans": "",
  "font-display": "",
  "font-mono": "",
  "text-xs": "",
  "text-sm": "",
  "text-base": "",
  "text-lg": "",
  "text-xl": "",
  "text-2xl": "",
  "heading-scale": ""
}
```

### Spacing and Radius

```json
{
  "space-1": "",
  "space-2": "",
  "space-3": "",
  "space-4": "",
  "space-6": "",
  "space-8": "",
  "radius-sm": "",
  "radius-md": "",
  "radius-lg": "",
  "shadow-sm": "",
  "shadow-md": "",
  "shadow-lg": ""
}
```

## 3. Breakpoints

- mobile: ""
- tablet: ""
- desktop: ""
- widescreen: ""

## 4. Component Tokens

### Buttons
- primary:
- secondary:
- ghost:
- destructive:

### Inputs
- field border:
- field background:
- error border:
- success border:

### Cards and surfaces
- bg:
- border:
- shadow:
- radius:

## 5. CSS / Tailwind Mapping

```text
--color-primary => bg-primary / text-primary
--color-surface => bg-surface / border-surface
--spacing-4 => p-4 / gap-4
--radius-md => rounded-md
--shadow-sm => shadow-sm
```

## 6. React Native Mapping

```text
primary -> colors.primary
background -> colors.background
text -> colors.text
radius-lg -> 16
spacing-4 -> 16
shadow-md -> { elevation: 4 }
```

## 7. Implementation Rules

- Use semantic tokens, not hardcoded random hex values.
- Prefer consistent spacing rhythm and a single radius system.
- Keep focus styles visible and accessible.
- Respect the root `DESIGN.md` intent; this file only defines the implementation contract.
- If the design-system contract is not available, keep using the plugin's current fallback patterns and references.

## 8. Validation Checklist

- [ ] colors used consistently
- [ ] typography hierarchy is coherent
- [ ] spacing rhythm is controlled
- [ ] accessibility contrast is acceptable
- [ ] breakpoints are respected
- [ ] component tokens match the product brief
