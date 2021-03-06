from django.shortcuts import render
from .models import DestinationConfigs, WorklistConfigs, WorkstationConfigs
from django.contrib.auth.decorators import login_required
from .forms import ServerConfigForm
# Create your views here.


@login_required
def server_config(request):
    if request.user.is_superuser:

        if request.method == 'POST':

            workstation_ae = request.POST.get('workstation_ae')
            worklist_ae = request.POST.get('worklist_ae')
            worklist_ip = request.POST.get('worklist_ip')
            worklist_port = request.POST.get('worklist_port')
            destination_ae = request.POST.get('destination_ae')
            destination_ip = request.POST.get('destination_ip')
            destination_port = request.POST.get('destination_port')

            worklist_configs, _ = WorklistConfigs.objects.update_or_create(id=1, defaults={'worklist_ae': worklist_ae, 'worklist_ip': worklist_ip, 'worklist_port': worklist_port})
            destination_configs, _ = DestinationConfigs.update_or_create(id=1, defaults={'destination_ae': destination_ae, 'destination_ip': destination_ip, 'destination_port': destination_port})
            workstation_configs, _ = WorkstationConfigs.objects.update_or_create(id=1, defaults={'workstation_ae': workstation_ae})


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
            # existing config for worklist, storage destination and
            # workstations

            worklist_configs, _ = WorklistConfigs.objects.get_or_create(id=1,defaults={'worklist_ae': '', 'worklist_ip': '0.0.0.0', 'worklist_port': 0}) 
            destination_configs, _ = DestinationConfigs.objects.get_or_create(id=1, defaults={'destination_ae': '', 'destination_ip': '0.0.0.0', 'destination_port': 0}) 
            workstation_configs, _ = WorkstationConfigs.objects.get_or_create(id=1, defaults={'workstation_ae': ''}) 
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

    else:
        context = {
            login_error: 'You are not authorized to view this page. Please contact your PACS Administrator'
        }

        return render(request, 'tech_forms/registation/login.html', context)
