# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Regenerate the SVG diagrams shown in the documentation from their Graphviz sources (requires the "dot" command).
# The SVG files are committed, so that neither the CI nor the readers need Graphviz.
# Four files are produced from each source diagrams/<diagram>.dot:
#   - <diagram>_{light,dark}.svg         are complete SVG files, opened on their own to see the diagram at full size;
#   - <diagram>_{light,dark}_inline.svg  are stripped versions, embedded as is in the HTML of a documentation page,
#                                        so that the links of the diagram are clickable (they would not be in an <img> tag).
# The short links of the sources are expanded by diagrams/links.sed, the dark variant is obtained by substituting the colors
# of the light one with diagrams/dark_palette.sed, and fonts are widened to a fallback list so that the diagrams look the same everywhere.
DIAGRAMSDIR   = diagrams
STATICDIR     = $(SOURCEDIR)/_static
DIAGRAMS      = class_diagram workspace_diagram
SVG_COMMON    = -e 's/font-family="Helvetica,sans-Serif"/font-family="Helvetica, Arial, sans-serif"/g' -e 's/ xlink:title="&lt;TABLE&gt;"//g' -e '/^<title>.*<\/title>$$/d' -e 's|@DOCS_ROOT@|../|g'
SVG_INLINE    = $(SVG_COMMON) -e '/<svg/,$$!d' -e 's/<svg width="[^"]*" height="[^"]*"/<svg/'

diagrams:
	@for diagram in $(DIAGRAMS); do \
	    echo "Rendering $$diagram"; \
	    sed -E -f "$(DIAGRAMSDIR)/links.sed" "$(DIAGRAMSDIR)/$$diagram.dot" | dot -Tsvg | sed $(SVG_COMMON) > "$(STATICDIR)/$${diagram}_light.svg"; \
	    sed -E -f "$(DIAGRAMSDIR)/links.sed" "$(DIAGRAMSDIR)/$$diagram.dot" | dot -Tsvg | sed $(SVG_INLINE) > "$(STATICDIR)/$${diagram}_light_inline.svg"; \
	    sed -E -f "$(DIAGRAMSDIR)/links.sed" -f "$(DIAGRAMSDIR)/dark_palette.sed" "$(DIAGRAMSDIR)/$$diagram.dot" | dot -Tsvg | sed $(SVG_COMMON) > "$(STATICDIR)/$${diagram}_dark.svg"; \
	    sed -E -f "$(DIAGRAMSDIR)/links.sed" -f "$(DIAGRAMSDIR)/dark_palette.sed" "$(DIAGRAMSDIR)/$$diagram.dot" | dot -Tsvg | sed $(SVG_INLINE) -e 's/ id="/ id="dark_/g' > "$(STATICDIR)/$${diagram}_dark_inline.svg"; \
	done

.PHONY: help diagrams Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
