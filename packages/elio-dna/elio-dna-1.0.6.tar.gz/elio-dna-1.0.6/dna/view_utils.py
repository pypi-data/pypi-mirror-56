# -*- encoding: utf-8 -*-
from django.urls import reverse_lazy
from slugify.slugify import slugify


def pages_deeply(pages_dna):
    """Flatten out all the pages in the SITE_DNA for easy searching."""

    def items():
        for key, value in pages_dna.get("page", {}).items():
            yield key, value
            if isinstance(value, dict):
                for subkey, subvalue in pages_deeply(value).items():
                    yield subkey, subvalue

    return dict(items())


def get_page_dna(site_dna, current_page):
    """Find the details of the current page in the SITE_DNA."""
    all_pages = pages_deeply(site_dna)
    return all_pages.get(current_page, {})


def menu_lookahead(sub_pages_dna, current_page):
    """A lookahead to return if a menu has sub menus activated."""
    all_sub_pages = pages_deeply(sub_pages_dna)
    return current_page in all_sub_pages.keys()


def get_page_name_from_slug(site_dna, page_slug, thing_name):
    """Find the details of the current page in the SITE_DNA."""
    all_pages = pages_deeply(site_dna)
    for menu_key in all_pages.keys():
        if slugify(menu_key) == page_slug:
            return menu_key
    # If you can't find the page_key then it's probably an isolated thing.
    return thing_name


def get_model_dna(page_dna, thing_name, elio_role):
    """Find the details of a model of the current page/role in the SITE_DNA."""
    if not isinstance(page_dna, dict):
        return {}
    if thing_name in list(page_dna.get(elio_role, {})):
        if isinstance(page_dna[elio_role], dict):
            return page_dna[elio_role].get(thing_name, {})
    return {}


def get_page_menu(site_dna, current_page="", site_things=[]):
    """Convert the SITE_DNA into a menu."""
    menu = dict()
    # Start with every key of the current "page" dict.
    for page_name, page_vals in site_dna.get("page", {}).items():
        # Start building the menu one menuitem at a time.
        menu[page_name] = dict()
        if page_vals.get("url"):
            # Static link: Give this item the SITE_DNA URL
            menu[page_name]["url"] = page_vals.get("url")
        elif not page_vals.get("status") == "label":
            # Start give this item a URL if not a label
            menu[page_name]["url"] = reverse_lazy(
                "engage.page", kwargs={"page_slug": slugify(page_name)}
            )
        # Give the menuitem any status set in the SITE_DNA
        if page_vals.get("status"):
            menu[page_name]["status"] = page_vals.get("status")

        # Change the status to active if this menuitem is current page.
        if slugify(page_name) == slugify(current_page):
            menu[page_name]["status"] = "active"

        # If page is active, or (looking ahead) a sub page is active....
        if menu[page_name].get("status") or menu_lookahead(
            page_vals, current_page
        ):
            # If it was a subitem that was active (looking ahead).
            if not menu[page_name].get("status"):
                # Flag as a crumb to the active menu.
                menu[page_name]["status"] = "crumb"  # Make the breadcrumbs
            # Build the sub menu for this menuitem if active.
            sub_menu = get_page_menu(page_vals, current_page)
            # Add the sub to the current menuitem.
            if sub_menu.get("page"):
                menu[page_name].update(sub_menu)
    # Special case: Add a Browse Things section to the menu for all Things.
    if site_things:
        menu["Browse Things"] = {"status": "label", "page": {}}
        for thing in sorted(site_things):
            menu["Browse Things"]["page"][thing] = dict()
            menu["Browse Things"]["page"][thing]["url"] = reverse_lazy(
                "list.things", kwargs={"page_slug": thing, "thing": thing}
            )
            if thing == current_page:
                menu["Browse Things"]["page"][thing]["status"] = "active"
    return {"page": menu}
