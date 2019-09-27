from django.shortcuts import render
from .models import DestinationConfigs, WorklistConfigs, WorkstationConfigs
from .forms import ServerConfigForm
# Create your views here.


def server_config(request):

    if request.method == 'POST':

        workstation_ae = request.POST.get('workstation_ae')
        worklist_ae = request.POST.get('worklist_ae')
        worklist_ip = request.POST.get('worklist_ip')
        worklist_port = request.POST.get('worklist_port')
        destination_ae = request.POST.get('destination_ae')
        destination_ip = request.POST.get('destination_ip')
        destination_port = request.POST.get('destination_port')

        worklist_configs = WorklistConfigs.objects.get(id=1)
        destination_configs = DestinationConfigs.objects.get(id=1)
        workstation_configs = WorkstationConfigs.objects.get(id=1)

        worklist_configs.worklist_ae = worklist_ae
        worklist_configs.worklist_ip = worklist_ip
        worklist_configs.worklist_port = worklist_port
        worklist_configs.save()

        destination_configs.destination_ae = destination_ae
        destination_configs.destination_ip = destination_ip
        destination_configs.destination_port = destination_port
        destination_configs.save()

        workstation_configs.workstation_ae = workstation_ae
        workstation_configs.save()

        server_config_form = ServerConfigForm(
            initial={'worklist_ae': worklist_ae,
                     'worklist_ip': worklist_ip,
                     'worklist_port': worklist_port,
                     'destination_ae': destination_ae,
                     'destination_ip': destination_ip,
                     'destination_port': destination_port,
                     'workstation_ae': workstation_ae,


                     })

        context = {
            'worklist_ae': worklist_ae,
            'worklist_ip': worklist_ip,
            'worklist_port': worklist_port,
            'destination_ae': destination_ae,
            'destination_ip': destination_ip,
            'destination_port': destination_port,
            'workstation_ae': workstation_ae,
            'server_config_form': server_config_form

        }

        return render(request, 'server_configs/server_configs.html', context)

    else:
        # existing config for worklist, storage destination and workstations
        worklist_configs = WorklistConfigs.objects.get(id=1)
        destination_configs = DestinationConfigs.objects.get(id=1)
        workstation_configs = WorkstationConfigs.objects.get(id=1)

        # forms for submitting changes to worklist, storage destination and
        # workstations
        server_config_form = ServerConfigForm(
            initial={'workstation_ae': workstation_configs.workstation_ae,
                     'worklist_ip': worklist_configs.worklist_ip,
                     'worklist_ae': worklist_configs.worklist_ae,
                     'worklist_port': worklist_configs.worklist_port,
                     'destination_ip': destination_configs.destination_ip,
                     'destination_ae': destination_configs.destination_ae,
                     'destination_port': destination_configs.destination_port,


                     })
        context = {
            'worklist_ae': worklist_configs.worklist_ae,
            'worklist_ip': worklist_configs.worklist_ip,
            'worklist_port': worklist_configs.worklist_port,
            'destination_ae': destination_configs.destination_ae,
            'destination_ip': destination_configs.destination_ip,
            'destination_port': destination_configs.destination_port,
            'workstation_ae': workstation_configs.workstation_ae,
            'server_config_form': server_config_form

        }

        return render(request, 'server_configs/server_configs.html', context)
