# -*- encoding: utf-8 -*-
from dna.views import (
    EveryCreateViewMixin,
    EveryUpdateViewMixin,
    EveryDeleteViewMixin,
    EveryEngageViewMixin,
    EveryListViewMixin,
    EveryIterateViewMixin,
    EveryOptimizeViewMixin,
    EveryPageViewMixin,
    EveryHomeViewMixin,
)


class Criew(EveryCreateViewMixin):
    template_name = "chromosomes/thing_form.html"


class Uiew(EveryUpdateViewMixin):
    template_name = "chromosomes/thing_form.html"


class Diew(EveryDeleteViewMixin):
    template_name = "chromosomes/thing_delete.html"


class Eiew(EveryEngageViewMixin):
    template_name = "chromosomes/thing_engaged.html"


class Liew(EveryListViewMixin):
    template_name = "chromosomes/thing_listed.html"


class Iew(EveryIterateViewMixin):
    template_name = "chromosomes/thing_iterate.html"


class Oiew(EveryOptimizeViewMixin):
    template_name = "chromosomes/thing_optimize.html"


class Piew(EveryPageViewMixin):
    template_name = "chromosomes/thing_page.html"


class Hiew(EveryHomeViewMixin):
    template_name = "chromosomes/home_page.html"
