# Data Cleaning & Normalization

This directory contains domain-specific cleaning logic and documentation. The cleaning process follows a strict order to ensure data integrity and consistent indexing.

---

## Cleaning Order

The cleaning scripts should be executed in the following order:

1.  **[Addresses](addresses/README.md)**: Normalizes house numbers (splitting lists, expanding ranges) and filters invalid coordinates.
2.  **[Cities](cities/README.md)**: Filters city names and validates coordinates.
3.  **[Streets](streets/README.md)**: Cleans street names and validates geometry for indexing.

---

## Structure

Each domain is organized as a subdirectory containing:
- A dedicated `README.md` describing its specific cleaning rules and functions.
- A cleaning script that is called by the main pipeline.