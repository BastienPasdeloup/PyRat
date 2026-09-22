``rendering``
=============

The ``rendering`` subpackage is what shows a game while it is played.
A game creates one of these engines on its own, following its ``render_mode`` argument, so you rarely instantiate them yourself.

.. grid:: 1 1 3 3
   :gutter: 2

   .. grid-item-card:: :doc:`RenderingEngine <../RenderingEngine>`

      The base class of all rendering engines, which renders nothing.

   .. grid-item-card:: :doc:`PygameRenderingEngine <../PygameRenderingEngine>`

      The graphical interface, shown in a window.

   .. grid-item-card:: :doc:`ShellRenderingEngine <../ShellRenderingEngine>`

      The text interface, drawn directly in your terminal.

.. toctree::
   :maxdepth: 1

   ../RenderingEngine
   ../PygameRenderingEngine
   ../ShellRenderingEngine
