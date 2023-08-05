Init localization
-------------------------------------------------------------------------------

Usually you dont have to re(init) localisation in project,
but if required you can with command:

.. code-block:: bash

   $ pybabel extract --output=src/sphinx_dj_generator.pot src/sphinx_dj_generator/


Add locale translations
-------------------------------------------------------------------------------

To add additional translation files for new locale,
create required locale output folder with command (example for locale fr_FR):

.. code-block:: bash

   $ pybabel init --input-file=src/sphinx_dj_generator.pot --domain=sphinx_dj_generator --output-dir=src/locale --locale=fr_FR
