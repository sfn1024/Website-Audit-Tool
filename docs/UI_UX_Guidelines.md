# UI/UX Consistency Guidelines — Website Audit Tool

This document outlines the design principles, color palettes, and component patterns used in the Website Audit Tool to ensure future consistency.

## 🎨 Core Design System

### Colors
We use a clean, agency-quality palette with CSS variables defined in `src/index.css`.

| Variable | Value | Usage |
| :--- | :--- | :--- |
| `--primary` | `#2563eb` | Primary buttons, active state accents, section headers. |
| `--bg-main` | `#f8fafc` | The main application background. |
| `--bg-card` | `#ffffff` | Component card backgrounds. |
| `--text-main` | `#0f172a` | Primary text and headings. |
| `--text-muted` | `#64748b` | Sub-labels, captions, and non-essential text. |
| `--accent-insights`| `#f1f5f9` | Background for AI insight blocks. |

### Typography
- **Font Stack**: System sans-serif (`-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, etc.).
- **Line Height**: `1.5` for standard readability.
- **Headings**: Use `Inter` or standard bold sans-serif with `var(--text-main)`.

## 📐 Layout Principles

### Responsive Grid
The application uses a strategic 3-column view on desktop:
1. **Metrics (320px)**: Left-aligned technical data.
2. **Insights (1fr)**: Central qualitative analysis.
3. **Recommendations (1fr)**: Right-aligned actionable items.

**Breakpoints:**
- `< 768px`: Single column (Mobile).
- `768px - 1199px`: 2 columns (Metrics + Insights/Recs Stack).
- `>= 1200px`: 3 columns (Full View).

### Spacing & Borders
- **Radius**: `8px` (`--radius`) for all cards and inputs.
- **Shadows**: Use `--shadow-sm` for standard cards and `--shadow-md` for hovered or active items.
- **Container Max**: `1400px` to allow for the 3-column analysis.

## 🧩 Component Standards

### Cards
All results should be wrapped in a card:
- White background (`--bg-card`).
- `1px solid var(--border)` border.
- `1.5rem` padding.
- A `card-title` with a 20px `lucide-react` icon.

### Recommendations
- **Priority Pills**:
  - `P1`: Red bg (`#fee2e2`), Dark Red text (`#991b1b`).
  - `P2`: Amber bg (`#fef3c7`), Dark Amber text (`#92400e`).
  - `P3`: Green bg (`#dcfce7`), Dark Green text (`#166534`).
- **Action Items**: Always wrap in the dashed border-blue box (`.rec-action`) to differentiate them from the reasoning text.

## 🚦 Interaction States
- **Loading**: Use the `Loader2` icon from `lucide-react` with the `.loading-spinner` animation.
- **Buttons**: All buttons must have a hover transition (`0.2s`) to `var(--primary-hover)`.
- **Empty/Error**: Use the `.error-box` or `.full-width-fallback` for centralized error alerting.
