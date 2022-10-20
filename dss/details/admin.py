from django.contrib import admin
from .models import events
from .models import district
from .models import profile
from .models import schemes
from .models import eventsMaterials
from .models import tasks
from .models import tags
from .models import lawAndOrder
from .models import rally
from .models import calamity
from .models import crime
from .models import epidemic
from .models import publicGathering
from .models import department


admin.site.register(events.Event)
admin.site.register(department.department)
admin.site.register(district.District)
admin.site.register(profile.Profile)
admin.site.register(schemes.Scheme)
admin.site.register(eventsMaterials.EventFiles)
admin.site.register(tasks.Task)
admin.site.register(tags.Tag)
admin.site.register(lawAndOrder.LawAndOrder)
admin.site.register(rally.Rally)
admin.site.register(calamity.Calamity)
admin.site.register(crime.Crime)
admin.site.register(epidemic.Epidemic)
admin.site.register(publicGathering.PublicGathering)