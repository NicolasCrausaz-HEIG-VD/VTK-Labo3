# VTK - Labo 3 - Scanner d'un genou

> Nicolas Crausaz & Maxime Scharwath

## Indications

Lors du premier rendu, les distances os - peau sont calculés et écrits dans le fichier `distance_filter.vtk`. Si le fichier existe, les distances se sont pas recalculées et le fichier est lu directement.
Il est possible de forcer le recalcul en supprimant le fichier `distance_filter.vtk` ou en changeant la valeur à `True` de la variable `FORCE_RECOMPUTE_DISTANCES` dans le fichier `main.py`.
