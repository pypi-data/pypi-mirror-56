from typing import List

from sidecar.model.objects import ISidecarService
from sidecar.services.service_status_state import ServiceStatusState


class ServiceTerminationStartPolicy:
    def __init__(self, services: List[ISidecarService], service_status_state: ServiceStatusState):
        self._service_status_state = service_status_state

        service_names = set(s.name for s in services)
        # in teardown only dependencies between services are supported
        self._service_dependencies = {service.name: list([d for d in service.dependencies if d in service_names]) for
                                      service in services}

    def can_start_termination(self, service_name: str):
        dependencies = self._service_dependencies.get(service_name, [])
        return self._service_status_state.termination_done(service_names=dependencies)

