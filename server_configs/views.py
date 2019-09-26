from django.shortcuts import render
from .models import DestinationConfigs, WorklistConfigs

# Create your views here.


def server_config(request):

    worklist_configs = WorklistConfigs.objects.get(id=1)
    destination_configs = DestinationConfigs.objects.get(id=1)

    context = {
        'worklist_ae': worklist_configs.worklist_ae,
        'worklist_ip': worklist_configs.worklist_ip,
        'worklist_port': worklist_configs.worklist_port,
        'destination_ae': destination_configs.destination_ae,
        'destination_ip': destination_configs.destination_ip,
        'destination_port': destination_configs.destination_port
    }
    return render(request, 'server_configs/server_configs.html', context)
