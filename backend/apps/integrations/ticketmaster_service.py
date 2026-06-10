# Ticketmaster Discovery API integration — Sprint 0 stub.

import logging

logger = logging.getLogger(__name__)


class TicketmasterService:
    def search_events(self, city: str, date_from=None, date_to=None) -> list:
        logger.info("TicketmasterService.search_events called (stub)")
        return []


ticketmaster_service = TicketmasterService()
