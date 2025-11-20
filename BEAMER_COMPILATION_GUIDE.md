# LaTeX Beamer Presentation Compilation Guide

## Quick Start

### Compilation Command

```bash
pdflatex COMPREHENSIVE_PRESENTATION_DECK.tex
pdflatex COMPREHENSIVE_PRESENTATION_DECK.tex  # Run twice for references
```

Or use a build script:

```bash
#!/bin/bash
pdflatex COMPREHENSIVE_PRESENTATION_DECK.tex
pdflatex COMPREHENSIVE_PRESENTATION_DECK.tex
rm -f *.aux *.log *.nav *.out *.snm *.toc *.vrb
```

### Required LaTeX Packages

The presentation uses standard packages that should be available in most LaTeX distributions:

**Core Beamer:**
- `beamer` (with Madrid theme)

**Standard Packages:**
- `amsmath`, `amssymb` (mathematics)
- `graphicx` (figures)
- `booktabs` (professional tables)
- `xcolor` (colors)
- `tikz` (diagrams - optional, for future enhancements)
- `fontawesome5` (icons)

### Installing Missing Packages

If you get package errors:

**TeX Live (Linux/Mac):**
```bash
sudo tlmgr install fontawesome5
```

**MiKTeX (Windows):**
- MiKTeX will prompt to install missing packages automatically

**MacTeX:**
- Usually includes all packages, but if needed:
```bash
sudo tlmgr install fontawesome5
```

## Customization

### Changing Theme

Edit line 3 in the `.tex` file:
```latex
\usetheme{Madrid}  % Options: Madrid, Berlin, Warsaw, etc.
```

Popular alternatives:
- `Berlin` - More compact
- `Warsaw` - Sidebar navigation
- `Darmstadt` - Minimalist
- `Frankfurt` - Classic

### Changing Colors

Edit the color definitions (lines 8-11):
```latex
\definecolor{primaryblue}{RGB}{0,51,102}
\definecolor{secondarygreen}{RGB}{0,128,0}
\definecolor{accentorange}{RGB}{255,140,0}
```

### Changing Aspect Ratio

Edit line 1:
```latex
\documentclass[aspectratio=169]{beamer}  % 16:9 (widescreen)
% Options: 43 (4:3), 169 (16:9), 1610 (16:10)
```

## Adding Figures

To add figures, use:
```latex
\begin{frame}{Figure Title}
\begin{figure}
\centering
\includegraphics[width=0.8\textwidth]{path/to/figure.png}
\caption{Figure caption}
\end{figure}
\end{frame}
```

**Suggested figure locations:**
- `Presentation_Figures/` - Existing presentation figures
- `h1_loop_analysis/` - H1 loop visualizations
- `h1_loop_analysis/temporal_analysis/` - Temporal plots
- `h1_loop_analysis/event_correlation/` - Event correlation plots

## Troubleshooting

### Fontawesome5 Not Found

If `fontawesome5` is not available, you can:
1. Install it (see above)
2. Or comment out icon usage and use text instead

Replace:
```latex
\item[\faCheckCircle] Completed
```

With:
```latex
\item[$\checkmark$] Completed
```

### Compilation Errors

**Error: "Undefined control sequence"**
- Usually means a package is missing
- Install the missing package (see above)

**Error: "File not found"**
- Check figure paths are correct
- Use relative paths from the `.tex` file location

**Warning: "Overfull hbox"**
- Usually cosmetic, can be ignored
- Or adjust text/figure sizes

### Multiple Compilation Runs

Beamer sometimes needs 2-3 runs to resolve all references. This is normal.

## Output

The compilation produces:
- `COMPREHENSIVE_PRESENTATION_DECK.pdf` - The final presentation

## Presentation Tips

### Timing
- Full version: 10-12 minutes
- Condensed: 5-6 minutes (focus on slides 1, 4, 5, 7, 10, 12)

### Navigation
- Use arrow keys or spacebar to advance
- Press 'F' for fullscreen
- Press 'Esc' to exit fullscreen
- Press 'G' then slide number to jump

### Printing
- Use `\documentclass[handout]{beamer}` for printing
- Or use PDF viewer's print options with "Multiple pages per sheet"

## Advanced Customization

### Custom Slide Backgrounds

Add after `\begin{document}`:
```latex
\setbeamertemplate{background}{
  \includegraphics[width=\paperwidth]{background.png}
}
```

### Custom Fonts

Add before `\begin{document}`:
```latex
\usepackage{fontspec}
\setmainfont{Your Font Name}
```

### Animation

Beamer supports overlays:
```latex
\begin{itemize}
\item<1-> First item
\item<2-> Second item (appears on click 2)
\item<3-> Third item (appears on click 3)
\end{itemize}
```

## Version Control

The `.tex` file is text-based and works well with Git. The `.pdf` output can be regenerated, so you may want to add it to `.gitignore`:

```
*.pdf
*.aux
*.log
*.nav
*.out
*.snm
*.toc
*.vrb
```

## Support

For LaTeX/Beamer questions:
- [Beamer User Guide](https://ctan.org/pkg/beamer)
- [LaTeX Stack Exchange](https://tex.stackexchange.com/)

For presentation content questions:
- See `COMPREHENSIVE_PRESENTATION_DECK.md` for markdown version
- See speaker notes in the markdown file

