# Fitness Habit Tracker - Figma Design Guide

## Color Palette

### Primary Colors
- **Primary Blue**: `#0d6efd` - Main actions, links
- **Success Green**: `#198754` - Success states, positive actions
- **Info Cyan**: `#17a2b8` - Water tracking, information
- **Warning Yellow**: `#ffc107` - Warnings, alerts
- **Danger Red**: `#dc3545` - Errors, delete actions

### Neutral Colors
- **Dark**: `#212529` - Main text (light mode)
- **Secondary**: `#6c757d` - Secondary text
- **Light**: `#f8f9fa` - Backgrounds, cards
- **White**: `#ffffff` - White backgrounds

### Dark Mode Colors
- **Dark Background**: `#222222` (Bootswatch Darkly)
- **Dark Card**: `#303030`
- **Dark Text**: `#e9ecef`
- **Dark Secondary**: `#adb5bd`

## Typography

### Font Family
- **Primary**: System fonts (Bootstrap default)
  - `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif`

### Font Sizes
- **H1**: 2.5rem (40px) - Page titles
- **H2**: 2rem (32px) - Section headers
- **H3**: 1.75rem (28px) - Card headers
- **H4**: 1.5rem (24px) - Subsections
- **H5**: 1.25rem (20px) - Small headers
- **Body**: 1rem (16px) - Regular text
- **Small**: 0.875rem (14px) - Help text, labels

### Font Weights
- **Normal**: 400
- **Medium**: 500
- **Bold**: 700

## Spacing Scale (Bootstrap)

- **1**: 0.25rem (4px)
- **2**: 0.5rem (8px)
- **3**: 1rem (16px)
- **4**: 1.5rem (24px)
- **5**: 3rem (48px)

## Components

### Buttons
- **Height**: 38px (regular), 31px (small), 48px (large)
- **Padding**: 0.375rem 0.75rem
- **Border Radius**: 0.375rem (6px)
- **Font Size**: 1rem
- **Variants**: Primary, Success, Danger, Secondary, Outline

### Cards
- **Border Radius**: 0.375rem (6px)
- **Box Shadow**: 0 0.125rem 0.25rem rgba(0,0,0,0.075)
- **Padding**: 1rem - 1.5rem
- **Background**: White (light) / #303030 (dark)

### Forms
- **Input Height**: 38px (form-control)
- **Input Padding**: 0.375rem 0.75rem
- **Border**: 1px solid #ced4da
- **Border Radius**: 0.375rem
- **Focus Border**: #0d6efd
- **Placeholder Color**: #6c757d

### Navigation
- **Height**: 56px
- **Background**: Primary color
- **Text Color**: White
- **Active Link**: Lighter shade/underline

## Page Layouts

### Dashboard
- **Structure**: Header → Stats Cards Row → Charts → Activity Feed
- **Grid**: 12-column Bootstrap grid
- **Card Layout**: 3-4 cards per row on desktop

### Workout Session
- **Left Sidebar**: Exercise selector (33% width)
- **Right Content**: Current workout (67% width)
- **Fixed Header**: Workout timer and finish button

### Food Page
- **Search Bar**: Full width with filters
- **Food Grid**: 3-4 cards per row
- **Selected Food**: Highlighted card

## Icons

### Font Awesome 6.0
- **Size**: 1rem - 3rem depending on context
- **Color**: Inherits from parent or themed
- **Common Icons**:
  - Dumbbell: `fa-dumbbell`
  - Utensils: `fa-utensils`
  - Water: `fa-tint`
  - Calendar: `fa-calendar`
  - User: `fa-user`

## Animation & Transitions

- **Hover**: `transform: translateY(-2px)` + shadow
- **Transition**: `all 0.3s ease`
- **Card Fade In**: `animation-delay` based on index

## Responsive Breakpoints (Bootstrap)

- **xs**: < 576px (Mobile)
- **sm**: ≥ 576px (Mobile landscape)
- **md**: ≥ 768px (Tablet)
- **lg**: ≥ 992px (Desktop)
- **xl**: ≥ 1200px (Large desktop)

## Dark/Light Mode Toggle

- **Position**: Fixed bottom-right
- **Size**: 60px circle
- **Gradient**: Purple gradient
- **Icon**: Sun (light) / Moon (dark)

---

## How to Use This Guide in Figma:

1. **Create Color Styles**: Add all colors as Figma color styles
2. **Create Text Styles**: Set up typography styles for H1-H5, body, small
3. **Create Components**: Build button, card, form input components
4. **Use Auto Layout**: For responsive designs
5. **Create Variants**: For button states, light/dark modes
6. **Export**: Use as reference when coding

## Pages to Design:

- [ ] Login Page
- [ ] Register Page
- [ ] Dashboard
- [ ] Profile Page
- [ ] Workout Session
- [ ] Workouts List
- [ ] Food Diary
- [ ] Water Tracker
- [ ] Habits Page
- [ ] Exercise Page

---

**Next Steps:**
1. Create Figma account at figma.com
2. Start with one page (e.g., Dashboard)
3. Use this guide for consistency
4. Share design for feedback
5. Iterate and improve
