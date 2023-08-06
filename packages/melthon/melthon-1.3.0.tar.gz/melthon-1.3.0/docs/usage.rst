=====
Usage
=====

Folder structure
================

A Melthon project has following folder structure.
Folder names can be changed as option to the melthon command.

templates
  This is the only mandatory folder. It contains your Mako tempates (\*.mako) which
  will be rendered into HTML pages. This folder supports subfolders.
  To prevent a file from rendering, like base template or reusable parts, name your
  template ``*.template.mako`` or ``*.part.mako``.

static
  This folder contents will be copied to the root of the output folder.
  You can use this folder for static assets like CSS, JavaScript, images, ...

data
  If you want to have certain information available in a template, e.g. a telephone
  number, you can provide this information in YAML files. Each YAML file inside the
  ``data`` folder will be available as ``data['<FILENAME>']`` in your templates.
  E.g. ``general.yml`` will become ``data['general']``.

middleware
  In this folder, you can provide custom middleware. The middleware will run before
  and after the rendering of your site. It has access to the context. Please use
  following template::

    from melthon.middleware import Middleware


    class Middleware1(Middleware):
      def before(self, context):
        # <YOUR CUSTOM CODE>
        return context
        
      def after(self, context):
        # <YOUR CUSTOM CODE>
        return context

  You can define multiple middlewares (classes) in the same file. Method ``before``
  or ``after`` can be omitted in case it's not required.

output
  This folder will contain the rendered result


Command options
===============

Melthon currently supports 2 commands: ``melthon build`` and ``melthon clean``.
Please use ``melthon --help`` and ``melthon <command> --help`` to list the available options.
